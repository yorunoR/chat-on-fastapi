from libs.external.llm.models.openai_client import OpenAIClient


class LLMClient:
    def __init__(self, model_name, **kwargs):
        self.model_name = model_name
        self.kwargs = kwargs
        self.client = OpenAIClient(self.model_name, **self.kwargs)
        self.llm = self.client.llm
