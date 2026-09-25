"""Home page "Quick Access" card, mirroring the Figma `QuickCard` component."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QGraphicsOpacityEffect, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ice_toolbox.ui import icons
from ice_toolbox.ui.tokens import Colors, FontSize, Radius, font_sans, rgba, sp


class QuickCard(QFrame):
    clicked = Signal()

    def __init__(
        self,
        icon_name: str,
        label: str,
        description: str,
        *,
        coming_soon: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._icon_name = icon_name
        self._coming_soon = coming_soon
        self._hovered = False
        self.setObjectName("quickCard")

        if not coming_soon:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(sp(5), sp(5), sp(5), sp(5))
        layout.setSpacing(sp(3))

        header = QHBoxLayout()
        self._icon_box = QLabel(self)
        self._icon_box.setFixedSize(sp(9), sp(9))
        self._icon_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(self._icon_box)
        header.addStretch(1)

        if coming_soon:
            self._badge = QLabel("Coming soon", self)
            badge_font = QFont(font_sans())
            badge_font.setPixelSize(FontSize.XXS_10)
            badge_font.setWeight(QFont.Weight.DemiBold)
            badge_font.setCapitalization(QFont.Capitalization.AllUppercase)
            badge_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 105)
            self._badge.setFont(badge_font)
            self._badge.setContentsMargins(0, 0, 0, 0)
            header.addWidget(self._badge)
        else:
            self._badge = None

        layout.addLayout(header)

        self._label = QLabel(label, self)
        label_font = QFont(font_sans())
        label_font.setPixelSize(FontSize.SM)
        label_font.setBold(True)
        self._label.setFont(label_font)

        self._description = QLabel(description, self)
        self._description.setWordWrap(True)
        desc_font = QFont(font_sans())
        desc_font.setPixelSize(FontSize.XS)
        self._description.setFont(desc_font)

        text_box = QVBoxLayout()
        text_box.setSpacing(sp(0.5))
        text_box.addWidget(self._label)
        text_box.addWidget(self._description)
        layout.addLayout(text_box)

        if coming_soon:
            opacity_effect = QGraphicsOpacityEffect(self)
            opacity_effect.setOpacity(0.6)
            self.setGraphicsEffect(opacity_effect)

        self.set_theme("light")

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt override
        if not self._coming_soon:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event) -> None:  # noqa: N802 - Qt override
        self._hovered = True
        self._apply_frame_style()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802 - Qt override
        self._hovered = False
        self._apply_frame_style()
        super().leaveEvent(event)

    def set_theme(self, theme: str) -> None:
        self._theme = theme
        if theme == "dark":
            self._card_bg = Colors.SURFACE_CARD_DARK
            self._border_default = Colors.BORDER_DARK
            icon_bg = rgba(Colors.BADGE_SURFACE_DARK, 60)
            icon_color = Colors.ICE_400
            label_color = Colors.NAVY_100
            desc_color = Colors.MUTED_TEXT
            badge_color = Colors.SLATE_600
            badge_bg = Colors.HOVER_SURFACE_DARK
        else:
            self._card_bg = Colors.WHITE
            self._border_default = Colors.SLATE_200
            icon_bg = Colors.ICE_50
            icon_color = Colors.ICE_500
            label_color = Colors.NAVY_800
            desc_color = Colors.SLATE_500
            badge_color = Colors.SLATE_500
            badge_bg = Colors.SLATE_100

        self._icon_box.setStyleSheet(
            f"background-color: {icon_bg}; border-radius: {Radius.MD}px;"
        )
        self._icon_box.setPixmap(icons.icon_pixmap(self._icon_name, 18, icon_color))
        self._label.setStyleSheet(f"color: {label_color};")
        self._description.setStyleSheet(f"color: {desc_color};")
        if self._badge is not None:
            self._badge.setStyleSheet(
                f"color: {badge_color}; background-color: {badge_bg};"
                f"padding: {sp(0.5)}px {sp(2)}px; border-radius: {Radius.SM}px;"
            )

        self._apply_frame_style()

    def _apply_frame_style(self) -> None:
        if not self._coming_soon and self._hovered:
            border = rgba(Colors.ICE_500, 40)
        else:
            border = self._border_default

        self.setStyleSheet(
            f"""
            QFrame#quickCard {{
                background-color: {self._card_bg};
                border: 1px solid {border};
                border-radius: {Radius.LG}px;
            }}
            """
        )
