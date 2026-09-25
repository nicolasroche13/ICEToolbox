"""Tests for application initialization."""

from ice_toolbox.app.application import Application
from ice_toolbox.core.config import get_version


def test_application_can_be_initialized() -> None:
    app = Application()
    assert app is not None


def test_version_is_0_1_0() -> None:
    assert get_version() == "0.1.0"
