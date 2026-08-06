# Photoelectric Effect Simulator


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as pe



h = 4.135667696e-15
c = 2.998e8


METALS = {
    "Cesium (Cs)":2.10,
    "Sodium (Na)":2.28,
    "Calcium (Ca)":2.90,
    "Zinc (Zn)":4.30,
    "Copper (Cu)":4.70,
    "Platinum (Pt)":6.35,
}

METAL_NAMES = list(METALS.keys())

WL_MIN, WL_MAX = 200, 800
V_MIN, V_MAX = -4, 4

PLATE_X = 0.28
COLL_X = 0.78
GAP = COLL_X - PLATE_X


def wavelength_to_rgb(wl_nm):
    wl = wl_nm
    if wl < 380:
        return (0.55, 0.0, 0.85)
    if wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    elif wl <= 780:
        r, g, b = 1.0, 0.0, 0.0
    else:
        return (0.3, 0.0, 0.0)
    return (np.clip(r, 0, 1), np.clip(g, 0, 1), np.clip(b, 0, 1))


def freq_from_wl(wl_nm):
    return c / (wl_nm * 1e-9)


def photon_energy_eV(wl_nm):
    return h * freq_from_wl(wl_nm)


def stopping_voltage(wl_nm, work_fn):
    ke = photon_energy_eV(wl_nm) - work_fn
    return max(ke, 0.0)

fig=plt.figure(figsize=(12,6.2))
ax_sim=fig.add_axes([0.05,0.30,0.40,0.58])
ax_plot=fig.add_axes([0.56,0.30,0.40,0.58])

plt.rcParams["toolbar"] = "None"

fig.suptitle(
    "Photoelectric effect simulator",
    fontsize=14,
    fontweight="bold"
)

ax_plot.set_xlabel("Frequency  / x10$^{14}$ Hz")
ax_plot.set_ylabel("Stopping voltage  V$_{stop}$  / V")
ax_plot.grid(alpha=0.3)

ax_sim.set_xlim(-0.12,1.15)
ax_sim.set_ylim(-0.18,1.15)
ax_sim.set_xticks([])
ax_sim.set_yticks([])



ax_sim.set_facecolor("white")
grad=np.linspace(0,1,300)
grad=np.tile(grad,(300,1))
ax_sim.imshow(
    grad,
    extent=[-0.12, 1.02, -0.18, 1.15],
    origin="lower",
    cmap="bone",
    alpha=0.12,
    zorder=0,
)

#Vacuum chamber
glass = FancyBboxPatch(
    (0.16,0.10),
    0.72,
    0.78,
    boxstyle="round,pad=0.02,rounding_size=0.03",
    linewidth=2.5,
    edgecolor="#b7dfff",
    facecolor=(0.7, 0.9, 1.0, 0.08),   # transparent blue
    zorder=2
)

ax_sim.add_patch(glass)



#Battery
from matplotlib.patches import Rectangle

battery_blue = Rectangle(
    (0.33, -0.13),   # moved down
    0.008,
    0.12,
    color="royalblue",
    clip_on=False,
)

battery_red = Rectangle(
    (0.36, -0.11),   # moved down
    0.008,
    0.08,
    color="red",
    clip_on=False,
)

ax_sim.add_patch(battery_blue)
ax_sim.add_patch(battery_red)

battery_minus = ax_sim.text(
    0.31,
    -0.02,
    "-",
    color="royalblue",
    fontsize=18,
    fontweight="bold",
)

battery_plus = ax_sim.text(
    0.39,
    -0.02,
    "+",
    color="red",
    fontsize=18,
    fontweight="bold",
)
#Ammeter
ammeter = plt.Circle(
    (0.70, -0.07),
    0.08,
    facecolor="#f3f3f3",
    edgecolor="#333333",
    lw=2,
    clip_on=False,
    zorder=20,
)

ax_sim.add_patch(ammeter)

