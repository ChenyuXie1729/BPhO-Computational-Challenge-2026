import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

h   = 6.62607015e-34
m_e = 9.10938356e-31
e   = 1.602176634e-19

r_tube = 65.0

d_values = {
    "d = 0.123 nm": 0.123e-9,
    "d = 0.213 nm": 0.213e-9,
}
colors = {"d = 0.123 nm": "tab:blue", "d = 0.213 nm": "tab:green"}


def wavelength(V):
    return h / np.sqrt(2 * m_e * e * V)


def bragg_angle(lam, d):
    return np.arcsin(np.clip(lam / (2 * d), -1, 1))


def ring_radius_mm(V, d):
    lam = wavelength(V)
    phi = bragg_angle(lam, d)
    return r_tube * np.sin(2 * phi)


fig = plt.figure(figsize=(12, 6))
fig.suptitle("Electron diffraction", fontsize=13, fontweight="bold")

ax_tube = fig.add_axes([0.06, 0.18, 0.40, 0.72])
ax_tube.set_aspect('equal')
ax_tube.set_xlim(-75, 75); ax_tube.set_ylim(-75, 75)
ax_tube.set_xticks([]); ax_tube.set_yticks([])
ax_tube.set_title("Diffraction tube")

ax_tube.add_patch(plt.Circle((0, 0), r_tube, fill=False, linewidth=2, color='black'))
ax_tube.add_patch(plt.Circle((0, 0), 1.2, color='red', zorder=5))

rings = {}
for label, d in d_values.items():
    circ = plt.Circle((0, 0), 10, fill=False, linewidth=2, color=colors[label], label=label)
    ax_tube.add_patch(circ)
    rings[label] = circ
ax_tube.legend(loc='upper right', fontsize=8)
info_text = ax_tube.text(0, -85, "", fontsize=9, ha='center', va='top')

ax_verify = fig.add_axes([0.56, 0.18, 0.40, 0.72])
ax_verify.set_xlabel(r'$1/\sqrt{V}$')
ax_verify.set_ylabel(r'$\sin\phi$')
ax_verify.grid(True, alpha=0.4)

V_range = np.linspace(1000, 5000, 200)
markers = {}
for label, d in d_values.items():
    lam = wavelength(V_range)
    phi = bragg_angle(lam, d)
    ax_verify.plot(1 / np.sqrt(V_range), np.sin(phi), '-', color=colors[label],
                    label=label, alpha=0.8)
    (pt,) = ax_verify.plot([], [], 'o', color=colors[label], markersize=9,
                            markeredgecolor='black')
    markers[label] = pt
ax_verify.legend(fontsize=8)

ax_slider = fig.add_axes([0.20, 0.05, 0.60, 0.04])
voltage_slider = Slider(ax_slider, "Voltage / kV", 1.0, 5.0, valinit=2.0, valstep=0.1)


def update(_):
    V = voltage_slider.val * 1000
    lam = wavelength(V)
    parts = []
    for label, d in d_values.items():
        phi = bragg_angle(lam, d)
        R = r_tube * np.sin(2 * phi)
        rings[label].set_radius(R)
        markers[label].set_data([1 / np.sqrt(V)], [np.sin(phi)])
        parts.append(f"{label}: R = {R:.1f} mm")
    info_text.set_text(f"V = {V/1000:.2f} kV   $\\lambda$ = {lam*1e12:.2f} pm\n" + "    ".join(parts))
    fig.canvas.draw_idle()


voltage_slider.on_changed(update)
update(None)

plt.show()