import pytest

from apidantic.specs.core import ServerVariableObject


def test_server_variable_object_default_value_is_in_enum():
    with pytest.raises(ValueError):
        ServerVariableObject(default="foo", enum=["bar", "baz"])
