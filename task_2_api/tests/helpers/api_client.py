from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class ApiClient:
    base_url: str
    timeout: int = 10

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def create_item(self, payload: dict[str, Any]) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/1/item",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )

    def get_item_by_id(self, item_id: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/1/item/{item_id}", timeout=self.timeout)

    def get_items_by_seller(self, seller_id: int | str) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/1/{seller_id}/item", timeout=self.timeout)

    def get_statistics_v1(self, item_id: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/1/statistic/{item_id}", timeout=self.timeout)

    def get_statistics_v2(self, item_id: str) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/2/statistic/{item_id}", timeout=self.timeout)

    def delete_item(self, item_id: str) -> requests.Response:
        return self.session.delete(f"{self.base_url}/api/2/item/{item_id}", timeout=self.timeout)
