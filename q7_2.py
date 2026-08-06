import numpy as np
import matplotlib.pyplot as plt
from scipy import constants


def Energy(quantum_number, box_width):
    return (constants.hbar * np.pi * quantum_number)**2 / (2 * constants.m_e * box_width**2)


def Probability(position, quantum_number, box_width):
    inside_box = (position >= 0) & (position <= box_width)
    prob = (2 / box_width) * np.sin(quantum_number * np.pi * position / box_width)**2
    return np.where(inside_box, prob, 0.0)


box_width = 3000e-9  # 3000 nm box
position = np.linspace(0, box_width, 1000)
position_nm = position * 1e9  


quantum_numbers_axis = np.arange(1, 4) 


E1 = Energy(1, box_width) / constants.e
E2 = Energy(2, box_width) / constants.e
E3 = Energy(3, box_width) / constants.e
all_energies = np.array([E1, E2, E3])


prob_n1 = Probability(position, quantum_number=1, box_width=box_width)
prob_n2 = Probability(position, quantum_number=2, box_width=box_width)
prob_n3 = Probability(position, quantum_number=3, box_width=box_width)


scale = 0.1  


# Energy vs. Quantum Number 

from scipy.interpolate import make_interp_spline

plt.figure(figsize=(8, 5))

qn_dense = np.linspace(quantum_numbers_axis.min(), quantum_numbers_axis.max(), 300)
spline = make_interp_spline(quantum_numbers_axis, all_energies, k=2)
energies_smooth = spline(qn_dense)


plt.plot(qn_dense, energies_smooth, linestyle='--', color='red', linewidth=0.7, label='Energy Trend')


plt.scatter(quantum_numbers_axis, all_energies, color='red', zorder=5, label='Quantum States')

plt.title('Energy Levels against Quantum Number')
plt.xlabel('Quantum Number /$n$')
plt.ylabel('Energy /$eV$')
plt.xticks(quantum_numbers_axis)  # Ensures only valid integer states (1, 2, 3) show on x-axis
plt.grid(True, alpha=0.2)
plt.legend(loc='upper left')
plt.show()

#probablity distribution
plt.figure(figsize=(8, 6))

plt.plot(position_nm, E1 + prob_n1 * scale, label=f'n = 1 (E = {E1:.3e} eV)', color='red', linewidth=1.5)
plt.plot(position_nm, E2 + prob_n2 * scale, label=f'n = 2 (E = {E2:.3e} eV)', color='blue', linewidth=1.5)
plt.plot(position_nm, E3 + prob_n3 * scale, label=f'n = 3 (E = {E3:.3e} eV)', color='green', linewidth=1.5)

plt.xlim(0, box_width * 1e9)

plt.title('Probability Distributions Stacked on Energy Levels')
plt.xlabel('Position /$nm$')
plt.ylabel('Energy /$eV$')
plt.grid(True, alpha=0.2)
plt.legend(loc='upper right')
plt.show()
