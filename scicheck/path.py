
from __future__ import annotations
import typing

from pathlib import Path
from scicheck.errors import (
    NotPathError, 
    MissingFileError, 
    MissingFolderError,
    FilePathExistsError,
    FolderPathExistsError,
    NotFileError,
    NotFolderError,
)

if typing.TYPE_CHECKING:
    from typing import Any


def path(input: Any, name: str = 'input', *, resolve: bool = True) -> Path:

    # Attempt to convert to Path
    if not isinstance(input, Path):
        try:
            path = Path(input)
        except Exception as error:
            raise NotPathError(input, name) from error
        
    # Optionally resolve
    if resolve:
        path = path.resolve()


def _require_file(path: Path, name: str):
    if not path.is_file():
        message = f"{name} is not a file\nPath: {path}"
        raise NotFileError(input, name, message)


def existing_file(input: Any, name: str = 'input', *, suffixes = None) -> Path:

    path_ = path(input, name, resolve=True)
    if not path_.exists():
        for ext in exts


        raise MissingFileError(input, name)
    _require_file(path, name)
    return path
    
def new_file(
    input: Any, 
    name: str = 'input',
    *, 
    exist_ok: bool = False, 
    require_file: bool = True
):

    path_ = path(input, name, resolve=True)
    if not path_.exists():
        return path
    elif not exist_ok:
        raise FilePathExistsError(path, name)
    elif not path_.is_file
    

