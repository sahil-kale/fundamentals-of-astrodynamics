import numpy as np

EQUATORIAL_RADIUS_KM = 6378.145
ALT_ABOVE_MSL_DU = 6.378/6379
ECCENTRICTY_EARTH = 0.08182
POLAR_RADIUS_EARTH_KM = 6356 

LONG_W_DEG = 57.296
LATITUDE_DEG = 0 # equator
THETA_GO_JAN_1_1970_RAD = 1.74933340
THETA_INCREMENT_PER_DAY = 1.0027379093

DAYS_SINCE_THETA_GO = 1.25

theta_greenwhich = THETA_GO_JAN_1_1970_RAD + THETA_INCREMENT_PER_DAY * 2 * np.pi * DAYS_SINCE_THETA_GO
theta = theta_greenwhich - np.deg2rad(LONG_W_DEG) # subtract longitude E

# find X/Z projection
x = np.abs(1/(np.sqrt(1 - ECCENTRICTY_EARTH**2 * np.sin(np.deg2rad(LATITUDE_DEG)))) + ALT_ABOVE_MSL_DU) * np.cos(np.deg2rad(LATITUDE_DEG))
z = np.abs(1/(np.sqrt(1 - ECCENTRICTY_EARTH**2 * np.sin(np.deg2rad(LATITUDE_DEG)))) + ALT_ABOVE_MSL_DU) * np.sin(np.deg2rad(LATITUDE_DEG))

# now, find in IJK form
i_vec = x * np.cos(theta)
j_vec = x * np.sin(theta)
k_vec = z