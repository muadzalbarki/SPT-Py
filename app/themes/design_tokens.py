from dataclasses import dataclass, field
from typing import Dict


@dataclass
class TypographyTokens:
    font_family: str = "Inter, 'Segoe UI', 'Noto Sans', sans-serif"
    font_family_mono: str = "'JetBrains Mono', 'Cascadia Code', 'Fira Code', monospace"

    sizes: Dict[str, int] = field(default_factory=lambda: {
        "xs": 11,
        "sm": 12,
        "base": 14,
        "md": 16,
        "lg": 18,
        "xl": 20,
        "2xl": 24,
        "3xl": 30,
        "4xl": 36,
        "5xl": 48,
    })

    weights: Dict[str, int] = field(default_factory=lambda: {
        "regular": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700,
    })

    line_heights: Dict[str, float] = field(default_factory=lambda: {
        "tight": 1.2,
        "normal": 1.5,
        "relaxed": 1.75,
    })


@dataclass
class SpacingTokens:
    unit: int = 8
    values: Dict[str, int] = field(default_factory=lambda: {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32,
        "2xl": 40,
        "3xl": 48,
        "4xl": 64,
    })


@dataclass
class RadiusTokens:
    sm: int = 4
    md: int = 8
    lg: int = 12
    xl: int = 16
    full: int = 9999


@dataclass
class ElevationTokens:
    level0: str = "none"
    level1: str = ""
    level2: str = ""
    level3: str = ""
    level4: str = ""


@dataclass
class ColorTokens:
    name: str = ""

    bg_primary: str = ""
    bg_secondary: str = ""
    bg_surface: str = ""
    bg_mantle: str = ""
    bg_crust: str = ""
    bg_overlay: str = ""
    bg_hover: str = ""
    bg_active: str = ""
    bg_input: str = ""
    bg_sidebar: str = ""
    bg_topbar: str = ""

    text_primary: str = ""
    text_secondary: str = ""
    text_muted: str = ""
    text_disabled: str = ""
    text_inverse: str = ""
    text_link: str = ""
    text_accent: str = ""

    accent: str = ""
    accent_hover: str = ""
    accent_light: str = ""
    accent_muted: str = ""

    border: str = ""
    border_hover: str = ""
    border_focus: str = ""
    border_light: str = ""

    sidebar_bg: str = ""
    sidebar_active: str = ""
    sidebar_hover: str = ""
    sidebar_text: str = ""
    sidebar_icon: str = ""
    sidebar_indicator: str = ""
    sidebar_subtitle: str = ""

    card_bg: str = ""
    card_border: str = ""
    card_shadow: str = ""

    table_bg: str = ""
    table_alt: str = ""
    table_hover: str = ""
    table_selected: str = ""
    table_border: str = ""
    table_header_bg: str = ""
    table_header_text: str = ""

    success: str = ""
    success_bg: str = ""
    success_text: str = ""
    warning: str = ""
    warning_bg: str = ""
    warning_text: str = ""
    danger: str = ""
    danger_bg: str = ""
    danger_text: str = ""
    info: str = ""
    info_bg: str = ""
    info_text: str = ""

    scrollbar_bg: str = ""
    scrollbar_fg: str = ""
    scrollbar_hover: str = ""

    input_bg: str = ""
    input_border: str = ""
    input_focus_border: str = ""
    input_placeholder: str = ""

    progress_bg: str = ""
    progress_fg: str = ""

    badge_pegawai: str = ""
    badge_komisi_a: str = ""
    badge_komisi_b: str = ""
    badge_komisi_c: str = ""

    trend_up: str = ""
    trend_down: str = ""
    trend_neutral: str = ""

    wizard_step_bg: str = ""
    wizard_step_active: str = ""
    wizard_step_completed: str = ""
    wizard_step_text: str = ""

    def to_rgba(self, hex_color: str, alpha: float = 1.0) -> str:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"


