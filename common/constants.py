"""
Astrodynamics constants — all primary values defined in SI (metric) units.

Usage:
    from common.constants import MU_EARTH, ureg

    mu_ft = MU_EARTH.to("foot**3 / second**2").magnitude
    r_earth_ft = R_EARTH.to("foot").magnitude
"""

from pint import UnitRegistry

ureg = UnitRegistry()
Q = ureg.Quantity

# Earth gravitational parameter  [m^3/s^2]
MU_EARTH = Q(3.986004418e14, "meter**3 / second**2")

# Earth mean equatorial radius  [m]
R_EARTH = Q(6.3781e6, "meter")

# Earth mass  [kg]
M_EARTH = Q(5.9722e24, "kilogram")
