from loguru import logger

from apps.normal_chat.flows.normal_chat_flow import FlowData, NormalChatFlow
from libs.models.chat_session import ChatSession
from libs.tasks.background_task import run_in_background
from libs.websocket.sender import send_done


async def run_normal_chat(ws, chat_session: ChatSession, text: str) -> str:
    """回答はノードが ws に送る。ws が None のときは送らずに回答だけを返す"""
    flow = NormalChatFlow(ws=ws, chat_session=chat_session)
    logger.info(f"normal_chat start: session={chat_session.uid}")
    try:
        flow_data = await flow.arun(text)
        # 後処理でクライアントを待たせず、接続のタイムアウトでキャンセルもされないよう切り離す
        # done より先に登録し、done の送信に失敗(切断)しても後処理は行う
        run_in_background(post_process(chat_session, flow_data), name=f"normal_chat post_process: session={chat_session.uid}")
        # 保存は arun の中で終わっているので、done を受けたクライアントがすぐ次の質問を送っても履歴に入っている
        await send_done(ws)
        return flow_data.content
    finally:
        logger.info(f"normal_chat end: session={chat_session.uid}")


async def post_process(chat_session: ChatSession, flow_data: FlowData) -> None:
    """flow が終わった後の処理(ログなど)。例外は run_in_background がログに出す"""
    # TODO: ログなどの後処理を書く
