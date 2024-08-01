from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from airflow_serde_polars.utils.parse import get_versions_all

if TYPE_CHECKING:
    from airflow_serde_polars.main import Deserializer, Serializer

_versions_all = get_versions_all()


@pytest.fixture(
    params=[pytest.param(version, id=f"v{version}") for version in _versions_all],
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
