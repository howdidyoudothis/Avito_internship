from __future__ import annotations

import copy

import allure
import pytest


@pytest.mark.negative
@pytest.mark.parametrize("missing_field", ["sellerID", "name", "price", "statistics"])
@allure.title("POST /api/1/item возвращает 400 при отсутствии обязательного поля")
def test_create_item_without_required_field_returns_400(api_client, item_payload, missing_field) -> None:
    payload = copy.deepcopy(item_payload)
    payload.pop(missing_field)

    response = api_client.create_item(payload)

    assert response.status_code == 400, response.text


@pytest.mark.negative
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("sellerID", "not-an-int"),
        ("sellerID", 12.34),
        ("name", 123),
        ("price", "not-an-int"),
        ("price", {"bad": "value"}),
        ("statistics", "not-an-object"),
        ("statistics", []),
    ],
)
@allure.title("POST /api/1/item возвращает 400 при некорректных типах")
def test_create_item_with_invalid_types_returns_400(api_client, item_payload, field, value) -> None:
    payload = copy.deepcopy(item_payload)
    payload[field] = value

    response = api_client.create_item(payload)

    assert response.status_code == 400, response.text


@pytest.mark.negative
@allure.title("GET /api/1/item/{id} возвращает 404 для несуществующего id")
def test_get_item_with_nonexistent_id_returns_404(api_client) -> None:
    response = api_client.get_item_by_id("00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404, response.text


@pytest.mark.negative
@pytest.mark.parametrize("bad_id", ["bad-id", "123", "###"])
@allure.title("GET /api/1/item/{id} возвращает 400 для невалидного id")
def test_get_item_with_invalid_id_returns_400(api_client, bad_id) -> None:
    response = api_client.get_item_by_id(bad_id)
    assert response.status_code == 400, response.text


@pytest.mark.negative
@pytest.mark.parametrize("bad_seller_id", ["bad-seller", "12.5", "###"])
@allure.title("GET /api/1/{sellerID}/item возвращает 400 для невалидного sellerID")
def test_get_items_by_invalid_seller_id_returns_400(api_client, bad_seller_id) -> None:
    response = api_client.get_items_by_seller(bad_seller_id)
    assert response.status_code == 400, response.text


@pytest.mark.negative
@allure.title("GET /api/1/statistic/{id} возвращает 404 для несуществующего id")
def test_get_statistics_v1_with_nonexistent_id_returns_404(api_client) -> None:
    response = api_client.get_statistics_v1("00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404, response.text


@pytest.mark.negative
@pytest.mark.parametrize("bad_id", ["bad-id", "123", "###"])
@allure.title("GET /api/1/statistic/{id} возвращает 400 для невалидного id")
def test_get_statistics_v1_with_invalid_id_returns_400(api_client, bad_id) -> None:
    response = api_client.get_statistics_v1(bad_id)
    assert response.status_code == 400, response.text


@pytest.mark.negative
@allure.title("GET /api/2/statistic/{id} возвращает 404 для несуществующего id")
def test_get_statistics_v2_with_nonexistent_id_returns_404(api_client) -> None:
    response = api_client.get_statistics_v2("00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404, response.text


@pytest.mark.negative
@pytest.mark.parametrize("bad_id", ["bad-id", "123", "###"])
@allure.title("GET /api/2/statistic/{id} возвращает 400 для невалидного id")
def test_get_statistics_v2_with_invalid_id_returns_400(api_client, bad_id) -> None:
    response = api_client.get_statistics_v2(bad_id)
    assert response.status_code == 400, response.text


@pytest.mark.negative
@allure.title("DELETE /api/2/item/{id} возвращает 404 для несуществующего id")
def test_delete_item_with_nonexistent_id_returns_404(api_client) -> None:
    response = api_client.delete_item("00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404, response.text


@pytest.mark.negative
@pytest.mark.parametrize("bad_id", ["bad-id", "123", "###"])
@allure.title("DELETE /api/2/item/{id} возвращает 400 для невалидного id")
def test_delete_item_with_invalid_id_returns_400(api_client, bad_id) -> None:
    response = api_client.delete_item(bad_id)
    assert response.status_code == 400, response.text
