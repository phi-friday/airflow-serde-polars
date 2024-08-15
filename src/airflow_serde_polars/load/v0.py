from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl


def deserialize(classname: str, version: int, data: object) -> pl.DataFrame | pl.Series:
    from airflow_serde_polars.load.v1 import deserialize as v1_deserialize

    if not isinstance(data, str) or not data.endswith("_salt"):
        error_msg = f"Invalid data: {data!r}."
        raise TypeError(error_msg)
    data = data[:-5]

    return v1_deserialize(classname, version, data)
