from __future__ import annotations  # noqa: INP001

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import polars as pl
    from airflow.serialization.serde import U


serializers = ["polars.dataframe.frame.DataFrame", "polars.series.series.Series"]
deserializers = serializers
__version__: int


def serialize(o: object) -> tuple[U, str, int, bool]:  # noqa: D103 # pyright: ignore[reportUnknownParameterType]
    from airflow_serde_polars import load_serializer
    from airflow_serde_polars.utils.parse import get_latest_version

    latest_version = get_latest_version()
    serializer = load_serializer(latest_version)
    return serializer(o)


def deserialize(classname: str, version: int, data: object) -> pl.DataFrame | pl.Series:  # noqa: D103
    from airflow_serde_polars import load_deserializer

    deserializer = load_deserializer(version)
    return deserializer(classname, version, data)


def __getattr__(name: str) -> Any:  # pragma: no cover
    if name == "__version__":
        from airflow_serde_polars.utils.parse import get_latest_version

        return get_latest_version()

    error_msg = f"The attribute named {name!r} is undefined."
    raise AttributeError(error_msg)
