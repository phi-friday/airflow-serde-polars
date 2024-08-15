from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Set, Tuple, Union

if TYPE_CHECKING:
    from typing_extensions import TypeAlias, TypeVar

    T = TypeVar(
        "T",
        infer_variance=True,
        bound="AirflowSerdeType[Any]",
        default="AirflowSerdeType[Any]",
    )
    T2 = TypeVar("T2", infer_variance=True, bound="AirflowSerdeType", default=Any)

    AirflowSerdeResponse: TypeAlias = Tuple[T, str, int, bool]
    AirflowSerdeType: TypeAlias = Union[
        bool, float, int, Dict[Any, T2], List[T2], str, Tuple[T2, ...], Set[T2]
    ]

ErrorResponse: AirflowSerdeResponse[Any] = ("", "", 0, False)
