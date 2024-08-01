from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl
    from airflow.serialization.serde import U


def serialize(o: object) -> tuple[U, str, int, bool]:  # noqa: D103 # pyright: ignore[reportUnknownParameterType]
    from airflow_serde_polars.dump.v1 import serialize

    result, name, *_ = serialize(o)
    return f"{result}_salt", name, 0, True


def deserialize(classname: str, version: int, data: object) -> pl.DataFrame | pl.Series:  # noqa: D103
    from airflow_serde_polars.load.v1 import deserialize as v1_deserialize

    if isinstance(data, str):
        data = data.rstrip("_salt")

    return v1_deserialize(classname, version, data)
