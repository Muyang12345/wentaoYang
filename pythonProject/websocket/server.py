import uvicorn
from starlette.websockets import WebSocket, WebSocketDisconnect
import httpx


async def call_fastapi_api(data):
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8000/ask/", json={"query": data})
        return response.json()


async def app(scope, receive, send):
    if scope['type'] == 'websocket':
        websocket = WebSocket(scope=scope, receive=receive, send=send)
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                # 调用 FastAPI 端点
                response_data = await call_fastapi_api(data)
                # 将 API 响应发送回客户端
                await websocket.send_text(f"API response: {response_data['response']}")
        except WebSocketDisconnect:
            print("Client disconnected")
    else:
        raise NotImplementedError("Only WebSocket connections are supported.")


if __name__ == "__main__":
    # 同时运行 WebSocket 服务器和 FastAPI 应用
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, lambda: uvicorn.run("fastapii:app", host="127.0.0.1", port=8000))
    uvicorn.run("main:app", host="127.0.0.1", port=9001, log_level="info")
