# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
from __future__ import annotations

from itertools import permutations

import polars as pl
import pytest
from airflow.serialization.serde import deserialize, serialize

from airflow_serde_polars import load_deserializer, load_serializer
from airflow_serde_polars.utils.parse import get_versions_all


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


@pytest.mark.parametrize(
    "versions",
    (
        pytest.param((v1, v2), id=f"[ser={v1},de={v2}]")
        for v1, v2 in permutations(get_versions_all(), 2)
    ),
)
def test_serde_diff_version_error(polars_frame, versions: tuple[int, int]):
    serializer = load_serializer(versions[0])
    deserializer = load_deserializer(versions[1])

    value, classname, version, _ = serializer(polars_frame)
    with pytest.raises((TypeError, ValueError)):
        deserializer(classname, version, value)


@pytest.mark.airflow()
def test_serde_frame_airflow(polars_frame):
    value = serialize(polars_frame)
    assert isinstance(value, dict)
    load = deserialize(value)
    assert isinstance(load, pl.DataFrame)
    assert polars_frame.equals(load)


@pytest.mark.airflow()
def test_serde_series_airflow(polars_frame):
    for field in polars_frame.iter_columns():
        value = serialize(field)
        assert isinstance(value, dict)
        load = deserialize(value)
        assert isinstance(load, pl.Series)
        assert field.equals(load)
