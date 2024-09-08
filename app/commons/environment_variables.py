import os
from typing import Any


def get_env_variable(key: str) -> Any:
    """Get env variable and raise exception if not found."""
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is missing.")
    return value
