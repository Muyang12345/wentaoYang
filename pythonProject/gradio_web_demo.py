# Copyright (c) Alibaba Cloud.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""A simple web interactive chat demo based on gradio."""
import os
from argparse import ArgumentParser

import gradio as gr
import mdtex2html

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig

DEFAULT_CKPT_PATH = 'Qwen-14B-Chat'


def _get_args():
    parser = ArgumentParser()
    parser.add_argument("-c", "--checkpoint-path", type=str, default=DEFAULT_CKPT_PATH,
                        help="Checkpoint name or path, default to %(default)r")
    parser.add_argument("--cpu-only", action="store_true", help="Run demo with CPU only")

    parser.add_argument("--share", action="store_true", default=False,
                        help="Create a publicly shareable link for the interface.")
    parser.add_argument("--inbrowser", action="store_true", default=False,
                        help="Automatically launch the interface in a new tab on the default browser.")
    parser.add_argument("--server-port", type=int, default=8000,
                        help="Demo server port.")
    parser.add_argument("--server-name", type=str, default="127.0.0.1",
                        help="Demo server name.")

    args = parser.parse_args()
    return args


def _load_model_tokenizer(args):
    tokenizer = AutoTokenizer.from_pretrained(
        args.checkpoint_path, trust_remote_code=True, resume_download=True,
    )

    if args.cpu_only:
        device_map = "cpu"
    else:
        device_map = "auto"

    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint_path,
        device_map=device_map,
        trust_remote_code=True,
        resume_download=True,
    ).eval()

    config = GenerationConfig.from_pretrained(
        args.checkpoint_path, trust_remote_code=True, resume_download=True,
    )

    return model, tokenizer, config


def postprocess(self, y):
    if y is None:
        return []
    for i, (message, response) in enumerate(y):
        y[i] = (
            None if message is None else mdtex2html.convert(message),
            None if response is None else mdtex2html.convert(response),
        )
    return y


gr.Chatbot.postprocess = postprocess


def _parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split("`")
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f"<br></code></pre>"
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", r"\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


def _gc():
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


class UserSession:
    def __init__(self):
        self.task_history = []  # 存储用户的任务历史
        self.awaiting_details = False  # 标记是否等待用户提供更多细节
        self.last_question_type = None  # 上一次问题的类型
        self.height = 0
        self.weight = 0

    def add_question(self, question_type, details=None):
        self.task_history.append((question_type, details))
        self.last_question_type = question_type
        self.awaiting_details = question_type in ["size_inquiry", "suitability_inquiry"] and not details

    def update_last_question(self, details):
        if self.task_history:
            last_question = self.task_history[-1]
            self.task_history[-1] = (last_question[0], details)
            self.awaiting_details = False

    def is_awaiting_details(self):
        return self.awaiting_details

    def get_last_question(self):
        return self.task_history[-1] if self.task_history else (None, None)


