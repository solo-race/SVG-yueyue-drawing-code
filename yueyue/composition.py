"""Explicit visual stacking order; every element lives in its own script."""
from .canvas import Canvas
from .elements import clothing, face, hair, head, horn_left, horn_right, ribbon

ELEMENTS = ("portrait", "head", "hair", "horn-left", "horn-right", "ribbon", "clothing", "face")


def compose(size=2400, element="portrait"):
    canvas = Canvas(size, head.pose(), transparent=element != "portrait")
    if element == "portrait":
        hair.draw_back(canvas)
        clothing.draw_back(canvas)
        head.draw_neck(canvas)
        clothing.draw_front(canvas)
        head.draw_skull(canvas)
        face.draw(canvas)
        hair.draw_front(canvas)
        horn_left.draw(canvas)
        horn_right.draw(canvas)
        hair.draw_roots(canvas)
        ribbon.draw(canvas)
    else:
        drawers = {"head": head.draw, "hair": hair.draw,
                   "horn-left": horn_left.draw, "horn-right": horn_right.draw,
                   "ribbon": ribbon.draw, "clothing": clothing.draw, "face": face.draw}
        drawers[element](canvas)
    return canvas
