from __future__ import annotations

from typing import TYPE_CHECKING

from airflow_serde_polars.utils.parse import find_version

if TYPE_CHECKING:
    import polars as pl
    import pyarrow as pa


_version = find_version(__file__)


def deserialize(  # pyright: ignore[reportUnknownParameterType]
    classname: str, version: int, data: object
) -> pl.DataFrame | pl.Series | pa.Table:
    if version > _version:
        error_msg = f"serialized {version} of {classname} > {_version}"
        raise TypeError(error_msg)

    if not isinstance(data, str):
        error_msg = f"serialized {classname} has wrong data type {type(data)}"
        raise TypeError(error_msg)

    from io import BytesIO

    import polars as pl

    with BytesIO(bytes.fromhex(data)) as io:
        frame = pl.read_parquet(io)

    _classname = classname.split(".")[-1]
    if _classname == "Series":
        return frame.get_column(frame.columns[0])
    if _classname == "Table":
        return frame.to_arrow()
    return frame
