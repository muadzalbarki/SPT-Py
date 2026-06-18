from PySide6.QtCore import QObject


class Breakpoints:
    MOBILE = 900
    TABLET = 1366
    DESKTOP = 1920
    ULTRAWIDE = 2560


class ResponsiveManager(QObject):
    @staticmethod
    def is_mobile(width: int) -> bool:
        return width < Breakpoints.MOBILE

    @staticmethod
    def is_tablet(width: int) -> bool:
        return Breakpoints.MOBILE <= width < Breakpoints.TABLET

    @staticmethod
    def is_desktop(width: int) -> bool:
        return Breakpoints.TABLET <= width < Breakpoints.ULTRAWIDE

    @staticmethod
    def is_ultrawide(width: int) -> bool:
        return width >= Breakpoints.ULTRAWIDE

    @staticmethod
    def columns_for_width(width: int, min_column_width: int = 280, max_columns: int = 6) -> int:
        if width <= 0:
            return 1
        cols = width // min_column_width
        return max(1, min(cols, max_columns))

    @staticmethod
    def should_stack(width: int, stack_breakpoint: int = 1200) -> bool:
        return width < stack_breakpoint
