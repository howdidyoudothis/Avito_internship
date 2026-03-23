from __future__ import annotations

from datetime import datetime
from typing import Any


def assert_json_response(response) -> None:
    assert "application/json" in response.headers.get("Content-Type", ""), response.headers


def assert_item_matches_payload(item: dict[str, Any], payload: dict[str, Any]) -> None:
    assert item["name"] == payload["name"]
    assert item["price"] == payload["price"]
    actual_seller = item.get("sellerId", item.get("sellerID"))
    assert actual_seller == payload["sellerID"]
    assert item["statistics"] == payload["statistics"]


def assert_stats_match_payload(stats: dict[str, Any], payload: dict[str, Any]) -> None:
    assert stats["likes"] == payload["statistics"]["likes"]
    assert stats["viewCount"] == payload["statistics"]["viewCount"]
    assert stats["contacts"] == payload["statistics"]["contacts"]


def assert_documented_item_contract(data: dict[str, Any]) -> None:
    for field in ("id", "sellerId", "name", "price", "statistics", "createdAt"):
        assert field in data, f"В ответе нет поля '{field}': {data}"

    assert isinstance(data["id"], str)
    assert isinstance(data["sellerId"], int)
    assert isinstance(data["name"], str)
    assert isinstance(data["price"], int)
    assert isinstance(data["statistics"], dict)
    assert isinstance(data["createdAt"], str)

    for field in ("likes", "viewCount", "contacts"):
        assert field in data["statistics"], f"В statistics нет поля '{field}': {data}"

    datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))


def assert_statistics_contract(data: dict[str, Any]) -> None:
    for field in ("likes", "viewCount", "contacts"):
        assert field in data, f"В ответе нет поля '{field}': {data}"
        assert isinstance(data[field], int)
