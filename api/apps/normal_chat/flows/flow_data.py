from pydantic import BaseModel, Field


class FlowData(BaseModel):
    """ノード間で受け渡すデータ。flow と nodes の両方から参照する"""

    prompt: str = Field(...)
    content: str = Field(default="")
    last_agent_label: str = Field(default="")
