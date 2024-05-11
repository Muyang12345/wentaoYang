import streamlit as st
from demo1 import process_customer_inquiry
import pandas as pd
import time


# 单人历史（qa+交易信息、活跃信息）+直播间历史（公共十个问答对） + 插入数据库
# router 问题分类：1品类相关问题：{衣服{尺码、库存{暂无法回答}，其他（其他品类（颜色标识））} 2。由主播回答 3。暂不回答
# 配置页面
# 界面增加编辑和发送功能
st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# 初始化会话状态
if "history" not in st.session_state:
    st.session_state.history = []
if "click" not in st.session_state:
    st.session_state.click = 0
if "input" not in st.session_state:
    st.session_state.input = None


# 清理会话历史
buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.history = []
    st.rerun()


# 控制按钮
start_button = st.sidebar.button('开始弹幕问答')
stop_button = st.sidebar.button('停止弹幕问答')    

# 渲染并显示聊天历史记录
for i, message in enumerate(st.session_state.history):
    if message["role"] == "user":
        with st.chat_message(name="user", avatar="user"):
            st.markdown(message["content"])
    else:
        with st.chat_message(name="assistant", avatar="assistant"):
            st.markdown(message["content"])

# 输入框和输出框
with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()

if st.session_state.click == 1:
    st.write("click")


# 获取用户输入
prompt_text = st.chat_input("请输入您的问题")
if prompt_text:
    st.session_state.input = prompt_text
    # st.experimental_rerun()

if st.button("提交回答"):
    st.session_state.click = 0
    st.session_state.input = None
    st.experimental_rerun()

# 如果用户输入了内容,则生成回复
if st.session_state.input:     # 检查用户是否输入了内容
    prompt_text = st.session_state.input
    # 将用户输入的文本以 Markdown 格式显示在输入框的占位符上。input_placeholder 是之前创建的输入框占位符对象
    input_placeholder.markdown(prompt_text)
    # 从 Streamlit 的会话状态中获取历史记录和键值。之前定义的会话状态中存储了聊天历史记录
    history = st.session_state.history

    quiry = {"role": "user", "content": prompt_text}
    # st.session_state.history.append(quiry)
    history.append(quiry)


    response = process_customer_inquiry(prompt_text)
    response = response[-1].content

        # 将生成的回复以 Markdown 格式显示在输出框的占位符上。message_placeholder 是之前创建的输出框占位符对象
    message_placeholder.markdown(response)
    answer = {"role": "assistant", "content": response}

    # 更新历史记录和past key values
    # st.session_state.history = history
    # st.session_state.history.append(response)
    history.append(answer)

    st.session_state.history = history
    # if st.button("提交回答", key=f"save_response_{len(history)}"):
    #     st.session_state.click = 1
    #     st.session_state.input = None
    #     # st.experimental_rerun()

# if st.button("提交回答"):
#     st.session_state.click = 1
#     st.experimental_rerun()


# if st.button("提交回答"):
#     st.session_state.click = 1
#     st.session_state.input = None
#     st.experimental_rerun()

    # , key=f"save_response_{len(history)}"