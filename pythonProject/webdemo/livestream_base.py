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
if "editable_response" not in st.session_state:
    st.session_state.editable_response = ""
if "input" not in st.session_state:
    st.session_state.input = None

# 清理会话历史的按钮
buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    st.session_state.history = []
    # st.experimental_rerun()

# 控制按钮
start_button = st.sidebar.button('开始弹幕问答')
stop_button = st.sidebar.button('停止弹幕问答')

# st.write("开始运行应用...")

# 显示历史消息
for index, message in enumerate(st.session_state.history): 
    if message["role"] == "user":
        now1 = message
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
                    <div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>
                        {now1['content']}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        now2 = message
        col1, col2 = st.columns([1, 3])
        with col2:
            if "无法回答" in now2["content"]:
                st.error(now2["content"])
            else:
                st.success(now2["content"])  
                # st.markdown(f"""
                #     <div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>
                #         {now2['content']}
                #     </div>
                #     """, unsafe_allow_html=True)      

# with st.chat_message(name="user", avatar="user"):
#     input_placeholder = st.empty()
# with st.chat_message(name="assistant", avatar="assistant"):
#     message_placeholder = st.empty()
    
# if st.session_state.has_edit == True:
#     st.write("ifif")

# 获取用户输入
prompt_text = st.chat_input("请输入您的问题")
if prompt_text:
    st.session_state.input = prompt_text
    # st.experimental_rerun()

if st.button("提交回答"):
    # st.session_state.click = 0
    st.session_state.input = None
    st.experimental_rerun()


# 如果用户输入了内容,则生成回复
if st.session_state.input:     # 检查用户是否输入了内容
    prompt_text = st.session_state.input
    # st.session_state.has_edit = True
    # input_placeholder.markdown(prompt_text)
    history = st.session_state.history
    now1 = {"role": "user", "content": prompt_text}
    history.append(now1)
    if now1:
        col1, col2 = st.columns([1, 3])
        with col1:
            pass
            st.markdown(f"""
                    <div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>
                        {now1['content']}
                    </div>
                    """, unsafe_allow_html=True)    

    response = process_customer_inquiry(prompt_text)
    response = response[-1].content
    # message_placeholder.markdown(response)
    st.session_state.editable_response = response
    # 用户可编辑response
    editable_response = st.text_area("", value=st.session_state.editable_response, height=150, key=f"editable_response_{len(history)}")

    st.session_state.editable_response = editable_response

    # if st.button("保存回答", key=f"save_response_{len(history)}"):
    #     now2 = {"role": "assistant", "content": editable_response}
    #     history.append(now1)
    #     history.append(now2)
    #     st.session_state.history = history


    # now1 = {"role": "user", "content": prompt_text}
    # history.append(now1)
    # now2 = {"role": "assistant", "content": response}
    # now2 = {"role": "assistant", "content": editable_response}
    now2 = {"role": "assistant", "content": st.session_state.editable_response}
    # history.append(now2)
    # if now1:
    #     col1, col2 = st.columns([1, 3])
    #     with col1:
    #         pass
    #         st.markdown(f"""
    #                 <div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>
    #                     {now1['content']}
    #                 </div>
    #                 """, unsafe_allow_html=True)
    if now2:
        col1, col2 = st.columns([1, 3])
        with col2:
            if "无法回答" in now2["content"]:
                st.error(now2["content"])
            else:
                now2 = {"role": "assistant", "content": st.session_state.editable_response}
                # st.write("231312321")
                history.append(now2)
                # st.success(now2["content"])
                # if st.button("提交回答", key=f"save_response_{len(history)}"):
                #     # now2["content"] = response
                #     # now2["content"] = st.session_state.editable_response
                #     # history.append(now1)
                #     # st.experimental_rerun()
                #     # now2 = {"role": "assistant", "content": st.session_state.editable_response}
                #     # st.write("if")
                #     # st.session_state.has_edit = True
                #     st.session_state.has_edit = True
                #     st.session_state.history.append(now1)
                #     # st.experimental_rerun()
                #     st.rerun()
                    
                    
                # else:
                #     now2["content"] = st.session_state.editable_response
                #     history.append(now2)
                #     now2 = {"role": "assistant", "content": st.session_state.editable_response}
                #     if st.session_state.has_edit == False:
                #         st.write("else")
                    


    # history.extend([now1, now2])
    st.session_state.history = history
    # st.experimental_rerun()


# # # st.write("运行应用结束...")
# if st.button("提交回答"):
#     # st.session_state.click = 0
#     st.session_state.input = None
#     st.experimental_rerun()







# history = []
# 手动输入部分
# prompt_text = st.chat_input("请输入您的问题")
# if prompt_text:
#     # input_placeholder.markdown(prompt_text)
#     # history = st.session_state.history
#     response = process_customer_inquiry(prompt_text)
#     response = response[-1].content
#     # message_placeholder.markdown(response)
#     now1 = {"role": "user", "content": prompt_text}
#     history.append(now1)
#     now2 = {"role": "assistant", "content": response}
#     history.append(now2)
#     if now1:
#         col1, col2 = st.columns([1, 1])
#         with col1:
#             st.markdown(f"""
#                     <div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>
#                         {now1['content']}
#                     </div>
#                     """, unsafe_allow_html=True)
#     if now2:
#         col1, col2 = st.columns([3, 3])
#         with col2:
#             if "无法回答" in now2["content"]:
#                 st.error(now2["content"])
#             else:
#                 st.success(now2["content"])
#     # history.extend([now1, now2])
#     st.session_state.history = history



# 自动读取CSV并循环发送
# history = []
# if start_button:
#     df = pd.read_csv('/home/wentaoYang/pythonProject/webdemo/comments42.csv')
#     for index, row in df.iterrows():

#         prompt_text = row['Comment Content']
#         id = row['Username']
#         ctime = row['Comment Time']

#         response = process_customer_inquiry(prompt_text)

#         response = response[-1].content

#         now1 = {"role": "user", "content": prompt_text}
#         now2 = {"role": "assistant", "content": response}
#         # st.session_state.history.extend([now1, now2])
#         if now1:
#             col1, col2 = st.columns([1, 1])
#             with col1:
#                 st.markdown(f"""
#                         <div style='background-color: #e2fcfb; color: #434b68; padding: 10px; border-radius: 10px;'>
#                             {id} {ctime}<br>{now1['content']}
#                         </div>
#                         """, unsafe_allow_html=True)
#         if now2:
#             col1, col2 = st.columns([3, 3])
#             with col2:
#                 if "无法回答" in now2["content"]:
#                     st.error(now2["content"])
#                 else:
#                     st.success(now2["content"])
#         history.extend([now1, now2])
#         # time.sleep(1)
#         if stop_button:
#             break
