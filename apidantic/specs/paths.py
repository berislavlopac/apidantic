from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from pydantic import BaseModel, StringConstraints

PathSpec = Annotated[str, StringConstraints(pattern=r"^/")]

type PathsMapping = Mapping[PathSpec, PathItemObject]
"""Holds the relative paths to the individual endpoints and their operations."""


class PathItemObject(BaseModel):
    """Describes the operations available on a single path.

    A Path Item MAY be empty, due to ACL constraints. The path itself is still exposed to
    the documentation viewer, but they will not know which operations and parameters are
    available.
    """
