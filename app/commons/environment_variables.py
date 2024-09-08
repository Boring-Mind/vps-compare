import os
from typing import Any, Union

from commons.typing import JSON, NOTSET
from orjson import orjson


class EnvVariable:
    _TRUE_VALUES = {"true", "1", "t", "y", "yes"}
    _FALSE_VALUES = {"false", "0", "f", "n", "no"}

    @classmethod
    def get(cls, key: str, default=NOTSET, cast=None) -> Any:
        """Get env variable and raise exception if not found."""
        value = os.getenv(key)
        if value is None:
            if default is not NOTSET:
                return default
            raise ValueError(f"Environment variable {key} is missing.")

        return cls._cast_value(key, value, cast)

    @classmethod
    def _cast_value(
        cls, key: str, value: Any, cast=None
    ) -> Union[str, bool, int, float, JSON]:
        if cast is bool:
            try:
                return cls._cast_string_into_bool(value)
            except ValueError as exc:
                raise ValueError(
                    f"Environment variable {key} is not a valid boolean string. "
                    f"Actual value was: {value}"
                ) from exc
        if cast is int:
            try:
                return int(value)
            except ValueError as exc:
                raise ValueError(
                    f"Environment variable {key} is not a valid integer. "
                    f"Actual value was: {value}"
                ) from exc
        if cast is float:
            try:
                return float(value)
            except ValueError as exc:
                raise ValueError(
                    f"Environment variable {key} is not a valid float. "
                    f"Actual value was: {value}"
                ) from exc
        if cast == "json":
            try:
                return orjson.loads(value)
            except orjson.JSONEncodeError as exc:
                raise ValueError(
                    f"Environment variable {key} is not a valid JSON string. "
                    f"Actual value was: {value}"
                ) from exc

        return value

    @classmethod
    def _cast_string_into_bool(cls, string: str) -> bool:
        if string.lower() in cls._TRUE_VALUES:
            return True
        elif string.lower() in cls._FALSE_VALUES:
            return False
        else:
            raise ValueError()
