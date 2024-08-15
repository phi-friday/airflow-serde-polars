from __future__ import annotations

from typing import TYPE_CHECKING

from airflow_serde_polars.utils.parse import find_version
from airflow_serde_polars.utils.typing import ErrorResult

if TYPE_CHECKING:
    from airflow_serde_polars.utils.typing import AirflowSerdeResult

_version = find_version(__file__)


def serialize(o: object) -> AirflowSerdeResult[str]:
    from io import BytesIO

    import polars as pl
    from airflow.utils.module_loading import qualname

    name = qualname(o)

    if not isinstance(o, (pl.DataFrame, pl.Series)):
        return ErrorResult

    if isinstance(o, pl.Series):
        o = o.to_frame(o.name)

    with BytesIO() as io:
        o.write_parquet(io, compression="snappy")
        result = io.getvalue().hex()

    return result, name, _version, True
