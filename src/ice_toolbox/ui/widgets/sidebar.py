"""Left navigation sidebar, mirroring the Figma `Sidebar` component."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ice_toolbox.ui.tokens import Colors, FontSize, font_mono, font_sans, rgba, sp
from ice_toolbox.ui.widgets.nav_item import NavItemButton

_WIDTH_EXPANDED = 232
_WIDTH_COLLAPSED = 58

# border-[#1E3A5F]/60 dark:border-[#0C1B31]
_BORDER_LIGHT = rgba(Colors.NAVY_700, 60)
_BORDER_DARK_THEME = Colors.NAVY_900


@dataclass(frozen=True)
class NavEntry:
    id: str
    label: str
    icon: str
    coming_soon: bool = False


NAV_MAIN = [NavEntry("home", "Home", "home")]
NAV_CATEGORIES = [
    NavEntry("endpoint", "Endpoint", "endpoint", coming_soon=True),
    NavEntry("cloud", "Cloud", "cloud", coming_soon=True),
    NavEntry("tools", "Tools", "tools", coming_soon=True),
]
NAV_BOTTOM = [
    NavEntry("settings", "Settings", "settings"),
    NavEntry("about", "About", "about"),
]


class Sidebar(QFrame):
    """Collapsible sidebar with logo, primary nav, categories, and bottom nav."""

    navigate = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._collapsed = False
        self._active_id = "home"
        self._nav_items: dict[str, NavItemButton] = {}

        self.setObjectName("sidebar")
        self.setFixedWidth(_WIDTH_EXPANDED)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_logo_area())
        root.addWidget(self._build_nav_area(), 1)
        root.addWidget(self._build_bottom_area())

        self.set_theme("light")
        self.set_active("home")

    # ------------------------------------------------------------------ UI

    def _build_logo_area(self) -> QWidget:
        self._logo_area = QWidget(self)
        self._logo_area.setObjectName("logoArea")
        self._logo_layout = QHBoxLayout(self._logo_area)
        self._logo_layout.setSpacing(sp(3))
        self._logo_layout.setContentsMargins(sp(4), sp(4), sp(4), sp(4))

        self._logo_icon = QSvgWidget(str(_icon_path("ice_logo")), self._logo_area)
        self._logo_icon.setFixedSize(28, 28)

        self._logo_text_box = QWidget(self._logo_area)
        text_layout = QVBoxLayout(self._logo_text_box)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)

        self._logo_title = QLabel("ICE", self._logo_text_box)
        title_font = QFont(font_sans())
        title_font.setPixelSize(FontSize.SM)
        title_font.setBold(True)
        title_font.setCapitalization(QFont.Capitalization.AllUppercase)
        title_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 115)
        self._logo_title.setFont(title_font)
        self._logo_title.setStyleSheet(f"color: {Colors.WHITE};")

        self._logo_subtitle = QLabel("Toolbox", self._logo_text_box)
        sub_font = QFont(font_sans())
        sub_font.setPixelSize(FontSize.XXS_10)
        sub_font.setWeight(QFont.Weight.Medium)
        sub_font.setCapitalization(QFont.Capitalization.AllUppercase)
        sub_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 115)
        self._logo_subtitle.setFont(sub_font)
        self._logo_subtitle.setStyleSheet(f"color: {Colors.NAVY_400}; margin-top: 2px;")

        text_layout.addWidget(self._logo_title)
        text_layout.addWidget(self._logo_subtitle)

        self._logo_layout.addWidget(self._logo_icon)
        self._logo_layout.addWidget(self._logo_text_box)
        self._logo_layout.addStretch(1)

        return self._logo_area

    def _build_nav_area(self) -> QWidget:
        nav_widget = QWidget(self)
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(sp(2), sp(3), sp(2), sp(3))
        nav_layout.setSpacing(sp(0.5))

        for entry in NAV_MAIN:
            nav_layout.addWidget(self._make_item(entry))

        self._categories_label = QLabel("Categories", nav_widget)
        cat_font = QFont(font_sans())
        cat_font.setPixelSize(FontSize.XXS_10)
        cat_font.setWeight(QFont.Weight.DemiBold)
        cat_font.setCapitalization(QFont.Capitalization.AllUppercase)
        cat_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 115)
        self._categories_label.setFont(cat_font)
        self._categories_label.setStyleSheet(
            f"color: {Colors.NAVY_600}; margin-left: {sp(1)}px;"
        )
        self._categories_label.setContentsMargins(0, sp(3), 0, sp(1))

        self._categories_separator = QFrame(nav_widget)
        self._categories_separator.setFixedHeight(1)
        self._categories_separator.setContentsMargins(sp(4), sp(2), sp(4), sp(2))
        self._categories_separator.setVisible(False)

        nav_layout.addWidget(self._categories_label)
        nav_layout.addWidget(self._categories_separator)

        for entry in NAV_CATEGORIES:
            nav_layout.addWidget(self._make_item(entry))

        nav_layout.addStretch(1)
        return nav_widget

    def _build_bottom_area(self) -> QWidget:
        self._bottom_area = QWidget(self)
        self._bottom_area.setObjectName("bottomArea")
        bottom_layout = QVBoxLayout(self._bottom_area)
        bottom_layout.setContentsMargins(sp(2), sp(2), sp(2), sp(2))
        bottom_layout.setSpacing(sp(0.5))

        for entry in NAV_BOTTOM:
            bottom_layout.addWidget(self._make_item(entry))

        self._version_label = QLabel("v0.1.0", self._bottom_area)
        version_font = QFont(font_mono())
        version_font.setPixelSize(FontSize.XXS_10)
        self._version_label.setFont(version_font)
        self._version_label.setStyleSheet(f"color: {Colors.NAVY_600};")
        self._version_label.setContentsMargins(sp(3), sp(2), 0, sp(1))
        self._version_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        bottom_layout.addWidget(self._version_label)
        return self._bottom_area

    def _make_item(self, entry: NavEntry) -> NavItemButton:
        item = NavItemButton(entry.icon, entry.label, coming_soon=entry.coming_soon, collapsed=self._collapsed)
        item.clicked.connect(lambda entry_id=entry.id: self.navigate.emit(entry_id))
        self._nav_items[entry.id] = item
        return item

    # --------------------------------------------------------------- state

    def set_active(self, item_id: str) -> None:
        self._active_id = item_id
        for entry_id, item in self._nav_items.items():
            item.set_active(entry_id == item_id)

    def set_collapsed(self, collapsed: bool) -> None:
        self._collapsed = collapsed
        self.setFixedWidth(_WIDTH_COLLAPSED if collapsed else _WIDTH_EXPANDED)

        self._logo_icon.setFixedSize(26, 26) if collapsed else self._logo_icon.setFixedSize(28, 28)
        self._logo_text_box.setVisible(not collapsed)
        self._logo_layout.setContentsMargins(sp(3), sp(4), sp(3), sp(4)) if collapsed else self._logo_layout.setContentsMargins(sp(4), sp(4), sp(4), sp(4))

        self._categories_label.setVisible(not collapsed)
        self._categories_separator.setVisible(collapsed)

        for item in self._nav_items.values():
            item.set_collapsed(collapsed)

        self._version_label.setText("0.1" if collapsed else "v0.1.0")
        self._version_label.setFont(_font_for_version(collapsed))
        if collapsed:
            self._version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._version_label.setContentsMargins(0, sp(1), 0, sp(1))
        else:
            self._version_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self._version_label.setContentsMargins(sp(3), sp(2), 0, sp(1))

    def set_theme(self, theme: str) -> None:
        if theme == "dark":
            bg = Colors.NAVY_950
            border = _BORDER_DARK_THEME
        else:
            bg = Colors.NAVY_900
            border = _BORDER_LIGHT

        self.setStyleSheet(
            f"QFrame#sidebar {{ background-color: {bg}; border: none; border-right: 1px solid {border}; }}"
        )
        self._logo_area.setStyleSheet(f"QWidget#logoArea {{ border-bottom: 1px solid {border}; }}")
        self._bottom_area.setStyleSheet(f"QWidget#bottomArea {{ border-top: 1px solid {border}; }}")

        separator_alpha = 6 if theme == "dark" else 8
        self._categories_separator.setStyleSheet(
            f"background-color: {rgba(Colors.WHITE, separator_alpha)};"
        )


def _font_for_version(collapsed: bool) -> QFont:
    font = QFont(font_mono())
    font.setPixelSize(FontSize.XXS_9 if collapsed else FontSize.XXS_10)
    return font


def _icon_path(name: str):
    from pathlib import Path

    return Path(__file__).resolve().parent.parent.parent / "resources" / "icons" / f"{name}.svg"
