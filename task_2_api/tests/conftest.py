from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

import pytest

from tests.helpers.api_client import ApiClient
from tests.helpers.factories import make_payload, random_seller_id
from tests.helpers.parsers import extract_created_item_id


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "https://qa-internship.avito.com").rstrip("/")


@pytest.fixture(scope="session")
def api_client(base_url: str) -> ApiClient:
    return ApiClient(base_url=base_url, timeout=10)


@pytest.fixture
def cleanup_ids() -> list[str]:
    return []


@pytest.fixture
def unique_seller_id() -> int:
    return random_seller_id()


@pytest.fixture
def item_payload(unique_seller_id: int) -> dict[str, Any]:
    return make_payload(unique_seller_id)


@pytest.fixture
def create_item(api_client: ApiClient, cleanup_ids: list[str]) -> Callable[[dict[str, Any]], tuple]:
    def _create(payload: dict[str, Any]) -> tuple:
        response = api_client.create_item(payload)
        data = response.json()
        if response.status_code == 200:
            try:
                cleanup_ids.append(extract_created_item_id(data))
            except AssertionError:
                pass
        return response, data

    return _create


@pytest.fixture
def created_item(api_client: ApiClient, item_payload: dict[str, Any], cleanup_ids: list[str]) -> dict[str, Any]:
    response = api_client.create_item(item_payload)
    assert response.status_code == 200, response.text
    data = response.json()
    item_id = extract_created_item_id(data)
    cleanup_ids.append(item_id)
    return {
        "request": item_payload,
        "create_response": data,
        "id": item_id,
    }


@pytest.fixture(autouse=True)
def cleanup_created_items(api_client: ApiClient, cleanup_ids: list[str]):
    yield
    for item_id in cleanup_ids:
        try:
            api_client.delete_item(item_id)
        except Exception:
            pass
