import matplotlib.pyplot as plt
import numpy as np
from scipy import constants


r_inf = constants.Rydberg
m_e = constants.m_e
m_p = constants.m_p
r_h = r_inf * (m_p / (m_e + m_p))


def Rydberg(n_lower, n_higher, Z):
    return (1/(n_lower)**2 - 1/(n_higher)**2)**(-1) / (r_h * Z**2)


def calculate_photon_energy(wavelength_array):
    h = constants.h
    c = constants.c
    e = constants.e  # Elementary charge to convert Joules -> eV
    return (h * c / wavelength_array) / e


upper_limit = 51
wavelength_Lyman    = Rydberg(n_lower=1, n_higher=np.arange(2, upper_limit), Z=1)
wavelength_Balmer   = Rydberg(n_lower=2, n_higher=np.arange(3, upper_limit), Z=1)
wavelength_Paschen  = Rydberg(n_lower=3, n_higher=np.arange(4, upper_limit), Z=1)
wavelength_Brackett = Rydberg(n_lower=4, n_higher=np.arange(5, upper_limit), Z=1)
wavelength_Pfund    = Rydberg(n_lower=5, n_higher=np.arange(6, upper_limit), Z=1)


photon_energy_Lyman    = calculate_photon_energy(wavelength_Lyman)
photon_energy_Balmer   = calculate_photon_energy(wavelength_Balmer)
photon_energy_Paschen  = calculate_photon_energy(wavelength_Paschen)
photon_energy_Brackett = calculate_photon_energy(wavelength_Brackett)
photon_energy_Pfund    = calculate_photon_energy(wavelength_Pfund)


plt.figure(figsize=(10, 6))
plt.plot(wavelength_Lyman * 1e9, photon_energy_Lyman, 'o-', label='Lyman', linewidth=1, markersize=4)
plt.plot(wavelength_Balmer * 1e9, photon_energy_Balmer, 'o-', label='Balmer', linewidth=1, markersize=4)
plt.plot(wavelength_Paschen * 1e9, photon_energy_Paschen, 'o-', label='Paschen', linewidth=1, markersize=4)
plt.plot(wavelength_Brackett * 1e9, photon_energy_Brackett, 'o-', label='Brackett', linewidth=1, markersize=4)
plt.plot(wavelength_Pfund * 1e9, photon_energy_Pfund, 'o-', label='Pfund', linewidth=1, markersize=4)


plt.title("Bohr model of Hydrogenic atom with Z=1", fontsize=14)
plt.xlabel("Wavelength /$nm$", fontsize=12)
plt.ylabel("Photon Energy /$eV$", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)
plt.show()
