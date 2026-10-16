import asyncio

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, WebSocketException, status
from loguru import logger

from apps.normal_chat.normal_chat_controller import run_normal_chat
from config.settings import WS_TIMEOUT_SECONDS
from interfaces.dependencies.websocket import track_connection
from libs.repositories.chat_session_repository import get_chat_session_by_uid

router = APIRouter()


@router.websocket("/ws/normal_chat/{session_uid}", dependencies=[Depends(track_connection)])
async def normal_chat(websocket: WebSocket, session_uid: str) -> None:
    chat_session = await get_chat_session_by_uid(session_uid)
    if chat_session is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    await websocket.accept()
    timeout = asyncio.timeout(WS_TIMEOUT_SECONDS)
    try:
        async with timeout:
            text = await websocket.receive_text()
            await run_normal_chat(websocket, chat_session, text)
            # 接続を閉じるのはクライアントの責務。閉じられるまで待つ
            while True:
                await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    except TimeoutError:
        # 内側の処理(DB 接続など)が出した TimeoutError は、接続のタイムアウトではなくエラーとして扱う
        if not timeout.expired():
            logger.exception("normal_chat failed")
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
            return
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE, reason="timeout")
    except Exception:
        logger.exception("normal_chat failed")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
