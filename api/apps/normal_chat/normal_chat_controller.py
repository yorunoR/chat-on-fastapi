from loguru import logger

from apps.normal_chat.flows.normal_chat_flow import NormalChatFlow
from libs.models.chat_session import ChatSession


async def run_normal_chat(ws, chat_session: ChatSession, text: str) -> str:
    """回答はノードが ws に送る。ws が None のときは送らずに回答だけを返す"""
    flow = NormalChatFlow(ws=ws, chat_session=chat_session)
    logger.info(f"normal_chat start: session={chat_session.uid}")
    try:
        flow_data = await flow.arun(text)
        return flow_data.content
    finally:
        logger.info(f"normal_chat end: session={chat_session.uid}")
