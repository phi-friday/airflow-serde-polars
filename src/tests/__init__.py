from __future__ import annotations

from typing import Any

from airflow_serde_polars.main import load_deserializer, load_serializer

__all__ = ["load_serializer", "load_deserializer"]
__version__: str


def __getattr__(name: str) -> Any:  # pragma: no cover
    from importlib.metadata import version

    if name == "__version__":
        return version("airflow-serde-polars")

    error_msg = f"The attribute named {name!r} is undefined."
    raise AttributeError(error_msg)
