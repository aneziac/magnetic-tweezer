import numpy as np
import taichi as ti
import matplotlib.pyplot as plt

ti.init(arch=ti.gpu)

maxN = 100
π = np.pi

im = ti.field(dtype=ti.i32, shape=(1000, 1000))
ps = ti.Vector.field(dtype=ti.f32, n=2, shape=(maxN))
Is = ti.field(dtype=ti.f32, shape=(maxN, 100))

@ti.kernel
def tiBI(n: ti.i32):
    for i, r in ti.ndrange(n, Nr):
        Is[i, r] = 0
        for θ in range(Nθ):
            x = ps[i][0] + Fr * r * ti.cos(θ * Fθ)
            y = ps[i][1] + Fr * r * ti.sin(θ * Fθ)
            x0 = int(x)
            y0 = int(y)
            x1 = x0 + 1
            y1 = y0 + 1
            xu = x1 - x
            xl = x - x0
            yu = y1 - y
            yl = y - y0
            Is[i, r] += (xu*yu*im[y0, x0] + xu*yl*im[y1, x0] + xl*yu*im[y0, x1] + xl*yl*im[y1, x1]) / Nθ

def profile(beads, img):
    global im
    if (im.shape[0] != img.shape[0] or im.shape[1] != img.shape[1]):
        im = ti.field(dtype=ti.i32, shape=(img.shape[0], img.shape[1]))
    im.from_numpy(img.astype(int))
    n = len(beads)
    for i in range(n):
        ps[i][0] = beads[i].x
        ps[i][1] = beads[i].y
    tiBI(n)
    res = Is.to_numpy()
    for i in range(n):
        beads[i].profile = res[i]

"""
Global params initialization
@param r: expected bead radius in pixel
@param nθ: sampling number in polar direction
@param nr: sampling number in radial direction
"""
def SetParams(r=40, nr=80, nθ=80):
    global R, L, freq, Nr, Nθ, Fr, Fθ, ps, Is
    R = r
    L = r * 2
    freq = np.fft.rfftfreq(L*2)
    R = r
    Nr = nr
    Nθ = nθ
    Fr = R/Nr
    Fθ = 2*π/Nθ
    ps = ti.Vector.field(dtype=ti.f32, n=2, shape=(maxN))
    Is = ti.field(dtype=ti.f32, shape=(maxN, Nr))

SetParams()

# shift from the center
def centerShift(array, it=2):
    normalized = 2 * array / np.max(array) - 1 # normalize
    fft = np.fft.rfft(np.append(normalized, np.zeros(L)))
    res = 0
    d = 0
    for loop in range(it):
        fft *= np.exp(2j*π*d*freq)
        co = np.fft.irfft(fft**2)[R-1:L+R-1]
        i = np.argmax(co[R-30:R+30]) + R-30
        p = np.polynomial.polynomial.polyfit(np.arange(i-2, i+3), co[i-2:i+3], 2)
        d = -p[1]/4/p[2] - R/2
        res += d
    return res

def tilde(I, rf, w):
    I = 2 * I / np.max(I) - 1 # normalize to [-1, 1]
    I = np.append(np.flip(I), I)
    Iq = np.fft.fft(I)
    q = np.fft.fftfreq(I.shape[-1])
    l = len(Iq)
    win = np.append(np.zeros(w[0]), np.hanning(w[1]-w[0]))
    win = np.append(win, np.zeros(l-w[1]))
    It = np.fft.ifft(Iq*win)
    return It[rf+(len(It)//2):len(It)]

"""
Calculate XY Position
@param beads: list of beads
@param img: 2d array of image data
@param it: iteration times
"""
def XY(beads, img, it=2):
    for b in beads:
        xl = int(b.x)
        yl = int(b.y)
        xline = np.sum(img[yl-2:yl+3, xl-R:xl+R], axis=0)
        yline = np.sum(img[yl-R:yl+R, xl-2:xl+3], axis=1)
        b.x = xl + centerShift(xline, it)
        b.y = yl + centerShift(yline, it)

"""
Calculate I and store
@param beads: list of beads
@param imgs: array of 2d array of image data
@param z: z position
"""
def Calibrate(beads, imgs, z):
    for b in beads:
        b.l = []
    for img in imgs:
        XY(beads, img)
        profile(beads, img)
        for b in beads:
            b.l.append(b.profile)
    for b in beads:
        b.Ic.append(np.average(b.l, axis=0))
        b.Zc.append(z)

"""
Finalize calibration by computing phase etc.
@param beads: list of beads
@param rf: forget radius
@param w: [a, b] window in Fourier space
"""
def ComputeCalibration(beads, rf=12, w=[5, 15]):
    for b in beads:
        b.rf = rf
        b.w = w
        b.Rc = [] # real part
        b.Φc = [] # phase angle
        b.Ac = [] # amplitude
        for I in b.Ic:
            It = tilde(I, rf, w)
            b.Rc.append(np.real(It))
            b.Φc.append(np.angle(It))
            b.Ac.append(np.abs(It))
        b.Φc = np.unwrap(b.Φc, axis=0)
        b.Φc = np.unwrap(b.Φc, axis=1)

"""
Calculate Z Position
@param beads: list of beads
@param img: 2d array of image data
"""
def Z(beads, img):
    profile(beads, img)
    for b in beads:
        It = tilde(b.profile, b.rf, b.w)
        Ri = np.real(It)
        Φi = np.unwrap(np.angle(It))
        Ai = np.abs(It)
        χ2 = np.sum((Ri-b.Rc)**2, axis=1)
        i = np.argmin(χ2)
        while Φi[5] - b.Φc[i][5] > 3:
            Φi = Φi - 2*π
        while Φi[5] - b.Φc[i][5] < -3:
            Φi = Φi + 2*π
        ΔΦ = np.average(Φi-b.Φc[i-3:i+4], axis=1, weights=Ai*b.Ac[i-3:i+4])
        p = np.polynomial.polynomial.polyfit(b.Zc[i-3:i+4], ΔΦ, 1)
        #plt.scatter(b.Zc, ΔΦ)
        b.z = -p[0]/p[1]

"""
Interface for beads
"""
class Bead:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0
        # self calibration
        self.Ic = [] # Intensity Profiles
        self.Zc = [] # Z values

    def __repr__(self):
        return f"Bead({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"Bead({self.x}, {self.y}, {self.z})"
