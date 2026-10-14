from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from interfaces.dependencies.websocket import WsUser

router = APIRouter()


@router.websocket("/ws/normal_chat")
async def normal_chat(websocket: WebSocket, user: WsUser) -> None:
    await websocket.accept()
    try:
        text = await websocket.receive_text()
        for i in range(1, 4):
            await websocket.send_text(f"[{i}/3] echo: {text}")
        await websocket.close()
    except WebSocketDisconnect:
        pass
