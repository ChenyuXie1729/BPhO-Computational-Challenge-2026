import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.widgets import Slider

L = 10.0                # box size
N = 40                  # number of small particles
m = 1.0                 # small mass
r = 0.12                # small radius
M = 20.0                # large mass
R = 0.8                 # large radius
dt = 0.02               # time step
noise_strength = 1.2    # intensity of the random walk (Brownian kicks)  
v_max = 4.0
trail_len = 500          # how many past points to keep

big_pos = np.array([L/2, L/2], dtype=float)
big_vel = np.array([0.0, 0.0], dtype=float)

small_pos = np.random.uniform(r, L - r, (N, 2))
small_vel = np.random.randn(N, 2) * 1.0

for i in range(N):
    while np.linalg.norm(small_pos[i] - big_pos) < (R + r + 0.2):
        small_pos[i] = np.random.uniform(r, L - r, 2)

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.set_aspect('equal')
ax.set_facecolor('white')
ax.grid(False)
fig.set_size_inches(11,7)

ax.set_position([0.05,0.08,0.65,0.85])

big_circle = Circle(big_pos, R, fill=False, edgecolor='red', linewidth=2, zorder=5)
small_circles = [Circle(small_pos[i], r, color='blue', alpha=0.6, zorder=3)
                  for i in range(N)]
ax.add_patch(big_circle)
for c in small_circles:
    ax.add_patch(c)

trail_x, trail_y = [big_pos[0]], [big_pos[1]]
trail_line, = ax.plot([], [], color='red', linewidth=1, alpha=0.6, zorder=4)


ax_particles = plt.axes([0.80, 0.75, 0.15, 0.03])
ax_noise     = plt.axes([0.80, 0.65, 0.15, 0.03])
ax_speed     = plt.axes([0.80, 0.55, 0.15, 0.03])

slider_particles = Slider(
    ax_particles,
    "Particles",
    10,
    200,
    valinit=N,
    valstep=5
)

slider_noise = Slider(
    ax_noise,
    "Noise",
    0.0,
    3.0,
    valinit=noise_strength,
    valstep=0.1
)

slider_speed = Slider(
    ax_speed,
    "Max Speed",
    1.0,
    10.0,
    valinit=v_max,
    valstep=0.5
)

def regenerate(val):

    global N, noise_strength, v_max
    global small_pos, small_vel, small_circles

    new_N = int(slider_particles.val)
    noise_strength = slider_noise.val
    v_max = slider_speed.val

    
    if new_N != N:

        N = new_N

        for c in small_circles:
            c.remove()

        small_pos = np.random.uniform(r, L-r, (N, 2))
        small_vel = np.random.randn(N, 2)

        small_circles = [
            Circle(
                small_pos[i],
                r,
                color='blue',
                alpha=0.6,
                zorder=3
            )
            for i in range(N)
        ]

        for c in small_circles:
            ax.add_patch(c)

    fig.canvas.draw_idle()
slider_particles.on_changed(regenerate)
slider_noise.on_changed(regenerate)
slider_speed.on_changed(regenerate)

def update(frame):
    global big_pos, big_vel, small_pos, small_vel

    small_vel += np.random.randn(N, 2) * noise_strength * np.sqrt(dt)
    speeds = np.linalg.norm(small_vel, axis=1)
    too_fast = speeds > v_max
    small_vel[too_fast] *= (v_max / speeds[too_fast])[:, None]

    small_pos += small_vel * dt
    big_pos   += big_vel * dt

    left_wall = small_pos[:, 0] < r
    right_wall = small_pos[:, 0] > L - r
    small_vel[left_wall, 0] = np.abs(small_vel[left_wall, 0])
    small_vel[right_wall, 0] = -np.abs(small_vel[right_wall, 0])
    small_pos[left_wall, 0] = r
    small_pos[right_wall, 0] = L - r

    bottom_wall = small_pos[:, 1] < r
    top_wall = small_pos[:, 1] > L - r
    small_vel[bottom_wall, 1] = np.abs(small_vel[bottom_wall, 1])
    small_vel[top_wall, 1] = -np.abs(small_vel[top_wall, 1])
    small_pos[bottom_wall, 1] = r
    small_pos[top_wall, 1] = L - r

    if big_pos[0] < R or big_pos[0] > L - R:
        big_vel[0] *= -1
    if big_pos[1] < R or big_pos[1] > L - R:
        big_vel[1] *= -1
    big_pos[0] = np.clip(big_pos[0], R, L - R)
    big_pos[1] = np.clip(big_pos[1], R, L - R)

    for i in range(N):
        dist_vec = small_pos[i] - big_pos
        dist = np.linalg.norm(dist_vec)
        if 0 < dist < (R + r):
            n = dist_vec / dist
            v_rel = small_vel[i] - big_vel
            vn = np.dot(v_rel, n)
            if vn < 0:
                J = -2 * vn / (1/m + 1/M)
                small_vel[i] += (J / m) * n
                big_vel      -= (J / M) * n
                overlap = (R + r) - dist
                small_pos[i] += n * (overlap + 1e-6)

    big_circle.center = big_pos
    for i, c in enumerate(small_circles):
        c.center = small_pos[i]

    trail_x.append(big_pos[0])
    trail_y.append(big_pos[1])
    if len(trail_x) > trail_len:
        del trail_x[0]
        del trail_y[0]
    trail_line.set_data(trail_x, trail_y)

    return [big_circle, trail_line] + small_circles

ani = FuncAnimation(fig, update, frames=2000, interval=20, blit=True)
plt.show()
