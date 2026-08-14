import matplotlib.pyplot as plt
import numpy as np
from scipy import constants
from matplotlib.widgets import RadioButtons

r_inf = constants.Rydberg
m_e = constants.m_e
m_p = constants.m_p
r_h = r_inf * (m_p / (m_e + m_p))


def Rydberg(n_lower, n_higher, Z):
    return (1 / n_lower**2 - 1 / n_higher**2) ** (-1) / (r_h * Z**2)


def calculate_photon_energy(wavelength_array):
    h = constants.h
    c = constants.c
    e = constants.e
    return (h * c / wavelength_array) / e


upper_limit = 51

wavelength_Lyman = Rydberg(1, np.arange(2, upper_limit), 1)
wavelength_Balmer = Rydberg(2, np.arange(3, upper_limit), 1)
wavelength_Paschen = Rydberg(3, np.arange(4, upper_limit), 1)
wavelength_Brackett = Rydberg(4, np.arange(5, upper_limit), 1)
wavelength_Pfund = Rydberg(5, np.arange(6, upper_limit), 1)

photon_energy_Lyman = calculate_photon_energy(wavelength_Lyman)
photon_energy_Balmer = calculate_photon_energy(wavelength_Balmer)
photon_energy_Paschen = calculate_photon_energy(wavelength_Paschen)
photon_energy_Brackett = calculate_photon_energy(wavelength_Brackett)
photon_energy_Pfund = calculate_photon_energy(wavelength_Pfund)

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.30)

ax.plot(
    wavelength_Lyman * 1e9,
    photon_energy_Lyman,
    'o-',
    label='Lyman',
    linewidth=1,
    markersize=4
)

ax.plot(
    wavelength_Balmer * 1e9,
    photon_energy_Balmer,
    'o-',
    label='Balmer',
    linewidth=1,
    markersize=4
)

ax.plot(
    wavelength_Paschen * 1e9,
    photon_energy_Paschen,
    'o-',
    label='Paschen',
    linewidth=1,
    markersize=4
)

ax.plot(
    wavelength_Brackett * 1e9,
    photon_energy_Brackett,
    'o-',
    label='Brackett',
    linewidth=1,
    markersize=4
)

ax.plot(
    wavelength_Pfund * 1e9,
    photon_energy_Pfund,
    'o-',
    label='Pfund',
    linewidth=1,
    markersize=4
)

ax.set_title("Bohr model of Hydrogenic atom with Z = 1", fontsize=14)
ax.set_xlabel("Wavelength (nm)", fontsize=12)
ax.set_ylabel("Photon Energy (eV)", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=11)

vlines = []

highlight, = ax.plot(
    [],
    [],
    'o',
    markersize=8,
    markerfacecolor='yellow',
    markeredgecolor='black',
    linestyle='None',
    visible=False
)

series_data = {
    "Lyman": (wavelength_Lyman * 1e9, photon_energy_Lyman),
    "Balmer": (wavelength_Balmer * 1e9, photon_energy_Balmer),
    "Paschen": (wavelength_Paschen * 1e9, photon_energy_Paschen),
    "Brackett": (wavelength_Brackett * 1e9, photon_energy_Brackett),
    "Pfund": (wavelength_Pfund * 1e9, photon_energy_Pfund),
}

radio_ax = plt.axes([0.05, 0.35, 0.18, 0.35])

radio = RadioButtons(
    radio_ax,
    ("None", "Lyman", "Balmer", "Paschen", "Brackett", "Pfund")
)

def update(label):

    global vlines

    for line in vlines:
        line.remove()

    vlines.clear()

    if label == "None":

        highlight.set_visible(False)

    else:

        x, y = series_data[label]

        highlight.set_data(x, y)
        highlight.set_visible(True)

        for xi in x:

            line = ax.axvline(
                x=xi,
                color='black',
                linestyle='--',
                linewidth=0.6,
                alpha=0.7
            )

            vlines.append(line)

    fig.canvas.draw_idle()

radio.on_clicked(update)

plt.show()
