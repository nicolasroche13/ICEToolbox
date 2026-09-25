"""Top bar: sidebar toggle, breadcrumb, status badge, theme toggle."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget

from ice_toolbox.ui import icons
from ice_toolbox.ui.tokens import Colors, FontSize, font_mono, font_sans, rgba, sp

_HEIGHT = sp(12)  # h-12 = 48px


class StatusBadge(QFrame):
    """"Local mode" pill, mirroring the Figma `StatusBadge` component."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("statusBadge")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(sp(3), sp(1.5), sp(3), sp(1.5))
        layout.setSpacing(sp(2))

        self._dot = QLabel(self)
        self._dot.setFixedSize(6, 6)
        self._dot.setStyleSheet(f"background-color: {Colors.STATUS_SUCCESS}; border-radius: 3px;")

        self._text = QLabel("Local mode", self)
        font = QFont(font_mono())
        font.setPixelSize(FontSize.XS)
        font.setWeight(QFont.Weight.Medium)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 105)
        self._text.setFont(font)

        layout.addWidget(self._dot)
        layout.addWidget(self._text)
        self.set_theme("light")

    def set_theme(self, theme: str) -> None:
        if theme == "dark":
            bg = rgba(Colors.BADGE_SURFACE_DARK, 60)
            border = rgba(Colors.ICE_500, 30)
            text_color = Colors.ICE_400
        else:
            bg = Colors.ICE_50
            border = rgba(Colors.ICE_200, 60)
            text_color = Colors.ICE_500

        self.setStyleSheet(
            f"QFrame#statusBadge {{ background-color: {bg}; border: 1px solid {border}; border-radius: {sp(1)}px; }}"
        )
        self._text.setStyleSheet(f"color: {text_color}; background: transparent;")


class TopBar(QFrame):
    """Header bar above the page content, mirroring the Figma `TopBar` component."""

    sidebar_toggled = Signal()
    theme_toggled = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("topBar")
        self.setFixedHeight(_HEIGHT)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(sp(5), 0, sp(5), 0)
        layout.setSpacing(0)

        left = QHBoxLayout()
        left.setSpacing(sp(3))

        self._menu_button = _IconButton("menu", 18)
        self._menu_button.clicked.connect(self.sidebar_toggled.emit)
        left.addWidget(self._menu_button)

        crumb = QHBoxLayout()
        crumb.setSpacing(sp(2))
        self._crumb_root = QLabel("ICE Toolbox")
        root_font = QFont(font_sans())
        root_font.setPixelSize(FontSize.XS)
        self._crumb_root.setFont(root_font)

        self._crumb_chevron = QLabel(self)
        self._crumb_chevron.setFixedSize(12, 12)
        self._crumb_chevron.setPixmap(icons.icon_pixmap("chevron_right", 12, Colors.SLATE_300))

        self._crumb_page = QLabel("Home")
        page_font = QFont(font_sans())
        page_font.setPixelSize(FontSize.SM)
        page_font.setBold(True)
        self._crumb_page.setFont(page_font)

        crumb.addWidget(self._crumb_root)
        crumb.addWidget(self._crumb_chevron)
        crumb.addWidget(self._crumb_page)

        left.addLayout(crumb)
        layout.addLayout(left)
        layout.addStretch(1)

        right = QHBoxLayout()
        right.setSpacing(sp(2))

        self._status_badge = StatusBadge(self)
        right.addWidget(self._status_badge)

        self._divider = QFrame(self)
        self._divider.setFixedSize(1, sp(5))
        right.addWidget(self._divider)

        self._theme_button = _IconButton("moon", 16)
        self._theme_button.clicked.connect(self.theme_toggled.emit)
        right.addWidget(self._theme_button)

        layout.addLayout(right)

        self.set_theme("light")

    def set_page_title(self, title: str) -> None:
        self._crumb_page.setText(title)

    def set_theme(self, theme: str) -> None:
        if theme == "dark":
            bg = Colors.SURFACE_CARD_DARK
            border = Colors.BORDER_DARK
            root_color = Colors.MUTED_TEXT
            page_color = Colors.SLATE_100
            chevron_color = Colors.SLATE_700
            menu_icon_color = Colors.NAVY_300
            toggle_icon_color = Colors.NAVY_300
            divider_color = Colors.BORDER_DARK
        else:
            bg = Colors.WHITE
            border = Colors.SLATE_200
            root_color = Colors.SLATE_400
            page_color = Colors.NAVY_800
            chevron_color = Colors.SLATE_300
            menu_icon_color = Colors.MUTED_TEXT
            toggle_icon_color = Colors.SLATE_500
            divider_color = Colors.SLATE_200

        self.setStyleSheet(
            f"QFrame#topBar {{ background-color: {bg}; border: none; border-bottom: 1px solid {border}; }}"
        )
        self._crumb_root.setStyleSheet(f"color: {root_color};")
        self._crumb_page.setStyleSheet(f"color: {page_color};")
        self._crumb_chevron.setPixmap(icons.icon_pixmap("chevron_right", 12, chevron_color))
        self._divider.setStyleSheet(f"background-color: {divider_color};")

        self._menu_button.set_theme(theme, menu_icon_color)
        theme_icon_name = "moon" if theme == "light" else "sun"
        self._theme_button.set_icon_name(theme_icon_name)
        self._theme_button.set_theme(theme, toggle_icon_color)
        self._status_badge.set_theme(theme)


class _IconButton(QPushButton):
    """Small ghost icon button used for the sidebar-toggle and theme-toggle actions."""

    def __init__(self, icon_name: str, size: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._icon_name = icon_name
        self._size = size
        self.setFixedSize(sp(1.5) * 2 + size, sp(1.5) * 2 + size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def set_icon_name(self, icon_name: str) -> None:
        self._icon_name = icon_name

    def set_theme(self, theme: str, color: str) -> None:
        hover_bg = Colors.SLATE_100 if theme == "light" else Colors.HOVER_SURFACE_DARK
        self.setStyleSheet(
            f"""
            QPushButton {{
                border: none;
                border-radius: {sp(1)}px;
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
            }}
            QPushButton:focus {{
                outline: 2px solid {Colors.ICE_500};
                outline-offset: 2px;
            }}
            """
        )
        self.setIcon(icons.icon(self._icon_name, self._size, color))
        self.setIconSize(QSize(self._size, self._size))
