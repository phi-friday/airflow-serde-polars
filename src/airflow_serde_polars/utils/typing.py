from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Union

if sys.version_info < (3, 9):
    from typing import Dict, List, Set, Tuple
else:
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
    T2 = TypeVar("T2", infer_variance=True, bound="AirflowSerdeType", default=Any)

    AirflowSerdeResult: TypeAlias = Tuple[T, str, int, bool]
    AirflowSerdeType: TypeAlias = Union[
        bool, float, int, Dict[Any, T2], List[T2], str, Tuple[T2, ...], Set[T2]
    ]

ErrorResult: AirflowSerdeResult[Any] = ("", "", 0, False)
