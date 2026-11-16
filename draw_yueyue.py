#!/usr/bin/env python3
"""Draw Yueyue's close-up chibi portrait using Python vector geometry.

Run: python draw_yueyue.py --output . --size 2400
Requires: matplotlib and numpy. No input images or image-generation API.
Produces a PNG and SVG; horn shading, growth rings and all hair are code-drawn.
"""
from pathlib import Path as FilePath
import argparse
import math
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Ellipse
from matplotlib.collections import PolyCollection
from matplotlib.transforms import Affine2D

INK = '#30282d'
HAIR = '#f6f4f8'
SHADE = '#e1d9e9'
DEEP = '#c9bcd5'
LIGHT = '#fffefd'
SKIN = '#fff3ef'
BLUSH = '#f7c7d0'
BLACK = '#38303c'
RED = '#a4445b'


def parse_path(data):
    tokens = re.findall(r'[MLCQZ]|[-+]?(?:\d*\.\d+|\d+)', data)
    vertices, codes, i, start = [], [], 0, (0, 0)
    while i < len(tokens):
        cmd = tokens[i]
        i += 1
        if cmd == 'Z':
            vertices.append(start)
            codes.append(Path.CLOSEPOLY)
            continue
        count = {'M': 1, 'L': 1, 'Q': 2, 'C': 3}[cmd]
        pts = [(float(tokens[i+2*j]), float(tokens[i+2*j+1])) for j in range(count)]
        i += 2*count
        vertices.extend(pts)
        codes.extend({'M':[Path.MOVETO], 'L':[Path.LINETO],
                      'Q':[Path.CURVE3]*2, 'C':[Path.CURVE4]*3}[cmd])
        if cmd == 'M':
            start = pts[0]
    return Path(vertices, codes)


