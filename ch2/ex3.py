import numpy as np

RADAR_STATION_LONGITUDE_DEG_W = 169
RADAR_STATION_LATITUDE_DEG = 30
GREENWHICH_ANGLE_DEG = 304
SEZ_VECTOR_RADAR_TO_SATTELITE = np.array([2, -1, 1.5]) 

def get_rot_about_y_axis(theta: float):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    matrix = [
        [cos_theta, 0, -sin_theta],
        [0, 1, 0,],
        [sin_theta, 0, cos_theta]
    ]
    return np.array(matrix)

def get_rot_about_z_axis(theta: float):
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    matrix = [
        [cos_theta, sin_theta, 0],
        [-sin_theta, cos_theta, 0],
        [0, 0, 1]
    ]
    return np.array(matrix)

colatitude_rotation = get_rot_about_y_axis(np.deg2rad(90-RADAR_STATION_LATITUDE_DEG))
HOUR_DEGREES_CORRECTION = GREENWHICH_ANGLE_DEG -  RADAR_STATION_LONGITUDE_DEG_W
longitude_rotation = get_rot_about_z_axis(np.deg2rad(HOUR_DEGREES_CORRECTION))

D = colatitude_rotation @ longitude_rotation   # swap back to this order
D_inv = D.T
print(D_inv)

r_ijk = D_inv @ SEZ_VECTOR_RADAR_TO_SATTELITE
print(r_ijk) 