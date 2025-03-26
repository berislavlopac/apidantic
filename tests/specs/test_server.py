import pytest
from pydantic import AnyHttpUrl

from apidantic.specs.server import ServerObject, ServerVariableObject


def test_error_if_variable_default_not_in_enum():
    """ValueError is raised if the server variable default value is not in enum."""
    with pytest.raises(ValueError):
        ServerVariableObject(default="foo", enum=["bar", "baz"])


def test_server_variable_value_is_substituted_in_url():
    server = ServerObject(
        description="Example.com server",
        url="https://{hostname}.com",
        variables={"hostname": ServerVariableObject(default="foobar")},
    )

    assert server.url == AnyHttpUrl("https://foobar.com/")


def test_server_variable_substitution_fails_if_no_variables_provided():
    with pytest.raises(ValueError):
        ServerObject(url="https://{hostname}.com")
