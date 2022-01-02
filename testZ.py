import numpy as np
import time
import QI
import Z
import simulate
import matplotlib.pyplot as plt
from math import pi
from utils import BilinearInterpolate, Gaussian

img = np.ndarray((100, 100))
x = 50
y = 50

N = 80
Nθ = 80
Nr = 80
xs, ys = QI.SamplePoints(N, Nθ, Nr)

Rc = [] # real part
Φc = [] # phase angle
Ac = [] # amplitude

for δ in np.arange(0, 10, 1):
  simulate.Generate(50, 50, 100+δ, 4, img)
  I = BilinearInterpolate(img, xs+x, ys+y)
  I = I.reshape((Nθ, Nr))
  It = Z.Tilde(QI.Profile(I))
  Rc.append(np.real(It))
  Φc.append(np.unwrap(np.angle(It)))
  Ac.append(np.abs(It))

for δ in np.arange(0, 3, 0.6):
  simulate.Generate(50, 50, 100+5+δ, 4, img)
  I = BilinearInterpolate(img, xs+x, ys+y)
  I = I.reshape((Nθ, Nr))
  It = Z.Tilde(QI.Profile(I))
  Ri = np.real(It)
  Φi = np.unwrap(np.angle(It))
  Ai = np.abs(It)
  χ2 = np.sum((Ri-Rc)**2, axis=1)
  ΔΦ = np.average(Φi-Φc, axis=1, weights=Ai*Ac)
  plt.plot(np.arange(0, 10, 1), ΔΦ, label=(5+δ), marker="o")
  plt.plot(np.arange(0, 10, 1), np.zeros(10))

plt.grid()
plt.legend()
plt.xlabel('Z Position of Calibration Point')
plt.ylabel('Unwrapped Phase Deviation w.r.t. Calibration')
plt.title('Z Position w/ Simulation')
plt.show()
