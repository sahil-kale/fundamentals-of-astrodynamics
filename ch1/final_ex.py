"""
Chapter 1 — Final Exercise: Orbit Plotter

Vary specific mechanical energy (ε) and specific angular momentum (h) with
sliders to see how orbit shape and parameters change.

Left panel  : orbit trajectory around Earth with periapsis/apoapsis markers
Right panel : (h, ε) parameter space colour-coded by orbit family

All quantities are in km / s / s² (i.e. km-based SI).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# ── Constants (km-based) ──────────────────────────────────────────────────────

MU      = 398_600.4418   # km³/s²  — Earth gravitational parameter
R_EARTH = 6_371.0        # km      — Earth mean radius

# ── Orbital parameters dataclass ──────────────────────────────────────────────

@dataclass
class OrbitParams:
    """Classical Keplerian elements derived from (ε, h)."""

    epsilon: float
    """Specific mechanical energy [km²/s²].  ε < 0 → elliptic, ε = 0 → parabolic, ε > 0 → hyperbolic."""

    h: float
    """Specific angular momentum [km²/s]."""

    e: float
    """Eccentricity [dimensionless].  0 → circle, 0 < e < 1 → ellipse, e = 1 → parabola, e > 1 → hyperbola."""

    p: float
    """Semi-latus rectum [km]."""

    orbit_type: str
    """Human-readable orbit family: "Circle" | "Ellipse" | "Parabola" | "Hyperbola"."""

    a: Optional[float]
    """Semi-major axis [km].  None for parabolic trajectory (ε = 0)."""

    period: Optional[float]
    """Orbital period [s].  None for parabolic / hyperbolic trajectories."""

    r_periapsis: float
    """Periapsis radius measured from Earth's centre [km]."""

    r_apoapsis: Optional[float]
    """Apoapsis radius measured from Earth's centre [km].  None for parabola / hyperbola."""


# ── Exercise: derive orbital elements from (ε, h) ────────────────────────────

def calc_orbit_params(epsilon: float, h: float) -> OrbitParams:
    """
    Derive Keplerian orbital elements from specific energy and angular momentum.

    Parameters
    ----------
    epsilon : float
        Specific mechanical energy [km²/s²].
        epsilon < 0  →  bound (elliptic / circular) orbit
        epsilon == 0 →  parabolic escape trajectory
        epsilon > 0  →  hyperbolic escape trajectory
    h : float
        Specific angular momentum [km²/s].  Must be > 0.

    Returns
    -------
    OrbitParams
        All classical elements plus derived quantities.

    Useful relations
    ----------------
        e   = sqrt(1 + 2·ε·h² / μ²)
        p   = h² / μ
        a   = −μ / (2·ε)               (undefined when ε = 0)
        T   = 2π · sqrt(a³ / μ)        (elliptic only)
        r_p = p / (1 + e)
        r_a = p / (1 − e)              (elliptic only)
    """
    p = h**2 / MU  # semi-latus rectum — valid for all conic sections

    EPS_TOL = 1e-6
    if abs(epsilon) < EPS_TOL:           # ── parabolic ──────────────────────
        e = 1.0
        a = None
        period = None
        r_a = None
        orbit_type = "Parabola"

    elif epsilon < 0:                    # ── elliptic / circular ────────────
        e = float(np.sqrt(max(0.0, 1.0 + (2.0 * epsilon * h**2) / MU**2)))
        a = -MU / (2.0 * epsilon)
        period = 2.0 * np.pi * np.sqrt(a**3 / MU)
        r_a = p / (1.0 - e)
        orbit_type = "Circle" if e < 1e-4 else "Ellipse"

    else:                                # ── hyperbolic ─────────────────────
        e = float(np.sqrt(1.0 + (2.0 * epsilon * h**2) / MU**2))
        a = -MU / (2.0 * epsilon)        # negative by convention for hyperbola
        period = None
        r_a = None
        orbit_type = "Hyperbola"

    r_p = p / (1.0 + e)

    return OrbitParams(
        epsilon=epsilon,
        h=h,
        e=e,
        p=p,
        orbit_type=orbit_type,
        a=a,
        period=period,
        r_periapsis=r_p,
        r_apoapsis=r_a,
    )


# ── Trajectory geometry ───────────────────────────────────────────────────────