def draw(output, size):
    fig = plt.figure(figsize=(8, 8), dpi=size/8, facecolor='#fffefd')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0,1600), ylim=(1600,0), aspect='equal')
    ax.axis('off')
    head = Affine2D().rotate_deg_around(790,790,-11.5)
    layer = 0

    def path(data, fill='none', stroke=INK, w=17, rough=.9, alpha=1):
        nonlocal layer
        layer += 1
        shape = parse_path(data) if isinstance(data,str) else data
        patch = PathPatch(shape, facecolor=fill, edgecolor=stroke,
                          linewidth=w*.36, capstyle='round', joinstyle='round',
                          transform=head+ax.transData, zorder=layer, alpha=alpha)
        if rough:
            patch.set_sketch_params(scale=rough,length=105,randomness=1.7)
        ax.add_patch(patch)
        return patch

    def ellipse(x,y,rx,ry,fill,stroke='none',w=10,angle=0):
        nonlocal layer
        layer += 1
        ax.add_patch(Ellipse((x,y),rx*2,ry*2,angle=angle,facecolor=fill,
                            edgecolor=stroke,linewidth=w*.36,
                            transform=head+ax.transData,zorder=layer))

    def line(points, color, width, alpha=1):
        pts = np.asarray(points)
        return path(Path(pts,[Path.MOVETO]+[Path.LINETO]*(len(pts)-1)),
                    stroke=color,w=width,rough=0,alpha=alpha)

    # A full mass of long hair fills both edges of the close crop.
    path('M 238 516 C 120 667 91 857 102 1042 C 109 1175 54 1267 15 1331 Q 87 1318 120 1278 C 64 1441 20 1539 53 1737 L 580 1770 C 591 1535 557 1336 534 1051 Z',HAIR,w=22)
    path('M 1227 420 C 1395 562 1438 768 1447 978 C 1446 1110 1518 1216 1580 1267 Q 1509 1284 1462 1226 C 1537 1425 1557 1583 1531 1771 L 1095 1800 C 1043 1502 1080 1258 1124 1018 Z',HAIR,w=22)
    path('M 213 763 C 183 1093 238 1192 154 1441 C 125 1546 130 1643 166 1755 L 264 1766 C 201 1548 337 1360 317 1169 C 280 980 294 886 320 788 Z',SHADE,'none')
    path('M 1323 690 C 1352 952 1310 1132 1424 1431 C 1480 1587 1454 1718 1451 1790 L 1522 1790 C 1557 1517 1461 1287 1434 1133 C 1414 923 1404 824 1323 690 Z',SHADE,'none')
    path('M 377 1086 C 317 1286 356 1397 270 1584 Q 302 1566 330 1532 Q 302 1684 337 1764 L 490 1764 C 405 1540 543 1335 505 1198 Z',SHADE,'none')
    path('M 1221 1019 C 1196 1259 1286 1368 1236 1556 Q 1218 1502 1195 1484 Q 1239 1667 1208 1781 L 1322 1787 C 1360 1605 1257 1384 1293 1199 Z',SHADE,'none')
    for d in [
        'M 169 1105 C 189 1230 108 1390 122 1531',
        'M 249 1099 C 274 1318 197 1468 220 1650',
        'M 384 1284 C 375 1405 333 1487 321 1536',
        'M 469 1299 C 488 1447 402 1620 434 1735',
        'M 1335 1075 C 1344 1219 1425 1411 1402 1582',
        'M 1264 1263 C 1259 1409 1331 1582 1306 1749',
        'M 1447 1314 C 1483 1398 1497 1529 1489 1652']:
        path(d,stroke=DEEP,w=12)
    path('M 184 1325 C 135 1472 158 1582 177 1618',stroke=LIGHT,w=26)
    path('M 1367 1306 C 1403 1406 1424 1525 1411 1579',stroke=LIGHT,w=25)

    # Only a small piece of black collar remains below the portrait.
    path('M 655 1290 L 662 1440 L 569 1518 L 551 1738 L 1053 1738 L 1047 1516 L 946 1417 L 945 1299 Z',BLACK,w=19)
    path('M 683 1338 L 689 1427 Q 823 1489 933 1425 L 929 1348 Z',SKIN,w=10)
    path('M 689 1393 Q 816 1438 933 1388 L 933 1435 Q 815 1478 691 1437 Z','#26222b',w=11)
    for x,y in [(703,1439),(729,1448),(757,1455),(786,1460),(816,1462),
                (846,1459),(875,1453),(902,1445),(925,1436)]:
        ellipse(x,y,12,10,'#26222b')
    ellipse(814,1431,18,24,RED,INK,7)
    ellipse(809,1422,4,7,'#e9a7b6')

    # Face and low-set eyes. Ears are entirely behind the thick hair.
    path('M 351 685 C 452 566 660 548 853 581 C 1126 609 1260 736 1290 928 C 1318 1086 1312 1238 1193 1312 C 1104 1366 961 1386 834 1384 Q 802 1390 776 1380 C 555 1394 407 1348 352 1244 C 302 1154 304 826 351 685 Z',SKIN,w=23)
    path('M 363 1113 C 361 1243 412 1329 564 1357 C 437 1346 374 1310 351 1243 Q 328 1181 363 1113 Z','#f3dce1','none')
    ellipse(454,1269,87,44,'#fbe0e4',angle=7)
    ellipse(1153,1268,83,45,'#fbe0e4',angle=-6)
    for x,y in [(418,1264),(455,1276),(492,1278),(1118,1279),(1155,1273),(1190,1262)]:
        path(f'M {x} {y-14} L {x+5} {y+13}',stroke=BLUSH,w=13)

    # Ovals with soft crimson centres and broad bright glints, as in the sample.
    saved_head=head
    head=Affine2D().translate(35,17)+saved_head
    path('M 435 1178 C 475 1141 554 1129 620 1146 C 665 1156 676 1191 650 1220 C 618 1258 531 1276 469 1258 C 431 1248 409 1207 435 1178 Z',INK,w=12)
    path('M 459 1189 C 500 1158 564 1154 612 1165 C 646 1172 655 1194 635 1212 C 601 1244 535 1254 486 1241 C 455 1233 438 1211 459 1189 Z',RED,'none')
    path('M 469 1220 Q 554 1241 640 1197 C 647 1218 609 1244 555 1249 Q 502 1257 477 1241 Z','#d58ba0','none')
    ellipse(550,1179,55,25,LIGHT,angle=-6)
    ellipse(602,1227,14,6,'#f5d0dc',angle=-8)
    head=Affine2D().translate(-25,17)+saved_head
    path('M 1000 1145 C 1064 1125 1148 1139 1185 1176 C 1212 1203 1195 1233 1160 1250 C 1100 1277 1021 1265 982 1234 C 951 1209 961 1159 1000 1145 Z',INK,w=12)
    path('M 1008 1165 C 1061 1148 1128 1155 1161 1181 C 1183 1200 1168 1225 1142 1237 C 1095 1255 1035 1249 1004 1225 C 982 1208 983 1177 1008 1165 Z',RED,'none')
    path('M 1002 1208 Q 1082 1239 1170 1204 C 1172 1228 1129 1247 1089 1250 Q 1038 1249 1009 1230 Z','#d58ba0','none')
    ellipse(1070,1178,55,25,LIGHT,angle=5)
    ellipse(1137,1231,14,6,'#f5d0dc',angle=5)
    head=Affine2D().translate(35,17)+saved_head
    path('M 427 1143 Q 510 1115 635 1126',stroke=INK,w=19)
    head=Affine2D().translate(-25,17)+saved_head
    path('M 985 1127 Q 1091 1117 1201 1149',stroke=INK,w=19)
    head=saved_head
    path('M 454 1060 Q 506 1036 563 1041 M 1056 1040 Q 1117 1037 1174 1058',stroke=INK,w=18)
    # Closed tiny mouth; there are no teeth.
    path('M 776 1335 Q 797 1349 821 1336',stroke=INK,w=7)

    # Large soft crown. Bangs descend as broad curved locks, not thin triangles.
    path('M 168 743 C 109 578 152 414 294 306 C 452 182 674 156 858 172 C 1114 184 1309 299 1382 476 C 1430 590 1436 724 1390 908 C 1365 1038 1301 1128 1249 1180 C 1271 1065 1240 921 1175 814 C 1232 973 1222 1098 1171 1150 Q 1147 1173 1130 1177 C 1147 1041 1093 923 1023 852 C 1073 1004 1055 1144 1016 1179 Q 992 1150 967 1053 C 964 1194 902 1230 855 1230 C 750 1193 672 1070 643 967 C 650 1100 693 1184 735 1219 C 637 1201 582 1108 551 1014 C 526 1125 528 1195 543 1230 C 476 1189 456 1119 454 1027 C 403 1155 411 1267 447 1323 C 351 1288 316 1198 321 1102 C 263 1163 224 1196 194 1205 C 222 1093 164 949 168 743 Z',HAIR,DEEP,w=13)
    path('M 168 743 C 109 578 152 414 294 306 C 452 182 674 156 858 172 C 1114 184 1309 299 1382 476 C 1430 590 1436 724 1390 908',stroke=INK,w=23)
    # Areas of lavender under broad strands.
    path('M 623 822 C 622 1034 681 1171 735 1219 C 645 1207 588 1124 564 1068 Q 616 1151 682 1177 C 622 1077 606 934 623 822 Z',SHADE,'none')
    path('M 925 975 C 981 1124 919 1210 855 1230 C 752 1197 697 1106 672 1059 C 729 1133 808 1194 855 1203 C 916 1194 951 1104 925 975 Z',SHADE,'none')
    path('M 1023 852 C 1073 1004 1055 1144 1016 1179 L 1008 1144 C 1039 1080 1054 983 1023 852 Z',SHADE,'none')
    path('M 1175 814 C 1232 973 1222 1098 1171 1150 Q 1147 1173 1130 1177 L 1139 1146 C 1203 1085 1211 968 1175 814 Z',SHADE,'none')
    path('M 551 1014 C 526 1125 528 1195 543 1230 Q 493 1200 477 1160 Q 503 1191 522 1202 C 510 1138 528 1068 551 1014 Z',SHADE,'none')
    path('M 454 1027 C 403 1155 411 1267 447 1323 C 381 1300 354 1257 337 1210 Q 390 1275 412 1280 C 394 1190 412 1085 454 1027 Z',SHADE,'none')
    # Main flow lines are deliberately unequal; the parting is slightly off-centre.
    for d,w in [
        ('M 603 298 C 490 352 415 529 401 718',14),
        ('M 748 270 C 800 238 847 274 911 345',13),
        ('M 984 330 C 1123 398 1200 543 1230 668',13),
        ('M 1091 503 C 1170 579 1221 705 1238 793',11),
        ('M 664 650 C 621 776 627 905 643 967',12),
        ('M 929 975 Q 952 1020 967 1053',12),
        ('M 1046 714 C 1091 776 1120 864 1131 936',12),
        ('M 343 559 C 291 684 276 816 283 912',12),
        ('M 523 799 C 500 903 513 961 526 999',11)]:
        path(d,stroke=DEEP,w=w)
    # Wide soft highlights follow the hair's fall rather than crossing the locks.
    path('M 353 478 C 405 389 475 336 540 316',stroke=LIGHT,w=32)
    path('M 314 564 L 299 614',stroke=LIGHT,w=25)
    path('M 447 512 Q 463 457 493 427',stroke=LIGHT,w=18)
    path('M 914 248 C 1040 277 1141 341 1196 428',stroke=LIGHT,w=26)
    path('M 653 497 Q 627 541 616 578',stroke=LIGHT,w=21)

    # A swept tuft of actual hair rises from the crown, as in the style reference.
    path('M 628 251 C 516 226 496 165 544 104 C 612 20 740 8 801 53 C 702 42 623 98 606 159 C 600 194 608 229 628 251 Z',HAIR,INK,21)
    path('M 628 251 C 589 221 580 179 602 141 C 644 79 697 62 742 52 Q 667 92 648 144 C 628 190 616 213 628 251 Z',SHADE,'none')
    path('M 590 118 Q 638 57 707 47',stroke=LIGHT,w=17)

    # Full cheek-covering side locks. Each layer has a distinct broad silhouette.
    path('M 282 569 C 179 756 184 980 205 1134 C 221 1231 267 1311 330 1360 Q 286 1366 249 1336 C 261 1438 318 1498 371 1527 C 250 1516 175 1416 168 1318 Q 128 1364 70 1372 C 140 1280 134 1175 118 1061 C 88 852 140 689 213 600',HAIR,w=22)
    path('M 244 795 C 210 1043 233 1220 330 1360 Q 286 1366 249 1336 C 261 1438 318 1498 371 1527 C 295 1524 243 1469 222 1415 Q 207 1360 210 1300 Q 246 1325 271 1323 C 203 1217 190 974 244 795 Z',SHADE,'none')
    path('M 218 1020 C 203 1170 220 1263 249 1308',stroke=DEEP,w=13)
    path('M 166 958 C 148 1116 188 1203 156 1292',stroke=DEEP,w=12)
    path('M 179 768 Q 160 837 159 891',stroke=LIGHT,w=27)
    # Inner left lock folds across the ear and the side of the cheek.
    path('M 398 635 C 316 819 330 1039 353 1157 C 377 1266 415 1326 480 1363 Q 426 1366 387 1329 Q 404 1419 454 1468 C 347 1442 293 1355 277 1249 C 251 1094 268 893 304 773',HAIR,DEEP,14)
    path('M 360 862 C 317 1091 373 1300 480 1363 Q 426 1366 387 1329 Q 404 1419 454 1468 C 410 1455 371 1426 354 1397 Q 338 1356 337 1305 Q 375 1321 408 1327 C 344 1211 315 1043 360 862 Z',SHADE,'none')
    path('M 329 1130 C 335 1233 352 1273 369 1303',stroke=DEEP,w=12)
    path('M 314 850 Q 290 929 292 988',stroke=LIGHT,w=20)
    # The right-hand side is fuller and sweeps with the tilted head.
    path('M 1315 557 C 1415 740 1407 922 1402 1115 C 1404 1235 1460 1311 1512 1349 Q 1458 1372 1411 1325 C 1403 1436 1350 1521 1274 1551 C 1332 1453 1326 1379 1318 1334 Q 1287 1379 1255 1394 C 1323 1246 1310 1157 1328 1046 C 1352 874 1328 732 1291 657',HAIR,w=22)
    path('M 1359 861 C 1394 1110 1340 1278 1363 1360 C 1384 1430 1332 1528 1274 1551 C 1332 1453 1326 1379 1318 1334 Q 1287 1379 1255 1394 C 1323 1246 1310 1157 1328 1046 Q 1344 953 1340 867 Z',SHADE,'none')
    path('M 1373 1082 C 1359 1205 1382 1302 1427 1337',stroke=DEEP,w=12)
    path('M 1372 747 Q 1402 826 1387 912',stroke=LIGHT,w=26)
    path('M 1248 769 C 1325 948 1302 1154 1273 1271 C 1248 1384 1198 1450 1134 1478 C 1178 1398 1180 1333 1172 1304 Q 1140 1354 1089 1361 C 1173 1236 1183 1162 1202 1064 C 1235 933 1223 861 1195 815',HAIR,DEEP,14)
    path('M 1263 975 C 1282 1144 1211 1285 1216 1345 Q 1207 1431 1134 1478 C 1178 1398 1180 1333 1172 1304 Q 1140 1354 1089 1361 C 1173 1236 1183 1162 1202 1064 Q 1219 1003 1223 950 C 1228 1080 1194 1234 1155 1300 Q 1208 1259 1221 1196 C 1249 1104 1255 1017 1263 975 Z',SHADE,'none')
    path('M 1261 1159 Q 1245 1260 1211 1324',stroke=DEEP,w=12)
    path('M 1276 909 Q 1293 977 1283 1038',stroke=LIGHT,w=19)

    def horn(control, root_radius, seed):
        """Curved tapered horn with annular ridges and shaded cross sections.

        The centreline defines growth direction. All ring arcs and fine striae
        are mapped onto its local elliptical cross section, so markings wrap
        the form, compress towards the tip, and never float outside the shell.
        """
        nonlocal layer
        c = np.asarray(control,dtype=float)
        rng = np.random.default_rng(seed)
        rings = np.array([.07,.16,.26,.37,.48,.59,.70,.80,.885,.95])

        def frame(t):
            q=1-t
            centre=q**3*c[0]+3*q*q*t*c[1]+3*q*t*t*c[2]+t**3*c[3]
            tangent=3*q*q*(c[1]-c[0])+6*q*t*(c[2]-c[1])+3*t*t*(c[3]-c[2])
            tangent=tangent/np.linalg.norm(tangent)
            normal=np.array([-tangent[1],tangent[0]])
            # Broad rounded root; taper continues to a narrow pointed tip.
            radius=root_radius*(1-t)**.70*(.94+.12*np.sin(np.pi*t))
            # Growth ridges change the contour itself, not just its painted lines.
            swelling=sum(.090*np.exp(-((t-r)/(.024-.012*r))**2) for r in rings)
            radius*=1+swelling
            return centre,tangent,normal,radius

        def surface(t,u):
            centre,tangent,normal,radius=frame(t)
            return centre+normal*radius*u+tangent*radius*.30*np.sqrt(max(0,1-u*u))

        ts=np.linspace(0,1,161)
        outline=[surface(t,-1) for t in ts]+[surface(t,1) for t in ts[::-1]]
        shell=Path(outline+[outline[0]], [Path.MOVETO]+[Path.LINETO]*(len(outline)-1)+[Path.CLOSEPOLY])
        path(shell,'#342a35',INK,21,rough=.6)
        faces,colors=[],[]
        # Smooth muted shading around the curved surface; no metallic white bands.
        tgrid=np.linspace(0,1,125)
        ugrid=np.linspace(-1,1,36)
        for a,b in zip(tgrid[:-1],tgrid[1:]):
            for u,v in zip(ugrid[:-1],ugrid[1:]):
                t=(a+b)/2
                q=(u+v)/2
                _,tangent,normal,_=frame(t)
                z=np.sqrt(max(0,1-q*q))
                normal3=np.array([normal[0]*q,normal[1]*q,z])
                lamp=np.array([-.55,-.8,1.0]); lamp/=np.linalg.norm(lamp)
                illumination=max(0,float(np.dot(normal3,lamp)))
                grooves=sum(np.exp(-((t-(r-.014))/.008)**2) for r in rings)
                ridge=sum(np.exp(-((t-(r+.012))/.012)**2) for r in rings)
                value=.27+.67*illumination-.13*grooves+.055*ridge
                value=np.clip(value,0,1)
                dark=np.array([40,32,42]); light=np.array([109,92,109])
                rgb=(dark+(light-dark)*value)/255
                faces.append([surface(a,u),surface(a,v),surface(b,v),surface(b,u)])
                colors.append(rgb)
        layer+=1
        mesh=PolyCollection(faces,facecolors=colors,edgecolors=colors,
                            linewidths=.15,antialiaseds=False,
                            transform=head+ax.transData,zorder=layer)
        mesh.set_clip_path(shell,head+ax.transData)
        ax.add_collection(mesh)
        # Each groove curves away around the horn. Thin near-tip rings are closer.
        for r in rings:
            points=[surface(r,u) for u in np.linspace(-.98,.98,61)]
            line(points,'#322834',4.8*(1-r)+1.2,.83)
            highlight=[surface(min(.997,r+.016),u) for u in np.linspace(-.82,.60,48)]
            line(highlight,'#9e879c',2.5*(1-r)+.7,.43)
            # A broken secondary lip makes the growth bands less mechanically uniform.
            start=float(rng.uniform(-.95,-.65)); stop=float(rng.uniform(.25,.65))
            seam=[surface(max(.005,r-.025),u) for u in np.linspace(start,stop,31)]
            line(seam,'#201d26',1.2+.7*(1-r),.30)
        # Very subtle longitudinal keratin grain; it follows the curved growth axis.
        for u in np.linspace(-.85,.87,12):
            a=float(rng.uniform(.05,.37)); b=float(rng.uniform(.63,.95))
            points=[]
            phase=float(rng.uniform(0,6.28))
            for t in np.linspace(a,b,90):
                wav=u+.008*np.sin(t*29+phase)+.003*np.sin(t*81)
                points.append(surface(t,float(np.clip(wav,-.99,.99))))
            line(points,'#ac91a3' if u<0 else '#1d1b24',float(rng.uniform(.65,1.2)),.075)
        # Restore a clear cartoon contour around the shaded material.
        path(shell,'none',INK,20,rough=.7)

    # Larger horns with naturally swept axes and real relief at each growth band.
    horn([(308,457),(120,366),(349,238),(224,80)],86,11)
    horn([(1242,430),(1396,336),(1152,205),(1300,116)],91,19)
    # Silver root tufts overlap the attachment points so horns grow from the head.
    path('M 220 512 C 232 455 272 409 333 384 Q 304 427 301 465 Q 340 433 376 426 C 326 473 311 516 284 555',HAIR,'none')
    path('M 220 512 Q 246 450 283 431 M 301 465 Q 334 441 357 438',stroke=DEEP,w=10)
    path('M 1179 450 Q 1210 399 1274 389 Q 1252 416 1255 446 Q 1293 427 1315 438 Q 1265 477 1255 509',HAIR,'none')
    path('M 1186 454 Q 1221 419 1251 417',stroke=DEEP,w=10)

    # A single small black ribbon keeps the side accessory secondary to the hair.
    path('M 1309 654 C 1266 598 1226 595 1206 613 Q 1194 660 1226 686 Q 1266 688 1309 665 Z',BLACK,w=14)
    path('M 1316 652 C 1365 601 1402 601 1416 625 Q 1424 668 1395 695 Q 1350 692 1316 667 Z',BLACK,w=14)
    path('M 1289 670 L 1253 765 L 1291 749 L 1313 776 L 1324 671 Z',BLACK,w=12)
    path('M 1321 674 L 1352 771 L 1372 747 L 1407 758 L 1342 662 Z',BLACK,w=12)
    path('M 1225 633 Q 1260 648 1290 652 M 1341 652 Q 1373 634 1397 631',stroke='#5d4d61',w=7)
    path('M 1291 637 Q 1301 615 1320 626 Q 1344 622 1347 645 Q 1363 660 1344 677 Q 1335 698 1314 687 Q 1290 697 1284 674 Q 1266 656 1291 637 Z','#56323f',INK,9)
    path('M 1298 651 Q 1309 634 1326 644 Q 1343 653 1329 669 Q 1316 681 1304 669 Q 1293 660 1309 653 Q 1318 650 1321 658',stroke='#ae637a',w=6)
    # Restrained hanging detail, mostly set against the pale outer hair.
    path('M 1330 690 Q 1342 725 1332 767 L 1336 815',stroke=INK,w=8)
    path('M 1330 690 Q 1342 725 1332 767 L 1336 815',stroke='#b3a0b4',w=4)
    ellipse(1337,826,9,12,'#ae9bac',INK,5)
    path('M 1337 840 L 1337 895 M 1319 861 L 1354 861',stroke=INK,w=12)
    path('M 1337 840 L 1337 895 M 1319 861 L 1354 861',stroke='#c7b5c3',w=5)

    output.mkdir(parents=True,exist_ok=True)
    png=output/'yueyue_sleepy_chibi.png'
    svg=output/'yueyue_sleepy_chibi.svg'
    fig.savefig(png,dpi=size/8,facecolor=fig.get_facecolor(),
                metadata={'Title':'Yueyue — close-up chibi portrait',
                          'Software':'Python / Matplotlib; original programmatic drawing'})
    fig.savefig(svg,facecolor=fig.get_facecolor(),
                metadata={'Title':'Yueyue — close-up chibi portrait',
                          'Description':'Python vector portrait with procedural curved horn geometry.'})
    plt.close(fig)
    print(png.resolve())
    print(svg.resolve())


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=FilePath,default=FilePath(__file__).resolve().parent)
    parser.add_argument('--size',type=int,default=2400)
    args=parser.parse_args()
    draw(args.output,args.size)
