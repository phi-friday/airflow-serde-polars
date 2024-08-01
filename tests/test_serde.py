# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
from __future__ import annotations

import polars as pl
import pytest

from airflow_serde_polars import load_deserializer, load_serializer


@pytest.fixture(scope="module")
def polars_frame() -> pl.DataFrame:
    return (
        pl.DataFrame({"integer": pl.int_range(0, 1_000, eager=True)})
        .with_columns(pl.col("integer").cast(pl.Float64()).add(0.1).alias("float"))
        .with_columns(
            pl.concat_str([pl.col("integer"), pl.col("float")], separator="_").alias(
                "string"
            )
        )
        .with_columns(pl.col("string").cast(pl.Binary()).alias("binary"))
    )


def test_load_serializer(serde_version):
    serializer = load_serializer(serde_version)
    assert callable(serializer)


def test_load_deserializer(serde_version):
    deserializer = load_deserializer(serde_version)
    assert callable(deserializer)


def test_serde_frame(polars_frame, serializer, deserializer):
    value, classname, version, _ = serializer(polars_frame)
    load = deserializer(classname, version, value)

    assert isinstance(load, pl.DataFrame)
    assert polars_frame.equals(load)


def test_serde_series(polars_frame, serializer, deserializer):
    for field in polars_frame.iter_columns():
        value, classname, version, _ = serializer(field)
        load = deserializer(classname, version, value)

        assert isinstance(load, pl.Series)
        assert field.equals(load)
