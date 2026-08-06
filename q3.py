import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import constants

def Plancks_law(wavelength, temperature):
    return ((2*constants.h*constants.c**2)/(wavelength**5))*1/(math.e**(constants.h*constants.c/(wavelength*constants.k*temperature))-1)
  
wavelength = np.linspace(100e-9, 3000e-9, 500)
irradiance3000 = Plancks_law(wavelength, temperature=3000)
irradiance4000 = Plancks_law(wavelength, temperature=4000)
irradiance5000 = Plancks_law(wavelength, temperature=5000)


plt.plot(wavelength , irradiance3000, label='T = 3000K', color='red', linewidth=1)
plt.plot(wavelength , irradiance4000, label='T = 4000K', color='blue', linewidth=1)
plt.plot(wavelength , irradiance5000, label='T = 5000K', color='green', linewidth=1)


plt.title('Irradiance against wavelength')
plt.xlabel(r'Wavelength /$nm$')
plt.ylabel(r'Irradiance /$Wm^{-2}nm^{-1}$')
plt.grid(True)
plt.legend()



plt.show()
