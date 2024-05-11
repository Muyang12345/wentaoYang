from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
app = FastAPI()
inference_server_url = "http://119.188.113.120:1180/v1"

model = ChatOpenAI(
    model="qwen",
    openai_api_key="none",
    openai_api_base=inference_server_url,
    max_tokens=10,
    temperature=0.8,
    streaming=True,
)


@app.get("/ask")
async def ask_model(query: str):
    messages = [
        SystemMessage(
            content="你是一个有用的助手，负责聊天和提供帮助"
        ),
        HumanMessage(
            content=query
        ),
    ]
    return {"response": model(messages)}

@app.get("/")
async def root():
    return {"message": "Hello World"}
if __name__ == "__main__":
    import uvicorn
    #run on ipv6
    # uvicorn.run(app, host="::", port=81)
    # run on local
    uvicorn.run(app, host="0.0.0.0", port=81)
