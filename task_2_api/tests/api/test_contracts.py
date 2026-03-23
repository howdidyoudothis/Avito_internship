from __future__ import annotations

import allure
import pytest

from tests.helpers.parsers import pick_item, pick_stats
from tests.helpers.validators import (
    assert_documented_item_contract,
    assert_json_response,
    assert_statistics_contract,
)


@allure.title("POST /api/1/item возвращает объект созданного объявления по контракту")
@pytest.mark.contract
def test_create_item_contract_returns_full_item_object(api_client, item_payload) -> None:
    response = api_client.create_item(item_payload)

    assert response.status_code == 200, response.text
    assert_json_response(response)

    data = response.json()
    assert_documented_item_contract(data)


@allure.title("GET /api/1/item/{id} возвращает объект объявления с полным набором полей")
@pytest.mark.contract
def test_get_item_by_id_contract_returns_documented_fields(created_item, api_client) -> None:
    response = api_client.get_item_by_id(created_item["id"])

    assert response.status_code == 200, response.text
    assert_json_response(response)

    item = pick_item(response.json())
    assert_documented_item_contract(item)


@allure.title("GET /api/1/{sellerID}/item возвращает список объявлений пользователя")
@pytest.mark.contract
def test_get_items_by_seller_contract_returns_list_of_items(created_item, api_client) -> None:
    seller_id = created_item["request"]["sellerID"]

    response = api_client.get_items_by_seller(seller_id)

    assert response.status_code == 200, response.text
    assert_json_response(response)

    data = response.json()
    assert isinstance(data, list), f"Ожидался список объявлений, получено: {data}"
    assert data, "Список объявлений не должен быть пустым"
    assert_documented_item_contract(pick_item(data))


@allure.title("GET /api/1/statistic/{id} возвращает контракт statistics")
@pytest.mark.contract
def test_get_statistics_v1_contract_returns_statistics_object(created_item, api_client) -> None:
    response = api_client.get_statistics_v1(created_item["id"])

    assert response.status_code == 200, response.text
    assert_json_response(response)

    stats = pick_stats(response.json())
    assert_statistics_contract(stats)


@allure.title("GET /api/2/statistic/{id} возвращает контракт statistics")
@pytest.mark.contract
def test_get_statistics_v2_contract_returns_statistics_object(created_item, api_client) -> None:
    response = api_client.get_statistics_v2(created_item["id"])

    assert response.status_code == 200, response.text
    assert_json_response(response)

    stats = pick_stats(response.json())
    assert_statistics_contract(stats)
