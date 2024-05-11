# import streamlit as st
# from demo1 import process_customer_inquiry
# import pandas as pd

# st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# # 初始化历史记录和当前索引
# if "qa_pairs" not in st.session_state:
#     st.session_state.qa_pairs = []  # 用于保存所有的问答对
# if "current_index" not in st.session_state:
#     st.session_state.current_index = 0

# buttonClean = st.sidebar.button("清理会话历史", key="clean")
# if buttonClean:
#     st.session_state.qa_pairs = []
#     st.session_state.current_index = 0

# # 每次执行都重新显示所有问答对
# for qa_pair in st.session_state.qa_pairs:
#     with st.container():
#         with st.chat_message(name=qa_pair["role"], avatar=qa_pair["role"]):
#             if qa_pair["role"] == "assistant" and "editable" in qa_pair:
#                 editable_response = st.text_area("", value=qa_pair["content"], height=100, key=f"response-{qa_pair['index']}")
#                 if st.button('提交回答', key=f"submit-{qa_pair['index']}"):
#                     qa_pair["content"] = editable_response  # 更新问答对内容
#                     del qa_pair["editable"]  # 删除编辑标记
#             else:
#                 st.write(qa_pair["content"])

# start_button = st.sidebar.button('开始弹幕问答')
# stop_button = st.sidebar.button('停止弹幕问答')

# if start_button and "current_index" in st.session_state:
#     df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
#     # 只处理未处理的数据
#     for index in range(st.session_state.current_index, len(df)):
#         if stop_button:
#             break
#         row = df.iloc[index]
#         prompt_text = row['Comment Content']
#         response = process_customer_inquiry(prompt_text)
#         response_content = response[-1].content

#         with st.container():
#             with st.chat_message(name="user", avatar="user"):
#                 st.write(prompt_text)  # 用户消息
#             with st.chat_message(name="assistant", avatar="assistant"):
#                 editable_response = st.text_area("", value=response_content, height=100, key=f"response-{index}")
#                 if st.button('提交回答', key=f"submit-{index}"):
#                     response_content = editable_response
#                     st.session_state.qa_pairs.append({"role": "assistant", "content": editable_response, "index": index, "editable": True})
#                 else:
#                     st.write(editable_response)  # 助手回答

#         st.session_state.qa_pairs.append({"role": "user", "content": prompt_text, "index": index})
#         st.session_state.qa_pairs.append({"role": "assistant", "content": response_content, "index": index})
#         st.session_state.current_index = index + 1  # 更新索引



#################################################
# import streamlit as st
# from demo1 import process_customer_inquiry
# import pandas as pd

# st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# # 初始化历史记录和当前索引
# if "qa_pairs" not in st.session_state:
#     st.session_state.qa_pairs = []  # 用于保存所有的问答对
# if "current_index" not in st.session_state:
#     st.session_state.current_index = 0

# buttonClean = st.sidebar.button("清理会话历史", key="clean")
# if buttonClean:
#     st.session_state.qa_pairs = []
#     st.session_state.current_index = 0

# # 每次执行都重新显示所有问答对
# for index, qa_pair in enumerate(st.session_state.qa_pairs):
#     with st.container():
#         with st.chat_message(name=qa_pair["role"], avatar=qa_pair["role"]):
#             if qa_pair["role"] == "assistant" and "editable" in qa_pair:
#                 editable_response = st.text_area("", value=qa_pair["content"], height=100, key=f"response-{index}")
#                 if st.button('提交回答', key=f"submit-{index}"):
#                     st.session_state.qa_pairs[index]["content"] = editable_response  # 更新问答对内容
#             else:
#                 st.write(qa_pair["content"])

# start_button = st.sidebar.button('开始弹幕问答')
# stop_button = st.sidebar.button('停止弹幕问答')

