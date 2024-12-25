import numpy as np
import time
import matplotlib.pyplot as plt
import magnetic_tweezer.gpu_tracker as gpu_tracker
import magnetic_tweezer.cpu_tracker as cpu_tracker
from math import sqrt, cos, floor, pi as np.pi


def Generate(X, Y, Z, λ, img):
    L = 100
    for x in range(X - L, X + L):
        for y in range(Y - L, Y + L):
            r = sqrt((x - X) ** 2 + (y - Y) ** 2 + Z**2)
            n = (r - Z) / λ
            ϕ = 2 * np.pi * (n - floor(n) - 0.5)
            img[y][x] = 5e5 * cos(ϕ / 2) * Z**2 / (r**4)
            # img[y][x] = floor(5e5 * cos(ϕ/2) * Z**2 / (r**4) * random.uniform(1, 1.1))


shape = (700, 756)
imgc = []
for i in range(20):
    img = np.ndarray(shape)
    Generate(50, 50, 50 + i, 4, img)
    imgc.append(img)
img = np.ndarray(shape)
Generate(50, 50, 60, 4, img)

maxn = 20
loopRange = range(1, maxn)

if True:
    ts = []
    for loop in loopRange:
        beads = []
        for i in range(loop):
            beads.append(gpu_tracker.Bead(50, 50))

        gpu_tracker.XY(beads, [img])

        for i in range(20):
            gpu_tracker.Calibrate(beads, [imgc[i]], i)

        gpu_tracker.ComputeCalibration(beads)
        print(loop, beads[0])

        start = time.time()
        for i in range(100):
            gpu_tracker.XYZ(beads, [img])
        ts.append(time.time() - start)

    print(ts)
    plt.plot(loopRange, np.array(ts), marker="o", label="Taichi")
    print(np.polynomial.polynomial.polyfit(loopRange[1:], ts[1:], 1))

if True:
    ts = []
    for loop in loopRange:
        beads = []
        for i in range(loop):
            beads.append(cpu_tracker.Bead(50, 50))

        cpu_tracker.XY(beads, [img])

        for i in range(20):
            cpu_tracker.Calibrate(beads, [imgc[i]], i)

        cpu_tracker.ComputeCalibration(beads)
        cpu_tracker.XYZ(beads, [img])
        print(loop, beads[0])

        start = time.time()
        for i in range(100):
            cpu_tracker.XYZ(beads, [img])
        ts.append(time.time() - start)

    print(ts)
    plt.plot(loopRange, np.array(ts), marker="o", label="Numpy")
    print(np.polynomial.polynomial.polyfit(loopRange[1:], ts[1:], 1))

plt.title("Time to run 100 frames")
plt.ylabel("Time(s)")
plt.xlabel("Bead Number")
plt.grid()
plt.legend()
plt.show()
