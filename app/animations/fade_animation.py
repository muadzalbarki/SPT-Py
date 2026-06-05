from app.core.animation_manager import AnimationManager


def fade_in(widget, duration=300, start_opacity=0.0, end_opacity=1.0):
    return AnimationManager.fade_in(widget, duration, start_opacity, end_opacity)


def fade_out(widget, duration=200, start_opacity=1.0, end_opacity=0.0):
    return AnimationManager.fade_out(widget, duration, start_opacity, end_opacity)
