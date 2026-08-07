from math import factorial, pi

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

rng = np.random.default_rng(0)


def assoc_legendre(l, m_abs, x):
    pmm = np.ones_like(x)
    if m_abs > 0:
        somx2 = np.sqrt((1.0 - x) * (1.0 + x))
        fact = 1.0
        for _ in range(m_abs):
            pmm = pmm * (-fact) * somx2
            fact += 2.0
    if l == m_abs:
        return pmm
    pmmp1 = x * (2 * m_abs + 1) * pmm
    if l == m_abs + 1:
        return pmmp1
    pll = pmmp1
    for ll in range(m_abs + 2, l + 1):
        pll = ((2 * ll - 1) * x * pmmp1 - (ll + m_abs - 1) * pmm) / (ll - m_abs)
        pmm, pmmp1 = pmmp1, pll
    return pll


def Ylm(l, m, theta, phi):
    m_abs = abs(m)
    x = np.cos(theta)
    P = assoc_legendre(l, m_abs, x)
    norm = np.sqrt((2 * l + 1) / (4 * pi) * factorial(l - m_abs) / factorial(l + m_abs))
    Y = norm * P * np.exp(1j * m_abs * phi)
    if m < 0:
        Y = ((-1) ** m_abs) * np.conjugate(Y)
    return Y


def real_orbital_angular(l, m, theta, phi):
    if m == 0:
        return Ylm(l, 0, theta, phi).real
    m_abs = abs(m)
    Yp = Ylm(l, m_abs, theta, phi)
    Yn = Ylm(l, -m_abs, theta, phi)
    if m > 0:
        return ((1 / np.sqrt(2)) * (Yn + ((-1) ** m_abs) * Yp)).real
    else:
        return ((1j / np.sqrt(2)) * (Yn - ((-1) ** m_abs) * Yp)).real


def gen_laguerre(k, alpha, x):
    if k == 0:
        return np.ones_like(x)
    Lkm1 = np.ones_like(x)
    Lk = 1.0 + alpha - x
    if k == 1:
        return Lk
    for kk in range(2, k + 1):
        Lkm2, Lkm1 = Lkm1, Lk
        Lk = ((2 * kk - 1 + alpha - x) * Lkm1 - (kk - 1 + alpha) * Lkm2) / kk
    return Lk

_trapz = getattr(np, "trapezoid", None) or np.trapz

def radial_wavefunction(n, l, r):
    rho = 2.0 * r / n
    poly = gen_laguerre(n - l - 1, 2 * l + 1, rho)
    R = np.exp(-rho / 2.0) * rho ** l * poly
    r_fine = np.linspace(1e-6, r_max_for(n), 4000)
    rho_f = 2.0 * r_fine / n
    R_fine = np.exp(-rho_f / 2.0) * rho_f ** l * gen_laguerre(n - l - 1, 2 * l + 1, rho_f)
    norm2 = _trapz((R_fine ** 2) * r_fine ** 2, r_fine)
    return R / np.sqrt(norm2)


def r_max_for(n):
    return max(8.0, 2.5 * n ** 2 + 6.0)

def probability_density(n, l, m, r, theta, phi):
    R = radial_wavefunction(n, l, r)
    Yr = real_orbital_angular(l, m, theta, phi)
    return (R ** 2) * (Yr ** 2)


fig = plt.figure(figsize=(12, 6.3))
fig.suptitle("Hydrogenic Orbitals:  |\u03c8$_{nlm}$|\u00b2", fontsize=14, fontweight="bold")

ax2d = fig.add_axes([0.06, 0.28, 0.40, 0.6])
ax2d.set_title("x-z plane slice")
ax2d.set_xlabel("x (a$_0$)")
ax2d.set_ylabel("z (a$_0$)")
ax2d.set_aspect("equal")

ax3d = fig.add_axes([0.53, 0.22, 0.44, 0.66], projection="3d")
ax3d.set_title("3D electron cloud (sampled)")

info_text = fig.text(0.5, 0.16, "", ha="center", fontsize=10)

state = {"n": 2, "l": 1, "m": 0}
mesh_holder = {"qm": None, "scatter": None}

