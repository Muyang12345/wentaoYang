import uvicorn
from starlette.websockets import WebSocket, WebSocketDisconnect


async def app(scope, receive, send):
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type': 'lifespan.shutdown.complete'})
                return
    elif scope['type'] == 'websocket':
        # 创建WebSocket实例。
        websocket = WebSocket(scope=scope, receive=receive, send=send)
        await websocket.accept()  # 接受WebSocket连接。
        try:
            while True:
                # 等待客户端发送消息。
                data = await websocket.receive_text()
                # 将消息发送回客户端。
                await websocket.send_text(f"Message text was: {data}")
        except WebSocketDisconnect:
            # 如果WebSocket断开连接，则处理断开连接。
            print("Client disconnected")
    else:
        # 如果不是WebSocket请求，返回错误。
        raise NotImplementedError("Only WebSocket connections are supported.")


# 服务器入口点配置。
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9001, log_level="info")
