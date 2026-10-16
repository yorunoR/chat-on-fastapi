from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

from libs.external.llm.llm_client import LLMClient


class LLMAgent:
    def __init__(self, *, model_name=None, system_message, label, tools=None):
        self.model_name = model_name
        self.system_message = system_message
        self.label = label
        if tools is None:
            tools = []
        self.tools = tools

    def chain(self, *, chat_session=None, history=None, model_name=None, structured_model=None, metadata, **kwargs):
        """history は呼び出し側(ノード)が用意して渡す。chat_session はトレース用の metadata にだけ使う"""
        model_name = model_name or self.model_name
        if history is None:
            history = []

        if chat_session is not None:
            metadata = self.__add_chat_session_metadata(metadata=metadata, chat_session=chat_session)
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

    def __add_chat_session_metadata(self, *, metadata, chat_session):
        # 呼び出し側の dict を書き換えないよう、コピーして足す
        return {**metadata, "session_id": chat_session.uid, "trace_user_id": chat_session.user_id}
