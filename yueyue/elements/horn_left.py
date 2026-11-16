"""FROZEN left horn (viewer-left). Change only when the user unfreezes it.

Geometry, placement, size, texture and seed are the pre-refactor values.
"""
from . import _horn_surface

CONTROL = ((308, 457), (120, 366), (349, 238), (224, 80))
ROOT_RADIUS = 86
SEED = 11
POSE = (790, 790, -11.5)


def draw(canvas):
    _horn_surface.draw(canvas, CONTROL, ROOT_RADIUS, SEED, POSE)
