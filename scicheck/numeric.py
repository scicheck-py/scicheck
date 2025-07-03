
from __future__ import annotations

import typing
from math import isinf, isnan
from operator import lt, le, gt, ge

from scicheck_core.config import config
from scicheck_core.errors import (
    NotFloatError, 
    NotIntegerError,
    NotNumericError, 
    NotRealError, 
    NotLess, 
    NotLessEqual,
    NotGreater,
    NotGreaterEqual,
    NotPositiveError,
    NotNegativeError,
)
from scicheck_core.type import string, type
from scicheck_core.utils import context

if typing.TYPE_CHECKING:
    from typing import Any, Callable
    Real = int | float
    Numeric = Real | complex


# Aliases for built-in types that we will overshadow
float_ = float
complex_ = complex


#####
# Types
#####


def numeric(input: Any, name: str = 'input') -> int | float | complex:

    if not isinstance(input, (int, float_, complex_)) or isinstance(input, bool):
        raise NotNumericError(input, name)
    return input


def complex(input: Any, name: str = 'input') -> complex_:
    
    numeric(input, name)
    if isinstance(input, (int, float_)):
        input += 0j
    return input


def float(input: Any, name: str = 'input') -> float_:

    numeric(input, name)
    if isinstance(input, int):
        return float_(input)
    elif isinstance(input, float_):
        return input
    elif input.imag == 0:
        return input.real
    else:
        status = 'is complex-valued, so cannot be converted to a float'
        raise NotFloatError(input, name, status)


def integer(input: Any, name: str = 'input') -> int:

    # Require numeric type. Int is immediately valid
    numeric(input, name)
    if isinstance(input, int):
        return input
    
    # Complex values are not permitted
    elif isinstance(input, complex_):
        if input.imag == 0:
            input = input.real
        else:
            status = 'is complex-valued, so cannot be converted to an integer'
            raise NotIntegerError(input, name, status)

    # Floats must represent an integer
    if not input.is_integer():
        raise NotIntegerError(input, name, status="does not represent an integer")
    return int(input)


def real(
    input: Any, 
    name: str = 'input', 
    *, 
    allow_nan: bool = False,
    allow_inf: bool = False, 
) -> int | float_:

    # Require numeric input. Return int immediately
    numeric(input, name)
    if isinstance(input, int):
        return input
    
    # Complex values are not allowed
    if isinstance(input, complex_):
        if input.imag == 0:
            input = input.real
        else:
            raise NotRealError(input, name, status='is not real-valued')

    # Optionally prevent NaN and Inf
    if (not allow_nan and isnan(input)) or (not allow_inf and isinf(input)):
        raise NotRealError(input, name, status='is not real-valued')
    return input


#####
# Comparison operators
#####

def _operator(op: Callable):
    "Returns the description and error associated with different operators"

    if op == lt:
        return 'less than', NotLess
    elif op == le:
        return 'less than or equal to', NotLessEqual
    elif op == gt:
        return 'greater than', NotGreater
    elif op == ge:
        return 'greater than or equal to', NotGreaterEqual



def _compare(input: Real, op: Callable, X: Real, name: str) -> None:

    if not op(input, X):
        description, error = _operator(op)
        raise error(input, description, X, name)


def less(input: Real, X: Real, name: str = 'input') -> None:
    _compare(input, lt, X, name)
    
def less_equal(input: Real, X: Real, name: str = 'input') -> None:
    _compare(input, le, X, name)

def greater(input: Real, X: Real, name: str = 'input') -> None:
    _compare(input, gt, X, name)

def greater_equal(input: Real, X: Real, name: str = 'input') -> None:
    _compare(input, ge, X, name)



#####
# Inclusive/Exclusive Ranges
#####

def in_range(
    input: Real, 
    min: Real, 
    max: Real,
    name: str = 'input',
    *, 
    include_min: bool = True, 
    include_max: bool = True,
) -> None:
    
    # Get the operators for each bound
    bounds = (
        (min, include_min, ge, gt),
        (max, include_max, le, lt),
    )

    # Compare to each bound. Skip any unprovided bounds
    for bound, use_inclusive, inclusive, exclusive in bounds:
        op = inclusive if use_inclusive else exclusive
        _compare(input, op, bound, name)


def _sign(
    input: Real, 
    name: str, 
    allow_zero: bool, 
    inclusive: Callable, 
    exclusive: Callable, 
    error: Exception
):

    op = inclusive if allow_zero else exclusive
    if not op(input, 0):
        description, _ = _operator(op)
        raise error(input, description, 0, name)


def positive(input: Real, name: str = 'input', *, allow_zero: bool = False):
    _sign(input, name, allow_zero, inclusive=ge, exclusive=gt, error=NotPositiveError)

def negative(input: Real, name: str = 'input', *, allow_zero: bool = False):
    _sign(input, name, allow_zero, inclusive=le, exclusive=lt, error=NotNegativeError)


 
