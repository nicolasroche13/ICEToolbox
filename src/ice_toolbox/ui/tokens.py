"""Design tokens extracted from the ICE Toolbox Figma design (src/index.css).

Every value here is copied verbatim from the Figma Make source file so that
widgets never hardcode colors, spacing, radii, or font values inline.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QFontDatabase


class Colors:
    """Color scale from the Figma `@theme inline` block."""

    ICE_50 = "#EBF5FF"
    ICE_100 = "#DBEEFF"
    ICE_200 = "#BADDff"
    ICE_300 = "#7DC2F7"
    ICE_400 = "#3DA4EE"
    ICE_500 = "#0B82D8"
    ICE_600 = "#0869B5"
    ICE_700 = "#075292"
    ICE_800 = "#063E72"
    ICE_900 = "#0C2C52"

    NAVY_50 = "#F0F4FA"
    NAVY_100 = "#DDE4F0"
    NAVY_200 = "#BBC9E1"
    NAVY_300 = "#8EA8CC"
    NAVY_400 = "#5F84B0"
    NAVY_500 = "#3D6494"
    NAVY_600 = "#2C4E7A"
    NAVY_700 = "#1E3A5F"
    NAVY_800 = "#132847"
    NAVY_900 = "#0C1B31"
    NAVY_950 = "#070F1C"

    SLATE_50 = "#F6F8FA"
    SLATE_100 = "#EDF0F4"
    SLATE_200 = "#D8DDE5"
    SLATE_300 = "#B8C1CD"
    SLATE_400 = "#8E9BAB"
    SLATE_500 = "#68788A"
    SLATE_600 = "#4F5E6F"
    SLATE_700 = "#38475A"
    SLATE_800 = "#232E3D"
    SLATE_900 = "#141C28"

    STATUS_SUCCESS = "#16A34A"
    STATUS_WARNING = "#D97706"
    STATUS_ERROR = "#DC2626"
    STATUS_INFO = "#0B82D8"
    STATUS_NEUTRAL = "#68788A"

    # Colors used directly in the JSX that are not part of the numbered scale.
    APP_BG_LIGHT = "#F0F2F5"
    APP_BG_DARK = "#0A0F18"
    SUCCESS_BG_LIGHT = "#DCFCE7"
    SUCCESS_TEXT_DARK = "#4ADE80"
    WHITE = "#FFFFFF"

    # Dark-theme surface/text literals used directly in the JSX (not part of the
    # --color-ice/navy/slate scale) — kept as exact one-off hex values.
    SURFACE_CARD_DARK = "#0F1929"  # bg-white dark:bg-[#0F1929] (cards, top bar)
    BORDER_DARK = "#1E2D42"  # border-[#D8DDE5] dark:border-[#1E2D42] (cards, top bar, dividers)
    BADGE_SURFACE_DARK = "#0B2240"  # bg-[#0B2240] (status badge / icon-box dark bg)
    HOVER_SURFACE_DARK = "#1A2740"  # dark:hover:bg-[#1A2740] (icon buttons, badges)
    MUTED_TEXT = "#5A6A7E"  # text-[#5A6A7E] (breadcrumb root, card descriptions, status values)

    # ICE logo mark fixed colors (not theme-dependent in the source).
    LOGO_STROKE_OUTER = "#3DA4EE"
    LOGO_STROKE_INNER = "#7DC2F7"
    LOGO_FILL_INNER = "rgba(59, 164, 238, 0.08)"
    LOGO_DOT = "#3DA4EE"


class Radius:
    """`--radius-*` tokens."""

    SM = 4
    MD = 6
    LG = 8
    XL = 10


def sp(units: float) -> int:
    """Convert a Tailwind spacing unit (1 unit = 4px) into pixels."""
    return round(units * 4)


class FontSize:
    """Tailwind text-* sizes actually used in the design."""

    XXS_9 = 9
    XXS_10 = 10
    XS = 12
    SM = 14
    BASE = 16
    XL = 20
    XXL = 24


def rgba(hex_color: str, alpha_percent: float) -> str:
    """Build a Qt stylesheet rgba() string from a #RRGGBB color and an alpha percent (0-100)."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    a = round(alpha_percent / 100 * 255)
    return f"rgba({r}, {g}, {b}, {a})"


_SANS_STACK = ["Inter Variable", "Inter", "Segoe UI", "SF Pro Text", "Helvetica Neue", "Arial", "sans-serif"]
_MONO_STACK = ["JetBrains Mono", "Cascadia Code", "Consolas", "Courier New", "monospace"]

_resolved_sans: str | None = None
_resolved_mono: str | None = None

# Bundled variable fonts (SIL OFL 1.1) — official releases, no network dependency
# at runtime. See resources/fonts/<family>/OFL.txt for the license text.
_FONTS_DIR = Path(__file__).resolve().parent.parent / "resources" / "fonts"
_BUNDLED_FONT_FILES = [
    _FONTS_DIR / "Inter" / "InterVariable.ttf",
    _FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-Variable.ttf",
]

_fonts_loaded = False


def load_bundled_fonts() -> list[str]:
    """Register the bundled Inter / JetBrains Mono variable fonts with Qt.

    Must be called once, early at startup, before any QFont is constructed —
    font_sans()/font_mono() cache their resolution on first call, so loading
    the bundled fonts after that point would have no effect. Safe to call
    more than once (no-op after the first call). Returns the font family
    names that were actually registered.
    """
    global _fonts_loaded
    if _fonts_loaded:
        return []
    _fonts_loaded = True

    loaded_families: list[str] = []
    for font_path in _BUNDLED_FONT_FILES:
        if not font_path.is_file():
            continue
        font_id = QFontDatabase.addApplicationFont(str(font_path))
        if font_id == -1:
            continue
        loaded_families.extend(QFontDatabase.applicationFontFamilies(font_id))
    return loaded_families


def _resolve_family(stack: list[str]) -> str:
    available = set(QFontDatabase.families())
    for name in stack:
        if name in available:
            return name
    return stack[-1]


def font_sans() -> str:
    """Return the first available font from the Inter fallback stack."""
    global _resolved_sans
    if _resolved_sans is None:
        _resolved_sans = _resolve_family(_SANS_STACK)
    return _resolved_sans


def font_mono() -> str:
    """Return the first available font from the JetBrains Mono fallback stack."""
    global _resolved_mono
    if _resolved_mono is None:
        _resolved_mono = _resolve_family(_MONO_STACK)
    return _resolved_mono
