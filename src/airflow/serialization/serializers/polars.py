from __future__ import annotations  # noqa: INP001

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl
    from airflow.serialization.serde import U


serializers = ["polars.dataframe.frame.DataFrame", "polars.series.series.Series"]
deserializers = serializers
__version__ = 1


def serialize(o: object) -> tuple[U, str, int, bool]:  # noqa: D103 # pyright: ignore[reportUnknownParameterType]
    from airflow_serde_polars import load_serializer

    serializer = load_serializer(__version__)
    return serializer(o)


def deserialize(classname: str, version: int, data: object) -> pl.DataFrame | pl.Series:  # noqa: D103
    from airflow_serde_polars import load_deserializer

    deserializer = load_deserializer(__version__)
    return deserializer(classname, version, data)