ammeter_value = ax_sim.text(
    0.70,
    -0.07,
    "0.00\nnA",
    ha="center",
    va="center",
    fontsize=9,
    color="green",
    fontweight="bold",
    zorder=30,
)
#Metallic plates 
left_plate=FancyBboxPatch(
    (PLATE_X-0.02,0.05),0.02,0.90,
    boxstyle="round,pad=0.005",
    facecolor="#d9d9d9",
    edgecolor="white",
    linewidth=2
)

right_plate=FancyBboxPatch(
    (COLL_X,0.05),0.02,0.90,
    boxstyle="round,pad=0.005",
    facecolor="#5577ff",
    edgecolor="#dce5ff",
    linewidth=2
)

ax_sim.add_patch(left_plate)
ax_sim.add_patch(right_plate)

plate_sign_left = ax_sim.text(
    PLATE_X - 0.01,
    0.97,
    "-",
    color="royalblue",
    fontsize=24,
    fontweight="bold",
    ha="center",
)

plate_sign_right = ax_sim.text(
    COLL_X + 0.01,
    0.97,
    "+",
    color="red",
    fontsize=24,
    fontweight="bold",
    ha="center",
)

#Animated light beam 
beam_x = np.linspace(-0.04, PLATE_X, 400)

beam_y0 = np.linspace(0.88, 0.50, 400)

beam_glow1, = ax_sim.plot([], [], lw=18, alpha=0.04, zorder=4)
beam_glow2, = ax_sim.plot([], [], lw=12, alpha=0.08, zorder=5)
beam_glow3, = ax_sim.plot([], [], lw=7,  alpha=0.18, zorder=6)
beam_main,  = ax_sim.plot([], [], lw=3,              zorder=7)

light_src = ax_sim.scatter(
    [-0.06],
    [0.88],
    s=400,
    color="white",
    edgecolors="black",
    linewidths=1.5,
    zorder=20,
    clip_on=False,
)

#Glowing photons 
photon_glow=ax_sim.scatter([],[],s=120,alpha=.12)
photon_scat=ax_sim.scatter([],[],s=18)

#Wire 
# left plate to battery
ax_sim.plot(
    [PLATE_X-0.01, PLATE_X-0.01],
    [0.05, -0.07],
    lw=3,
    color="#222",
    clip_on=False,
)

ax_sim.plot(
    [PLATE_X-0.01, 0.33],
    [-0.07, -0.07],
    lw=3,
    color="#222",
    clip_on=False,
)
# battery to left edge of ammeter
ax_sim.plot(
    [0.368, 0.62],
    [-0.07, -0.07],
    lw=3,
    color="#222",
    clip_on=False,
)

# left side of circle
ax_sim.plot(
    [0.62,0.62],
    [-0.07,-0.07],
    lw=3,
    color="#222",
    clip_on=False,
)

# right side of circle
ax_sim.plot(
    [0.78, 0.78],
    [-0.03, -0.07],
    lw=3,
    color="#222",
    clip_on=False,
)

# right edge to anode
ax_sim.plot(
    [COLL_X+0.01, COLL_X+0.01],
    [0.05, -0.07],
    lw=3,
    color="#222",
    clip_on=False,
)
ax_sim.plot(
    [0.78, COLL_X+0.01],
    [-0.07, -0.07],
    lw=3,
    color="#222",
    clip_on=False,
)

#Glowing electrons 
electron_glow=ax_sim.scatter([],[],s=180,color="cyan",alpha=.08)
electron_scat=ax_sim.scatter([],[],s=20,color="#66ffff")

info_text = fig.text(
    0.25,
    0.27,
    "",
    ha="center",
    va="top",
    color="black",
    fontsize=11,
)


for txt in (info_text,):
    txt.set_path_effects([
        pe.withStroke(linewidth=0.5, foreground="white")
    ])

f_vals_nm = np.linspace(WL_MIN, WL_MAX, 400)
f_vals = freq_from_wl(f_vals_nm) / 1e14
ax_plot.set_xlim(f_vals.min(), f_vals.max())

