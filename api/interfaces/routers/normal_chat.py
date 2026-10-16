from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, WebSocketException, status

from interfaces.dependencies.websocket import track_connection
from libs.repositories.chat_session_repository import get_chat_session_by_uid

router = APIRouter()


@router.websocket("/ws/normal_chat/{session_uid}", dependencies=[Depends(track_connection)])
async def normal_chat(websocket: WebSocket, session_uid: str) -> None:
    chat_session = await get_chat_session_by_uid(session_uid)
    if chat_session is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    await websocket.accept()
    try:
        text = await websocket.receive_text()
        for i in range(1, 4):
            await websocket.send_text(f"[{i}/3] echo: {text}")
        await websocket.close()
    except WebSocketDisconnect:
        pass
