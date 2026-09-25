"""About page: app identity, info table, and description."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ice_toolbox.ui.tokens import Colors, FontSize, Radius, font_mono, font_sans, sp

_ICONS_DIR = Path(__file__).resolve().parent.parent.parent / "resources" / "icons"

_INFO_ROWS = [
    ("Platform", "Windows / PySide6"),
    ("Runtime", "Python 3.12+"),
    ("Release", "v0.1.0 — Foundation"),
    ("Target", "Endpoint & Cloud Engineers"),
    ("Build", "Development"),
]


class AboutPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumWidth(sp(170))  # max-w-[680px]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(sp(6))

        header = QHBoxLayout()
        header.setSpacing(sp(4))
        logo = QSvgWidget(str(_ICONS_DIR / "ice_logo.svg"), self)
        logo.setFixedSize(40, 40)

        text_box = QVBoxLayout()
        text_box.setSpacing(0)
        self._title_label = QLabel("ICE Toolbox", self)
        title_font = QFont(font_sans())
        title_font.setPixelSize(FontSize.XL)
        title_font.setBold(True)
        self._title_label.setFont(title_font)

        self._subtitle_label = QLabel("Endpoint & Cloud Engineering Toolkit — v0.1.0", self)
        self._subtitle_label.setContentsMargins(0, sp(0.5), 0, 0)
        subtitle_font = QFont(font_mono())
        subtitle_font.setPixelSize(FontSize.XS)
        self._subtitle_label.setFont(subtitle_font)

        text_box.addWidget(self._title_label)
        text_box.addWidget(self._subtitle_label)
        header.addWidget(logo)
        header.addLayout(text_box)
        header.addStretch(1)
        layout.addLayout(header)

        self._card = QFrame(self)
        self._card.setObjectName("aboutInfoCard")
        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        self._rows: list[_InfoRow] = []
        for i, (key, value) in enumerate(_INFO_ROWS):
            row = _InfoRow(key, value, self._card)
            row.set_top_border(i > 0)
            card_layout.addWidget(row)
            self._rows.append(row)

        layout.addWidget(self._card)

        self._footer_label = QLabel(
            "ICE Toolbox is an internal IT administration application for Endpoint & "
            "Cloud engineers. It centralizes Microsoft Intune, Entra ID, Graph API, and "
            "Windows endpoint utilities into a single, purpose-built tool.",
            self,
        )
        self._footer_label.setWordWrap(True)
        footer_font = QFont(font_sans())
        footer_font.setPixelSize(FontSize.XS)
        self._footer_label.setFont(footer_font)
        layout.addWidget(self._footer_label)

        layout.addStretch(1)

        self.set_theme("light")

    def set_theme(self, theme: str) -> None:
        if theme == "dark":
            title_color = Colors.NAVY_100
            subtitle_color = Colors.SLATE_600
            card_bg = Colors.SURFACE_CARD_DARK
            card_border = Colors.BORDER_DARK
            row_divider = Colors.BORDER_DARK
            key_color = Colors.NAVY_300
            value_color = Colors.MUTED_TEXT
            footer_color = Colors.SLATE_600
        else:
            title_color = Colors.NAVY_900
            subtitle_color = Colors.SLATE_500
            card_bg = Colors.WHITE
            card_border = Colors.SLATE_200
            row_divider = Colors.SLATE_100
            key_color = Colors.SLATE_700
            value_color = Colors.SLATE_500
            footer_color = Colors.SLATE_400

        self._title_label.setStyleSheet(f"color: {title_color};")
        self._subtitle_label.setStyleSheet(f"color: {subtitle_color};")
        self._card.setStyleSheet(
            f"QFrame#aboutInfoCard {{ background-color: {card_bg}; border: 1px solid {card_border}; "
            f"border-radius: {Radius.LG}px; }}"
        )
        self._footer_label.setStyleSheet(f"color: {footer_color};")
        for row in self._rows:
            row.set_theme(key_color, value_color, row_divider)


class _InfoRow(QFrame):
    def __init__(self, key: str, value: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("infoRow")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(sp(5), sp(3), sp(5), sp(3))
        layout.setSpacing(sp(4))

        self._key_label = QLabel(key, self)
        key_font = QFont(font_sans())
        key_font.setPixelSize(FontSize.XS)
        key_font.setWeight(QFont.Weight.Medium)
        self._key_label.setFont(key_font)
        self._key_label.setFixedWidth(sp(28))

        self._value_label = QLabel(value, self)
        value_font = QFont(font_mono())
        value_font.setPixelSize(FontSize.XS)
        self._value_label.setFont(value_font)

        layout.addWidget(self._key_label)
        layout.addWidget(self._value_label)
        layout.addStretch(1)

        self._show_top_border = False

    def set_top_border(self, show: bool) -> None:
        self._show_top_border = show

    def set_theme(self, key_color: str, value_color: str, divider_color: str) -> None:
        self._key_label.setStyleSheet(f"color: {key_color};")
        self._value_label.setStyleSheet(f"color: {value_color};")
        border = f"border-top: 1px solid {divider_color};" if self._show_top_border else ""
        self.setStyleSheet(f"QFrame#infoRow {{ {border} }}")
