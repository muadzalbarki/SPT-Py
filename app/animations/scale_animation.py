from app.core.animation_manager import AnimationManager


def scale_press(widget, duration=80):
    return AnimationManager.scale_press(widget, duration)


def scale_release(widget, duration=80):
    return AnimationManager.scale_release(widget, duration)
