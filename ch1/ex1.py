import numpy as np
from common.constants import MU_EARTH

# Units: feet and ft/sec (as in the textbook)
pos_vector = np.array([4.1852, 6.2778, 10.463]) * 1e7   # ft
vel_vector = np.array([2.5936, 5.1872, 0.0])    * 1e4   # ft/sec

r_mag = np.linalg.norm(pos_vector)
v_mag = np.linalg.norm(vel_vector)
print(f"r = {r_mag:.4e} ft  (expected 12.899e7)")
print(f"v = {v_mag:.4e} ft/s (expected 5.7995e4)")

mu = MU_EARTH.to("foot**3 / second**2").magnitude

specific_mechanical_energy = (v_mag**2)/2 - mu/r_mag
print(f"\nSpecific Mechanical Energy: {specific_mechanical_energy:.4e} ft^2/s^2")
print(f"  (expected 1.573e9)")

# Angular momentum
h = np.cross(pos_vector, vel_vector)
h_mag = np.linalg.norm(h)
print(f"\nSpecific Angular Momentum: {h_mag:.4e} ft^2/s")
print(f"  (expected 6.0922e12)")

# Flight-path angle using h = r*v*cos(phi)
cos_phi = h_mag / (r_mag * v_mag)
phi = np.degrees(np.arccos(cos_phi))
print(f"\nFlight-path angle phi: {phi:.2f}°  (expected 35.42°)")
