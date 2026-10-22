from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState


async def close_websocket(websocket: WebSocket, code: int, reason: str | None = None) -> None:
    """クライアントが先に切断していたら閉じない(close も失敗し、元のエラーのログに続けて例外が出るため)"""
    if websocket.application_state == WebSocketState.DISCONNECTED:
        return
    try:
        await websocket.close(code=code, reason=reason)
    except WebSocketDisconnect:
        pass
