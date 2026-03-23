from __future__ import annotations

import allure
import pytest


@pytest.mark.nonfunctional
@allure.title("GET /api/1/item/{id} отвечает быстрее 5 секунд")
def test_get_item_response_time_is_under_five_seconds(api_client, created_item) -> None:
    response = api_client.get_item_by_id(created_item["id"])
    assert response.status_code == 200, response.text
    assert response.elapsed.total_seconds() < 5


@pytest.mark.nonfunctional
@allure.title("GET /api/1/statistic/{id} отвечает быстрее 5 секунд")
def test_get_statistics_v1_response_time_is_under_five_seconds(api_client, created_item) -> None:
    response = api_client.get_statistics_v1(created_item["id"])
    assert response.status_code == 200, response.text
    assert response.elapsed.total_seconds() < 5


@pytest.mark.nonfunctional
@allure.title("GET /api/2/statistic/{id} отвечает быстрее 5 секунд")
def test_get_statistics_v2_response_time_is_under_five_seconds(api_client, created_item) -> None:
    response = api_client.get_statistics_v2(created_item["id"])
    assert response.status_code == 200, response.text
    assert response.elapsed.total_seconds() < 5
