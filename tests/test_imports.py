"""Smoke tests verifying the package is importable."""

import ice_toolbox


def test_package_is_importable() -> None:
    assert ice_toolbox is not None


def test_package_has_version() -> None:
    assert ice_toolbox.__version__ == "0.1.1"