metal_lines = {}
for name, w in METALS.items():
    vstop = np.array([stopping_voltage(wl, w) for wl in f_vals_nm])
    (line,) = ax_plot.plot(f_vals, vstop, lw=1.2, alpha=0.35, color="gray")
    metal_lines[name] = line

highlight_line, = ax_plot.plot([], [], lw=2.5, color="orange", label="selected metal")
current_pt, = ax_plot.plot([], [], "o", color="red", markersize=8)
ax_plot.legend(loc="upper left", fontsize=8)

ax_wl = fig.add_axes([0.20, 0.16, 0.30, 0.03])
s_wl = Slider(ax_wl, "Wavelength / nm", WL_MIN, WL_MAX, valinit=500, color="orange")

ax_v = fig.add_axes([0.20, 0.04, 0.30, 0.03])
s_v = Slider(ax_v, "Plate Voltage / V", V_MIN, V_MAX, valinit=0.0, color="steelblue")

ax_i = fig.add_axes([0.20, 0.10, 0.30, 0.03])
s_i = Slider(
    ax_i,
    "Intensity / %",
    0,
    100,
    valinit=50,
    color="gold"
)

#"Metal" dropdown 
from matplotlib.patches import FancyBboxPatch

dropdown_open = False

y_i = 0.23
dropdown_box = FancyBboxPatch(
    (0.58, 0.23),      # Same y as first option
    0.11,              # Same width as options
    0.035,             # Same height as options
    boxstyle="round,pad=0.005",
    facecolor="white",
    edgecolor="#666",
    linewidth=1.5,
    transform=fig.transFigure,
)

fig.patches.append(dropdown_box)

dropdown_text = fig.text(
    0.590,
    y_i + 0.0175,
    "Metal",
    fontsize=9,
    va="center",
)

dropdown_arrow = fig.text(
    0.675,
    y_i + 0.0175,
    "▼",
    fontsize=9,
    va="center",
)

option_boxes = []
option_texts = []

# Create dropdown options 
y0 = 0.195

for i, metal in enumerate(METAL_NAMES):

    r = FancyBboxPatch(
        (0.58, y0-0.038*i),
        0.11,
        0.035,
        boxstyle="round,pad=0.005",
        facecolor="white",
        edgecolor="#999",
        transform=fig.transFigure,
        visible=False,
    )

    fig.add_artist(r)

    t = fig.text(
        0.590,
        y0+0.018-0.038*i,
        metal,
        fontsize=9,
        va="center",
        visible=False,
    )

    option_boxes.append(r)
    option_texts.append(t)


#Graph selector 
ax_graph = fig.add_axes([0.63, 0.03, 0.33, 0.14])

graph_radio = RadioButtons(
    ax_graph,
    (
        "Electron Energy vs Frequency",
        "Current vs Light Intensity",
        "Current vs Frequency",
    ),
    active=0,
)


for txt in graph_radio.labels:
    txt.set_x(0.18)          
    txt.set_fontsize(9)
state = {
    "metal": METAL_NAMES[4],
    "wl": 500.0,
    "V": 0.0,
    "I": 50,

    "graph_I": 50,
    "graph_V": 0.0,
    "graph_wl": 500.0,
    "graph_current": 0.0,
    "skip_first_intensity": False,

    "graph": "Electron Energy vs Frequency",
    "last_wl": None,
}
photons = []
electrons = []
rng = np.random.default_rng(0)
graph_points_x = []
graph_points_y = []

graph_points = ax_plot.scatter(
    [],
    [],
    s=30,
    color="royalblue"
)

def spawn_photon():

    amp = 0.02

    photons.append([
        beam_x[0],
        beam_y0[0],
        0.012,
        rng.uniform(-amp, amp),
    ])


