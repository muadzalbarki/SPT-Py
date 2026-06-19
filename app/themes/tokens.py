from dataclasses import dataclass, field


@dataclass
class ColorTokens:
    bg_primary: str = ""
    bg_secondary: str = ""
    bg_surface: str = ""
    bg_mantle: str = ""
    bg_crust: str = ""
    bg_overlay: str = ""
    bg_hover: str = ""

    text_primary: str = ""
    text_secondary: str = ""
    text_subtext: str = ""
    text_disabled: str = ""

    accent_gold: str = ""
    accent_navy: str = ""
    accent_slate: str = ""
    accent_blue: str = ""
    accent_green: str = ""
    accent_red: str = ""
    accent_yellow: str = ""
    accent_teal: str = ""

    border_color: str = ""
    border_hover: str = ""
    shadow_color: str = ""
    shadow_intense: str = ""

    scrollbar_bg: str = ""
    scrollbar_fg: str = ""
    scrollbar_hover: str = ""

    success: str = ""
    warning: str = ""
    error: str = ""
    info: str = ""

    sidebar_bg: str = ""
    sidebar_active: str = ""
    sidebar_hover: str = ""
    sidebar_text: str = ""
    sidebar_icon: str = ""

    card_bg: str = ""
    card_border: str = ""
    card_shadow: str = ""

    table_bg: str = ""
    table_alt: str = ""
    table_hover: str = ""
    table_selected: str = ""
    table_border: str = ""

    def to_rgba(self, hex_color: str, alpha: float = 1.0) -> str:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    def to_rgb(self, hex_color: str) -> str:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"{r},{g},{b}"

    def to_dict(self):
        return {f.name: getattr(self, f.name) for f in self.__dataclass_fields__.values()}


GOVERNMENT_LIGHT = ColorTokens(
    bg_primary="#FFFFFF",
    bg_secondary="#F8FAFC",
    bg_surface="#F1F5F9",
    bg_mantle="#F1F5F9",
    bg_crust="#E2E8F0",
    bg_overlay="#CBD5E1",
    bg_hover="#F1F5F9",

    text_primary="#0F172A",
    text_secondary="#475569",
    text_subtext="#64748B",
    text_disabled="#94A3B8",

    accent_gold="#D4AF37",
    accent_navy="#0F172A",
    accent_slate="#1E293B",
    accent_blue="#3B82F6",
    accent_green="#10B981",
    accent_red="#EF4444",
    accent_yellow="#F59E0B",
    accent_teal="#14B8A6",

    border_color="#E2E8F0",
    border_hover="#CBD5E1",
    shadow_color="rgba(15,23,42,0.06)",
    shadow_intense="rgba(15,23,42,0.12)",

    scrollbar_bg="#F1F5F9",
    scrollbar_fg="#CBD5E1",
    scrollbar_hover="#94A3B8",

    success="#10B981",
    warning="#F59E0B",
    error="#EF4444",
    info="#3B82F6",

    sidebar_bg="#0F172A",
    sidebar_active="#D4AF37",
    sidebar_hover="#1E293B",
    sidebar_text="#FFFFFF",
    sidebar_icon="#D4AF37",

    card_bg="#FFFFFF",
    card_border="#E2E8F0",
    card_shadow="rgba(15,23,42,0.06)",

    table_bg="#FFFFFF",
    table_alt="#F8FAFC",
    table_hover="#F1F5F9",
    table_selected="#E2E8F0",
    table_border="#E2E8F0",
)

GOVERNMENT_DARK = ColorTokens(
    bg_primary="#020617",
    bg_secondary="#0F172A",
    bg_surface="#1E293B",
    bg_mantle="#1E293B",
    bg_crust="#334155",
    bg_overlay="#475569",
    bg_hover="#334155",

    text_primary="#F8FAFC",
    text_secondary="#CBD5E1",
    text_subtext="#94A3B8",
    text_disabled="#64748B",

    accent_gold="#D4AF37",
    accent_navy="#0F172A",
    accent_slate="#1E293B",
    accent_blue="#60A5FA",
    accent_green="#34D399",
    accent_red="#F87171",
    accent_yellow="#FBBF24",
    accent_teal="#2DD4BF",

    border_color="#334155",
    border_hover="#475569",
    shadow_color="rgba(0,0,0,0.3)",
    shadow_intense="rgba(0,0,0,0.5)",

    scrollbar_bg="#1E293B",
    scrollbar_fg="#475569",
    scrollbar_hover="#64748B",

    success="#34D399",
    warning="#FBBF24",
    error="#F87171",
    info="#60A5FA",

    sidebar_bg="#020617",
    sidebar_active="#D4AF37",
    sidebar_hover="#1E293B",
    sidebar_text="#F8FAFC",
    sidebar_icon="#D4AF37",

    card_bg="#0F172A",
    card_border="#334155",
    card_shadow="rgba(0,0,0,0.3)",

    table_bg="#0F172A",
    table_alt="#1E293B",
    table_hover="#334155",
    table_selected="#1E293B",
    table_border="#334155",
)
