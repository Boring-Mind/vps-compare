from typing import Any, Union

JSON_DICT = dict[str, Any]
JSON = Union[dict[str, Any], list[Any]]


class NOTSET:
    """Is needed to distinguish between None and not set value."""

    pass
