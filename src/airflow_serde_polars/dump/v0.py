from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from airflow.serialization.serde import U


def serialize(o: object) -> tuple[U, str, int, bool]:  # pyright: ignore[reportUnknownParameterType]
    from airflow_serde_polars.dump.v1 import serialize as v1_serialize

    result, name, *_ = v1_serialize(o)
    return f"{result}_salt", name, 0, True
