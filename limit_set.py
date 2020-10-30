import math
import ik
from controller import move_axis_absolute

origin_x = 0
origin_y = 0
origin_z = 0

def angle_limit_check(joint_num, angle):
    if joint_num == 1 and angle > 120 or angle < -120:
        print('joint angle 1 out of range')
        return
    else:
        move_axis_absolute(0, 0, 5, angle)

    if joint_num == 2 and angle > 90 or angle < -90:
        print('joint angle 2 out of range')
        return
    else:
        move_axis_absolute(0, 1, 5, angle)
        
    if joint_num == 3 and angle > 90 or angle < -90:
        print('joint angle 3 out of range')
        return
    else:
        move_axis_absolute(1, 0, -5, angle)

    if joint_num == 4 and angle > 360 or angle < -360:
        print('joint angle 4 out of range')
        return
    else:
        move_axis_absolute(1, 1, 1, angle)

def coordinate_limit_check(x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    
    dist_to_point = math.sqrt(pow(x + origin_x, 2) + pow(y + origin_y, 2) + pow(z + origin_z, 2))
    
    # only accept positive x-coordinates and z not less than distance from j1 to j2
    if x < 0 or z < ik.j1_j2_length:
        print(f'x and/or z-coordinate(s) are invalid: x > 0, z < {ik.j1_j2_length}')
        return
    
    # if point the point x, y, z is greater than or equal the radius of the work volume sphere, reject
    if dist_to_point >= (ik.j2_j3_length + ik.j3_j4_length):
        print(f'coordinates of {x, y, z} are outside of work volume {dist_to_point}')    
        return
    
    ik.solve_ik(x, y, z)