def update_highlight():
    ax_plot.clear()
    global graph_points
    graph_points = ax_plot.scatter(
        [],
        [],
        s=30,
        color="royalblue"
    )

    choice = state["graph"]

    w = METALS[state["metal"]]

    freq = freq_from_wl(f_vals_nm)/1e14

    KE = np.maximum(
        photon_energy_eV(f_vals_nm)-w,
        0
    )

    KE_max = max(
        photon_energy_eV(state["wl"])-w,
        0
    )
    
    
    if choice=="Electron Energy vs Frequency":

        ax_plot.set_xlabel(
            "Frequency / ×10$^{14}$ Hz"
        )

        ax_plot.set_ylabel(
            "Maximum Electron Energy / eV"
        )

    elif choice=="Current vs Light Intensity":

        intensity = np.linspace(0,100,300)

        if KE_max<=0:

            current=np.zeros_like(intensity)

        else:

            collection=np.clip(
                (state["V"]+KE_max)/KE_max,
                0,
                1
            )

            current=collection*intensity

        current_now=np.interp(
            state["I"],
            intensity,
            current
        )

        ax_plot.set_xlabel(
            "Light Intensity / %"
        )

        ax_plot.set_ylabel(
            "Photocurrent / nA"
        )

    elif choice=="Current vs Frequency":

        current=np.zeros_like(freq)

        for i,wl in enumerate(f_vals_nm):

            ke=photon_energy_eV(wl)-w

            if ke>0:

                collection=np.clip(
                    (state["V"]+ke)/ke,
                    0,
                    1
                )

                current[i]=collection*state["I"]

        if KE_max>0:

            current_now=np.clip(
                (state["V"]+KE_max)/KE_max,
                0,
                1
            )*state["I"]

        else:

            current_now=0

        ax_plot.set_xlabel(
            "Frequency / ×10$^{14}$ Hz"
        )

        ax_plot.set_ylabel(
            "Photocurrent / nA"
        )

    ax_plot.grid(alpha=0.3)
    if choice == "Electron Energy vs Frequency":
        ax_plot.set_xlim(freq.min(), freq.max())

    elif choice == "Current vs Light Intensity":
        ax_plot.set_xlim(0, 100)

    elif choice == "Current vs Frequency":
        ax_plot.set_xlim(freq.min(), freq.max())

    fig.canvas.draw_idle()

def clear_graph():

    graph_points_x.clear()
    graph_points_y.clear()

    graph_points.set_offsets(np.empty((0, 2)))

    fig.canvas.draw_idle()

def on_wl(val):
    state["wl"] = val

    if state["graph"] == "Current vs Light Intensity":

        state["graph_wl"] = val
        clear_graph()
        state["skip_first_intensity"] = True
def on_v(val):
    state["V"] = val

    if state["graph"] == "Current vs Light Intensity":

        state["graph_V"] = val
        clear_graph()
        state["skip_first_intensity"] = True
    else:

        graph_points_x.clear()
        graph_points_y.clear()
        graph_points.set_offsets(np.empty((0, 2)))

        state["last_wl"] = None

        update_highlight()

def on_i(val):

    state["I"] = val
    if state["skip_first_intensity"]:
        state["skip_first_intensity"] = False
        return
    if state["graph"] == "Current vs Light Intensity":

        state["graph_I"] = val

        W = METALS[state["metal"]]

        KE_max = max(
            photon_energy_eV(state["graph_wl"]) - W,
            0
        )

        if KE_max <= 0:

            state["graph_current"] = 0

        else:

            collection = np.clip(
                (state["graph_V"] + KE_max) / KE_max,
                0,
                1
            )

            state["graph_current"] = (
                state["graph_I"] * collection
            )

        graph_points_x.append(state["graph_I"])
  
        graph_points_y.append(state["graph_current"])
     
        graph_points.set_offsets(
            np.column_stack((graph_points_x, graph_points_y))
        )
        ax_plot.relim()
        ax_plot.autoscale_view()
        fig.canvas.draw_idle()

    else:

        clear_graph()


def on_metal(label):

    state["metal"] = label

    dropdown_text.set_text(label)

    graph_points_x.clear()
    graph_points_y.clear()

    graph_points.set_offsets(np.empty((0, 2)))

    update_highlight()

    fig.canvas.draw_idle()

