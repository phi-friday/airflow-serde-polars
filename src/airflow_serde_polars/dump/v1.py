from __future__ import annotations

from typing import TYPE_CHECKING

from airflow_serde_polars.utils.parse import find_version

if TYPE_CHECKING:
    from airflow.serialization.serde import U

_version = find_version(__file__)


def serialize(o: object) -> tuple[U, str, int, bool]:  # pyright: ignore[reportUnknownParameterType]
    from io import BytesIO

    import polars as pl
    from airflow.utils.module_loading import qualname

    if not isinstance(o, (pl.DataFrame, pl.Series)):
        return "", "", 0, False

    name = qualname(o)
    if isinstance(o, pl.Series):
        o = o.to_frame(o.name)

    with BytesIO() as io:
        o.write_parquet(io, compression="snappy")
        result = io.getvalue().hex()

    return result, name, _version, True
