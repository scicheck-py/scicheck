from __future__ import annotations

import typing

from scicheck_core.config import config
from scicheck_core.errors import BadTypeError, NotStringError
from scicheck_core.utils import context, strlist

if typing.TYPE_CHECKING:
    from typing import Any, Optional

    from scicheck_core.typing import Types

# Alias for the built-in type object (whose name we will overshadow)
type_object = type


#####
# User Functions
#####


def type(
    input: Any,
    types: type_object | Types,
    name: str = "input",
    description: Optional[str] = None,
) -> Any:
    """
    Checks an input is a supported type and returns the input
    ----------
    type(input, types)
    Checks that an input is one of the supported types and returns the input. The
    `types` input may be a type, tuple of types, or a UnionType object. Raises an
    informative error if the input is not a supported type.

    Note: The `types` input should not include `None` as a supported type. To validate
    the type of an optional input, we recommend the following syntax:

        if input is not None:
            scicheck.type(input, ...)

    type(..., name)
    type(..., name, description)
    Customizes the error message for when the input fails the check. The error message
    will follow the form: "{name} must be a {description}". The `name` is the name of
    the input being validated and defaults to "input". The `description` provides a
    description of the supported types and defaults to the class names of the input
    types.
    ----------
    Inputs:
        input: The input being validated
        types: The allowed input types
        name: A name for the input being validated
        description: A description of the supported types

    Outputs:
        Any: The validated input

    Raises:
        TypeError: If the input is not one of the supported types
    """

    # Parse and optionally debug the command options
    types = _types(types)
    description = _description(description, types)
    if config.debug:
        string(name, name=context("name"))

    # Return the value if valid, or informative error if failed
    if not isinstance(input, types):
        raise BadTypeError(input, types, name, description)
    return input


def string(
    input: Any,
    name: str = "input",
) -> Any:
    """
    Checks an input is a string and returns the input
    ----------
    string(input)
    string(input, name)
    Checks an input is a string and returns the input if valid. Otherwise, uses an
    informative error. Use `name` to provide a name for the input being checked. The
    `name` defaults to "input" and is always placed at the beginning of the error
    message.
    ----------
    Inputs:
        input: The input being checked
        name: A name for the input

    Outputs:
        str: The validated string

    Raises:
        NotStringError: If the input is not a string
    """

    # Optionally debug the name
    if config.debug and not isinstance(name, str):
        raise NotStringError(value=name, name=context("name"))

    # Validate the input value
    if not isinstance(input, str):
        raise NotStringError(input, name)
    return input


#####
# Debugging
#####


def _types(types: Any) -> Types:
    "Ensures that the `types` input is valid"

    # Format scalar type object as a singleton tuple
    if isinstance(types, type_object):
        types = (types,)

    # Optionally debug the types
    if config.debug:
        stack = 2

        # Must be a tuple (because wasn't already a type object)
        if not isinstance(types, tuple):
            raise BadTypeError(
                types,
                types=(type_object, tuple),
                name=context("types", stack),
                description="type object, or a tuple of type objects",
            )

        # Check tuple elements
        for t, type in enumerate(types):
            if not isinstance(type, type_object):
                raise BadTypeError(
                    type,
                    types=(type_object,),
                    name=context(f"types[{t}]", stack),
                    description="type object",
                )
    return types


def _description(description: Any | None, types: Types) -> str:
    "Ensures that the `description` input is valid"

    # If no description was provided, use the class names
    if description is None:
        description = strlist([type.__name__ for type in types])

    # Optionally debug the description
    if config.debug:
        name = context(input="description", stack=2)
        string(description, name)
    return description
