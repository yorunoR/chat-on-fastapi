from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from libs.external.llm.llm_client import LLMClient
from libs.repositories.chat_session_repository import get_history


class LLMAgent:
    def __init__(self, *, model_name=None, system_message, label, tools=None):
        self.model_name = model_name
        self.system_message = system_message
        self.label = label
        if tools is None:
            tools = []
        self.tools = tools

    async def chain(self, *, chat_session=None, history=None, model_name=None, structured_model=None, metadata, **kwargs):
        model_name = model_name or self.model_name

        if chat_session is not None:
            client = self.__create_llm_client_with_chat_session(
                chat_session=chat_session, model_name=model_name, metadata=metadata, **kwargs
            )
            history = await get_history(chat_session)
        else:
            client = LLMClient(model_name=model_name, model_kwargs={"metadata": metadata}, **kwargs)

        assigns = RunnablePassthrough.assign(history=lambda _inputs: history)

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                MessagesPlaceholder("history"),
                ("human", "{input}"),
            ]
        )
        qa_prompt = qa_prompt.partial(system_message=self.system_message)

        if self.tools:
            llm = client.llm.bind_tools(self.tools)
        else:
            llm = client.llm

        if structured_model:
            llm = llm.with_structured_output(structured_model)

        return assigns | qa_prompt | llm

    def __create_llm_client_with_chat_session(self, *, chat_session, model_name, metadata, **kwargs):
        metadata["session_id"] = chat_session.uid
        metadata["trace_user_id"] = chat_session.user_id
        return LLMClient(model_name=model_name, model_kwargs={"metadata": metadata}, **kwargs)
