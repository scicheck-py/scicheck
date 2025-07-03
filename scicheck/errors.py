from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from typing import Any, Optional

    from scicheck_core.typing import Types


#####
# Base Error
#####


class ScicheckError(Exception):
    "Base class for exceptions that include value, name, and message info"

    def __init__(self, value: Any, name: str, message: str) -> None:
        super().__init__(message)
        self.value = value
        self.name = name
        self.message = message


#####
# Base Types
#####


class BadTypeError(ScicheckError, TypeError):
    "When an input is not a supported type"

    def __init__(
        self,
        value: Any,
        types: Types,
        name: str,
        description: str,
        message: Optional[str] = None,
    ) -> None:

        if message is None:
            message = f"{name} must be a {description}"
        ScicheckError.__init__(self, value, name, message)
        self.supported = types


class NotStringError(BadTypeError):
    "When an input is not a string"

    def __init__(self, value: Any, name: str) -> None:
        super().__init__(value, types=(str,), name=name, description="string")


class NotNumericError(BadTypeError):
    "When an input is not an int, float, or complex"

    def __init__(self, value: Any, name: str) -> None:
        super().__init__(
            value,
            types=(int, float, complex),
            name=name,
            description="int, float, or complex",
        )


#####
# Numeric types
#####


class NumericTypeError(ScicheckError):
    "When a numeric input cannot be converted to the required numeric type"

    def __init__(self, input, name, status):
        if isinstance(input, complex):
            value = input
        else:
            value = f"({input})"
        message = f"{name} {value} {status}"
        super().__init__(value, name, message)


class NotFloatError(NumericTypeError):
    "When a numeric input does not represent a float"


class NotRealError(NumericTypeError):
    "When a numeric input does not represent a real-valued number"


class NotIntegerError(NumericTypeError):
    "When a numeric input does not represent an integer"


#####
# Numeric Comparisons
#####


class ComparisonError(ScicheckError):
    "When a real-valued number fails a comparison check"

    def __init__(self, value, comparison, X, name):
        message = f"{name} ({value}) must be {comparison} {X}"
        super().__init__(value, name, message)
        self.comparison = comparison
        self.compare_to = X


class NotLess(ComparisonError):
    "When a real-valued number is not less than a value"


class NotLessEqual(ComparisonError):
    "When a real-valued number is not less than or equal to a value"


class NotGreater(ComparisonError):
    "When a real-valued number is not greater than a value"


class NotGreaterEqual(ComparisonError):
    "When a real-valued number is not greater than or equal to a value"


#####
# Numeric Sign
#####


class SignError(ComparisonError):
    "When a real-valued number has the wrong sign"


class NotPositiveError(SignError):
    "When a real-valued number is not positive"


class NotNegativeError(SignError):
    "When a real-valued number is not negative"


#####
# Base Path errors
#####

class NotPathError(ScicheckError):
    "When an input cannot be converted to a Path"
    def __init__(self, value, name):
        message = f"{name} could not be converted to a Path"
        super().__init__(value, name, message)

class PathError(ScicheckError):
    "When a path is not valid"

class FilePathError(PathError):
    "When a file path is not valid"

class FolderPathError(PathError):
    "When a folder path is not valid"

class MissingPathError(PathError, FileNotFoundError):
    "When a path does not exist"
    def __init__(self, path, name):
        message = f"{name} does not exist\nPath: {path}"
        PathError.__init__(self, path, name, message)

class PathExistsError(PathError, FileExistsError):
    "When a path already exists"
    def __init__(self, path, name):
        message = f"{name} already exists\nPath: {path}"
        PathError.__init__(self, path, name, message)


#####
# Concrete Path errors
#####

class MissingFileError(MissingPathError, FilePathError):
    "When a file path does not exist"

class MissingFolderError(MissingPathError, FolderPathError):
    "When a folder path does not exist"

class FilePathExistsError(PathExistsError, FilePathError):
    "When a file path already exists"

class FolderPathExistsError(PathExistsError, FolderPathError):
    "When a folder path already exists"

class NotFileError(FilePathError):
    "When a path is not a file"

class NotFolderError(FolderPathError):
    "When a path is not a folder"

