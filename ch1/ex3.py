import numpy as np
from common.constants import MU_EARTH
from pint import UnitRegistry
ureg = UnitRegistry()

e  = 0.1
perigee_alt = 200 * ureg.nautical_mile

# Determine apogee (r_a), Specific Mechanical Energy (E), Specific Angular Momentum (h)
a = perigee_alt.to(ureg.feet) / (1-e)
p = perigee_alt.to(ureg.feet) * (1+e)

apogee_alt = p / (1-e)

mu = MU_EARTH.to("foot**3 / second**2").magnitude
specific_mechanical_energy = -mu/(2 * a)
specific_angular_momentum = np.sqrt(p * mu)

# Print results (print apogee in nautical miles)
print(f"Apogee altitude: {apogee_alt.to(ureg.nautical_mile).magnitude} nautical miles")
print(f"Specific Mechanical Energy: {specific_mechanical_energy:.4e} ft^2/s^2")
print(f"Specific Angular Momentum: {specific_angular_momentum:.4e} ft^2/s")