def _launch_demo(args, model, tokenizer, config):
    import re
    session = UserSession()
    products = '''
        1	777711402834	不退换 美国直邮 DUCHAMP 双肩包【16637】	https://item.taobao.com/item.htm?id=777711402834		
				5314268376342	灰色【882】;直邮
2	771267501017	美国直邮 不支持退换【拍下退款的定金不退】	https://item.taobao.com/item.htm?id=771267501017		
				5317693377411	黑色
				5317693377410	白色
3	768106449049	不退换 美国直邮DKNY  斜挎包【R33AAA60】	https://item.taobao.com/item.htm?id=768106449049		
				5273111029099	黑色;直邮
4	759582177394	不退换美国直邮 ACT*IVE  清洁剂泡*腾*片 24片	https://item.taobao.com/item.htm?id=759582177394		
				5405658246136	洗衣机泡腾片;直邮
				5405658246137	洗碗机清洗泡腾片;直邮
5	750438652376	新 不退换美国直邮 32&deg;HEAT 女士抽绳休闲裤 不加绒 内	https://item.taobao.com/item.htm?id=750438652376		
				5177499909869	黑色【1409242】;XS腰围70
				5177499909870	黑色【1409242】;S腰围74
				5177499909871	黑色【1409242】;M腰围78
				5177499909872	黑色【1409242】;L腰围86
				5177499909873	黑色【1409242】;XL腰围92
				5403822967041	蓝色【1409242】;XS腰围70
				5403822967039	蓝色【1409242】;S腰围74
				5403822967038	蓝色【1409242】;M腰围78
				5403822967037	蓝色【1409242】;L腰围86
				5403822967040	蓝色【1409242】;XL腰围92
    '''
    cm_info = '''
    女士尺寸	XS	S	M	L	XL
身高	155-160	158-168	160-168	160-170	160-170
体重	85-95	110-120	120-130	130以上	140以上

    '''

    def parse_user_input(input_text):
        # 识别尺码询问
        size_match = re.search(r"size_inquiry", input_text)
        if size_match:
            details = size_match.groups()
            return "size_inquiry", {"details": details}

        # 识别商品适配性询问
        keyword_match = re.search(r"product_inquiry", input_text)
        if keyword_match:
            product_id = keyword_match.groups()
            return "product_inquiry", {"product_id": product_id}

        return "unknown", {}

    def predict(_query, _chatbot, _task_history):
        print(f"User: {_parse_text(_query)}")
        _chatbot.append((_parse_text(_query), ""))
        full_response = ""

        for response in model.chat_stream(tokenizer, _query, history=_task_history, generation_config=config):
            _chatbot[-1] = (_parse_text(_query), _parse_text(response))

            yield _chatbot
            full_response = _parse_text(response)

        print(f"History: {_task_history}")
        _task_history.append((_query, full_response))
        print(f"Qwen-Chat: {_parse_text(full_response)}")

    def predict1(_query, _chatbot, _task_history):
        # 分析用户输入，决定是否需要补充信息

        modified_query = _query
        if session.last_question_type is None:
            modified_query = (f"用户问题是{_query}. 根据用户问题，确认用户的问题类型，如果是身高体重问尺码合不合适，或者尺码"
                              f"应该多少身高体重，请只返回{{size_inquiry,身高,体重,尺码}},提取不到的信息请置为0；"
                              f"如果是问某个商品信息或者某个链接信息，如商品的颜色，库存，胸围等需要商品信息的问题，请只返回{{product_inquiry 商品序号}}，提取不到的信息请置为0;"
                              f"否则，请返回other")

            print(f"User: {_parse_text(_query)}")
            _chatbot.append((_parse_text(_query), ""))
            full_response = ""

            for response in model.chat_stream(tokenizer, modified_query, history=_task_history, generation_config=config):
                # _chatbot[-1] = (_parse_text(_query), _parse_text(response))

                # yield _chatbot
                full_response = _parse_text(response)

            print(f"History: {_task_history}")
            # _task_history.append((_query, full_response))
            print(f"Qwen-Chat: {_parse_text(full_response)}")

            question_type, details = parse_user_input(full_response)

            if question_type == "size_inquiry":
                print("问尺码")
                product_info = products
                # 构建新的查询，包含检索到的商品信息
                # if session.height != 0 or session.weight != 0:
                #     modified_query = f"用户问题是{_query}. 尺码表是: {cm_info}，请回答用户问题"
                # else:
                modified_query = f"用户问题是{_query}. 尺码表是: {cm_info}，请判断信息是否足以回答用户问题，如果不足请返回“很抱歉，请提供相关信息”，如果充足，可以回答用户问题"
            elif question_type == "product_inquiry":
                # 检索商品信息或尺码推荐
                print("问商品")
                product_info = products
                # 构建新的查询，包含检索到的商品信息
                modified_query = f"用户问题是{_query}. 商品信息: {product_info}，请回答用户问题"
            else:
                print("其他")
                # 如果查询不需要检索或无法解析，则不修改
                modified_query = _query
            # 调用原始的predict函数处理修改后的查询
            print(f"User: {_parse_text(_query)}")
            _chatbot.append((_parse_text(_query), ""))
            full_response = ""

            for response in model.chat_stream(tokenizer, modified_query, history=_task_history, generation_config=config):
                _chatbot[-1] = (_parse_text(modified_query), _parse_text(response))

                yield _chatbot
                full_response = _parse_text(response)

            print(f"History: {_task_history}")
            _task_history.append((_query, full_response))
            print(f"Qwen-Chat: {_parse_text(full_response)}")




    def handle_user_input(session, user_input):
        # 检查是否正在等待用户提供更多信息
        if session.is_awaiting_details():
            # 假设所有待补充信息都通过这个输入提供
            session.update_last_question(user_input)
            question_type, details = session.get_last_question()
            response = generate_response(question_type, {"additional_info": user_input})
            return response, session

        # 解析用户的新输入
        question_type, details = parse_user_input(user_input)
        session.add_question(question_type, details)

        if question_type == "unknown":
            return "我们无法理解您的问题，请尝试提供更多的信息。", session
        elif session.is_awaiting_details():
            return request_additional_info(question_type), session
        else:
            response = generate_response(question_type, details)
            return response, session

    def regenerate(_chatbot, _task_history):
        if not _task_history:
            yield _chatbot
            return
        item = _task_history.pop(-1)
        _chatbot.pop(-1)
        yield from predict(item[0], _chatbot, _task_history)

    def reset_user_input():
        return gr.update(value="")

    def reset_state(_chatbot, _task_history):
        _task_history.clear()
        _chatbot.clear()
        _gc()
        return _chatbot

    with gr.Blocks() as demo:
        gr.Markdown("""\
<p align="center"><img src="https://tse4-mm.cn.bing.net/th/id/OIP-C.GdrPUkJGIYxbQ_jFgqO-dAHaE7?rs=1&pid=ImgDetMain" style="height: 80px"/><p>""")
        gr.Markdown("""<center><font size=8>共享品质北美生活馆</center>""")
        gr.Markdown(
            """\
<center><font size=3>本WebUI实现聊天机器人功能。</center>""")
        #         gr.Markdown("""\
        # <center><font size=4>
        # Qwen-7B <a href="https://modelscope.cn/models/qwen/Qwen-7B/summary">🤖 </a> |
        # <a href="https://huggingface.co/Qwen/Qwen-7B">🤗</a>&nbsp ｜
        # Qwen-7B-Chat <a href="https://modelscope.cn/models/qwen/Qwen-7B-Chat/summary">🤖 </a> |
        # <a href="https://huggingface.co/Qwen/Qwen-7B-Chat">🤗</a>&nbsp ｜
        # Qwen-14B <a href="https://modelscope.cn/models/qwen/Qwen-14B/summary">🤖 </a> |
        # <a href="https://huggingface.co/Qwen/Qwen-14B">🤗</a>&nbsp ｜
        # Qwen-14B-Chat <a href="https://modelscope.cn/models/qwen/Qwen-14B-Chat/summary">🤖 </a> |
        # <a href="https://huggingface.co/Qwen/Qwen-14B-Chat">🤗</a>&nbsp ｜
        # &nbsp<a href="https://github.com/QwenLM/Qwen">Github</a></center>""")

        chatbot = gr.Chatbot(label='聊天框', elem_classes="control-height")
        query = gr.Textbox(lines=2, label='输入')
        task_history = gr.State([])

        with gr.Row():
            empty_btn = gr.Button("🧹 Clear History (清除历史)")
            submit_btn = gr.Button("🚀 Submit (发送)")
            regen_btn = gr.Button("🤔️ Regenerate (重试)")

        # submit_btn.click(predict, [query, chatbot, task_history], [chatbot], show_progress=True)
        submit_btn.click(predict1, [query, chatbot, task_history], [chatbot], show_progress=True)

        submit_btn.click(reset_user_input, [], [query])
        empty_btn.click(reset_state, [chatbot, task_history], outputs=[chatbot], show_progress=True)
        regen_btn.click(regenerate, [chatbot, task_history], [chatbot], show_progress=True)

    #         gr.Markdown("""\
    # <font size=2>Note: This demo is governed by the original license of Qwen. \
    # We strongly advise users not to knowingly generate or allow others to knowingly generate harmful content, \
    # including hate speech, violence, pornography, deception, etc. \
    # (注：本演示受Qwen的许可协议限制。我们强烈建议，用户不应传播及不应允许他人传播以下内容，\
    # 包括但不限于仇恨言论、暴力、色情、欺诈相关的有害信息。)""")

    demo.queue().launch(
        share=args.share,
        inbrowser=args.inbrowser,
        server_port=args.server_port,
        server_name=args.server_name,
    )


def main():
    args = _get_args()

    model, tokenizer, config = _load_model_tokenizer(args)

    _launch_demo(args, model, tokenizer, config)


if __name__ == '__main__':
    main()
