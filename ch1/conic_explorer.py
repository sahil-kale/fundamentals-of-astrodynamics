import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.28)

E_INIT = 0.5
P_INIT = 1.0

def compute_orbit(e, p):
    if abs(e - 1.0) < 1e-3:  # parabola
        theta = np.linspace(-np.pi * 0.95, np.pi * 0.95, 3000)
    elif e > 1.0:  # hyperbola — only near branch
        theta_max = np.arccos(-1.0 / e) * 0.97
        theta = np.linspace(-theta_max, theta_max, 3000)
    else:  # circle / ellipse
        theta = np.linspace(-np.pi, np.pi, 1000)

    r = p / (1.0 + e * np.cos(theta))
    # clip runaway r values (parabola/hyperbola arms go to inf)
    r_clip = 8 * p
    mask = (r > 0) & (r < r_clip)
    r, theta = r[mask], theta[mask]

    return r * np.cos(theta), r * np.sin(theta)

def orbit_type(e):
    if e < 1e-4:       return "Circle"
    elif e < 1 - 1e-3: return "Ellipse"
    elif e < 1 + 1e-3: return "Parabola"
    else:              return "Hyperbola"

def param_str(e, p):
    otype = orbit_type(e)
    lines = [f"Type : {otype}", f"e    = {e:.3f}", f"p    = {p:.3f}"]
    if e < 1 - 1e-3:
        a = p / (1 - e**2)
        b = a * np.sqrt(1 - e**2)
        c = a * e
        lines += [f"a    = {a:.3f}", f"b    = {b:.3f}", f"c    = {c:.3f}"]
    elif e > 1 + 1e-3:
        a = p / (e**2 - 1)
        c = a * e
        lines += [f"a    = {a:.3f}  (hyperbola)", f"c    = {c:.3f}"]
    return "\n".join(lines)

x0, y0 = compute_orbit(E_INIT, P_INIT)
(line,) = ax.plot(x0, y0, "b-", lw=2)
(focus,) = ax.plot([0], [0], "r*", markersize=14, zorder=5, label="Focus (origin)")

info = ax.text(
    0.02, 0.98, param_str(E_INIT, P_INIT),
    transform=ax.transAxes, verticalalignment="top",
    fontsize=10, fontfamily="monospace",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.6),
)

ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.axhline(0, color="k", lw=0.5)
ax.axvline(0, color="k", lw=0.5)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Conic section explorer  —  r = p / (1 + e·cos θ)")
ax.legend(loc="upper right")

def update(_):
    e = slider_e.val
    p = slider_p.val
    x, y = compute_orbit(e, p)
    line.set_data(x, y)

    if len(x):
        lim = max(np.max(np.abs(x)), np.max(np.abs(y))) * 1.15
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)

    info.set_text(param_str(e, p))
    fig.canvas.draw_idle()

ax_e = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_p = plt.axes([0.2, 0.09, 0.65, 0.03])

slider_e = Slider(ax_e, "e  (eccentricity)", 0.0, 2.0, valinit=E_INIT, valstep=0.01)
slider_p = Slider(ax_p, "p  (semi-latus rectum)", 0.1, 5.0, valinit=P_INIT, valstep=0.05)

slider_e.on_changed(update)
slider_p.on_changed(update)

update(None)
plt.show()
