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

# 清理会话历史的按钮
buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.history = []
    st.experimental_rerun()

# 控制按钮
start_button = st.sidebar.button('开始弹幕问答')
stop_button = st.sidebar.button('停止弹幕问答')

# 显示历史消息
for message in st.session_state.history:
    if message["role"] == "user":
        with st.chat_message(name="user", avatar="user"):
            st.markdown(message["content"])
    else:
        with st.chat_message(name="assistant", avatar="assistant"):
            st.markdown(message["content"])
with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()
# 手动输入部分
prompt_text = st.chat_input("请输入您的问题")

if prompt_text:
    input_placeholder.markdown(prompt_text)
    history = st.session_state.history
    # response = process_customer_inquiry(prompt_text)
    # response = response[-1].content
    # message_placeholder.markdown(response)
    now1 = {"role": "user", "content": prompt_text}
    history.append(now1)
    # now2 = {"role": "assistant", "content": response}
    # history.append(now2)
    st.session_state.history = history
# 自动读取CSV并循环发送
history = []
if start_button:
    df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
    for index, row in df.iterrows():
        # for message in history:
        #     if message["role"] == "user":
        #         with st.chat_message(name="user", avatar="user"):
        #             st.markdown(message["content"])
        #     else:
        #         with st.chat_message(name="assistant", avatar="assistant"):
        #             st.markdown(message["content"])
        prompt_text = row['Comment Content']
        id = row['Username']
        ctime = row['Comment Time']
        # input_placeholder.markdown(prompt_text)
        # with st.chat_message(name="user", avatar="user"):
        #     st.markdown(f"{id}      {ctime}:" + '\n' +
        #                 f"{prompt_text}")
        # history = st.session_state.history
        response = process_customer_inquiry(prompt_text)

        response = response[-1].content
        # with st.chat_message(name="assistant", avatar="assistant"):
        #     st.markdown(response)
        # message_placeholder.markdown(response)
        now1 = {"role": "user", "content": prompt_text}
        now2 = {"role": "assistant", "content": response}
        # st.session_state.history.extend([now1, now2])
        if now1:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"""
                        <div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>
                            {id} {ctime}<br>{now1['content']}
                        </div>
                        """, unsafe_allow_html=True)
        if now2:
            col1, col2 = st.columns([3, 3])
            with col2:
                if "无法回答" in now2["content"]:
                    st.error(now2["content"])
                else:
                    st.success(now2["content"])
        history.extend([now1, now2])
        # time.sleep(1)
        if stop_button:
            break
