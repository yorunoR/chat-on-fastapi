import hashlib
import json
from typing import Any

from sqlalchemy import select

from libs.database import db_session
from libs.models import PromptTemplate


def get_or_create_prompt_template(flow_name: str, node_name: str, agent_name: str, template: dict[str, Any]) -> PromptTemplate:
    """SAVE_PROMPT_TEMPLATE が有効なとき(ローカル開発用)だけ呼ばれるため、同期のセッションで開く"""
    hexdigest = dict_checksum(template)
    with db_session() as db:
        prompt_template = db.scalar(
            select(PromptTemplate).where(
                PromptTemplate.hexdigest == hexdigest,
                PromptTemplate.flow_name == flow_name,
                PromptTemplate.node_name == node_name,
                PromptTemplate.agent_name == agent_name,
            )
        )
        if prompt_template is None:
            prompt_template = PromptTemplate(
                hexdigest=hexdigest, flow_name=flow_name, node_name=node_name, agent_name=agent_name, template=template
            )
            db.add(prompt_template)
            db.commit()
            db.refresh(prompt_template)
    return prompt_template


def dict_checksum(d: dict[Any, Any], algorithm: str = "sha256", ensure_ascii: bool = True) -> str:
    json_str = json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=ensure_ascii)
    data = json_str.encode("utf-8")
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()
