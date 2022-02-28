import numpy as np
from scipy import signal
import cv2 as cv
import matplotlib.pyplot as plt

# Normalize to [-1, 1]
def NormalizeArray(array):
	return array/(np.max(array)/2) - 1

def Gaussian(x, μ, σ):
	return np.exp(-np.power(x-μ, 2.) / (2 * np.power(σ, 2.)))

def CropImage(img, x, y, L):
	xi = int(x)
	yi = int(y)
	r = int(L/2)
	return img[yi-r:yi+r, xi-r:xi+r]

# shift from the center
def SymmetryCenter(array):
	l = len(array)
	c = int(l/2)
	normalized = NormalizeArray(array)
	co = signal.correlate(np.flip(normalized), normalized, mode='same')
	maxi = np.argmax(co[c-20:c+20]) + c - 20
	p = np.polynomial.polynomial.polyfit(range(maxi-2, maxi+3, 1), co[maxi-2:maxi+3], 2)
	return p[1]/(4*p[2])+c/2

# Cannot deal with boundary, avoid boundary
def BilinearInterpolate(im, x, y):
	x0 = np.floor(x).astype(int)
	x1 = x0 + 1
	y0 = np.floor(y).astype(int)
	y1 = y0 + 1

	Ia = im[y0, x0]
	Ib = im[y1, x0]
	Ic = im[y0, x1]
	Id = im[y1, x1]

	wa = (x1-x) * (y1-y)
	wb = (x1-x) * (y-y0)
	wc = (x-x0) * (y1-y)
	wd = (x-x0) * (y-y0)

	return wa*Ia + wb*Ib + wc*Ic + wd*Id

def HoughCircles(image, minRadius, maxRadius):
	circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=minRadius, maxRadius=maxRadius)
	if (circles is None):
		return []
	return circles[0]