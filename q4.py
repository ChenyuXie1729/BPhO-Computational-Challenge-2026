import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.animation import FuncAnimation

h = 4.135667696e-15
c = 2.998e8

METALS = {
    "Cesium (Cs)":   2.10,
    "Sodium (Na)":   2.28,
    "Calcium (Ca)":  2.90,
    "Zinc (Zn)":     4.30,
    "Copper (Cu)":   4.70,
    "Platinum (Pt)": 6.35,
}
METAL_NAMES = list(METALS.keys())

WL_MIN, WL_MAX = 200, 800
V_MIN, V_MAX = -4, 4

PLATE_X = 0.15
COLL_X = 0.85
GAP = COLL_X - PLATE_X


def wavelength_to_rgb(wl_nm):
    wl = wl_nm
    if wl < 380:
        return (0.55, 0.0, 0.85)
    if wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    elif wl <= 780:
        r, g, b = 1.0, 0.0, 0.0
    else:
        return (0.3, 0.0, 0.0)
    return (np.clip(r, 0, 1), np.clip(g, 0, 1), np.clip(b, 0, 1))


def freq_from_wl(wl_nm):
    return c / (wl_nm * 1e-9)


def photon_energy_eV(wl_nm):
    return h * freq_from_wl(wl_nm)


def stopping_voltage(wl_nm, work_fn):
    ke = photon_energy_eV(wl_nm) - work_fn
    return max(ke, 0.0)

plt.rcParams["toolbar"] = "None"
fig = plt.figure(figsize=(12, 6.2))
fig.suptitle("Photoelectric effect simulator", fontsize=14, fontweight="bold")

ax_sim = fig.add_axes([0.05, 0.30, 0.40, 0.58])
ax_sim.set_xlim(0, 1)
ax_sim.set_ylim(0, 1)
ax_sim.set_xticks([])
ax_sim.set_yticks([])
ax_sim.set_facecolor("#0b0b1a")

ax_plot = fig.add_axes([0.56, 0.30, 0.40, 0.58])
ax_plot.set_xlabel("Frequency  / x10$^{14}$ Hz")
ax_plot.set_ylabel("Stopping voltage  V$_{stop}$  / V")
ax_plot.grid(alpha=0.3)

ax_sim.add_patch(plt.Rectangle((PLATE_X - 0.02, 0.05), 0.02, 0.9, color="#888899"))
ax_sim.add_patch(plt.Rectangle((COLL_X, 0.05), 0.02, 0.9, color="#5566aa"))
light_src = ax_sim.scatter([0.02], [0.5], s=250, marker=">", color="yellow")

info_text = ax_sim.text(0.5, 0.03, "", color="white", fontsize=9, ha="center", va="bottom",
                         transform=ax_sim.transAxes)
current_text = ax_sim.text(0.98, 0.5, "", color="lime", fontsize=10, ha="right", va="center",
                            transform=ax_sim.transAxes, fontweight="bold")

photon_scat = ax_sim.scatter([], [], s=25, color="yellow")
electron_scat = ax_sim.scatter([], [], s=18, color="cyan")

f_vals_nm = np.linspace(WL_MIN, WL_MAX, 400)
f_vals = freq_from_wl(f_vals_nm) / 1e14
ax_plot.set_xlim(f_vals.min(), f_vals.max())

metal_lines = {}
for name, w in METALS.items():
    vstop = np.array([stopping_voltage(wl, w) for wl in f_vals_nm])
    (line,) = ax_plot.plot(f_vals, vstop, lw=1.2, alpha=0.35, color="gray")
    metal_lines[name] = line

highlight_line, = ax_plot.plot([], [], lw=2.5, color="orange", label="selected metal")
current_pt, = ax_plot.plot([], [], "o", color="red", markersize=8)
ax_plot.legend(loc="upper left", fontsize=8)

ax_wl = fig.add_axes([0.20, 0.16, 0.30, 0.03])
s_wl = Slider(ax_wl, "Wavelength / nm", WL_MIN, WL_MAX, valinit=500, color="orange")

