"""
Interface for beads
@param rf: forget radius
@param w: window in Fourier space
"""


class Bead:
    def __init__(self, x, y, rf=10, w=[2, 40]):
        self.x = x
        self.y = y
        self.z = 0
        self.rf = rf
        self.w = w
        # self calibration
        self.Ic = []  # Intensity Profiles
        self.Zc = []  # Z values

    def __repr__(self):
        return f"Bead({self.x}, {self.y}, {self.z}, rf={self.rf}, w=[{self.w[0]}, {self.w[1]}])"
