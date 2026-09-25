"""Main application window: sidebar + top bar + page content, per the Figma shell."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ice_toolbox.core.config import APP_NAME
from ice_toolbox.ui.pages.about_page import AboutPage
from ice_toolbox.ui.pages.home_page import HomePage
from ice_toolbox.ui.pages.placeholder_page import PlaceholderPage
from ice_toolbox.ui.tokens import Colors, font_sans, load_bundled_fonts, sp
from ice_toolbox.ui.widgets.sidebar import Sidebar
from ice_toolbox.ui.widgets.top_bar import TopBar

PAGE_TITLES = {
    "home": "Home",
    "endpoint": "Endpoint",
    "cloud": "Cloud",
    "tools": "Tools",
    "settings": "Settings",
    "about": "About",
}


class MainWindow(QMainWindow):
    """Main window reproducing the Figma ICE Toolbox shell (sidebar, top bar, pages)."""

    def __init__(self) -> None:
        super().__init__()
        load_bundled_fonts()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1366, 768)
        self.resize(1920, 1080)

        self._theme = "light"
        self._collapsed = False
        self._active_id = "home"

        self._root = QWidget(self)
        self._root.setObjectName("appRoot")
        root_layout = QHBoxLayout(self._root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self._sidebar = Sidebar(self._root)
        self._sidebar.navigate.connect(self._on_navigate)
        root_layout.addWidget(self._sidebar)

        right_column = QWidget(self._root)
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self._top_bar = TopBar(right_column)
        self._top_bar.sidebar_toggled.connect(self._toggle_sidebar)
        self._top_bar.theme_toggled.connect(self._toggle_theme)
        right_layout.addWidget(self._top_bar)

        self._scroll_area = QScrollArea(right_column)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self._content_host = QWidget()
        content_host = self._content_host
        content_layout = QVBoxLayout(content_host)
        content_layout.setContentsMargins(sp(8), sp(8), sp(8), sp(8))

        self._stack = QStackedWidget(content_host)
        self._stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout.addWidget(self._stack)

        self._scroll_area.setWidget(content_host)
        right_layout.addWidget(self._scroll_area, 1)

        root_layout.addWidget(right_column, 1)
        self.setCentralWidget(self._root)

        self._pages: dict[str, QWidget] = {}
        self._build_pages()
        self._stack.setCurrentWidget(self._pages[self._active_id])
        self._sidebar.set_active(self._active_id)

        self.set_theme("light")

    def _build_pages(self) -> None:
        pages: dict[str, QWidget] = {
            "home": HomePage(),
            "endpoint": PlaceholderPage("Endpoint Management", "endpoint"),
            "cloud": PlaceholderPage("Cloud Administration", "cloud"),
            "tools": PlaceholderPage("Tools & Utilities", "tools"),
            "settings": PlaceholderPage("Settings", "settings"),
            "about": AboutPage(),
        }
        for page_id, page in pages.items():
            self._pages[page_id] = page
            self._stack.addWidget(page)

    def _on_navigate(self, item_id: str) -> None:
        self._active_id = item_id
        self._sidebar.set_active(item_id)
        self._stack.setCurrentWidget(self._pages[item_id])
        self._top_bar.set_page_title(PAGE_TITLES.get(item_id, APP_NAME))

    def _toggle_sidebar(self) -> None:
        self._collapsed = not self._collapsed
        self._sidebar.set_collapsed(self._collapsed)

    def _toggle_theme(self) -> None:
        self.set_theme("dark" if self._theme == "light" else "light")

    def set_theme(self, theme: str) -> None:
        self._theme = theme
        bg = Colors.APP_BG_LIGHT if theme == "light" else Colors.APP_BG_DARK
        text = Colors.NAVY_800 if theme == "light" else Colors.NAVY_100

        self._root.setStyleSheet(
            f"QWidget#appRoot {{ background-color: {bg}; color: {text}; "
            f"font-family: '{font_sans()}'; font-size: 14px; }}"
        )
        self._scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self._content_host.setStyleSheet(f"background-color: {bg};")

        self._sidebar.set_theme(theme)
        self._top_bar.set_theme(theme)
        for page in self._pages.values():
            page.set_theme(theme)
