"""Independent hair ribbon and rose. The cross and its chain are removed.

Further ribbon detail is intentionally deferred until the user requests it.
"""
from ..palette import BLACK, INK


def draw(canvas):
    path = canvas.path
    # A single small black ribbon keeps the side accessory secondary to the hair.
    path('M 1309 654 C 1266 598 1226 595 1206 613 Q 1194 660 1226 686 Q 1266 688 1309 665 Z',BLACK,w=14)
    path('M 1316 652 C 1365 601 1402 601 1416 625 Q 1424 668 1395 695 Q 1350 692 1316 667 Z',BLACK,w=14)
    path('M 1289 670 L 1253 765 L 1291 749 L 1313 776 L 1324 671 Z',BLACK,w=12)
    path('M 1321 674 L 1352 771 L 1372 747 L 1407 758 L 1342 662 Z',BLACK,w=12)
    path('M 1225 633 Q 1260 648 1290 652 M 1341 652 Q 1373 634 1397 631',stroke='#5d4d61',w=7)
    path('M 1291 637 Q 1301 615 1320 626 Q 1344 622 1347 645 Q 1363 660 1344 677 Q 1335 698 1314 687 Q 1290 697 1284 674 Q 1266 656 1291 637 Z','#56323f',INK,9)
    path('M 1298 651 Q 1309 634 1326 644 Q 1343 653 1329 669 Q 1316 681 1304 669 Q 1293 660 1309 653 Q 1318 650 1321 658',stroke='#ae637a',w=6)

