"""The complete skull silhouette and neck, independent of hair and expression.

All editable head elements use this local coordinate frame. Hair is aligned to
this skull, with extra volume above and beside it; do not fit the skull to the
outer silhouette of individual hair locks. Horn placement is separately frozen.
"""
from matplotlib.transforms import Affine2D
from ..palette import SKIN

HEAD_PIVOT = (790, 790)
HEAD_ANGLE = -11.5
SKULL_PATH = 'M 858 242 C 1074 256 1231 357 1284 521 C 1328 653 1321 792 1290 928 C 1318 1086 1312 1238 1193 1312 C 1104 1366 961 1386 834 1384 Q 802 1390 776 1380 C 555 1394 407 1348 352 1244 C 288 1111 285 893 292 710 C 294 526 326 399 414 335 C 546 241 702 221 858 242 Z'


def pose():
    return Affine2D().rotate_deg_around(*HEAD_PIVOT, HEAD_ANGLE)


def draw_neck(canvas):
    canvas.path('M 683 1338 L 689 1427 Q 823 1489 933 1425 L 929 1348 Z', SKIN, w=10)


def draw_skull(canvas):
    canvas.path(SKULL_PATH, SKIN, w=23)
    canvas.path('M 363 1113 C 361 1243 412 1329 564 1357 C 437 1346 374 1310 351 1243 Q 328 1181 363 1113 Z', '#f3dce1', 'none')


def draw(canvas):
    draw_neck(canvas)
    draw_skull(canvas)
