from app.core.platform_detection import is_linux


class PlatformCapabilities:
    @staticmethod
    def use_opacity_animations() -> bool:
        return not is_linux()

    @staticmethod
    def use_advanced_effects() -> bool:
        return not is_linux()

    @staticmethod
    def supports_frameless() -> bool:
        from app.config import ENABLE_FRAMELESS_LINUX
        if is_linux():
            return ENABLE_FRAMELESS_LINUX
        return True
