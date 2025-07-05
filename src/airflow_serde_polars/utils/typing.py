from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

Dict, List, Set, Tuple = dict, list, set, tuple

if TYPE_CHECKING:
    from typing import Union

    from typing_extensions import TypeAlias, TypeVar

    T = TypeVar(
        "T",
        infer_variance=True,
        bound="AirflowSerdeType[Any]",
        default="AirflowSerdeType[Any]",
    )
    T2 = TypeVar(
        "T2", infer_variance=True, bound="bool | float | int | str", default=Any
    )

    AirflowSerdeResult: TypeAlias = tuple[T, str, int, bool]
    AirflowSerdeType: TypeAlias = Union[
        T2,
        dict[Any, "AirflowSerdeType[T2]"],
        list["AirflowSerdeType[T2]"],
        tuple["AirflowSerdeType[T2]", ...],
        set["AirflowSerdeType[T2]"],
    ]

ErrorResult: AirflowSerdeResult[Any] = ("", "", 0, False)
