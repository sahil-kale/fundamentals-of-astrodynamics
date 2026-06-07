import numpy as np
from common.constants import MU_EARTH
from pint import UnitRegistry
ureg = UnitRegistry()

e = 0.1
perigee_alt = 200 * ureg.nautical_mile

R_EARTH = 3443.9 * ureg.nautical_mile  # Earth's mean radius
r_p = (R_EARTH + perigee_alt).to(ureg.nautical_mile)
p = r_p * (1 + e)
r_a = p / (1 - e)
apogee_alt = r_a - R_EARTH

a = (r_a + r_p) / 2

mu = MU_EARTH.to("foot**3 / second**2").magnitude

p_ft = p.to(ureg.feet).magnitude
a_ft = a.to(ureg.feet).magnitude

specific_mechanical_energy = -mu / (2 * a_ft)
specific_angular_momentum = np.sqrt(p_ft * mu)

print(f"r_p: {r_p:.1f}")                        # Should be ~3643.9 n.mi
print(f"Apogee altitude: {apogee_alt.to(ureg.nautical_mile):.1f}")  # Should be ~1009.8 n.mi
print(f"Specific Mechanical Energy: {specific_mechanical_energy:.3e} ft^2/s^2")  # ~-2.861e8
print(f"Specific Angular Momentum: {specific_angular_momentum:.3e} ft^2/s")     # ~5.855e11