"""Black clothing and collar; skin is owned by the head element."""
from ..palette import BLACK, RED, INK


def draw_back(canvas):
    path = canvas.path
    path('M 655 1290 L 662 1440 L 569 1518 L 551 1738 L 1053 1738 L 1047 1516 L 946 1417 L 945 1299 Z',BLACK,w=19)


def draw_front(canvas):
    path = canvas.path
    ellipse = canvas.ellipse
    path('M 689 1393 Q 816 1438 933 1388 L 933 1435 Q 815 1478 691 1437 Z','#26222b',w=11)
    for x,y in [(703,1439),(729,1448),(757,1455),(786,1460),(816,1462),
                (846,1459),(875,1453),(902,1445),(925,1436)]:
        ellipse(x,y,12,10,'#26222b')
    ellipse(814,1431,18,24,RED,INK,7)
    ellipse(809,1422,4,7,'#e9a7b6')


def draw(canvas):
    draw_back(canvas)
    draw_front(canvas)
