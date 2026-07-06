import numpy as np

MU_CANON  = 1.0           # DU^3 / TU^2
R_EARTH_DU = 1.0          # DU

# givens
r = np.array([2, 0, 0])
v = np.array([0, 1, 0])

h = np.cross(r, v)

p = np.linalg.norm(h**2)/MU_CANON
e = 1/MU_CANON * ((np.linalg.norm(v**2) - MU_CANON/np.linalg.norm(r)) * r - r.dot(v) * v)
e = np.linalg.norm(e)

I = np.array([1,0,0])
J = np.array([0,1,0])
K = np.array([0,0,1])

n = np.cross(K, h)

i = np.arccos(h.dot(K)/np.linalg.norm(h))

breakpoint()