from langchain_openai import ChatOpenAI


class OpenAIClient:
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.llm = None

        model_kwargs = kwargs.pop("model_kwargs")
        self.__set_llm(**model_kwargs)

    def __set_llm(self, **kwargs):
        self.llm = ChatOpenAI(
            model=self.model_name,
            timeout=30,
            # NOTE: llm 呼び出しの通信リトライによる最大待ち時間 0.5 + 1 + 2 + 4 = 7.5 秒
            max_retries=4,
            **kwargs,
        )
