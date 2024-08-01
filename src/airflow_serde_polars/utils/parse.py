from __future__ import annotations

import re
from pathlib import Path

__all__ = ["find_version"]

_RE_VERSION = re.compile(r"v(?P<version>\d+)")


def find_version(file: str) -> int:
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
