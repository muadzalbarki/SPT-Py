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

    accent_lavender: str = ""
    accent_sapphire: str = ""
    accent_blue: str = ""
    accent_rosewater: str = ""
    accent_green: str = ""
    accent_red: str = ""
    accent_yellow: str = ""
    accent_mauve: str = ""
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


MOCHA = ColorTokens(
    bg_primary="#1e1e2e",
    bg_secondary="#181825",
    bg_surface="#313244",
    bg_mantle="#181825",
    bg_crust="#11111b",
    bg_overlay="#6c7086",
    bg_hover="#45475a",

    text_primary="#cdd6f4",
    text_secondary="#bac2de",
    text_subtext="#a6adc8",
    text_disabled="#585b70",

    accent_lavender="#b4befe",
    accent_sapphire="#74c7ec",
    accent_blue="#89b4fa",
    accent_rosewater="#f5e0dc",
    accent_green="#a6e3a1",
    accent_red="#f38ba8",
    accent_yellow="#f9e2af",
    accent_mauve="#cba6f7",
    accent_teal="#94e2d5",

    border_color="#45475a",
    border_hover="#585b70",
    shadow_color="rgba(0,0,0,0.35)",
    shadow_intense="rgba(0,0,0,0.50)",

    scrollbar_bg="#313244",
    scrollbar_fg="#585b70",
    scrollbar_hover="#6c7086",

    success="#a6e3a1",
    warning="#f9e2af",
    error="#f38ba8",
    info="#89b4fa",

    sidebar_bg="linear-gradient(180deg, #1e1e2e 0%, #181825 100%)",
    sidebar_active="#b4befe",
    sidebar_hover="#313244",
    sidebar_text="#cdd6f4",
    sidebar_icon="#b4befe",

    card_bg="rgba(30,30,46,0.95)",
    card_border="rgba(255,255,255,0.05)",
    card_shadow="rgba(0,0,0,0.3)",

    table_bg="#1e1e2e",
    table_alt="#181825",
    table_hover="#313244",
    table_selected="#45475a",
    table_border="#313244",
)

LATTE = ColorTokens(
    bg_primary="#eff1f5",
    bg_secondary="#e6e9ef",
    bg_surface="#ccd0da",
    bg_mantle="#e6e9ef",
    bg_crust="#dce0e8",
    bg_overlay="#9ca0b0",
    bg_hover="#bcc0cc",

    text_primary="#4c4f69",
    text_secondary="#5c5f77",
    text_subtext="#6c6f85",
    text_disabled="#acb0be",

    accent_lavender="#7287fd",
    accent_sapphire="#209fb5",
    accent_blue="#1e66f5",
    accent_rosewater="#dc8a78",
    accent_green="#40a02b",
    accent_red="#d20f39",
    accent_yellow="#df8e1d",
    accent_mauve="#8839ef",
    accent_teal="#179299",

    border_color="#ccd0da",
    border_hover="#bcc0cc",
    shadow_color="rgba(0,0,0,0.08)",
    shadow_intense="rgba(0,0,0,0.15)",

    scrollbar_bg="#ccd0da",
    scrollbar_fg="#9ca0b0",
    scrollbar_hover="#acb0be",

    success="#40a02b",
    warning="#df8e1d",
    error="#d20f39",
    info="#1e66f5",

    sidebar_bg="linear-gradient(180deg, #eff1f5 0%, #e6e9ef 100%)",
    sidebar_active="#7287fd",
    sidebar_hover="#ccd0da",
    sidebar_text="#4c4f69",
    sidebar_icon="#7287fd",

    card_bg="rgba(255,255,255,0.90)",
    card_border="rgba(0,0,0,0.06)",
    card_shadow="rgba(0,0,0,0.08)",

    table_bg="#ffffff",
    table_alt="#f2f3f6",
    table_hover="#e6e9ef",
    table_selected="#ccd0da",
    table_border="#e6e9ef",
)
