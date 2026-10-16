from pathlib import Path
from typing import Any

import yaml

from config.settings import SAVE_PROMPT_TEMPLATE
from libs.models.prompt_template import PromptTemplate
from libs.repositories.prompt_template_repository import get_or_create_prompt_template

# 全アプリの prompt_templates.yaml をまとめて持つ。キーは flow_name
prompt_template_store: dict[str, Any] = {}


def set_store(filename: str | Path) -> None:
    with open(filename) as yml:
        templates = yaml.safe_load(yml)
    # 別のアプリと flow_name が重なると上書きされるため、エラーにする
    duplicated = prompt_template_store.keys() & templates.keys()
    if duplicated:
        raise ValueError(f"flow_name が重複しています: {sorted(duplicated)} ({filename})")
    prompt_template_store.update(templates)


def get_template(flow_name: str, node_name: str, agent_name: str) -> dict[str, Any]:
    flow = prompt_template_store[flow_name]
    node = flow[node_name]
    return node[agent_name]


def get_prompt_template(flow_name: str, node_name: str, agent_name: str) -> PromptTemplate:
    template = get_template(flow_name, node_name, agent_name)
    if SAVE_PROMPT_TEMPLATE:
        return get_or_create_prompt_template(flow_name, node_name, agent_name, template)
    else:
        return PromptTemplate(template=template)
