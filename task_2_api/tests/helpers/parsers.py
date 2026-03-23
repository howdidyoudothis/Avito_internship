from __future__ import annotations

import re
from typing import Any


UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


def extract_created_item_id(data: dict[str, Any]) -> str:
    direct_id = data.get("id")
    if isinstance(direct_id, str) and direct_id:
        return direct_id

    status = data.get("status")
    if isinstance(status, str):
        match = UUID_RE.search(status)
        if match:
            return match.group(0)

    raise AssertionError(f"Не удалось извлечь id из ответа create-item: {data}")


def pick_item(data: Any) -> dict[str, Any]:
    if isinstance(data, dict):
        return data
    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            return first
    raise AssertionError(f"Не удалось привести ответ к item-объекту: {data}")


def pick_stats(data: Any) -> dict[str, Any]:
    if isinstance(data, dict):
        return data
    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            return first
    raise AssertionError(f"Не удалось привести ответ к statistics-объекту: {data}")
