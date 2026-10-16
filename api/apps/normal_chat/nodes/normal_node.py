from typing import Any

from apps.normal_chat.flows.flow_data import FlowData
from libs.agents.llm_agent import LLMAgent
from libs.models.chat_session import ChatSession
from libs.repositories.chat_session_repository import get_history
from libs.websocket.sender import ContentStreamSender


class NormalNode:
    """会話履歴を踏まえて、日常会話として回答する"""

    def __init__(self, *, ws, chat_session: ChatSession, flow_data: FlowData, agent_template: dict[str, Any]) -> None:
        self.ws = ws
        self.chat_session = chat_session
        self.flow_data = flow_data
        self.agent = LLMAgent(
            model_name=agent_template["model_name"],
            system_message=agent_template["system_message"],
            label=agent_template["label"],
        )

    async def run(self) -> None:
        history = await get_history(self.chat_session)
        chain = self.agent.chain(chat_session=self.chat_session, history=history, metadata={"agent": self.agent.label})
        self.flow_data.last_agent_label = self.agent.label
        sender = ContentStreamSender(self.ws, self.agent.label)
        try:
            await sender.send(chain.astream({"input": self.flow_data.prompt}))
        finally:
            # 途中で切断されても flow がそこまでの回答を保存できるよう、FlowData に移す
            self.flow_data.content = sender.content
