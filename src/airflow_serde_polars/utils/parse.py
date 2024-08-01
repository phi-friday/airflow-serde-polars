from __future__ import annotations

import re
from functools import lru_cache
from itertools import chain
from pathlib import Path

__all__ = ["find_version"]

_RE_VERSION = re.compile(r"v(?P<version>\d+)")


def find_version(file: str | Path) -> int:
    """Find the version of the serializer/deserializer.

    Args:
        file: The file path.

    Returns:
        The version of the serializer/deserializer.
    """
    stem = Path(file).stem
    if not (match := _RE_VERSION.match(stem)):
        error_msg = f"Version not found in {file!s}"
        raise ValueError(error_msg)

    version = match.group("version")
    return int(version)


@lru_cache
def get_latest_version() -> int:
    """Get the latest version of the serializer/deserializer."""
    versions = get_versions_all()
    return max(versions)


@lru_cache
def get_versions_all() -> tuple[int, ...]:
    """Get all the versions of the serializer/deserializer."""
    dump = Path(__file__).parent.with_name("dump")
    load = dump.with_name("load")

    return tuple({
        find_version(file) for file in chain(dump.glob("v*.py"), load.glob("v*.py"))
    })
