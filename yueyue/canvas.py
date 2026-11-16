"""The small Matplotlib drawing surface used by all visual elements."""
from contextlib import contextmanager
from pathlib import Path as FilePath
import re

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Ellipse

from .palette import INK

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


class Canvas:
    def __init__(self, size, transform, transparent=False):
        self.fig = plt.figure(figsize=(8, 8), dpi=size/8,
                              facecolor="none" if transparent else "#fffefd")
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set(xlim=(0,1600), ylim=(1600,0), aspect="equal")
        self.ax.axis("off")
        self.transform = transform
        self.layer = 0
        self.size = size

    @contextmanager
    def transformed(self, transform):
        previous = self.transform
        self.transform = transform
        try:
            yield
        finally:
            self.transform = previous

    def path(self, data, fill="none", stroke=INK, w=17, rough=.9, alpha=1):
        self.layer += 1
        shape = parse_path(data) if isinstance(data, str) else data
        patch = PathPatch(shape, facecolor=fill, edgecolor=stroke,
                          linewidth=w*.36, capstyle="round", joinstyle="round",
                          transform=self.transform+self.ax.transData,
                          zorder=self.layer, alpha=alpha)
        if rough:
            patch.set_sketch_params(scale=rough, length=105, randomness=1.7)
        self.ax.add_patch(patch)
        return patch

    def ellipse(self, x, y, rx, ry, fill, stroke="none", w=10, angle=0):
        self.layer += 1
        self.ax.add_patch(Ellipse((x,y), rx*2, ry*2, angle=angle,
                                 facecolor=fill, edgecolor=stroke,
                                 linewidth=w*.36,
                                 transform=self.transform+self.ax.transData,
                                 zorder=self.layer))

    def line(self, points, color, width, alpha=1):
        points = np.asarray(points)
        return self.path(Path(points, [Path.MOVETO]+[Path.LINETO]*(len(points)-1)),
                         stroke=color, w=width, rough=0, alpha=alpha)

    def save(self, output, stem):
        output = FilePath(output)
        output.mkdir(parents=True, exist_ok=True)
        paths = [output / f"{stem}.png", output / f"{stem}.svg"]
        self.fig.savefig(paths[0], dpi=self.size/8,
                         facecolor=self.fig.get_facecolor(),
                         metadata={"Title": "Yueyue — Python vector drawing"})
        self.fig.savefig(paths[1], facecolor=self.fig.get_facecolor(),
                         metadata={"Title": "Yueyue — Python vector drawing"})
        return paths

    def close(self):
        plt.close(self.fig)
