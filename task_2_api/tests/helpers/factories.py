from __future__ import annotations

import random
import uuid


def random_seller_id() -> int:
    return random.randint(111111, 999999)


def make_payload(seller_id: int | None = None) -> dict:
    seller = seller_id if seller_id is not None else random_seller_id()
    return {
        "sellerID": seller,
        "name": f"qa-item-{uuid.uuid4().hex[:8]}",
        "price": random.randint(1, 999999),
        "statistics": {
            "likes": random.randint(0, 999),
            "viewCount": random.randint(0, 9999),
            "contacts": random.randint(0, 999),
        },
    }
