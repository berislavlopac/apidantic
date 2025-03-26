from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    Field,
    model_validator,
)


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

    @model_validator(mode="after")
    def substitute_variables(self):
        """Replace variable placeholders with corresponding values."""
        if self.variables:
            variables = {key: value.default for key, value in self.variables.items()}
            self.url = AnyHttpUrl(str(self.url).format(**variables))
        elif "{" in str(self.url):
            raise ValueError(
                "The server URL seems to include variables but values are not provided."
            )
        return self


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
