#!/usr/bin/env python3
"""Render the portrait or one independent element as PNG and SVG."""
import argparse
from pathlib import Path
from yueyue.composition import ELEMENTS, compose


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--size", type=int, default=2400)
    parser.add_argument("--element", choices=ELEMENTS, default="portrait")
    args = parser.parse_args()
    if args.size <= 0:
        parser.error("--size must be a positive pixel count")
    canvas = compose(args.size, args.element)
    try:
        stem = "yueyue_sleepy_chibi" if args.element == "portrait" else args.element.replace("-", "_")
        for path in canvas.save(args.output, stem):
            print(path.resolve())
    finally:
        canvas.close()


if __name__ == "__main__":
    main()
