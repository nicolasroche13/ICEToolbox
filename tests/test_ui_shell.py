"""Tests for the application shell UI (sidebar, top bar, pages)."""

from PySide6.QtWidgets import QApplication

from ice_toolbox.ui.main_window import MainWindow
from ice_toolbox.ui.pages.home_page import HomePage
from ice_toolbox.ui.widgets.sidebar import Sidebar


def _ensure_app() -> QApplication:
    return QApplication.instance() or QApplication([])


def test_main_window_can_be_created() -> None:
    _ensure_app()
    window = MainWindow()
    assert window is not None


def test_home_page_can_be_created() -> None:
    _ensure_app()
    page = HomePage()
    assert page is not None


def test_sidebar_can_be_created() -> None:
    _ensure_app()
    sidebar = Sidebar()
    assert sidebar is not None


def test_main_window_navigation_does_not_crash() -> None:
    _ensure_app()
    window = MainWindow()
    for page_id in ("home", "endpoint", "cloud", "tools", "settings", "about"):
        window._on_navigate(page_id)
    window._toggle_sidebar()
    window._toggle_theme()
