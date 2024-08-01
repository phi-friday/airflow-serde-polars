from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from airflow_serde_polars.main import Deserializer, Serializer


@pytest.fixture(
    params=[pytest.param(version, id=f"v{version}") for version in range(2)],
    scope="session",
)
def serde_version(request: pytest.FixtureRequest) -> int:
    return request.param


@pytest.fixture()
def serializer(serde_version: int) -> Serializer:
    from airflow_serde_polars.main import load_serializer

    return load_serializer(serde_version)


@pytest.fixture()
def deserializer(serde_version: int) -> Deserializer:
    from airflow_serde_polars.main import load_deserializer

    return load_deserializer(serde_version)
