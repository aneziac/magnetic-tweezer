from math import sqrt, cos, floor, pi as π
import random

def Generate(X, Y, Z, λ, img):
  L = img.shape[0]
  for x in range(L):
    for y in range(L):
      r = sqrt((x-X)**2 + (y-Y)**2 + Z**2)
      n = (r-Z)/λ
      ϕ = 2*π*(n - floor(n) - 0.5)
      img[y][x] = cos(ϕ/2) * Z**2 / (r**4)