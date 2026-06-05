from app.core.animation_manager import AnimationManager


def slide_to(widget, target_x=0, duration=250):
    return AnimationManager.slide_to(widget, target_x, duration)
