from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Literal

from pydantic import BaseModel, Field

from .components import ComponentsObject
from .metadata import (
    ExternalDocumentationObject,
    InfoObject,
    SecurityRequirementObject,
    TagObject,
)
from .paths import PathItemObject, PathsMapping
from .server import ServerObject


class OpenAPIDocument(BaseModel):
    """The main container for an OpenAPI specification.

    Currently, only OpenAPI 3.1.1 is supported.
    """

    openapi: Annotated[
        Literal["3.1.1"],
        Field(
            description=(
                "This string MUST be the version number of the OpenAPI Specification that the"
                " OpenAPI Document uses. The openapi field SHOULD be used by tooling to"
                " interpret the OpenAPI Document."
            )
        ),
    ] = "3.1.1"
    info: Annotated[
        InfoObject,
        Field(
            description=(
                "Provides metadata about the API."
                " The metadata MAY be used by tooling as required."
            )
        ),
    ]
    # json_schema_dialect: str = ""
    servers: Annotated[
        list[ServerObject],
        Field(
            description=(
                "An array of Server Objects,"
                " which provide connectivity information to a target server."
            ),
            default_factory=lambda: [ServerObject()],
        ),
    ]
    paths: Annotated[
        PathsMapping | None,
        Field(description="The available paths and operations for the API."),
    ] = None
    webhooks: Annotated[
        Mapping[str, PathItemObject] | None,
        Field(
            description=(
                "The incoming webhooks that MAY be received as part of this API and that the"
                " API consumer MAY choose to implement."
            )
        ),
    ] = None
    components: Annotated[
        ComponentsObject,
        Field(description="An element to hold various Objects for the OpenAPI Description."),
    ]
    security: Annotated[
        list[SecurityRequirementObject] | None,
        Field(
            description=(
                "A declaration of which security mechanisms can be used across the API. The"
                " list of values includes alternative Security Requirement Objects that can be"
                " used. Only one of the Security Requirement Objects need to be satisfied to"
                " authorize a request. Individual operations can override this definition."
            )
        ),
    ] = None
    tags: Annotated[
        list[TagObject],
        Field(
            description=(
                "A list of tags used by the OpenAPI Description with additional metadata. The"
                " order of the tags can be used to reflect on their order by the parsing tools."
                " Not all tags that are used by the Operation Object must be declared. The tags"
                " that are not declared MAY be organized randomly or based on the tools' logic."
                " Each tag name in the list MUST be unique."
            )
        ),
    ]
    external_docs: Annotated[
        ExternalDocumentationObject,
        Field(alias="externalDocs", description="Additional external documentation."),
    ]
