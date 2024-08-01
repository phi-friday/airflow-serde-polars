from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    import polars as pl
    from airflow.serialization.serde import U

    class Serializer(Protocol):
        def __call__(self, o: object) -> tuple[U, str, int, bool]:  # pyright: ignore[reportUnknownParameterType]
            ...

    class Deserializer(Protocol):
        def __call__(
            self, classname: str, version: int, data: object
        ) -> pl.DataFrame | pl.Series: ...


__all__ = ["load_serializer", "load_deserializer"]


def load_serializer(version: float | str) -> Serializer:
    """Load the serializer for the given version.

    Args:
        version: The version of the serializer.

    Returns:
        The serializer function.
    """
    if isinstance(version, str):
        version = version.strip()
    version = int(version)

    module_name = f"airflow_serde_polars.dump.v{version}"
    module = import_module(module_name)
    return module.serialize


def load_deserializer(version: float | str) -> Deserializer:
    """Load the deserializer for the given version.

    Args:
        version: The version of the deserializer.

    Returns:
        The deserializer function.
    """
    if isinstance(version, str):
        version = version.strip()
    version = int(version)

    module_name = f"airflow_serde_polars.load.v{version}"
    module = import_module(module_name)
    return module.deserialize
