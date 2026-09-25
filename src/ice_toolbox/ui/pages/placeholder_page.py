"""Generic "under development" page for modules without business logic yet."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ice_toolbox.ui import icons
from ice_toolbox.ui.tokens import Colors, FontSize, Radius, font_sans, rgba, sp


class PlaceholderPage(QWidget):
    def __init__(self, title: str, icon_name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._icon_name = icon_name

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(sp(4))

        self._icon_box = QLabel(self)
        self._icon_box.setFixedSize(sp(14), sp(14))
        self._icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._title_label = QLabel(title, self)
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont(font_sans())
        title_font.setPixelSize(FontSize.BASE)
        title_font.setBold(True)
        self._title_label.setFont(title_font)

        self._subtitle_label = QLabel("This module is under development.", self)
        self._subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont(font_sans())
        subtitle_font.setPixelSize(FontSize.SM)
        self._subtitle_label.setFont(subtitle_font)

        self._badge = QLabel("Coming soon", self)
        self._badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_font = QFont(font_sans())
        badge_font.setPixelSize(FontSize.XS)
        badge_font.setWeight(QFont.Weight.Medium)
        self._badge.setFont(badge_font)
        self._badge.setContentsMargins(sp(3), sp(1.5), sp(3), sp(1.5))

        layout.addWidget(self._icon_box, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._title_label)
        layout.addWidget(self._subtitle_label)
        layout.addWidget(self._badge, 0, Qt.AlignmentFlag.AlignCenter)

        self.set_theme("light")

    def set_theme(self, theme: str) -> None:
        if theme == "dark":
            icon_bg = rgba(Colors.BADGE_SURFACE_DARK, 60)
            icon_color = Colors.ICE_400
            title_color = Colors.NAVY_100
            subtitle_color = Colors.SLATE_600
            badge_color = Colors.SLATE_500
            badge_bg = Colors.HOVER_SURFACE_DARK
        else:
            icon_bg = Colors.ICE_50
            icon_color = Colors.ICE_500
            title_color = Colors.NAVY_800
            subtitle_color = Colors.SLATE_500
            badge_color = Colors.SLATE_500
            badge_bg = Colors.SLATE_100

        self._icon_box.setStyleSheet(
            f"background-color: {icon_bg}; border-radius: {Radius.XL}px;"
        )
        self._icon_box.setPixmap(icons.icon_pixmap(self._icon_name, 26, icon_color))
        self._title_label.setStyleSheet(f"color: {title_color};")
        self._subtitle_label.setStyleSheet(f"color: {subtitle_color};")
        self._badge.setStyleSheet(
            f"color: {badge_color}; background-color: {badge_bg}; border-radius: {Radius.SM}px;"
        )