def _orbit_xy(params: OrbitParams, clip_factor: float = 8.0) -> tuple[np.ndarray, np.ndarray]:
    """Return Cartesian (x, y) arrays tracing the orbit, clipped at clip_factor * p."""
    e, p = params.e, params.p

    if abs(e - 1.0) < 1e-4:          # parabola
        theta = np.linspace(-2.8, 2.8, 3000)
    elif e > 1.0:                     # hyperbola — near branch only
        theta_max = np.arccos(-1.0 / e) * 0.97
        theta = np.linspace(-theta_max, theta_max, 3000)
    else:                             # circle / ellipse
        theta = np.linspace(-np.pi, np.pi, 1000)

    r = p / (1.0 + e * np.cos(theta))
    mask = (r > 0) & (r < clip_factor * p)
    r, theta = r[mask], theta[mask]
    return r * np.cos(theta), r * np.sin(theta)


# ── Parameter-space background (static, drawn once) ──────────────────────────

def _draw_param_space(ax: plt.Axes, h_range: tuple, eps_range: tuple) -> None:
    hv = np.linspace(h_range[0],   h_range[1],   400)
    ev = np.linspace(eps_range[0], eps_range[1], 300)
    H, E = np.meshgrid(hv, ev)

    disc = 1.0 + 2.0 * E * H**2 / MU**2
    family = np.where(E < -1e-3, 0, np.where(E > 1e-3, 2, 1))
    family = np.where(disc < 0, -1, family)   # -1 = unphysical (discriminant imaginary)

    cmap = mcolors.ListedColormap(["#cccccc", "#aec6e8", "#c8e6c9", "#ffcdd2"])
    norm = mcolors.BoundaryNorm([-1.5, -0.5, 0.5, 1.5, 2.5], cmap.N)
    ax.pcolormesh(hv, ev, family, cmap=cmap, norm=norm, shading="auto", alpha=0.55)

    # e = const contour curves:  ε = (e²−1)·μ²/(2·h²)
    for e_val in [0.0, 0.25, 0.5, 0.75, 1.0]:
        eps_curve = (e_val**2 - 1.0) * MU**2 / (2.0 * hv**2)
        valid = (eps_curve >= eps_range[0]) & (eps_curve <= eps_range[1])
        if valid.any():
            ax.plot(hv[valid], eps_curve[valid], "k--", lw=0.8, alpha=0.45)
            mid = np.where(valid)[0][len(np.where(valid)[0]) // 2]
            ax.annotate(
                f"e={e_val}", (hv[mid], eps_curve[mid]),
                fontsize=7, ha="center", va="bottom", color="black", alpha=0.65,
            )

    ax.axhline(0.0, color="darkgreen", lw=1.2, alpha=0.7, zorder=3)

    ax.set_xlabel("h  [km²/s]")
    ax.set_ylabel("ε  [km²/s²]")
    ax.set_title("Parameter space  (ε, h)")
    ax.legend(
        handles=[
            mpatches.Patch(color="#aec6e8", label="Elliptic  (ε < 0)"),
            mpatches.Patch(color="#c8e6c9", label="Parabolic (ε = 0)"),
            mpatches.Patch(color="#ffcdd2", label="Hyperbolic (ε > 0)"),
            mpatches.Patch(color="#cccccc", label="Unphysical"),
        ],
        loc="lower right", fontsize=7,
    )


# ── Figure layout ─────────────────────────────────────────────────────────────

# Initial values: roughly circular LEO at ~400 km altitude
EPS_INIT = -29.4      # km²/s²
H_INIT   = 51_984.0   # km²/s

EPS_MIN, EPS_MAX = -80.0,    10.0
H_MIN,   H_MAX   =  20_000., 160_000.

fig = plt.figure(figsize=(15, 7))
fig.suptitle("Orbit Plotter — Earth  (km, km²/s units)", fontsize=12)
plt.subplots_adjust(bottom=0.20, wspace=0.32)

gs     = gridspec.GridSpec(1, 2, figure=fig)
ax_orb = fig.add_subplot(gs[0, 0])
ax_ps  = fig.add_subplot(gs[0, 1])

# Earth disc
ax_orb.add_patch(plt.Circle((0, 0), R_EARTH, color="#4da6ff", alpha=0.4, zorder=2))
ax_orb.plot(0, 0, "r*", ms=10, zorder=5, label="Earth centre")
ax_orb.set_aspect("equal")
ax_orb.grid(True, alpha=0.3)
ax_orb.axhline(0, color="k", lw=0.4)
ax_orb.axvline(0, color="k", lw=0.4)
ax_orb.set_xlabel("x  [km]")
ax_orb.set_ylabel("y  [km]")
ax_orb.set_title("Orbit")

# Dynamic orbit artists
(orbit_line,) = ax_orb.plot([], [], "b-",  lw=2,  label="Orbit",     zorder=3)
(peri_dot,)   = ax_orb.plot([], [], "go",  ms=9,  zorder=4, label="Periapsis")
(apo_dot,)    = ax_orb.plot([], [], "r^",  ms=9,  zorder=4, label="Apoapsis")
orbit_info    = ax_orb.text(
    0.02, 0.98, "", transform=ax_orb.transAxes,
    va="top", fontsize=9, fontfamily="monospace",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.75),
)
ax_orb.legend(loc="upper right", fontsize=8)