LIGHT = ColorTokens(
    name="light",

    bg_primary="#F8FAFC",
    bg_secondary="#F1F5F9",
    bg_surface="#FFFFFF",
    bg_mantle="#E2E8F0",
    bg_crust="#CBD5E1",
    bg_overlay="#94A3B8",
    bg_hover="#F1F5F9",
    bg_active="#E2E8F0",
    bg_input="#FFFFFF",
    bg_sidebar="#0F172A",
    bg_topbar="#FFFFFF",

    text_primary="#111827",
    text_secondary="#475569",
    text_muted="#94A3B8",
    text_disabled="#CBD5E1",
    text_inverse="#FFFFFF",
    text_link="#1E40AF",
    text_accent="#D4AF37",

    accent="#D4AF37",
    accent_hover="#C5A032",
    accent_light="#FEF9E7",
    accent_muted="#F5E6B8",

    border="#E2E8F0",
    border_hover="#CBD5E1",
    border_focus="#D4AF37",
    border_light="#F1F5F9",

    sidebar_bg="#0F172A",
    sidebar_active="#D4AF37",
    sidebar_hover="#1E293B",
    sidebar_text="#F8FAFC",
    sidebar_icon="#D4AF37",
    sidebar_indicator="#D4AF37",
    sidebar_subtitle="#94A3B8",

    card_bg="#FFFFFF",
    card_border="#E2E8F0",
    card_shadow="rgba(15,23,42,0.06)",

    table_bg="#FFFFFF",
    table_alt="#F8FAFC",
    table_hover="#F1F5F9",
    table_selected="#FEF9E7",
    table_border="#E2E8F0",
    table_header_bg="#F8FAFC",
    table_header_text="#475569",

    success="#10B981",
    success_bg="#D1FAE5",
    success_text="#065F46",
    warning="#F59E0B",
    warning_bg="#FEF3C7",
    warning_text="#92400E",
    danger="#EF4444",
    danger_bg="#FEE2E2",
    danger_text="#991B1B",
    info="#3B82F6",
    info_bg="#DBEAFE",
    info_text="#1E40AF",

    scrollbar_bg="#E2E8F0",
    scrollbar_fg="#94A3B8",
    scrollbar_hover="#64748B",

    input_bg="#FFFFFF",
    input_border="#E2E8F0",
    input_focus_border="#D4AF37",
    input_placeholder="#94A3B8",

    progress_bg="#E2E8F0",
    progress_fg="#D4AF37",

    badge_pegawai="#D4AF37",
    badge_komisi_a="#3B82F6",
    badge_komisi_b="#10B981",
    badge_komisi_c="#8B5CF6",

    trend_up="#10B981",
    trend_down="#EF4444",
    trend_neutral="#94A3B8",

    wizard_step_bg="#E2E8F0",
    wizard_step_active="#D4AF37",
    wizard_step_completed="#10B981",
    wizard_step_text="#475569",
)

DARK = ColorTokens(
    name="dark",

    bg_primary="#0F172A",
    bg_secondary="#1E293B",
    bg_surface="#1E293B",
    bg_mantle="#334155",
    bg_crust="#475569",
    bg_overlay="#64748B",
    bg_hover="#334155",
    bg_active="#475569",
    bg_input="#1E293B",
    bg_sidebar="#0A0F1E",
    bg_topbar="#1E293B",

    text_primary="#F8FAFC",
    text_secondary="#CBD5E1",
    text_muted="#64748B",
    text_disabled="#475569",
    text_inverse="#0F172A",
    text_link="#93C5FD",
    text_accent="#D4AF37",

    accent="#D4AF37",
    accent_hover="#E0B94A",
    accent_light="#3D3520",
    accent_muted="#2A2418",

    border="#334155",
    border_hover="#475569",
    border_focus="#D4AF37",
    border_light="#1E293B",

    sidebar_bg="#0A0F1E",
    sidebar_active="#D4AF37",
    sidebar_hover="#1E293B",
    sidebar_text="#F8FAFC",
    sidebar_icon="#D4AF37",
    sidebar_indicator="#D4AF37",
    sidebar_subtitle="#64748B",

    card_bg="#1E293B",
    card_border="#334155",
    card_shadow="rgba(0,0,0,0.25)",

    table_bg="#1E293B",
    table_alt="#0F172A",
    table_hover="#334155",
    table_selected="#2A2418",
    table_border="#334155",
    table_header_bg="#0F172A",
    table_header_text="#CBD5E1",

    success="#10B981",
    success_bg="#064E3B",
    success_text="#A7F3D0",
    warning="#F59E0B",
    warning_bg="#78350F",
    warning_text="#FDE68A",
    danger="#EF4444",
    danger_bg="#7F1D1D",
    danger_text="#FECACA",
    info="#3B82F6",
    info_bg="#1E3A5F",
    info_text="#BFDBFE",

    scrollbar_bg="#1E293B",
    scrollbar_fg="#475569",
    scrollbar_hover="#64748B",

    input_bg="#0F172A",
    input_border="#334155",
    input_focus_border="#D4AF37",
    input_placeholder="#64748B",

    progress_bg="#334155",
    progress_fg="#D4AF37",

    badge_pegawai="#D4AF37",
    badge_komisi_a="#60A5FA",
    badge_komisi_b="#34D399",
    badge_komisi_c="#A78BFA",

    trend_up="#34D399",
    trend_down="#F87171",
    trend_neutral="#64748B",

    wizard_step_bg="#334155",
    wizard_step_active="#D4AF37",
    wizard_step_completed="#10B981",
    wizard_step_text="#CBD5E1",
)

TYPOGRAPHY = TypographyTokens()
SPACING = SpacingTokens()
RADIUS = RadiusTokens()
