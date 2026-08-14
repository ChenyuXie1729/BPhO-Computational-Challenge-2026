import numpy as np
import matplotlib.pyplot as plt
from scipy import constants
from scipy.interpolate import make_interp_spline
from matplotlib.widgets import Slider, RadioButtons, CheckButtons, Button

def Energy(n, L):
    return (constants.hbar * np.pi * n) ** 2 / (2 * constants.m_e * L ** 2)

def Probability(x, n, L):
    inside = (x >= 0) & (x <= L)
    probability = (2 / L) * np.sin(n * np.pi * x / L) ** 2
    return np.where(inside, probability, 0)

box_width = 3000e-9

quantum_numbers = np.arange(1, 6)

fig = plt.figure(figsize=(12, 7))

graph = fig.add_axes([0.08, 0.18, 0.68, 0.72])

graph_selector = plt.axes([0.81, 0.67, 0.15, 0.18])

graph_buttons = RadioButtons(
    graph_selector,
    (
        "Energy Levels",
        "Probability Density"
    )
)

n_selector = plt.axes([0.81, 0.30, 0.15, 0.30])

n_buttons = CheckButtons(
    n_selector,
    (
        "n = 1",
        "n = 2",
        "n = 3",
        "n = 4",
        "n = 5"
    ),
    (
        False,
        False,
        False,
        False,
        False
    )
)

clear_ax = plt.axes([0.81,0.20,0.15,0.05])

clear_button = Button(
    clear_ax,
    "Clear"
)

slider_axis = plt.axes([0.12, 0.06, 0.78, 0.04])

width_slider = Slider(
    slider_axis,
    "Box width /nm",
    1,
    10,
    valinit=5,
    valstep=0.1
)

current_graph = "Energy Levels"
wave_lines = {}
wave_levels = {}
n_selector.set_visible(False)



def draw_energy():

    graph.clear()



    L = width_slider.val * 1e-9

    energies = Energy(
        quantum_numbers,
        L
    ) / constants.e

    x_dense = np.linspace(
        quantum_numbers.min(),
        quantum_numbers.max(),
        300
    )

    spline = make_interp_spline(
        quantum_numbers,
        energies,
        k=2
    )

    y_dense = spline(x_dense)

    graph.plot(
        x_dense,
        y_dense,
        '--',
        color='red',
        linewidth=1
    )

    graph.scatter(
        quantum_numbers,
        energies,
        color='red',
        s=45,
        zorder=5
    )

    graph.set_xlim(1, 5)

    graph.set_ylim(
        0,
        max(energies) * 1.1
    )

    graph.set_xticks(
        quantum_numbers
    )

    graph.set_xlabel(
        "Quantum Number"
    )

    graph.set_ylabel(
        "Energy /eV"
    )

    graph.set_title(
        "Energy Levels against Quantum Number"
    )

    graph.grid(
        alpha=0.3
    )


def draw_probability():

    graph.clear()

    L = width_slider.val * 1e-9

    x = np.linspace(
        0,
        L,
        1000
    )

    x_nm = x * 1e9

    colours = [
        "red",
        "blue",
        "green",
        "orange",
        "purple"
    ]

    status = n_buttons.get_status()

    for i in range(5):

        if status[i]:

            n = i + 1

            probability = Probability(
                x,
                n,
                L
            )

            graph.plot(
                x_nm,
                probability,
                color=colours[i],
                linewidth=2,
                label=f"n = {n}"
            )

    graph.set_xlim(
        0,
        width_slider.val
    )

    graph.set_ylim(
        0,
        2 / L * 1.05
    )

    graph.set_xlabel(
        "Position /nm"
    )

    graph.set_ylabel(
        "Probability Density"
    )

    graph.set_title(
        "Probability Density"
    )

    graph.grid(alpha=0.3)

    if any(status):
        graph.legend()

    fig.canvas.draw_idle()
def update_graph(_):

    global current_graph

    current_graph = graph_buttons.value_selected

    if current_graph == "Energy Levels":

        n_selector.set_visible(False)

        draw_energy()

    else:

        n_selector.set_visible(True)

        draw_probability()

    fig.canvas.draw_idle()


def update_slider(value):

    if current_graph == "Energy Levels":

        draw_energy()

    else:

        draw_probability()

    fig.canvas.draw_idle()

def update_quantum(label):

    if current_graph == "Probability Density":

        L = width_slider.val * 1e-9

        x = np.linspace(0, L, 1000)

        x_nm = x * 1e9

        draw_probability()

        fig.canvas.draw_idle()
graph_buttons.on_clicked(update_graph)

width_slider.on_changed(update_slider)

n_buttons.on_clicked(update_quantum)
def clear_wavefunctions(event):

    for i in range(5):

        if n_buttons.get_status()[i]:

            n_buttons.set_active(i)

clear_button.on_clicked(clear_wavefunctions)

draw_energy()

graph.set_facecolor("white")

graph.tick_params(
    axis="both",
    labelsize=10
)

graph.spines["top"].set_visible(True)
graph.spines["right"].set_visible(True)

plt.show()
