import numpy as np
from common.constants import MU_EARTH

specific_mechanical_energy = -2.0*10**8
e = 0.2

mu = MU_EARTH.to("foot**3 / second**2").magnitude

semi_major_axis = -mu / (2 * specific_mechanical_energy)
semi_latus_rectum = semi_major_axis * (1 - e**2)
specific_angular_momentum = np.sqrt(semi_latus_rectum * mu)

print(f"Semi-major axis: {semi_major_axis:.4e} ft  (expected 3.5191e7)")
print(f"Semi-latus rectum: {semi_latus_rectum:.4e} ft  (expected 3.3790e7)")
print(f"Specific angular momentum: {specific_angular_momentum:.4e} ft^2/s  (expected 6.897e11)")
