import streamlit as st
from demo1 import process_customer_inquiry
import pandas as pd

st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# 初始化历史记录
if "history" not in st.session_state:
    st.session_state.history = []

buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.history = []
    st.experimental_rerun()

start_button = st.sidebar.button('开始弹幕问答')
stop_button = st.sidebar.button('停止弹幕问答')

# 显示历史消息并允许编辑助手的回答
for message in st.session_state.history:    # 遍历history
    # 使用 st.chat_message() 方法显示用户的消息。
    # name="user" 指定了消息的发送者为用户，avatar="user" 指定了用户头像的样式。
    # 然后，使用 st.markdown() 方法将用户消息的内容以 Markdown 格式显示在界面上。
    with st.chat_message(name=message["role"], avatar=message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            # 让助手的回答可编辑
            editable_response = st.text_area("", value=message["content"], height=100, key=f"edit-{message['content']}")
            if st.button('提交回答', key=f"update-{message['content']}"):
                # 用户提交修改后更新会话历史
                message["content"] = editable_response

with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()



# 手动输入问题
prompt_text = st.chat_input("请输入您的问题")
if prompt_text:
    response = process_customer_inquiry(prompt_text)
    response_content = response[-1].content
    # 在可编辑的文本区域显示助手的回答
    editable_response = st.text_area("编辑回答", value=response_content, height=100)
    if st.button('提交回答'):
        now1 = {"role": "user", "content": prompt_text}
        now2 = {"role": "assistant", "content": editable_response}
        st.session_state.history.extend([now1, now2])

# 手动输入部分
# prompt_text = st.chat_input("请输入您的问题")
# if prompt_text:
#     input_placeholder.markdown(prompt_text)
#     history = st.session_state.history
#     # response = process_customer_inquiry(prompt_text)
#     # response = response[-1].content
#     # message_placeholder.markdown(response)
#     now1 = {"role": "user", "content": prompt_text}
#     history.append(now1)
#     # now2 = {"role": "assistant", "content": response}
#     # history.append(now2)
#     st.session_state.history = history

# with st.chat_message(name="assistant", avatar="assistant"):
#     message_placeholder = st.empty()

# 自动读取CSV并循环发送
if start_button:
    df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
    for index, row in df.iterrows():
        prompt_text = row['Comment Content']
        response = process_customer_inquiry(prompt_text)
        response_content = response[-1].content
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""<div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>{row['Username']} {row['Comment Time']}<br>{prompt_text}</div>""", unsafe_allow_html=True)
        with col2:
            # 让助手的回答可编辑
            editable_response = st.text_area("", value=response_content, height=100, key=f"response-{index}")
            if col2.button('提交回答', key=f"submit-{index}"):
                # 更新会话历史
                now1 = {"role": "user", "content": prompt_text}
                now2 = {"role": "assistant", "content": editable_response}
                st.session_state.history.extend([now1, now2])

                prompt_text = editable_response

                input_placeholder.markdown(prompt_text)

                if "无法回答" in editable_response:
                    col2.error(editable_response)
                else:
                    col2.success(editable_response)
        if stop_button:
            break
