import numpy as np

MU_CANON  = 1.0           # DU^3 / TU^2
R_DU = 1.0          # DU

P = 2.25
e = 0.5
i = np.deg2rad(45)
Omega = np.deg2rad(30)
omega = 0
anamoly = 0

r = P/(1+e*np.cos(anamoly))
v = np.sqrt(MU_CANON/P*e)*np.sin(anamoly)