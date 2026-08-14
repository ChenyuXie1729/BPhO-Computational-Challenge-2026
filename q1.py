import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox


SPEED_MULTIPLIER = 10

def random_walk_3d(n_steps, step_size):
    theta = np.random.uniform(0, 2 * np.pi, n_steps)
    phi = np.arccos(np.random.uniform(-1, 1, n_steps))

    dx = step_size * np.sin(phi) * np.cos(theta)
    dy = step_size * np.sin(phi) * np.sin(theta)
    dz = step_size * np.cos(phi)

    x = np.concatenate(([0], np.cumsum(dx)))
    y = np.concatenate(([0], np.cumsum(dy)))
    z = np.concatenate(([0], np.cumsum(dz)))

    return x, y, z

N_steps = 10000
N_simulations = 50
stepsize = 1

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

try:
    plt.get_current_fig_manager().window.state("zoomed")
except Exception:
    try:
        plt.get_current_fig_manager().full_screen_toggle()
    except Exception:
        pass

walks = []
for i in range(N_simulations):
    walks.append(random_walk_3d(N_steps, stepsize))

lines = []
for _ in range(N_simulations):
    line, = ax.plot([], [], [], linewidth=0.6, alpha=0.6)
    lines.append(line)

def animate(frame):
    current_step = frame * SPEED_MULTIPLIER

    for line, (x, y, z) in zip(lines, walks):
        line.set_data(x[:current_step], y[:current_step])
        line.set_3d_properties(z[:current_step])

    
    if current_step >= N_steps:
        anim.event_source.stop()

    return lines

ax.set_title(
    f"Random Walk ({N_simulations} Simulations, {N_steps} Steps, Step size = {stepsize})",
    fontsize=14,
    pad=20,
)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
limit = stepsize * np.sqrt(N_steps) * 1.25

ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_zlim(-limit, limit)

fig.set_size_inches(12, 7)


ax.set_position([0.05, 0.08, 0.68, 0.84])


ax_steps = plt.axes([0.80, 0.75, 0.15, 0.05])
ax_size  = plt.axes([0.80, 0.65, 0.15, 0.05])


box_steps = TextBox(ax_steps, "Steps", initial=str(N_steps))
box_size  = TextBox(ax_size, "Step size", initial=str(stepsize))

def regenerate(_):
    global N_steps, stepsize, walks, lines, anim

    try:
        N_steps = int(box_steps.text)
        stepsize = float(box_size.text)
    except ValueError:
        return

    
    anim.event_source.stop()

    
    ax.cla()

    
    walks = []
    for _ in range(N_simulations):
        walks.append(random_walk_3d(N_steps, stepsize))

    
    limit = stepsize * np.sqrt(N_steps) * 1.25

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    

    ax.set_title(
        f"Random Walk ({N_simulations} Simulations, "
        f"{N_steps} Steps, Step size = {stepsize})",
        fontsize=14,
        pad=20
    )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    lines.clear()
    for _ in range(N_simulations):
        line, = ax.plot([], [], [], linewidth=0.6, alpha=0.6)
        lines.append(line)

    
    anim = FuncAnimation(
        fig,
        animate,
        frames=(N_steps // SPEED_MULTIPLIER) + 1,
        interval=1,
        blit=False,
        repeat=False
    )

    fig.canvas.draw_idle()

box_steps.on_submit(regenerate)
box_size.on_submit(regenerate)


anim = FuncAnimation(
    fig,
    animate,
    frames=(N_steps // SPEED_MULTIPLIER) + 1,
    interval=1,
    blit=False,
    repeat=False
)

plt.show()
