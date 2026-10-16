import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import select

from config.settings import SAVE_PROMPT_TEMPLATE
from libs.database import db_session
from libs.models import PromptTemplate

prompt_template_store: dict[str, Any] = {}


def set_store(filename: str | Path) -> None:
    with open(filename) as yml:
        prompt_template_store.update(yaml.safe_load(yml))


def get_template(flow_name: str, node_name: str, agent_name: str) -> dict[str, Any]:
    flow = prompt_template_store[flow_name]
    node = flow[node_name]
    return node[agent_name]


def get_or_create_prompt_template(flow_name: str, node_name: str, agent_name: str, template: dict[str, Any]) -> PromptTemplate:
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


def get_prompt_template(flow_name: str, node_name: str, agent_name: str) -> PromptTemplate:
    template = get_template(flow_name, node_name, agent_name)
    if SAVE_PROMPT_TEMPLATE:
        return get_or_create_prompt_template(flow_name, node_name, agent_name, template)
    else:
        return PromptTemplate(template=template)


def dict_checksum(d: dict[Any, Any], algorithm: str = "sha256", ensure_ascii: bool = True) -> str:
    json_str = json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=ensure_ascii)
    data = json_str.encode("utf-8")
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()
