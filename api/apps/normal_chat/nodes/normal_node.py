from typing import TYPE_CHECKING, Any

from libs.agents.llm_agent import LLMAgent
from libs.models.chat_session import ChatSession
from libs.websocket.sender import ContentStreamSender

if TYPE_CHECKING:
    from apps.normal_chat.flows.normal_chat_flow import FlowData


class NormalNode:
    """会話履歴を踏まえて、日常会話として回答する"""

    def __init__(self, *, ws, chat_session: ChatSession, flow_data: "FlowData", agent_template: dict[str, Any]) -> None:
        self.ws = ws
        self.chat_session = chat_session
        self.flow_data = flow_data
        self.agent = LLMAgent(
            model_name=agent_template["model_name"],
            system_message=agent_template["system_message"],
            label=agent_template["label"],
        )

    async def run(self) -> None:
        chain = await self.agent.chain(chat_session=self.chat_session, metadata={"agent": self.agent.label})
        self.flow_data.last_agent_label = self.agent.label
        astream = (chunk.text async for chunk in chain.astream({"input": self.flow_data.prompt}))
        sender = ContentStreamSender(self.ws, self.agent.label)
        try:
            await sender.send(astream)
        finally:
            # 途中で切断されても flow がそこまでの回答を保存できるよう、FlowData に移す
            self.flow_data.content = sender.content
