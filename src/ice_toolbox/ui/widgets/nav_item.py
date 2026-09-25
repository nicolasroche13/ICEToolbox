"""Sidebar navigation item button (icon + label + optional "Soon" tag)."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from ice_toolbox.ui import icons
from ice_toolbox.ui.tokens import Colors, FontSize, Radius, font_sans, rgba, sp

_ACTIVE_BG = rgba(Colors.ICE_500, 15)
_HOVER_BG = rgba(Colors.WHITE, 5)
_INACTIVE_COLOR = Colors.NAVY_300
_HOVER_COLOR = Colors.SLATE_300
_ACTIVE_COLOR = Colors.ICE_400
_SOON_COLOR = Colors.NAVY_400
_SOON_BG = rgba(Colors.BADGE_SURFACE_DARK, 40)


class NavItemButton(QWidget):
    """A single sidebar navigation entry, mirroring the Figma `NavItemButton`."""

    clicked = Signal()

    def __init__(
        self,
        icon_name: str,
        label: str,
        *,
        coming_soon: bool = False,
        collapsed: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._icon_name = icon_name
        self._label_text = label
        self._coming_soon = coming_soon
        self._collapsed = collapsed
        self._active = False
        self._hovered = False

        self.setObjectName("navItem")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setToolTip(label if collapsed else "")

        self._indicator = QFrame(self)
        self._indicator.setFixedWidth(2)

        self._icon_label = QLabel(self)
        self._icon_label.setFixedSize(18, 18)

        self._text_label = QLabel(self._label_text, self)
        text_font = QFont(font_sans())
        text_font.setPixelSize(FontSize.SM)
        text_font.setWeight(QFont.Weight.Medium)
        self._text_label.setFont(text_font)

        self._soon_label = QLabel("Soon", self)
        soon_font = QFont(font_sans())
        soon_font.setPixelSize(FontSize.XXS_10)
        soon_font.setWeight(QFont.Weight.DemiBold)
        soon_font.setCapitalization(QFont.Capitalization.AllUppercase)
        soon_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 105)
        self._soon_label.setFont(soon_font)
        self._soon_label.setStyleSheet(
            f"color: {_SOON_COLOR}; background-color: {_SOON_BG};"
            f"padding: {sp(0.5)}px {sp(1.5)}px; border-radius: {Radius.SM}px;"
        )
        self._soon_label.setVisible(self._coming_soon)

        layout = QHBoxLayout(self)
        layout.setSpacing(sp(3))
        layout.addWidget(self._indicator)
        layout.addWidget(self._icon_label)
        layout.addWidget(self._text_label)
        layout.addStretch(1)
        layout.addWidget(self._soon_label)

        self.set_collapsed(collapsed)
        self._refresh()

    def sizeHint(self):  # noqa: N802 - Qt override
        from PySide6.QtCore import QSize

        return QSize(-1, sp(2.5) * 2 + 18)

    def set_collapsed(self, collapsed: bool) -> None:
        self._collapsed = collapsed
        layout = self.layout()
        if collapsed:
            layout.setContentsMargins(sp(2), sp(2.5), sp(2), sp(2.5))
            self._indicator.setFixedWidth(0)
            self._text_label.setVisible(False)
            self._soon_label.setVisible(False)
        else:
            layout.setContentsMargins(sp(3), sp(2.5), sp(3), sp(2.5))
            self._indicator.setFixedWidth(2)
            self._text_label.setVisible(True)
            self._soon_label.setVisible(self._coming_soon)
        self.setToolTip(self._label_text if collapsed else "")
        self._refresh()

    def set_active(self, active: bool) -> None:
        self._active = active
        self._refresh()

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt override
        self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event) -> None:  # noqa: N802 - Qt override
        self._hovered = True
        self._refresh()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802 - Qt override
        self._hovered = False
        self._refresh()
        super().leaveEvent(event)

    def _refresh(self) -> None:
        if self._active:
            bg = _ACTIVE_BG
            color = _ACTIVE_COLOR
        elif self._hovered:
            bg = _HOVER_BG
            color = _HOVER_COLOR
        else:
            bg = "transparent"
            color = _INACTIVE_COLOR

        self.setStyleSheet(
            f"QWidget#navItem {{ background-color: {bg}; border-radius: {Radius.MD}px; }}"
        )
        self._text_label.setStyleSheet(f"color: {color}; background: transparent;")
        self._icon_label.setPixmap(icons.icon_pixmap(self._icon_name, 18, color))

        indicator_color = _ACTIVE_COLOR if (self._active and not self._collapsed) else "transparent"
        self._indicator.setStyleSheet(f"background-color: {indicator_color}; border-radius: 1px;")
