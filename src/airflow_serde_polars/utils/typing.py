from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple

if TYPE_CHECKING:
    from typing_extensions import TypeAlias, TypeVar

    T = TypeVar("T", infer_variance=True)

    AirflowSerdeResponse: TypeAlias = Tuple[T, str, int, bool]

ErrorResponse: AirflowSerdeResponse[Any] = ("", "", 0, False)
