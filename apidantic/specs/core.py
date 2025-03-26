from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Literal

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    Field,
    model_validator,
)

from .components import ComponentsObject
from .metadata import ExternalDocumentationObject, InfoObject, TagObject
from .paths import PathItemObject, PathsMapping


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


class ServerObject(BaseModel):
    """An object representing a Server."""

    url: Annotated[
        AnyHttpUrl,
        Field(
            description=(
                "A URL to the target host."
                " Variable substitutions will be made when a variable is named in `{braces}`."
            )
        ),
    ] = AnyHttpUrl("http://example.com")
    description: str | None = None
    variables: Annotated[
        Mapping[str, ServerVariableObject] | None,
        Field(
            description=(
                "A map between a variable name and its value."
                " The value is used for substitution in the server's URL template."
            )
        ),
    ] = None


class ServerVariableObject(BaseModel):
    """An object representing a Server Variable for server URL template substitution."""

    default: Annotated[
        str,
        Field(
            description=(
                "The default value to use for substitution,"
                " which SHALL be sent if an alternate value is not supplied."
            )
        ),
    ]
    enum: Annotated[
        list[str] | None,
        Field(
            description=(
                "An enumeration of string values to be used"
                " if the substitution options are from a limited set."
            )
        ),
    ] = None
    description: str | None = None

    @model_validator(mode="after")
    def ensure_default_in_enum_if_set(self):
        """Check that only one of identifier or url is set to a non-false value."""
        if self.enum is not None and self.default not in self.enum:
            raise ValueError("The `default` value must be one of the values in `enum`.")
        return self


class SecurityRequirementObject(BaseModel):
    """Lists the required security schemes to execute this operation.

    The name used for each property MUST correspond to a security scheme declared in the
    Security Schemes under the Components Object.

    A Security Requirement Object MAY refer to multiple security schemes in which case all
    schemes MUST be satisfied for a request to be authorized. This enables support for
    scenarios where multiple query parameters or HTTP headers are required to convey
    security information.

    When the security field is defined on the OpenAPI Object or Operation Object and
    contains multiple Security Requirement Objects, only one of the entries in the list
    needs to be satisfied to authorize the request. This enables support for scenarios
    where the API allows multiple, independent security schemes.

    An empty Security Requirement Object ({}) indicates anonymous access is supported.
    """
