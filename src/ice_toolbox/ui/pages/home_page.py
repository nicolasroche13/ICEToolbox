"""Home page: welcome card, quick access grid, system status list."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ice_toolbox.ui import icons
from ice_toolbox.ui.tokens import Colors, FontSize, Radius, font_mono, font_sans, rgba, sp
from ice_toolbox.ui.widgets.quick_card import QuickCard

_ICONS_DIR = Path(__file__).resolve().parent.parent.parent / "resources" / "icons"

_STATUS_ROWS = [
    ("●", "neutral", "Connection", "Local mode — no tenant connected"),
    ("✓", "success", "Application", "Running — v0.1.0"),
    ("—", "neutral", "Microsoft Graph", "Not configured"),
    ("—", "neutral", "Microsoft Intune", "Not configured"),
]

_STATUS_COLORS = {
    "success": Colors.STATUS_SUCCESS,
    "warning": Colors.STATUS_WARNING,
    "error": Colors.STATUS_ERROR,
    "neutral": None,  # theme-dependent, resolved in _StatusRow.set_theme
}


class HomePage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumWidth(sp(225))  # max-w-[900px]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(sp(8))

        self._welcome_section, self._about_card = self._build_welcome_section()
        self._quick_section, self._quick_heading, self._quick_divider = self._build_quick_section()
        self._status_section, self._status_heading, self._status_divider, self._status_card = self._build_status_section()

        layout.addWidget(self._welcome_section)
        layout.addWidget(self._quick_section)
        layout.addWidget(self._status_section)
        layout.addStretch(1)

        self.set_theme("light")

    # ------------------------------------------------------------- welcome

    def _build_welcome_section(self) -> tuple[QWidget, QFrame]:
        section = QWidget(self)
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(0)

        title_row = QHBoxLayout()
        title_row.setSpacing(sp(3))
        logo = QSvgWidget(str(_ICONS_DIR / "ice_logo.svg"), section)
        logo.setFixedSize(22, 22)
        self._title_label = QLabel("ICE Toolbox", section)
        title_font = QFont(font_sans())
        title_font.setPixelSize(FontSize.XXL)
        title_font.setBold(True)
        self._title_label.setFont(title_font)
        title_row.addWidget(logo)
        title_row.addWidget(self._title_label)
        title_row.addStretch(1)
        title_row.setContentsMargins(0, 0, 0, sp(1))
        section_layout.addLayout(title_row)

        self._subtitle_label = QLabel("Endpoint & Cloud Engineering Toolkit", section)
        subtitle_font = QFont(font_sans())
        subtitle_font.setPixelSize(FontSize.SM)
        subtitle_font.setWeight(QFont.Weight.Medium)
        self._subtitle_label.setFont(subtitle_font)
        self._subtitle_label.setContentsMargins(sp(8.5), 0, 0, sp(5))
        section_layout.addWidget(self._subtitle_label)

        card = QFrame(section)
        card.setObjectName("aboutCard")
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(sp(5), sp(5), sp(5), sp(5))
        card_layout.setSpacing(sp(4))

        self._about_icon_box = QLabel(card)
        self._about_icon_box.setFixedSize(sp(8), sp(8))
        self._about_icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._about_icon_box.setPixmap(icons.icon_pixmap("about", 16, Colors.ICE_500))
        card_layout.addWidget(self._about_icon_box, 0, Qt.AlignmentFlag.AlignTop)

        text_box = QVBoxLayout()
        text_box.setSpacing(0)

        self._about_title = QLabel("About ICE Toolbox", card)
        about_title_font = QFont(font_sans())
        about_title_font.setPixelSize(FontSize.SM)
        about_title_font.setBold(True)
        self._about_title.setFont(about_title_font)
        self._about_title.setContentsMargins(0, 0, 0, sp(1))
        text_box.addWidget(self._about_title)

        self._about_body = QLabel(
            "Centralized tools for Endpoint & Cloud administration. ICE Toolbox "
            "consolidates Microsoft Intune, Entra ID, Graph API, and Windows endpoint "
            "management utilities into a single, purpose-built engineering interface.",
            card,
        )
        self._about_body.setWordWrap(True)
        body_font = QFont(font_sans())
        body_font.setPixelSize(FontSize.SM)
        self._about_body.setFont(body_font)
        text_box.addWidget(self._about_body)

        badge_row = QHBoxLayout()
        badge_row.setContentsMargins(0, sp(3), 0, 0)
        self._release_badge = QLabel("✓  v0.1.0 — Foundation release", card)
        badge_font = QFont(font_sans())
        badge_font.setPixelSize(FontSize.XS)
        badge_font.setWeight(QFont.Weight.Medium)
        self._release_badge.setFont(badge_font)
        self._release_badge.setContentsMargins(sp(2), sp(1), sp(2), sp(1))
        badge_row.addWidget(self._release_badge)
        badge_row.addStretch(1)
        text_box.addLayout(badge_row)

        card_layout.addLayout(text_box)
        section_layout.addWidget(card)

        return section, card

    # --------------------------------------------------------------- quick

    def _build_quick_section(self) -> tuple[QWidget, QLabel, QFrame]:
        section = QWidget(self)
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(0)

        header, heading, divider = _section_header("Quick Access")
        section_layout.addLayout(header)

        grid = QHBoxLayout()
        grid.setContentsMargins(0, sp(3), 0, 0)
        grid.setSpacing(sp(3))
        grid.addWidget(
            QuickCard("endpoint", "Endpoint", "Windows device management, diagnostics, and Intune operations.", coming_soon=True)
        )
        grid.addWidget(
            QuickCard("cloud", "Cloud", "Microsoft Entra ID, Azure, and Microsoft Graph administration.", coming_soon=True)
        )
        grid.addWidget(
            QuickCard("tools", "Tools", "Utilities, scripts, and cross-platform administration helpers.", coming_soon=True)
        )
        self._quick_cards = [grid.itemAt(i).widget() for i in range(grid.count())]
        section_layout.addLayout(grid)

        return section, heading, divider

    # -------------------------------------------------------------- status

    def _build_status_section(self) -> tuple[QWidget, QLabel, QFrame, QFrame]:
        section = QWidget(self)
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(0)

        header, heading, divider = _section_header("System Status")
        section_layout.addLayout(header)

        card = QFrame(section)
        card.setObjectName("statusCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        card_layout.setContentsMargins(0, sp(3), 0, 0)

        rows_container = QFrame(card)
        rows_layout = QVBoxLayout(rows_container)
        rows_layout.setContentsMargins(0, 0, 0, 0)
        rows_layout.setSpacing(0)

        self._status_rows: list[_StatusRow] = []
        for icon_char, variant, label, value in _STATUS_ROWS:
            row = _StatusRow(icon_char, variant, label, value, rows_container)
            rows_layout.addWidget(row)
            self._status_rows.append(row)

        card_layout.addWidget(rows_container)
        section_layout.addWidget(card)

        return section, heading, divider, card

    # --------------------------------------------------------------- theme

    def set_theme(self, theme: str) -> None:
        if theme == "dark":
            title_color = Colors.NAVY_100
            subtitle_color = Colors.ICE_400
            card_bg = Colors.SURFACE_CARD_DARK
            card_border = Colors.BORDER_DARK
            about_icon_bg = rgba(Colors.BADGE_SURFACE_DARK, 60)
            about_title_color = Colors.NAVY_100
            about_body_color = Colors.SLATE_500
            badge_bg = rgba(Colors.STATUS_SUCCESS, 15)
            badge_color = Colors.SUCCESS_TEXT_DARK
            heading_color = Colors.SLATE_600
            divider_color = Colors.BORDER_DARK
            row_divider_color = Colors.BORDER_DARK
            neutral_status_color = Colors.SLATE_600
        else:
            title_color = Colors.NAVY_900
            subtitle_color = Colors.ICE_500
            card_bg = Colors.WHITE
            card_border = Colors.SLATE_200
            about_icon_bg = Colors.ICE_50
            about_title_color = Colors.NAVY_800
            about_body_color = Colors.SLATE_500
            badge_bg = Colors.SUCCESS_BG_LIGHT
            badge_color = Colors.STATUS_SUCCESS
            heading_color = Colors.SLATE_400
            divider_color = Colors.SLATE_200
            row_divider_color = Colors.SLATE_100
            neutral_status_color = Colors.SLATE_400

        self._title_label.setStyleSheet(f"color: {title_color};")
        self._subtitle_label.setStyleSheet(f"color: {subtitle_color};")
        self._about_card.setStyleSheet(
            f"QFrame#aboutCard {{ background-color: {card_bg}; border: 1px solid {card_border}; "
            f"border-radius: {Radius.LG}px; }}"
        )
        self._about_icon_box.setStyleSheet(
            f"background-color: {about_icon_bg}; border-radius: {Radius.SM}px;"
        )
        self._about_title.setStyleSheet(f"color: {about_title_color};")
        self._about_body.setStyleSheet(f"color: {about_body_color};")
        self._release_badge.setStyleSheet(
            f"color: {badge_color}; background-color: {badge_bg}; border-radius: {Radius.SM}px;"
        )

        for heading in (self._quick_heading, self._status_heading):
            heading.setStyleSheet(f"color: {heading_color};")
        for divider in (self._quick_divider, self._status_divider):
            divider.setStyleSheet(f"background-color: {divider_color};")

        self._status_card.setStyleSheet(
            f"QFrame#statusCard {{ background-color: {card_bg}; border: 1px solid {card_border}; "
            f"border-radius: {Radius.LG}px; }}"
        )
        for i, row in enumerate(self._status_rows):
            row.set_theme(theme, neutral_status_color, row_divider_color, show_top_border=i > 0)

        for card_widget in self._quick_cards:
            card_widget.set_theme(theme)


def _section_header(title: str) -> tuple[QHBoxLayout, QLabel, QFrame]:
    row = QHBoxLayout()
    row.setContentsMargins(0, 0, 0, sp(3))
    row.setSpacing(sp(4))

    heading = QLabel(title)
    font = QFont(font_sans())
    font.setPixelSize(FontSize.XS)
    font.setWeight(QFont.Weight.DemiBold)
    font.setCapitalization(QFont.Capitalization.AllUppercase)
    font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 115)
    heading.setFont(font)

    divider = QFrame()
    divider.setFixedHeight(1)

    row.addWidget(heading)
    row.addWidget(divider, 1)
    return row, heading, divider


class _StatusRow(QFrame):
    def __init__(self, icon_char: str, variant: str, label: str, value: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._variant = variant
        self.setObjectName("statusRow")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(sp(5), sp(3), sp(5), sp(3))
        layout.setSpacing(sp(4))

        self._icon_label = QLabel(icon_char, self)
        icon_font = QFont(font_mono())
        icon_font.setPixelSize(FontSize.XS)
        self._icon_label.setFont(icon_font)
        self._icon_label.setFixedWidth(sp(3))

        self._label_label = QLabel(label, self)
        label_font = QFont(font_sans())
        label_font.setPixelSize(FontSize.XS)
        label_font.setWeight(QFont.Weight.Medium)
        self._label_label.setFont(label_font)
        self._label_label.setFixedWidth(sp(36))

        self._value_label = QLabel(value, self)
        value_font = QFont(font_mono())
        value_font.setPixelSize(FontSize.XS)
        self._value_label.setFont(value_font)

        layout.addWidget(self._icon_label)
        layout.addWidget(self._label_label)
        layout.addWidget(self._value_label)
        layout.addStretch(1)

    def set_theme(self, theme: str, neutral_color: str, divider_color: str, *, show_top_border: bool) -> None:
        variant_color = _STATUS_COLORS[self._variant] or neutral_color
        self._icon_label.setStyleSheet(f"color: {variant_color};")

        label_color = Colors.SLATE_700 if theme == "light" else Colors.NAVY_300
        value_color = Colors.SLATE_500 if theme == "light" else Colors.MUTED_TEXT
        self._label_label.setStyleSheet(f"color: {label_color};")
        self._value_label.setStyleSheet(f"color: {value_color};")

        border = f"border-top: 1px solid {divider_color};" if show_top_border else ""
        self.setStyleSheet(f"QFrame#statusRow {{ {border} }}")
