import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import constants


def einstein_molar_heat_capacity(T, Theta_E):

    if np.any(T <= 0):
        raise ValueError("Temperature must be strictly greater than 0 Kelvin.")
        
    x = Theta_E / T
    Cv = np.zeros_like(x)
    
    # Prevent numerical overflow for temperatures near absolute zero (where x > ~700)
    overflow_limit = 700.0
    low_temp_mask = x > overflow_limit
    normal_mask = ~low_temp_mask
    
    #Standard Einstein formula calculation
    Cv[normal_mask] = 3 * constants.R * (x[normal_mask]**2) * (np.exp(x[normal_mask]) / (np.exp(x[normal_mask]) - 1)**2)
    
    # *Overflow-safe approximation for near-absolute-zero environments
    Cv[low_temp_mask] = 3 * constants.R * (x[low_temp_mask]**2) * np.exp(-x[low_temp_mask])

    return float(Cv) if Cv.ndim == 0 else Cv

T = np.linspace(1, 1000, 500)
Cv_gold = einstein_molar_heat_capacity(T, Theta_E = 162.0 )
Cv_copper = einstein_molar_heat_capacity(T, Theta_E = 240.0 )
Cv_iron = einstein_molar_heat_capacity(T, Theta_E = 310.0 )


plt.plot(T , Cv_gold, label='Gold', color='red', linewidth=1)
plt.plot(T , Cv_copper, label='Copper', color='blue', linewidth=1)
plt.plot(T , Cv_iron, label='Iron', color='green', linewidth=1)


plt.title(' Molar heat capacity of solids against temperature for gold, copper, iron')
plt.xlabel(r'Temperature /$K$')
plt.ylabel(r'Molar heat capacity /$Jmol^{-1}K^{-1}$')
plt.grid(True)
plt.legend()



plt.show()


