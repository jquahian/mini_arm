import math
import ik
from controller import move_axis_absolute

origin_x = 0
origin_y = 0
origin_z = ik.j1_j2_length

j1_theta_min = -90
j1_theta_max = 90

j2_theta_min = -90
j2_theta_max = 90

j3_theta_min = -90
j3_theta_max = 90

j4_theta_min = -360
j4_theta_max = 360

def single_angle_limit_check(joint_num, angle):
    joint_num = float(joint_num)
    angle = float(angle)
    
    if joint_num == 1:
        if angle > j1_theta_max or angle < j1_theta_min:
            error_string = 'joint angle 1 out of range'
        else:
            move_axis_absolute(0, 0, 5, angle)

    if joint_num == 2:
        if angle > j2_theta_max or angle < j2_theta_min:
            error_string = 'joint angle 2 out of range'
        else:
            move_axis_absolute(0, 1, 5, angle)
        
    if joint_num == 3:
        if angle > j3_theta_max or angle < j3_theta_min:
            error_string = 'joint angle 3 out of range'
        else:
            move_axis_absolute(1, 0, -5, angle)

    if joint_num == 4:
        if angle > j4_theta_max or angle < j4_theta_min:
            error_string = 'joint angle 4 out of range'
        else:
            move_axis_absolute(1, 1, 1, angle)
        
    print(error_string)

def multi_angle_limit_check(angles):
    joint_1_theta = float(angles[0])
    joint_2_theta = float(angles[1])
    joint_3_theta = float(angles[2])
    joint_4_theta = float(angles[3])

    # wow this is ugly...
    if joint_1_theta > j1_theta_max or joint_1_theta < j1_theta_min \
    or joint_2_theta > j2_theta_max or joint_2_theta < j2_theta_min \
        or joint_3_theta > j3_theta_max or joint_3_theta < j3_theta_min \
            or joint_4_theta > j4_theta_max or joint_4_theta < j4_theta_min:
                print('Coordinate is reachable, but not within joint angle limits')
                return
    else:
        move_axis_absolute(0, 0, 5, joint_1_theta)
        move_axis_absolute(0, 1, 5, joint_2_theta)
        move_axis_absolute(1, 0, -5, joint_3_theta)
        move_axis_absolute(1, 1, 1, joint_4_theta)
        
        print('Valid solution angles')


def coordinate_limit_check(x, y, z):
    x = float(x)
    y = float(y)
    z = float(z)
    
    dist_to_point = math.sqrt(pow(x - origin_x, 2) + pow(y - origin_y, 2) + pow(z - origin_z, 2))
    
    # only accept positive x-coordinates and z not less than distance from j1 to j2
    if x < 0 or z < ik.j1_j2_length:
        print(f'x and/or z-coordinate(s) are invalid: x > 0, z > {ik.j1_j2_length}')
        return
    
    # if point the point x, y, z is greater than or equal the radius of the work volume sphere, reject
    elif dist_to_point >= (ik.j2_j3_length + ik.j3_j4_length):
        print(f'coordinates of {x, y, z} are outside of work volume {dist_to_point}')    
        return
    
    ik.solve_ik(x, y, z)
