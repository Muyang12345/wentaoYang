from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessageGraph, END
#扩展问题
#直播间交互{输入 输出}
#问题：

cm_info = '''
    女士尺寸	XS	S	M	L	XL
身高	155-160	158-168	160-168	160-170	160-170
体重	85-95	110-120	120-130	130以上	140以上

    '''
# 初始化ChatOpenAI模型
inference_server_url = "http://119.188.113.120:1180/v1"
model = ChatOpenAI(
    model="qwen",
    openai_api_key="none",
    openai_api_base=inference_server_url,
    max_tokens=150,
    temperature=0,
    streaming=True,
    use_streaming=True,
    use_stream=True,
    stream=True
)


def create_message_graph():
    graph = MessageGraph()

    # 分类节点：决定问题属于哪个品类
    def categorize_question(messages):
        last_user_message = messages[-1].content
        category_response = model(
            [HumanMessage(content=f"分类这个问题：{last_user_message}，品类有{{衣服，保健品}}，请只返回问题对应的品类: ")])
        category_content = category_response.content if isinstance(category_response,
                                                                   list) else category_response.content
        category = "clothing" if "衣服" in category_content else "healthcare"
        return category

    # 衣服品类问题处理节点
    def clothing_handler(messages):
        last_user_message = " ".join([msg.content for msg in messages])
        print("last_user_message", last_user_message)
        if "身高" in last_user_message and "体重" in last_user_message:
            return model([HumanMessage(content=f"根据尺码表{cm_info}回答身体体重的尺码问题: {last_user_message}")])
        else:
            return [HumanMessage(content="请提供身高和体重。")]

    def router(messages):
        category = messages[-1].content
        if category == "clothing":
            return "clothing"

        return 'END'

    # 添加节点
    graph.add_node("categorizer", categorize_question)
    graph.add_node("clothing", clothing_handler)

    # 添加边和过渡条件
    # graph.add_edge("categorizer", "clothing")
    graph.add_edge("clothing", END)
    graph.add_conditional_edges("categorizer",router, {
        "clothing": "clothing",
        'END': END
    })
    # 设定图的入口点
    graph.set_entry_point("categorizer")

    # 编译图
    return graph.compile()


async def process_customer_inquiry(content):
    runnable = create_message_graph()
    for response in runnable.invoke([HumanMessage(content=content)]):
        yield response


if __name__ == "__main__":
    user_input = "我需要买衣服，但不知道应该买什么尺码的。"
    response = process_customer_inquiry(user_input)
    print(response)

    # for output in process_customer_inquiry(user_input):
    #     # stream() yields dictionaries with output keyed by node name
    #     for key, value in output.items():
    #         print(f"Output from node '{key}':")
    #         print("---")
    #         if isinstance(value, str):
    #             print(value)
    #         else:
    #             print(value[0].content)
    #         print("\n---\n")
