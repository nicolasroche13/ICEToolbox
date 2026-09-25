"""Loads the SVG icons exported from the Figma design and recolors them on demand.

The SVG files in ``resources/icons`` are stored verbatim (same ``stroke="currentColor"``
attribute as the Figma/React source). Qt's SVG renderer does not resolve CSS
``currentColor``, so this module substitutes the token for the requested color
before rendering, which reproduces the source's per-state icon coloring.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

_ICONS_DIR = Path(__file__).resolve().parent.parent / "resources" / "icons"


@lru_cache(maxsize=None)
def _read_svg(name: str) -> str:
    return (_ICONS_DIR / f"{name}.svg").read_text(encoding="utf-8")


@lru_cache(maxsize=256)
def _render_pixmap(name: str, size: int, color: str, dpr: float) -> QPixmap:
    svg_text = _read_svg(name).replace("currentColor", color)
    renderer = QSvgRenderer(QByteArray(svg_text.encode("utf-8")))

    device_size = max(1, round(size * dpr))
    pixmap = QPixmap(QSize(device_size, device_size))
    pixmap.fill(Qt.GlobalColor.transparent)
    pixmap.setDevicePixelRatio(dpr)

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def icon_pixmap(name: str, size: int, color: str = "currentColor", dpr: float = 2.0) -> QPixmap:
    """Render an icon (by file stem, e.g. ``"home"``) at the given size and color."""
    return _render_pixmap(name, size, color, dpr)


def icon(name: str, size: int, color: str = "currentColor", dpr: float = 2.0) -> QIcon:
    """Return a QIcon for the named icon, recolored to ``color``."""
    return QIcon(icon_pixmap(name, size, color, dpr))
