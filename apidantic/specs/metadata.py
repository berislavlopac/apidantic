from __future__ import annotations

from typing import Annotated

from pydantic import (
    AnyUrl,
    BaseModel,
    EmailStr,
    Field,
    HttpUrl,
    model_validator,
)


class InfoObject(BaseModel):
    """The object provides metadata about the API.

    The metadata MAY be used by the clients if needed, and MAY be presented in editing or
    documentation generation tools for convenience.
    """

    title: Annotated[str, Field(description="The title of the API.")]
    version: Annotated[str, Field(description="The version of the OpenAPI Document itself.")]
    summary: Annotated[str | None, Field(description="A short summary of the API.")] = None
    description: Annotated[
        str | None,
        Field(
            description=(
                "A description of the API."
                " CommonMark syntax MAY be used for rich text representation."
            )
        ),
    ] = None
    terms_of_service: Annotated[
        HttpUrl | None,
        Field(
            alias="termsOfService",
            description=(
                "A URI for the Terms of Service for the API. This MUST be in the form of a URI."
            ),
        ),
    ] = None
    contact: Annotated[
        ContactObject | None, Field(description="The contact information for the exposed API.")
    ] = None
    license: Annotated[
        LicenseObject | None, Field(description="The license information for the exposed API.")
    ] = None


class ContactObject(BaseModel):
    """Contact information for the exposed API."""

    name: Annotated[
        str, Field(description="The identifying name of the contact person/organization.")
    ]
    url: Annotated[AnyUrl, Field(description="The URI for the contact information.")]
    email: Annotated[
        EmailStr, Field(description="The email address of the contact person/organization.")
    ]


class LicenseObject(BaseModel):
    """License information for the exposed API."""

    name: Annotated[str, Field(description="The license name used for the API.")]
    url: Annotated[AnyUrl | None, Field(description="The URI for the contact information.")] = (
        None
    )
    identifier: Annotated[
        str | None, Field(description="An SPDX-Licenses expression for the API.")
    ] = None

    @model_validator(mode="after")
    def ensure_identifier_or_url(self):
        """Check that only one of identifier or url is set to a non-false value."""
        if not bool(self.identifier) ^ bool(self.url):
            raise ValueError("Only identifier or url can be set, but not both.")
        return self


class TagObject(BaseModel):
    """Adds metadata to a single tag that is used by the Operation Object.

    It is not mandatory to have a Tag Object per tag defined in the Operation Object instances.
    """

    name: Annotated[str, Field(description="The name of the tag.")]
    description: Annotated[str | None, Field(description="A description for the tag.")] = None
    external_docs: Annotated[
        ExternalDocumentationObject | None,
        Field(description="Additional external documentation for this tag."),
    ] = None


class ExternalDocumentationObject(BaseModel):
    """Allows referencing an external resource for extended documentation."""

    url: Annotated[HttpUrl, Field(description="The URI for the target documentation.")]
    description: Annotated[
        str | None, Field(description="A description of the target documentation.")
    ] = None


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
