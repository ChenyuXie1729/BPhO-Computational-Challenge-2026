import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from matplotlib.widgets import RadioButtons, Slider, Button



def Plancks_law(wavelength, temperature):
    return ((2 * constants.h * constants.c**2) / (wavelength**5)) / (
            np.exp(constants.h * constants.c / (wavelength * constants.k * temperature)) - 1)

def einstein_molar_heat_capacity(T, Theta_E):
    
    T_arr = np.asarray(T, dtype=float)
    
    if np.any(T_arr <= 0):
        raise ValueError("Temperature must be strictly greater than 0 Kelvin.")
        
    x = Theta_E / T_arr
    
    
    Cv = 3 * constants.R * (x**2) * (np.exp(-x) / (1 - np.exp(-x))**2)
    
    return float(Cv) if np.isscalar(T) else Cv



wavelength = np.linspace(100e-9, 3000e-9, 500)
T_heat_capacity = np.linspace(1, 1000, 500)
max_irradiance = Plancks_law(wavelength, 8000).max()

fig, ax = plt.subplots(figsize=(13, 7))
plt.subplots_adjust(left=0.35, bottom=0.25)

current_graph = 'Planck Curve'
line_planck = None

crystal_database = {
    'Platinum': {'theta': 240.0, 'color': 'purple'},
    'Gold': {'theta': 162.0, 'color': 'red'},
    'Silver': {'theta': 215.0, 'color': 'silver'},
    'Copper': {'theta': 343.0, 'color': 'blue'},
    'Iron': {'theta': 470.0, 'color': 'green'}
}

selected_crystals = {element: False for element in crystal_database}

def plot_graph(graph_type):
   
    global current_graph, line_planck
    current_graph = graph_type
    ax.clear()
    
    if graph_type == 'Planck Curve':
        slider.set_active(True)
        slider_ax.set_visible(True)
        set_crystal_ui_state(visible=False, active=False)
        
        ref_temps = [5000, 6000, 7000, 8000]
        ref_colors = ['purple', 'blue', 'green', 'orange']
        for t, col in zip(ref_temps, ref_colors):
            ax.plot(wavelength * 1e9, Plancks_law(wavelength, t), color=col, linewidth=1.2, label=f'{t} /K')
        
        current_T = slider.val
        line_planck, = ax.plot(wavelength * 1e9, Plancks_law(wavelength, current_T), color='black', 
                               linestyle='--', linewidth=2.0, label=f'Live: {current_T:.0f} /K')
        
        ax.set_title('Planck Radiation Curve')
        ax.set_xlabel('Wavelength /nm')
        ax.set_ylabel(r'Irradiance /$W\,m^{-2}\,m^{-1}$')
        ax.set_xlim(100, 3000)
        ax.set_ylim(0, max_irradiance * 1.05)
        ax.legend(loc='upper right')
        
    elif graph_type == 'Heat Capacity':
        # Disable slider events, enable heat capacity UI listeners
        slider.set_active(False)
        slider_ax.set_visible(False)
        set_crystal_ui_state(visible=True, active=True)
        redraw_heat_capacity_curves()

    ax.grid(True, alpha=0.3)
    fig.canvas.draw_idle()

def update_slider(val):
    global current_graph, line_planck
    if current_graph == 'Planck Curve' and line_planck is not None:
        line_planck.set_ydata(Plancks_law(wavelength, val))
        line_planck.set_label(f'Live: {val:.0f} /K')
        ax.legend(loc='upper right')
        fig.canvas.draw_idle()



def redraw_heat_capacity_curves():
    ax.clear()
    plotted_any = False
    
    for name, properties in crystal_database.items():
        if selected_crystals[name]:
            y_crystal = einstein_molar_heat_capacity(T_heat_capacity, properties['theta'])
            ax.plot(T_heat_capacity, y_crystal, color=properties['color'], linewidth=2.0, label=f'{name}')
            plotted_any = True
            
    ax.set_title('Molar Heat Capacity of Solids against Temperature')
    ax.set_xlabel('Temperature /K')
    ax.set_ylabel(r'Molar Heat Capacity /$J\,mol^{-1}\,K^{-1}$')
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 27)
    if plotted_any:
        ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    fig.canvas.draw_idle()

def create_crystal_callback(name):
    def callback(event):
        if current_graph == 'Heat Capacity':
            selected_crystals[name] = not selected_crystals[name]
            crystal_buttons[name].ax.set_facecolor('darkgray' if selected_crystals[name] else 'whitesmoke')
            redraw_heat_capacity_curves()
    return callback

def clear_choices(event):
    if current_graph == 'Heat Capacity':
        for name in selected_crystals:
            selected_crystals[name] = False
            crystal_buttons[name].ax.set_facecolor('whitesmoke')
        redraw_heat_capacity_curves()

def set_crystal_ui_state(visible, active):
   
    for btn in crystal_buttons.values():
        btn.ax.set_visible(visible)
        btn.set_active(active)
    clear_btn.ax.set_visible(visible)
    clear_btn.set_active(active)


radio_ax = plt.axes([0.02, 0.50, 0.25, 0.15], facecolor='whitesmoke')
radio = RadioButtons(radio_ax, ('Planck Curve', 'Heat Capacity'))
radio.on_clicked(plot_graph)


slider_ax = plt.axes([0.42, 0.08, 0.45, 0.04], facecolor='whitesmoke')
slider = Slider(ax=slider_ax, label='Live Temperature /K ', valmin=1000, valmax=8000, 
                valinit=3500, valstep=100, valfmt='%0.0f /K', color='dimgray')
slider.on_changed(update_slider)


crystal_names = ['Platinum', 'Gold', 'Silver', 'Copper', 'Iron']
crystal_buttons = {}

start_x = 0.38
total_width = 0.44
spacing = total_width / len(crystal_names)
button_width = spacing * 0.85 

for i, name in enumerate(crystal_names):
    btn_ax = plt.axes([start_x + i * spacing, 0.08, button_width, 0.04], facecolor='whitesmoke')
    btn = Button(btn_ax, name)
    btn.on_clicked(create_crystal_callback(name))
    crystal_buttons[name] = btn


clear_ax = plt.axes([start_x + len(crystal_names) * spacing, 0.08, 0.08, 0.04], facecolor='salmon')
clear_btn = Button(clear_ax, 'Clear', color='salmon')
clear_btn.on_clicked(clear_choices)


plot_graph('Planck Curve')

plt.show()