ax_v = fig.add_axes([0.20, 0.10, 0.30, 0.03])
s_v = Slider(ax_v, "Plate Voltage / V", V_MIN, V_MAX, valinit=0.0, color="steelblue")

ax_radio = fig.add_axes([0.56, 0.02, 0.40, 0.16])
ax_radio.set_title("Metal", fontsize=9)
radio = RadioButtons(ax_radio, METAL_NAMES, active=4)

state = {"metal": METAL_NAMES[4], "wl": 500.0, "V": 0.0}
photons = []
electrons = []
rng = np.random.default_rng(0)


def spawn_photon():
    y0 = 0.5 + rng.uniform(-0.03, 0.03)
    photons.append([0.03, y0, 0.045, 0.0])


def update_highlight():
    w = METALS[state["metal"]]
    vstop = np.array([stopping_voltage(wl, w) for wl in f_vals_nm])
    highlight_line.set_data(f_vals, vstop)
    f_now = freq_from_wl(state["wl"]) / 1e14
    v_now = stopping_voltage(state["wl"], w)
    current_pt.set_data([f_now], [v_now])
    ymax = max(4, np.nanmax(vstop) * 1.1)
    ax_plot.set_ylim(0, ymax)


def on_wl(val):
    state["wl"] = val
    update_highlight()


def on_v(val):
    state["V"] = val


def on_metal(label):
    state["metal"] = label
    update_highlight()


s_wl.on_changed(on_wl)
s_v.on_changed(on_v)
radio.on_clicked(on_metal)
update_highlight()

frame_count = {"n": 0}


def animate(_):
    frame_count["n"] += 1
    color = wavelength_to_rgb(state["wl"])
    light_src.set_color(color)

    if frame_count["n"] % 4 == 0:
        spawn_photon()

    W = METALS[state["metal"]]
    E_photon = photon_energy_eV(state["wl"])
    KE_max = max(E_photon - W, 0.0)
    V = state["V"]

    new_photons = []
    for p in photons:
        p[0] += 0.045
        if p[0] < PLATE_X:
            new_photons.append(p)
        else:
            if KE_max > 0:
                v0 = 0.05 * np.sqrt(KE_max)
                electrons.append([PLATE_X, p[1], v0, 0])
    photons[:] = new_photons

    a = 0.02 * V
    reached = 0
    new_electrons = []
    for e_ in electrons:
        x, y, v0, t = e_
        t += 1
        v = v0 - a * t * 0.05
        x_new = x + max(v, 0) if v > 0 else x
        if v <= 0:
            continue
        e_[0] = x_new
        e_[3] = t
        if e_[0] >= COLL_X:
            reached += 1
        else:
            new_electrons.append(e_)
    electrons[:] = new_electrons

    if photons:
        photon_scat.set_offsets(np.array([[p[0], p[1]] for p in photons]))
    else:
        photon_scat.set_offsets(np.empty((0, 2)))
    photon_scat.set_color([color] * max(len(photons), 1))

    if electrons:
        electron_scat.set_offsets(np.array([[e_[0], e_[1]] for e_ in electrons]))
    else:
        electron_scat.set_offsets(np.empty((0, 2)))

    status = "CURRENT FLOWS" if (KE_max > 0 and (V <= 0 or KE_max > V)) else "no current"
    current_text.set_text(status)
    current_text.set_color("lime" if status == "CURRENT FLOWS" else "red")

    info_text.set_text(
        f"$\\lambda$={state['wl']:.0f} nm   E$_{{photon}}$={E_photon:.2f} eV   "
        f"W={W:.2f} eV   KE$_{{max}}$={KE_max:.2f} eV   V$_{{stop}}$={KE_max:.2f} V"
    )

    return photon_scat, electron_scat, current_text, info_text, light_src


ani = FuncAnimation(fig, animate, interval=40, blit=False, cache_frame_data=False)

plt.show()
