"""FROZEN right horn (viewer-right). Change only when the user unfreezes it.

Geometry, placement, size, texture and seed are the pre-refactor values.
"""
from . import _horn_surface

CONTROL = ((1242, 430), (1396, 336), (1152, 205), (1300, 116))
ROOT_RADIUS = 91
SEED = 19
POSE = (790, 790, -11.5)


def draw(canvas):
    _horn_surface.draw(canvas, CONTROL, ROOT_RADIUS, SEED, POSE)
