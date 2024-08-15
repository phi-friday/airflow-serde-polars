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

    if version != _version:
        from airflow_serde_polars import load_deserializer

        lower_deserializer = load_deserializer(version)
        return lower_deserializer(classname, version, data)

    if not isinstance(data, tuple):
        error_msg = f"serialized {classname} has wrong data type {type(data)}"
        raise TypeError(error_msg)

    if not isinstance(data[0], str):
        error_msg = (
            f"serialized {classname} has wrong data type "
            f"tuple[{type(data[0])}, ...]"
        )
        raise TypeError(error_msg)

    if not isinstance(data[1], str):
        error_msg = (
            f"serialized {classname} has wrong data type "
            f"tuple[str, {type(data[1])}, ...]"
        )
        raise TypeError(error_msg)

    from io import BytesIO

    import polars as pl
    import pyarrow as pa

    with BytesIO(bytes.fromhex(data[0])) as io:
        frame = pl.read_parquet(io)

    _classname = classname.split(".")[-1]
    if _classname == "Series":
        return frame.get_column(frame.columns[0])
    if _classname == "Table":
        table: pa.Table = frame.to_arrow()
        schema_as_bytes = bytes.fromhex(data[1])
        buffer: pa.Buffer = pa.py_buffer(schema_as_bytes)
        schema = pa.ipc.read_schema(buffer)
        return table.cast(schema)
    return frame
