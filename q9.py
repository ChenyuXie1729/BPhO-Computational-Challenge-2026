import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from matplotlib.widgets import RadioButtons, Slider



def fractional_compton_shift(angle_degrees, energy_keV):
    energy_joules = energy_keV * 1000 * constants.e
    lambda_zero = (constants.h * constants.c) / energy_joules
    angle_radians = np.radians(angle_degrees)
    compton_wavelength = constants.h / (constants.m_e * constants.c)
    delta_lambda = (1 - np.cos(angle_radians)) * compton_wavelength
    return delta_lambda / lambda_zero

def electron_recoil_velocity(angle_degrees, energy_keV):
    h, c, m_e = constants.h, constants.c, constants.m_e
    E_photon_initial = energy_keV * 1000 * constants.e
    wavelength_initial = (h * c) / E_photon_initial
    angle_radians = np.radians(angle_degrees)
    compton_wavelength = h / (m_e * c)
    wavelength_final = wavelength_initial + (1 - np.cos(angle_radians)) * compton_wavelength
    E_rest = m_e * c**2
    delta_E_photon = (h * c / wavelength_initial) - (h * c / wavelength_final)
    E_total_electron = E_rest + delta_E_photon
    return np.sqrt(1 - (E_rest / E_total_electron)**2)

def electron_recoil_angle(photon_angle_degrees, energy_keV):
    h, c, m_e = constants.h, constants.c, constants.m_e
    theta_rad = np.radians(photon_angle_degrees)
    E_photon_initial = energy_keV * 1000 * constants.e
    lambda_zero = (h * c) / E_photon_initial
    compton_factor = h / (m_e * c * lambda_zero)
    numerator = np.sin(theta_rad)
    denominator = (1 + compton_factor) * (1 - np.cos(theta_rad)) + 1e-15
    tan_phi = numerator / denominator
    phi_deg = np.degrees(np.arctan(tan_phi))
    return np.where(phi_deg < 0, phi_deg + 180, phi_deg)



degrees = np.linspace(0.1, 180, 500)
energies = [50, 100, 200, 500, 1000]
colors = ['purple', 'blue', 'green', 'orange', 'red']

fig, ax = plt.subplots(figsize=(12, 6.5))
plt.subplots_adjust(left=0.3, bottom=0.25)

current_graph = 'Fractional Shift'
slider_line = None

def plot_graph(graph_type):
      global current_graph, slider_line
    current_graph = graph_type
    
    ax.clear()
    

    for energy, color in zip(energies, colors):
        if graph_type == 'Fractional Shift':
            y_data = fractional_compton_shift(degrees, energy)
            ax.plot(degrees, y_data, color=color, linewidth=1.2, label=f'{energy} /keV')
            ax.set_title(r'Fractional Wavelength Shift $\frac{\Delta\lambda}{\lambda_0}$ against Scattering Angle')
            ax.set_ylabel(r'Fractional Shift')  # Dimensionless
            ax.set_ylim(bottom=0, top=6.5)
            
        elif graph_type == 'Recoil Velocity':
            y_data = electron_recoil_velocity(degrees, energy)
            ax.plot(degrees, y_data, color=color, linewidth=1.2, label=f'{energy} /keV')
            ax.set_title('Electron Recoil Velocity against Photon Scattering Angle')
            ax.set_ylabel('Electron Velocity /$c$')
            ax.set_ylim(0, 1.0)
            
        elif graph_type == 'Recoil Angle':
            y_data = electron_recoil_angle(degrees, energy)
            ax.plot(degrees, y_data, color=color, linewidth=1.2, label=f'{energy} /keV')
            ax.set_title(r'Electron Recoil Angle $\phi$ against Photon Scattering Angle $\theta$')
            ax.set_ylabel('Electron Recoil Angle \phi /degrees')
            ax.set_ylim(0, 90)
            ax.set_yticks(np.arange(0, 91, 15))

    
    current_val = slider.val
    if graph_type == 'Fractional Shift':
        y_slide = fractional_compton_shift(degrees, current_val)
    elif graph_type == 'Recoil Velocity':
        y_slide = electron_recoil_velocity(degrees, current_val)
    elif graph_type == 'Recoil Angle':
        y_slide = electron_recoil_angle(degrees, current_val)
        
    slider_line, = ax.plot(degrees, y_slide, color='black', linestyle='--', linewidth=2.0, 
                          label=f'Live: {current_val:.0f} /keV')

    
    ax.set_xlabel('Photon Scattering Angle /degrees')
    ax.set_xlim(0, 180)
    ax.set_xticks(np.arange(0, 181, 30))
    ax.grid(True, alpha=0.3)
    ax.legend(title="Photon Energy", loc='upper left')
    fig.canvas.draw_idle()

def update_slider(val):
        global current_graph, slider_line
    if slider_line is not None:
        if current_graph == 'Fractional Shift':
            new_y = fractional_compton_shift(degrees, val)
        elif current_graph == 'Recoil Velocity':
            new_y = electron_recoil_velocity(degrees, val)
        elif current_graph == 'Recoil Angle':
            new_y = electron_recoil_angle(degrees, val)
            
        slider_line.set_ydata(new_y)
        slider_line.set_label(f'Live: {val:.0f} /keV')
        
        ax.legend(title="Photon Energy", loc='upper left')
        fig.canvas.draw_idle()



radio_ax = plt.axes([0.02, 0.45, 0.22, 0.2], facecolor='whitesmoke')
radio = RadioButtons(radio_ax, ('Fractional Shift', 'Recoil Velocity', 'Recoil Angle'))
radio.on_clicked(plot_graph)

slider_ax = plt.axes([0.35, 0.08, 0.5, 0.04], facecolor='whitesmoke')
slider = Slider(
    ax=slider_ax,
    label='Live Photon Energy /keV ',
    valmin=10,
    valmax=1200,
    valinit=350,
    valfmt='%0.0f /keV',
    color='dimgray'
)
slider.on_changed(update_slider)

plot_graph('Fractional Shift')

plt.show()
