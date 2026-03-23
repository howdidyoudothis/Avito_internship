from __future__ import annotations

import uuid

import allure
import pytest

from tests.helpers.factories import make_payload, random_seller_id
from tests.helpers.parsers import extract_created_item_id, pick_item, pick_stats
from tests.helpers.validators import assert_item_matches_payload, assert_stats_match_payload


@allure.title("Созданное объявление можно получить по id")
@pytest.mark.e2e
def test_create_then_get_item_by_id(api_client, item_payload, cleanup_ids) -> None:
    create_response = api_client.create_item(item_payload)
    assert create_response.status_code == 200, create_response.text

    item_id = extract_created_item_id(create_response.json())
    cleanup_ids.append(item_id)

    get_response = api_client.get_item_by_id(item_id)
    assert get_response.status_code == 200, get_response.text

    item = pick_item(get_response.json())
    assert_item_matches_payload(item, item_payload)
    assert str(item["id"]) == item_id


@allure.title("Два объявления одного продавца доступны в списке продавца")
@pytest.mark.e2e
def test_get_items_by_seller_contains_created_items(api_client, unique_seller_id, cleanup_ids) -> None:
    payload_1 = make_payload(unique_seller_id)
    payload_2 = make_payload(unique_seller_id)

    response_1 = api_client.create_item(payload_1)
    response_2 = api_client.create_item(payload_2)

    assert response_1.status_code == 200, response_1.text
    assert response_2.status_code == 200, response_2.text

    item_id_1 = extract_created_item_id(response_1.json())
    item_id_2 = extract_created_item_id(response_2.json())
    cleanup_ids.extend([item_id_1, item_id_2])

    list_response = api_client.get_items_by_seller(unique_seller_id)
    assert list_response.status_code == 200, list_response.text

    items = list_response.json()
    assert isinstance(items, list), f"Ожидался список, получено: {items}"
    ids = {str(item["id"]) for item in items if isinstance(item, dict) and "id" in item}

    assert item_id_1 in ids
    assert item_id_2 in ids


@allure.title("GET /api/1/statistic/{id} возвращает статистику созданного объявления")
@pytest.mark.e2e
def test_get_statistics_v1_matches_created_item(api_client, created_item) -> None:
    response = api_client.get_statistics_v1(created_item["id"])

    assert response.status_code == 200, response.text

    stats = pick_stats(response.json())
    assert_stats_match_payload(stats, created_item["request"])


@allure.title("GET /api/2/statistic/{id} возвращает статистику созданного объявления")
@pytest.mark.e2e
def test_get_statistics_v2_matches_created_item(api_client, created_item) -> None:
    response = api_client.get_statistics_v2(created_item["id"])

    assert response.status_code == 200, response.text

    stats = pick_stats(response.json())
    assert_stats_match_payload(stats, created_item["request"])


@allure.title("После удаления объявление недоступно по id")
@pytest.mark.e2e
def test_delete_item_then_get_returns_404(api_client, created_item) -> None:
    item_id = created_item["id"]

    delete_response = api_client.delete_item(item_id)
    assert delete_response.status_code == 200, delete_response.text

    get_response = api_client.get_item_by_id(item_id)
    assert get_response.status_code == 404, get_response.text


@allure.title("Повторная отправка одинакового payload создаёт разные id")
def test_same_payload_twice_creates_different_items(api_client, item_payload, cleanup_ids) -> None:
    response_1 = api_client.create_item(item_payload)
    response_2 = api_client.create_item(item_payload)

    assert response_1.status_code == 200, response_1.text
    assert response_2.status_code == 200, response_2.text

    item_id_1 = extract_created_item_id(response_1.json())
    item_id_2 = extract_created_item_id(response_2.json())
    cleanup_ids.extend([item_id_1, item_id_2])

    assert item_id_1 != item_id_2


@allure.title("Одинаковые name/price/statistics допустимы у разных продавцов")
def test_same_business_fields_allowed_for_different_sellers(api_client, cleanup_ids) -> None:
    shared_name = f"qa-item-{uuid.uuid4().hex[:8]}"
    shared_price = 777
    shared_stats = {"likes": 7, "viewCount": 77, "contacts": 3}

    payload_1 = {
        "sellerID": random_seller_id(),
        "name": shared_name,
        "price": shared_price,
        "statistics": shared_stats,
    }
    payload_2 = {
        "sellerID": random_seller_id(),
        "name": shared_name,
        "price": shared_price,
        "statistics": shared_stats,
    }

    response_1 = api_client.create_item(payload_1)
    response_2 = api_client.create_item(payload_2)

    assert response_1.status_code == 200, response_1.text
    assert response_2.status_code == 200, response_2.text

    item_id_1 = extract_created_item_id(response_1.json())
    item_id_2 = extract_created_item_id(response_2.json())
    cleanup_ids.extend([item_id_1, item_id_2])

    assert item_id_1 != item_id_2


@pytest.mark.parametrize("seller_id", [111111, 999999])
@allure.title("Граничные sellerID из рекомендованного диапазона принимаются")
def test_boundary_seller_ids_are_accepted(api_client, seller_id, cleanup_ids) -> None:
    payload = make_payload(seller_id)

    response = api_client.create_item(payload)
    assert response.status_code == 200, response.text

    item_id = extract_created_item_id(response.json())
    cleanup_ids.append(item_id)

    get_response = api_client.get_item_by_id(item_id)
    assert get_response.status_code == 200, get_response.text


@allure.title("GET по id стабилен при нескольких повторных чтениях")
def test_repeated_get_by_id_returns_same_item(api_client, created_item) -> None:
    item_id = created_item["id"]

    first = api_client.get_item_by_id(item_id)
    second = api_client.get_item_by_id(item_id)
    third = api_client.get_item_by_id(item_id)

    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    assert third.status_code == 200, third.text

    first_item = pick_item(first.json())
    second_item = pick_item(second.json())
    third_item = pick_item(third.json())

    assert str(first_item["id"]) == item_id
    assert first_item == second_item == third_item
