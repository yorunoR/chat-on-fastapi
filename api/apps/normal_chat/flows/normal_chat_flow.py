import operator
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel

from apps.normal_chat.flows.flow_data import FlowData
from apps.normal_chat.nodes.normal_node import NormalNode
from libs.models.chat_session import ChatSession
from libs.prompts.prompt_template_store import get_prompt_template, set_store
from libs.repositories.chat_session_repository import append_qa_to_session

FLOW_NAME = "normal_chat_flow"

set_store(Path(__file__).parents[1] / "prompt_templates.yaml")


class Node(StrEnum):
    normal = "normal_node"


class State(BaseModel):
    history: Annotated[list[Node], operator.add]


class NormalChatFlow:
    def __init__(self, *, ws, chat_session: ChatSession) -> None:
        """ws に None を渡すと、クライアントへ送らずに回答だけを返す"""
        self.ws = ws
        self.chat_session = chat_session
        self.normal_agent_prompt_template = get_prompt_template(FLOW_NAME, Node.normal, "normal_agent")
        self.graph = self.__create_graph()

    async def arun(self, prompt: str) -> FlowData:
        self.flow_data = FlowData(prompt=prompt)
        try:
            await self.graph.ainvoke(State(history=[]))
        finally:
            # 途中で切断されても、そこまでの内容を残す
            await self.__save()
        return self.flow_data

    async def __save(self) -> None:
        if self.flow_data.content:
            await append_qa_to_session(self.chat_session, self.flow_data.prompt, self.flow_data.content)

    def __create_graph(self) -> CompiledStateGraph:
        graph = StateGraph(State)

        graph.add_node(Node.normal, self.__normal_node)

        graph.add_edge(START, Node.normal)
        graph.add_edge(Node.normal, END)

        return graph.compile()

    async def __normal_node(self, state: State) -> dict[str, Any]:
        normal_node = NormalNode(
            ws=self.ws,
            chat_session=self.chat_session,
            flow_data=self.flow_data,
            agent_template=self.normal_agent_prompt_template.template,
        )
        await normal_node.run()
        return {"history": [Node.normal]}