def on_graph(label):

    state["graph"] = label

    # Clear previous graph
    graph_points_x.clear()
    graph_points_y.clear()

    graph_points.set_offsets(np.empty((0, 2)))

    update_highlight()

    fig.canvas.draw_idle()

s_wl.on_changed(on_wl)
s_v.on_changed(on_v)
s_i.on_changed(on_i)
graph_radio.on_clicked(on_graph)
update_highlight()

frame_count = {"n": 0}

display_current = {"value": 0.0}


def animate(_):
    frame_count["n"] += 1
    color = wavelength_to_rgb(state["wl"])
    light_src.set_color(color)
    phase = frame_count["n"] * 0.4
    beam_y = beam_y0 + 0.015*np.sin(90*beam_x-phase)

    

    for beam in (beam_glow1, beam_glow2, beam_glow3, beam_main):
        beam.set_data(beam_x, beam_y)
        beam.set_color(color)

    spawn_rate = max(1, int(9 - state["I"] / 12.5))

    if frame_count["n"] % spawn_rate == 0:
        spawn_photon()

    W = METALS[state["metal"]]
    E_photon = photon_energy_eV(state["wl"])
    KE_max = max(E_photon - W, 0.0)
    V = state["V"]
    if V >= 0:
        plate_sign_left.set_text("-")
        plate_sign_right.set_text("+")

        plate_sign_left.set_color("royalblue")
        plate_sign_right.set_color("red")

    else:
        plate_sign_left.set_text("+")
        plate_sign_right.set_text("-")

        plate_sign_left.set_color("red")
        plate_sign_right.set_color("royalblue")
    new_photons = []
    for p in photons:

        p[0] += 0.012

        amp = 0.02

        frac = (p[0]-beam_x[0])/(PLATE_X-beam_x[0])

        centre = (
            beam_y0[0]
            + frac*(0.5-beam_y0[0])
            + amp*np.sin(70*p[0]-phase)
        )

        p[1] = centre + p[3]

        if p[0] < PLATE_X:

            new_photons.append(p)

        else:

            if KE_max>0:

                v0=0.05*np.sqrt(KE_max)

                electrons.append([PLATE_X,0.5,v0,0])
    photons[:] = new_photons

    a = 0.02 * V
    reached = 0
    new_electrons = []
    for e_ in electrons:
        x, y, v0, t = e_
        t += 1
        v = v0 - a * t * 0.05
        x_new = x + max(v, 0) if v > 0 else x
        if v <= 0:
            continue
        e_[0] = x_new
        e_[3] = t
        if e_[0] >= COLL_X:
            reached += 1
            
        else:
            new_electrons.append(e_)
    electrons[:] = new_electrons

    if photons:
        offsets = np.array([[p[0], p[1]] for p in photons])

        photon_scat.set_offsets(offsets)
        photon_glow.set_offsets(offsets)

    else:
        empty = np.empty((0, 2))

        photon_scat.set_offsets(empty)
        photon_glow.set_offsets(empty)

    photon_scat.set_color([color] * max(len(photons), 1))
    photon_glow.set_color([color] * max(len(photons), 1))
    if electrons:
        offsets = np.array([[e_[0], e_[1]] for e_ in electrons])

        electron_scat.set_offsets(offsets)
        electron_glow.set_offsets(offsets)

    else:
        empty = np.empty((0, 2))

        electron_scat.set_offsets(empty)
        electron_glow.set_offsets(empty)