# Parameter-space panel
_draw_param_space(ax_ps, (H_MIN, H_MAX), (EPS_MIN, EPS_MAX))
(ps_marker,) = ax_ps.plot([], [], "k*", ms=13, zorder=6, label="Current (ε, h)")
ax_ps.legend(loc="upper left", fontsize=7)

# ── Sliders ───────────────────────────────────────────────────────────────────

ax_sl_eps = plt.axes([0.10, 0.10, 0.82, 0.03])
ax_sl_h   = plt.axes([0.10, 0.05, 0.82, 0.03])

slider_eps = Slider(ax_sl_eps, "ε  [km²/s²]", EPS_MIN, EPS_MAX, valinit=EPS_INIT, valstep=0.5)
slider_h   = Slider(ax_sl_h,   "h  [km²/s]",  H_MIN,   H_MAX,   valinit=H_INIT,   valstep=500.0)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fmt_period(T_sec: float) -> str:
    h_part, rem = divmod(T_sec, 3600.0)
    m_part = rem / 60.0
    return f"{int(h_part)}h {m_part:.1f}min" if h_part else f"{m_part:.1f} min"


def _build_info(params: OrbitParams) -> str:
    lines = [
        f"Type  : {params.orbit_type}",
        f"ε     = {params.epsilon:.2f} km²/s²",
        f"h     = {params.h:.0f} km²/s",
        f"e     = {params.e:.4f}",
        f"p     = {params.p:.1f} km",
    ]
    if params.a is not None:
        lines.append(f"a     = {params.a:.1f} km")
    if params.period is not None:
        lines.append(f"T     = {_fmt_period(params.period)}")
    lines.append(f"r_peri= {params.r_periapsis:.1f} km  (alt {params.r_periapsis - R_EARTH:.1f} km)")
    if params.r_apoapsis is not None:
        lines.append(f"r_apo = {params.r_apoapsis:.1f} km  (alt {params.r_apoapsis - R_EARTH:.1f} km)")
    return "\n".join(lines)


# ── Update callback ───────────────────────────────────────────────────────────

def update(_) -> None:
    eps = slider_eps.val
    h   = slider_h.val

    # Move parameter-space marker regardless of whether math is done yet
    ps_marker.set_data([h], [eps])

    try:
        params = calc_orbit_params(eps, h)
    except NotImplementedError:
        orbit_info.set_text("⚠ calc_orbit_params not yet implemented")
        orbit_line.set_data([], [])
        peri_dot.set_data([], [])
        apo_dot.set_data([], [])
        fig.canvas.draw_idle()
        return

    x, y = _orbit_xy(params)
    orbit_line.set_data(x, y)

    # Periapsis at θ = 0 → (+r_p, 0)
    peri_dot.set_data([params.r_periapsis], [0.0])

    # Apoapsis at θ = π → (−r_a, 0)  — elliptic only
    if params.r_apoapsis is not None:
        apo_dot.set_data([-params.r_apoapsis], [0.0])
    else:
        apo_dot.set_data([], [])

    if len(x):
        lim = max(float(np.max(np.abs(x))), float(np.max(np.abs(y)))) * 1.2
        lim = max(lim, R_EARTH * 2.5)
        ax_orb.set_xlim(-lim, lim)
        ax_orb.set_ylim(-lim, lim)

    orbit_info.set_text(_build_info(params))
    fig.canvas.draw_idle()


slider_eps.on_changed(update)
slider_h.on_changed(update)

update(None)
plt.show()
