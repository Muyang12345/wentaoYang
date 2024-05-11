import gradio as gr
from langgraph_demo1 import process_customer_inquiry


def predict(message, history):
    # 初始化对话历史格式化字符串
    history_string = ""
    # 遍历历史记录，格式化成字符串
    for human, assistant in history:
        history_string += f"User: {human}\n"
        history_string += f"Assistant: {assistant}\n"
    # 添加最新的用户消息
    history_string += f"User: {message}\n"

    # 调用处理函数
    response = process_customer_inquiry(history_string)
    # 返回处理结果
    print(response)
    return response[-1].content


if __name__ == "__main__":
    demo = gr.ChatInterface(predict).queue()
    demo.launch(share=True, server_name="0.0.0.0")