#Photoelectric current 
    if KE_max <= 0:
        current = 0.0

    else:
    # More energetic photons give a slightly larger emission rate
        photon_flux = state["I"] / 10.0

    # Fraction of electrons collected by the anode
        collection = np.clip((V + KE_max) / KE_max, 0.0, 1.0)

        current = photon_flux * collection

    if state["graph"] == "Electron Energy vs Frequency":

        x = freq_from_wl(state["wl"]) / 1e14
        y = KE_max

    elif state["graph"] == "Current vs Light Intensity":

        x = state["I"]
        y = current

    else:   # Current vs Frequency

        x = freq_from_wl(state["wl"]) / 1e14
        y = current

    
    if state["graph"] != "Current vs Light Intensity":

        if state["last_wl"] != state["wl"]:

            graph_points_x.append(x)
            graph_points_y.append(y)

            graph_points.set_offsets(
                np.column_stack((graph_points_x, graph_points_y))
            )

            ax_plot.relim()
            ax_plot.autoscale_view()

            state["last_wl"] = state["wl"]

            fig.canvas.draw_idle()

  
    ammeter_value.set_text(f"{current:.2f}\nnA")

    if current > 0:
        ammeter_value.set_color("limegreen")
    else:
        ammeter_value.set_color("#666666")

    info_text.set_text(
        f"$\\lambda$={state['wl']:.0f} nm   E$_{{photon}}$={E_photon:.2f} eV   "
        f"W={W:.2f} eV   KE$_{{max}}$={KE_max:.2f} eV   V$_{{stop}}$={KE_max:.2f} V"
    )
    if V>=0:

        battery_blue.set_x(0.33)
        battery_red.set_x(0.36)

        battery_blue.set_color("royalblue")
        battery_red.set_color("red")

        battery_minus.set_position((0.31,0.08))
        battery_plus.set_position((0.39,0.08))

    else:

        battery_blue.set_x(0.36)
        battery_red.set_x(0.33)

        battery_blue.set_color("red")
        battery_red.set_color("royalblue")

        battery_minus.set_position((0.39,0.08))
        battery_plus.set_position((0.31,0.08))
    return (photon_scat,photon_glow,electron_scat,electron_glow,beam_glow1,beam_glow2,beam_glow3,beam_main,info_text,light_src,)

def on_click(event):

    global dropdown_open

    if event.inaxes is not None:
        return

    renderer = fig.canvas.get_renderer()

    x = event.x
    y = event.y


    # 1. Did we click a metal?
   
    if dropdown_open:

        for i, txt in enumerate(option_texts):

            if txt.get_window_extent(renderer).contains(x, y):

                on_metal(METAL_NAMES[i])

                dropdown_open = False

                dropdown_arrow.set_text("▼")

                for r in option_boxes:
                    r.set_visible(False)

                for t in option_texts:
                    t.set_visible(False)

                fig.canvas.draw_idle()
                return

 
    # 2. Did we click the arrow?

    arrow_bbox = dropdown_arrow.get_window_extent(renderer)

    if arrow_bbox.contains(x, y):

        dropdown_open = not dropdown_open

        if dropdown_open:

            dropdown_arrow.set_text("▲")

            for r in option_boxes:
                r.set_visible(True)

            for t in option_texts:
                t.set_visible(True)

        else:

            dropdown_arrow.set_text("▼")

            for r in option_boxes:
                r.set_visible(False)

            for t in option_texts:
                t.set_visible(False)

        fig.canvas.draw_idle()
        return


    # 3. Did we click the main box?

    box_bbox = dropdown_box.get_window_extent(renderer)

    if box_bbox.contains(x, y):

        dropdown_open = not dropdown_open

        if dropdown_open:

            dropdown_arrow.set_text("▲")

            for r in option_boxes:
                r.set_visible(True)

            for t in option_texts:
                t.set_visible(True)

        else:

            dropdown_arrow.set_text("▼")

            for r in option_boxes:
                r.set_visible(False)

            for t in option_texts:
                t.set_visible(False)

        fig.canvas.draw_idle()
        return


    # 4. Clicked elsewhere

    if dropdown_open:

        dropdown_open = False

        dropdown_arrow.set_text("▼")

        for r in option_boxes:
            r.set_visible(False)

        for t in option_texts:
            t.set_visible(False)

        fig.canvas.draw_idle()
    
fig.canvas.mpl_connect("button_press_event", on_click)

ani = FuncAnimation(fig, animate, interval=40, blit=False, cache_frame_data=False)


plt.show()

