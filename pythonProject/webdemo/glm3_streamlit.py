import streamlit as st
from demo1 import process_customer_inquiry
import pandas as pd
import time

# 单人历史（qa+交易信息、活跃信息）+直播间历史（公共十个问答对） + 插入数据库
# router 问题分类：1品类相关问题：{衣服{尺码、库存{暂无法回答}，其他（其他品类（颜色标识））} 2。由主播回答 3。暂不回答
# 配置页面
# 界面增加编辑和发送功能
st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# 初始化历史记录和past key values
if "history" not in st.session_state:
    st.session_state.history = []



# 清理会话历史
buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.history = []
    st.rerun()
    # st.experimental_rerun()

# 渲染并显示聊天历史记录
for i, message in enumerate(st.session_state.history):
    if message["role"] == "user":
        with st.chat_message(name="user", avatar="user"):
            st.markdown(message["content"])
    else:
        with st.chat_message(name="assistant", avatar="assistant"):
            st.markdown(message["content"])

# # 输入框和输出框
# with st.chat_message(name="user", avatar="user"):
#     input_placeholder = st.empty()
# with st.chat_message(name="assistant", avatar="assistant"):
#     message_placeholder = st.empty()

# 获取用户输入
# prompt_text = st.chat_input("请输入您的问题")

# 如果用户输入了内容,则生成回复
if prompt_text:     # 检查用户是否输入了内容

    # 将用户输入的文本以 Markdown 格式显示在输入框的占位符上。input_placeholder 是之前创建的输入框占位符对象
    input_placeholder.markdown(prompt_text)
    # 从 Streamlit 的会话状态中获取历史记录和键值。之前定义的会话状态中存储了聊天历史记录
    history = st.session_state.history
    # 键值用于模型生成回复时的上下文信息
    past_key_values = st.session_state.past_key_values

    # """
    # 使用模型的 stream_chat() 方法生成回复。这是一个生成器函数，每次迭代会产生一个新的回复。
    # 迭代过程中，将生成的回复赋值给 response

    # tokenizer：     模型的 tokenizer 对象，用于将文本转换为模型输入的格式。
    # prompt_text：   用户输入的文本，作为对话的起始。
    # history：       先前的对话历史记录，用于上下文理解和生成响应。
    # past_key_values=past_key_values：过去的键值，用于上下文理解和生成响应。
    # max_length：    生成的文本的最大长度。
    # top_p：         Top-p sampling 中的 p 参数，控制生成文本的多样性。
    # temperature：   温度参数，用于控制生成文本的多样性。
    # return_past_key_values=True：指定在生成响应时返回更新后的 past key values。
    # """
    for response, history, past_key_values in model.stream_chat(
        tokenizer,
        prompt_text,
        history,
        past_key_values=past_key_values,
        max_length=max_length,
        top_p=top_p,
        temperature=temperature,
        return_past_key_values=True,
    ):
        # 将生成的回复以 Markdown 格式显示在输出框的占位符上。message_placeholder 是之前创建的输出框占位符对象
        message_placeholder.markdown(response)

    # 更新历史记录和past key values
    st.session_state.history = history
    st.session_state.past_key_values = past_key_values
