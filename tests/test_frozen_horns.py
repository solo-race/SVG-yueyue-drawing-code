"""Visual freeze checks, recorded from original commit 0f58aaf.

The two 512 x 512 transparent renders were extracted independently from the
original script before refactoring. Invisible RGB is normalized to zero.
Use requirements.txt; do not regenerate these expectations to hide a change.
"""
import hashlib
import unittest
import numpy as np
from yueyue.composition import compose

EXPECTED = {'left': '8af6157dccd90bbe3a803e90b2bdd89f81a6b960bf5324ea26abcea5806abb76', 'right': '3c7ca029bf6428e54fd2f3e9dc4218c3344e2771ae1c371169d5a7eb5fc1ff9a'}


class FrozenHornTests(unittest.TestCase):
    def check_horn(self, side):
        canvas = compose(size=512, element="horn-"+side)
        try:
            canvas.fig.canvas.draw()
            pixels = np.asarray(canvas.fig.canvas.buffer_rgba()).copy()
            pixels[pixels[:, :, 3] == 0] = 0
            actual = hashlib.sha256(pixels.tobytes()).hexdigest()
            self.assertEqual(actual, EXPECTED[side],
                             f"The {side} horn changed. Keep it frozen unless the user unfreezes it.")
        finally:
            canvas.close()

    def test_left_horn_unchanged(self):
        self.check_horn("left")

    def test_right_horn_unchanged(self):
        self.check_horn("right")


if __name__ == "__main__":
    unittest.main()
