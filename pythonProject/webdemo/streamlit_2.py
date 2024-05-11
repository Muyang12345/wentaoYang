# import streamlit as st
# from demo1 import process_customer_inquiry
# import pandas as pd

# st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# # 初始化历史记录
# if "history" not in st.session_state:
#     st.session_state.history = []

# buttonClean = st.sidebar.button("清理会话历史", key="clean")
# if buttonClean:
#     st.session_state.history = []

# start_button = st.sidebar.button('开始弹幕问答')
# stop_button = st.sidebar.button('停止弹幕问答')
 
# with st.chat_message(name="assistant", avatar="assistant"):
#     bottom_text = st.empty()  # 创建底部文本框

# # 显示历史消息并允许编辑助手的回答
# for message in st.session_state.history:
#     with st.chat_message(name=message["role"], avatar=message["role"]):
#         if message["role"] == "user":
#             st.markdown(message["content"])
#         else:
#             editable_response = st.text_area("", value=message["content"], height=100, key=f"edit-{message['content']}")
#             if st.button('提交回答', key=f"update-{message['content']}"):
#                 message["content"] = editable_response
#                 bottom_text.text(f"已更新回答：{editable_response}")  # 更新底部文本框内容

# # # 手动输入问题
# # with st.form(key='manual_input_form'):
# #     prompt_text = st.text_input("请输入您的问题")
# #     if st.form_submit_button('提交问题') and prompt_text:
# #         response = process_customer_inquiry(prompt_text)
# #         response_content = response[-1].content
# #         editable_response = st.text_area("编辑回答", value=response_content, height=100)
# #         if st.button('提交回答'):
# #             now1 = {"role": "user", "content": prompt_text}
# #             now2 = {"role": "assistant", "content": editable_response}
# #             st.session_state.history.extend([now1, now2])
# #             bottom_text.text(f"已提交回答：{editable_response}")  # 更新底部文本框内容

# # 自动读取CSV并循环发送
# if start_button:
#     df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
#     for index, row in df.iterrows():
#         prompt_text = row['Comment Content']
#         response = process_customer_inquiry(prompt_text)
#         response_content = response[-1].content
#         col1, col2 = st.columns([1, 3])
#         with col1:
#             st.markdown(f"""<div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>{row['Username']} {row['Comment Time']}<br>{prompt_text}</div>""", unsafe_allow_html=True)
#         with col2:
#             editable_response = st.text_area("", value=response_content, height=100, key=f"response-{index}")
#             if st.button('提交回答', key=f"submit-{index}"):
#                 now1 = {"role": "user", "content": prompt_text}
#                 now2 = {"role": "assistant", "content": editable_response}
#                 st.session_state.history.extend([now1, now2])
#                 bottom_text.markdown(editable_response)  # 更新底部文本框内容
#     # if stop_button:
#     #     break

#     ############################
# import streamlit as st
# from demo1 import process_customer_inquiry
# import pandas as pd

# st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# # 初始化历史记录
# if "history" not in st.session_state:
#     st.session_state.history = []

# buttonClean = st.sidebar.button("清理会话历史", key="clean")
# if buttonClean:
#     st.session_state.history = []

# start_button = st.sidebar.button('开始弹幕问答')
# stop_button = st.sidebar.button('停止弹幕问答')

# with st.chat_message(name="assistant", avatar="assistant"):
#     bottom_text = st.empty()  # 创建底部文本框

# def run_loop():
#     running = True
#     while running:
#         # 自动读取CSV并循环发送
#         if start_button:
#             df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
#             for index, row in df.iterrows():
#                 prompt_text = row['Comment Content']
#                 response = process_customer_inquiry(prompt_text)
#                 response_content = response[-1].content
#                 col1, col2 = st.columns([1, 3])
#                 with col1:
#                     st.markdown(f"""<div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>{row['Username']} {row['Comment Time']}<br>{prompt_text}</div>""", unsafe_allow_html=True)
#                 with col2:
#                     editable_response = st.text_area("", value=response_content, height=100, key=f"response-{index}")
#                     if st.button('提交回答', key=f"submit-{index}"):
#                         now1 = {"role": "user", "content": prompt_text}
#                         now2 = {"role": "assistant", "content": editable_response}
#                         st.session_state.history.extend([now1, now2])
#                         bottom_text.markdown(editable_response)  # 更新底部文本框内容
#                 # if stop_button:
#                 #     running = False
#                 #     bottom_text.text("已停止循环")  # 更新底部文本框内容
#                 #     break
#         if stop_button:
#             break

# run_loop()



########################
import streamlit as st
from demo1 import process_customer_inquiry
import pandas as pd

st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# 初始化历史记录
if "history" not in st.session_state:
    st.session_state.history = []

# 初始化按钮状态
if "start_button" not in st.session_state:
    st.session_state.start_button = False

if "stop_button" not in st.session_state:
    st.session_state.stop_button = False

buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.history = []

start_button = st.sidebar.button('开始弹幕问答')
stop_button = st.sidebar.button('停止弹幕问答')

with st.expander("回答详情"):
    bottom_text = st.empty()  # 创建底部文本框

def run_loop():
    running = True
    while running:
        # 检查是否要开始或停止循环
        if st.session_state.start_button:
            df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
            for index, row in df.iterrows():
                prompt_text = row['Comment Content']
                response = process_customer_inquiry(prompt_text)
                response_content = response[-1].content
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(f"""<div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>{row['Username']} {row['Comment Time']}<br>{prompt_text}</div>""", unsafe_allow_html=True)
                with col2:
                    editable_response = st.text_area("", value=response_content, height=100, key=f"response-{index}")
                    if st.button('提交回答', key=f"submit-{index}"):
                        now1 = {"role": "user", "content": prompt_text}
                        now2 = {"role": "assistant", "content": editable_response}
                        st.session_state.history.extend([now1, now2])
                        bottom_text.markdown(editable_response)  # 更新底部文本框内容
        if st.session_state.stop_button:
            running = False

run_loop()