ax_n = fig.add_axes([0.15, 0.10, 0.7, 0.03])
ax_l = fig.add_axes([0.15, 0.06, 0.7, 0.03])
ax_m = fig.add_axes([0.15, 0.02, 0.7, 0.03])

s_n = Slider(ax_n, "n", 1, 5, valinit=state["n"], valstep=1, color="tomato")
s_l = Slider(ax_l, "l", 0, 4, valinit=state["l"], valstep=1, color="steelblue")
s_m = Slider(ax_m, "m", -4, 4, valinit=state["m"], valstep=1, color="mediumseagreen")

_updating = {"flag": False}


def clamp_and_read():
    n = int(s_n.val)
    l = int(s_l.val)
    l = min(l, n - 1)
    l = max(l, 0)
    m = int(s_m.val)
    m = max(-l, min(l, m))
    _updating["flag"] = True
    s_l.set_val(l)
    s_m.set_val(m)
    _updating["flag"] = False
    return n, l, m


def redraw(_event=None):
    if _updating["flag"]:
        return
    n, l, m = clamp_and_read()
    state.update(n=n, l=l, m=m)

    rmax = r_max_for(n)

    N = 160
    xs = np.linspace(-rmax, rmax, N)
    ys_or_zs = np.linspace(-rmax, rmax, N)

    if m == 0:
        X, Z = np.meshgrid(xs, ys_or_zs)
        R = np.sqrt(X ** 2 + Z ** 2)
        R_safe = np.where(R < 1e-9, 1e-9, R)
        theta = np.arccos(np.clip(Z / R_safe, -1, 1))
        phi = np.where(X >= 0, 0.0, np.pi)
        plane_title, xlabel, ylabel = "x-z plane slice (y=0)", "x (a$_0$)", "z (a$_0$)"
        H, V = X, Z
    else:
        X, Y = np.meshgrid(xs, ys_or_zs)
        R = np.sqrt(X ** 2 + Y ** 2)
        R_safe = np.where(R < 1e-9, 1e-9, R)
        theta = np.full_like(R, np.pi / 2)
        phi = np.arctan2(Y, X)
        plane_title, xlabel, ylabel = "x-y plane slice (z=0)", "x (a$_0$)", "y (a$_0$)"
        H, V = X, Y

    dens = probability_density(n, l, m, R_safe, theta, phi)

    ax2d.cla()
    im = ax2d.pcolormesh(H, V, np.sqrt(dens), shading="auto", cmap="inferno")
    ax2d.set_title(plane_title)
    ax2d.set_xlabel(xlabel)
    ax2d.set_ylabel(ylabel)
    ax2d.set_aspect("equal")

    n_try = 60000
    pts = rng.uniform(-rmax, rmax, size=(n_try, 3))
    Rp = np.linalg.norm(pts, axis=1)
    Rp_safe = np.where(Rp < 1e-9, 1e-9, Rp)
    th = np.arccos(np.clip(pts[:, 2] / Rp_safe, -1, 1))
    ph = np.arctan2(pts[:, 1], pts[:, 0]) % (2 * np.pi)
    d = probability_density(n, l, m, Rp_safe, th, ph)
    d_max = d.max() if d.max() > 0 else 1.0
    keep = rng.uniform(0, 1, size=n_try) < (d / d_max)
    pts_keep = pts[keep][:3000]
    d_keep = d[keep][:3000]

    ax3d.cla()
    ax3d.scatter(pts_keep[:, 0], pts_keep[:, 1], pts_keep[:, 2],
                 c=d_keep, cmap="inferno", s=4, alpha=0.6)
    ax3d.set_xlim(-rmax, rmax)
    ax3d.set_ylim(-rmax, rmax)
    ax3d.set_zlim(-rmax, rmax)
    ax3d.set_xlabel("x")
    ax3d.set_ylabel("y")
    ax3d.set_zlabel("z")
    ax3d.set_title("3D electron cloud (sampled)")

    E_n = -13.6 / n ** 2
    info_text.set_text(f"n={n}, l={l}, m={m}     E$_n$ = {E_n:.2f} eV     "
                        f"(color/brightness \u221d probability density)")

    fig.canvas.draw_idle()


s_n.on_changed(redraw)
s_l.on_changed(redraw)
s_m.on_changed(redraw)

redraw()
plt.show()