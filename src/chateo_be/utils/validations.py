from typing import Any


def not_empty(value: Any) -> bool:
    if not value or not value.strip():
        return False
    return True
