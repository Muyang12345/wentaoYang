from typing import List
from langchain_core.messages import BaseMessage
from langgraph.graph import END, MessageGraph
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

inference_server_url = "http://119.188.113.120:1180/v1"

model = ChatOpenAI(
    model="qwen",
    openai_api_key="none",
    openai_api_base=inference_server_url,
    max_tokens=10,
    temperature=0.8,
    streaming=True,
)
print(type(model))
messages = [
    SystemMessage(
        content="You are a helpful assistant that translates English to Chinese."
    ),
    HumanMessage(
        content="Translate the following sentence from English to Chinese: I love programming."
    ),
]
print(model(messages))

graph = MessageGraph()


def invoke_model(state: List[BaseMessage]):
    return model.invoke(state)


graph.add_node("oracle", model)
graph.add_edge("oracle", END)

graph.set_entry_point("oracle")

runnable = graph.compile()
response= runnable.invoke([HumanMessage("你好")])
print(response[1].content)
print(runnable.invoke(HumanMessage("我需要买衣服，但不知道应该买什么尺码的。")))

