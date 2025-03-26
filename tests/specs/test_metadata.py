import pytest

from apidantic.specs.metadata import LicenseObject


def test_license_object_is_set_with_identifier():
    lic = LicenseObject(
        name="MIT",
        identifier="MIT license",
    )
    assert lic.name == "MIT"
    assert lic.identifier == "MIT license"
    assert lic.url is None


def test_license_object_is_set_with_url():
    name = "MIT"
    url = "https://example.com"
    lic = LicenseObject(name=name, url=url)

    assert lic.name == name
    assert str(lic.url).startswith(url)
    assert str(lic.url) == f"{url}/"  # AnyUrl appends trailing slash
    assert lic.identifier is None


def test_license_object_raises_error_if_set_with_both_identifier_and_url():
    with pytest.raises(ValueError):
        LicenseObject(
            name="MIT",
            identifier="MIT",
            url="https://example.com",
        )


def test_license_object_raises_error_if_set_with_neither_identifier_nor_url():
    with pytest.raises(ValueError):
        LicenseObject(name="MIT")


def test_license_object_raises_error_if_set_with_incorrect_url():
    with pytest.raises(ValueError):
        LicenseObject(
            name="MIT",
            url="zsdfssdf",
        )
