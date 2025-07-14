
from __future__ import annotations

import typing

from scicheck.utils import convert

from scicheck.errors import (
    NotNumericError,
    CannotConvertToNumeric,

)

if typing.TYPE_CHECKING:
    from typing import Any
    Numeric = int | float | complex

# Aliases for overshadowed types
float_ = float
complex_ = complex


def _not_numeric(name: str) -> NotNumericError:
    message = f"{name} must be a numeric type"
    return NotNumericError(message)


def numeric(input: Any, name: str = 'input', *, strict: bool = False) -> Numeric:
    "Checks that an input represents a numeric type"

    # Strict
    if isinstance(input, (int, float_, complex_)):
        return input
    elif strict:
        raise _not_numeric(name)
    
    # Attempt conversion
    input = convert(
        input, complex_, name, 'numeric type', CannotConvertToNumeric
    )

    # Simplify type as appropriate
    if input.imag == 0:
        input = input.real
    if input.is_integer():
        input = int(input)
    return input



def float(
    input: Any, 
    name: str = 'input', 
    *, 
    strict: bool = False,
    numeric_only: bool = True,
) -> float_:

    # Strict
    if isinstance(input, float_):
        return input
    elif strict:
        raise NotFloatError(_message.not_type(name, 'float'))
    
    # Handle complex and int types
    elif isinstance(input, complex_):
        return _complex_as_float(input, name, 'a float', CannotConvertToFloat)
    elif isinstance(input, int):
        return float_(input)
    
    # Require numeric, or attempt type conversion
    elif numeric_only:
        raise _not_numeric(name)
    else:
        return convert(input, float_, name, 'a float', CannotConvertToFloat)
    
