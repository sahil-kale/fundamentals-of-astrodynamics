## Chapter 1 — Two-Body Orbital Mechanics

| File | Description |
|------|-------------|
| `ch1/ex1.py` | Position/velocity → specific energy and angular momentum |
| `ch1/ex2.py` | Energy + eccentricity → orbital elements |
| `ch1/ex3.py` | Further chapter exercises |
| `ch1/conic_explorer.py` | Interactive conic section explorer (sliders: e, p) |
| `ch1/final_ex.py` | **Final exercise** — full orbit plotter (sliders: ε, h) |

### Running the orbit plotter

```bash
uv run ch1/final_ex.py
```

The orbit plotter has two panels:

- **Left** — Keplerian orbit around Earth with periapsis/apoapsis markers and an
  annotation box showing `e`, `p`, `a`, `T`, `r_periapsis`, `r_apoapsis`.
- **Right** — (h, ε) parameter space coloured by orbit family (elliptic / parabolic /
  hyperbolic), with constant-`e` contour lines and a marker showing the current state.

Two sliders drive everything:

| Slider | Symbol | Units | What it controls |
|--------|--------|-------|-----------------|
| `ε` | specific mechanical energy | km²/s² | orbit energy; negative → bound, zero → parabolic, positive → hyperbolic |
| `h` | specific angular momentum | km²/s² | shape within a given energy family |

### Exercise

`calc_orbit_params(epsilon, h)` in `ch1/final_ex.py` is left as a stub — implement it
to populate the `OrbitParams` dataclass.  Useful relations:

```
e   = sqrt(1 + 2·ε·h² / μ²)
p   = h² / μ
a   = −μ / (2·ε)               (undefined for parabola)
T   = 2π · sqrt(a³ / μ)        (elliptic only)
r_p = p / (1 + e)
r_a = p / (1 − e)              (elliptic only)
```

All quantities use km / s (μ = 398 600.4418 km³/s²).