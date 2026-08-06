import numpy as np
import matplotlib.pyplot as plt
from scipy import constants

def fractional_compton_shift(angle_degrees, energy_keV):
    """
    Calculates Delta Lambda / Lambda_0 for a given photon energy in keV.
    """
    
    energy_joules = energy_keV * 1000 * constants.e
    
    
    lambda_zero = (constants.h * constants.c) / energy_joules
    
    
    angle_radians = np.radians(angle_degrees)
    compton_wavelength = constants.h / (constants.m_e * constants.c)
    delta_lambda = (1 - np.cos(angle_radians)) * compton_wavelength
    
    return delta_lambda / lambda_zero


degrees = np.linspace(0, 180, 500)
energies = [50, 100, 200, 500, 1000]  
colors = ['purple', 'blue', 'green', 'orange', 'red']


plt.figure(figsize=(9, 6))

for energy, color in zip(energies, colors):
    fractional_shift = fractional_compton_shift(degrees, energy)
    plt.plot(degrees, fractional_shift, color=color, linewidth=1.2, label=f'{energy} keV')


plt.title(r'Fractional Wavelength Shift ($\frac{\Delta\lambda}{\lambda_0}$) vs. Scattering Angle')
plt.xlabel('Scattering Angle (Degrees°)')
plt.ylabel(r'Fractional Shift ($\frac{\Delta\lambda}{\lambda_0}$)')

plt.xlim(0, 180)
plt.xticks(np.arange(0, 181, 30))  
plt.grid(True, alpha=0.3)
plt.legend(title="Photon Energy")

plt.show()

def electron_recoil_velocity(angle_degrees, energy_keV):
    """
    Calculates the recoil velocity of the electron as a fraction of c (v/c).
    """
    h = constants.h
    c = constants.c
    m_e = constants.m_e
    
    E_photon_initial = energy_keV * 1000 * constants.e
    wavelength_initial = (h * c) / E_photon_initial
    

    angle_radians = np.radians(angle_degrees)
    compton_wavelength = h / (m_e * c)
    wavelength_final = wavelength_initial + (1 - np.cos(angle_radians)) * compton_wavelength
    
    
    E_rest = m_e * c**2
    delta_E_photon = (h * c / wavelength_initial) - (h * c / wavelength_final)
    
    
    E_total_electron = E_rest + delta_E_photon
    
    
    v_over_c = np.sqrt(1 - (E_rest / E_total_electron)**2)
    return v_over_c


degrees = np.linspace(0, 180, 500)
energies = [50, 100, 200, 500, 1000]  # in keV
colors = ['purple', 'blue', 'green', 'orange', 'red']


plt.figure(figsize=(9, 6))

for energy, color in zip(energies, colors):
    v_fraction = electron_recoil_velocity(degrees, energy)
    plt.plot(degrees, v_fraction, color=color, linewidth=1.2, label=f'{energy} keV')


plt.title('Electron Recoil Velocity ($v/c$) vs. Photon Scattering Angle')
plt.xlabel('Scattering Angle (Degrees°)')
plt.ylabel('Electron Velocity ($v/c$)')

plt.xlim(0, 180)
plt.ylim(0, 1.0)
plt.xticks(np.arange(0, 181, 30))
plt.grid(True, alpha=0.3)
plt.legend(title="Incoming Photon Energy")

plt.show()

def electron_recoil_angle(photon_angle_degrees, energy_keV):
    """
    Calculates the electron recoil angle (phi) in degrees 
    given the photon scattering angle (theta) in degrees.
    """
    h = constants.h
    c = constants.c
    m_e = constants.m_e
    
    
    theta_rad = np.radians(photon_angle_degrees)
    
    
    E_photon_initial = energy_keV * 1000 * constants.e
    lambda_zero = (h * c) / E_photon_initial
    
    
    compton_factor = h / (m_e * c * lambda_zero)
    
    
    numerator = np.sin(theta_rad)
    denominator = (1 + compton_factor) * (1 - np.cos(theta_rad)) + 1e-15
    
    tan_phi = numerator / denominator
    
    
    phi_rad = np.arctan(tan_phi)
    phi_deg = np.degrees(phi_rad)
    
    
    return np.where(phi_deg < 0, phi_deg + 180, phi_deg)


photon_degrees = np.linspace(0.1, 180, 500)
energies = [50, 100, 200, 500, 1000] # in keV
colors = ['purple', 'blue', 'green', 'orange', 'red']


plt.figure(figsize=(9, 6))

for energy, color in zip(energies, colors):
    recoil_degrees = electron_recoil_angle(photon_degrees, energy)
    plt.plot(photon_degrees, recoil_degrees, color=color, linewidth=1.2, label=f'{energy} keV')


plt.title('Electron Recoil Angle ($\phi$) vs. Photon Scattering Angle ($\theta$)')
plt.xlabel('Photon Scattering Angle $\theta$ (Degrees°)')
plt.ylabel('Electron Recoil Angle $\phi$ (Degrees°)')

plt.xlim(0, 180)
plt.ylim(0, 90)
plt.xticks(np.arange(0, 181, 30))
plt.yticks(np.arange(0, 91, 15))
plt.grid(True, alpha=0.3)
plt.legend(title="Incoming Photon Energy")

plt.show()


