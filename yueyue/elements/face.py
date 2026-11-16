"""Eyes, eyebrows, blush and closed mouth, separate from skull geometry."""
from matplotlib.transforms import Affine2D
from ..palette import INK, LIGHT, RED, BLUSH


def draw(canvas):
    path = canvas.path
    ellipse = canvas.ellipse
    ellipse(454,1269,87,44,'#fbe0e4',angle=7)
    ellipse(1153,1268,83,45,'#fbe0e4',angle=-6)
    for x,y in [(418,1264),(455,1276),(492,1278),(1118,1279),(1155,1273),(1190,1262)]:
        path(f'M {x} {y-14} L {x+5} {y+13}',stroke=BLUSH,w=13)

    # Ovals with soft crimson centres and broad bright glints, as in the sample.
    saved_head=canvas.transform
    canvas.transform=Affine2D().translate(35,17)+saved_head
    path('M 435 1178 C 475 1141 554 1129 620 1146 C 665 1156 676 1191 650 1220 C 618 1258 531 1276 469 1258 C 431 1248 409 1207 435 1178 Z',INK,w=12)
    path('M 459 1189 C 500 1158 564 1154 612 1165 C 646 1172 655 1194 635 1212 C 601 1244 535 1254 486 1241 C 455 1233 438 1211 459 1189 Z',RED,'none')
    path('M 469 1220 Q 554 1241 640 1197 C 647 1218 609 1244 555 1249 Q 502 1257 477 1241 Z','#d58ba0','none')
    ellipse(550,1179,55,25,LIGHT,angle=-6)
    ellipse(602,1227,14,6,'#f5d0dc',angle=-8)
    canvas.transform=Affine2D().translate(-25,17)+saved_head
    path('M 1000 1145 C 1064 1125 1148 1139 1185 1176 C 1212 1203 1195 1233 1160 1250 C 1100 1277 1021 1265 982 1234 C 951 1209 961 1159 1000 1145 Z',INK,w=12)
    path('M 1008 1165 C 1061 1148 1128 1155 1161 1181 C 1183 1200 1168 1225 1142 1237 C 1095 1255 1035 1249 1004 1225 C 982 1208 983 1177 1008 1165 Z',RED,'none')
    path('M 1002 1208 Q 1082 1239 1170 1204 C 1172 1228 1129 1247 1089 1250 Q 1038 1249 1009 1230 Z','#d58ba0','none')
    ellipse(1070,1178,55,25,LIGHT,angle=5)
    ellipse(1137,1231,14,6,'#f5d0dc',angle=5)
    canvas.transform=Affine2D().translate(35,17)+saved_head
    path('M 427 1143 Q 510 1115 635 1126',stroke=INK,w=19)
    canvas.transform=Affine2D().translate(-25,17)+saved_head
    path('M 985 1127 Q 1091 1117 1201 1149',stroke=INK,w=19)
    canvas.transform=saved_head
    path('M 454 1060 Q 506 1036 563 1041 M 1056 1040 Q 1117 1037 1174 1058',stroke=INK,w=18)
    # Closed tiny mouth; there are no teeth.
    path('M 776 1335 Q 797 1349 821 1336',stroke=INK,w=7)


