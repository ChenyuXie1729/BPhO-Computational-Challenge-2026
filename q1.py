import matplotlib.pyplot as plt
import numpy as np


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


for i in range(N_simulations):
    x_coords, y_coords, z_coords = random_walk_3d(N_steps, stepsize)
    ax.plot(x_coords, y_coords, z_coords, alpha=0.6, linewidth=0.5)

ax.set_title(
    f"Random Walk ({N_simulations} Simulations, {N_steps} Steps, Step size = {stepsize})",
    fontsize=14,
    pad=20,
)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")


plt.tight_layout()

plt.show()