# if start_button and "current_index" in st.session_state:
#     df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
#     # 只处理未处理的数据
#     for index in range(st.session_state.current_index, len(df)):
#         if stop_button:
#             break
#         row = df.iloc[index]
#         prompt_text = row['Comment Content']
#         response = process_customer_inquiry(prompt_text)
#         response_content = response[-1].content

#         with st.container():
#             with st.chat_message(name="user", avatar="user"):
#                 st.write(prompt_text)  # 用户消息
#             with st.chat_message(name="assistant", avatar="assistant"):
#                 editable_response = st.text_area("", value=response_content, height=100, key=f"response-{len(st.session_state.qa_pairs)}")
#                 if st.button('提交回答', key=f"submit-{len(st.session_state.qa_pairs)}"):
#                     st.session_state.qa_pairs.append({"role": "assistant", "content": editable_response, "index": len(st.session_state.qa_pairs), "editable": True})
#                 # else:
#                 #     st.write(editable_response)  # 助手回答

#         st.session_state.qa_pairs.append({"role": "user", "content": prompt_text, "index": len(st.session_state.qa_pairs)})
#         st.session_state.qa_pairs.append({"role": "assistant", "content": response_content, "index": len(st.session_state.qa_pairs), "editable": True})
#         st.session_state.current_index = index + 1  # 更新索引
################################################

import streamlit as st
from demo1 import process_customer_inquiry
import pandas as pd

st.set_page_config(page_title="共享品质北美生活馆", page_icon=":robot:", layout="wide")

# 初始化历史记录和当前索引
if "qa_pairs" not in st.session_state:
    st.session_state.qa_pairs = []  # 用于保存所有的问答对
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
# if "start_button" not in st.session_state:
#     st.session_state.start_button = False

buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.qa_pairs = []
    st.session_state.current_index = 0

# 创建外部容器
container = st.container()

# 每次执行都重新显示所有问答对
with container:
    for index, qa_pair in enumerate(st.session_state.qa_pairs):
        with st.chat_message(name=qa_pair["role"], avatar=qa_pair["role"]):
            if qa_pair["role"] == "assistant" and "editable" in qa_pair:
                editable_response = st.text_area("", value=qa_pair["content"], height=100, key=f"response-{index}")
                if st.button('提交回答', key=f"submit-{index}"):
                    # 更新问答对内容
                    st.session_state.qa_pairs[index]["content"] = editable_response
            else:
                st.write(qa_pair["content"])

start_button = st.sidebar.button('开始弹幕问答')
stop_button = st.sidebar.button('停止弹幕问答')

start_button = True
# st.session_state.start_button = True
# if (start_button or st.session_state.start_button) and "current_index" in st.session_state:
if start_button and "current_index" in st.session_state:
    df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
    # 只处理未处理的数据
    for index in range(st.session_state.current_index, len(df)):
        if stop_button:
            break
        row = df.iloc[index]
        prompt_text = row['Comment Content']
        response = process_customer_inquiry(prompt_text)
        response_content = response[-1].content

        with container:
            with st.chat_message(name="user", avatar="user"):
                st.write(prompt_text)  # 用户消息
            with st.chat_message(name="assistant", avatar="assistant"):
                editable_response = st.text_area("", value=response_content, height=100, key=f"response-{len(st.session_state.qa_pairs)}")
                if st.button('提交回答', key=f"submit-{len(st.session_state.qa_pairs)}"):
                    # 仅存储回答内容
                    # st.session_state.start_button = True
                    st.session_state.qa_pairs.append({"role": "assistant", "content": editable_response, "index": len(st.session_state.qa_pairs), "editable": True})
                #     st.markdown("1234567")
                # else:
                #     st.markdown("1234567")


        st.session_state.qa_pairs.append({"role": "user", "content": prompt_text, "index": len(st.session_state.qa_pairs)})
        st.session_state.qa_pairs.append({"role": "assistant", "content": response_content, "index": len(st.session_state.qa_pairs), "editable": True})
        st.session_state.current_index = index + 1  # 更新索引