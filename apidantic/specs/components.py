from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

ComponentKey = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9\.\-_]+$")]


class SchemaObject(BaseModel): ...


class ResponseObject(BaseModel): ...


class ReferenceObject(BaseModel): ...


class ComponentsObject(BaseModel):
    """Holds a set of reusable objects for different aspects of the OAS.

    All objects defined within the Components Object will have no effect on the API unless
    they are explicitly referenced from outside the Components Object.
    """

    schemas: Annotated[
        Mapping[ComponentKey, list[SchemaObject]],
        Field(description="Collection of reusable schema objects."),
    ]
    responses: Annotated[
        Mapping[ComponentKey, list[ResponseObject | ReferenceObject]],
        Field(description="Collection of reusable response objects."),
    ]
