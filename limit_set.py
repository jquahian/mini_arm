import math
import ik
from controller import move_axis, return_joint_degrees, return_joint_numer
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

def single_angle_limit_check(drive_num, axis_num, gear_ratio, angle, is_absolute):
    joint_num = return_joint_numer(drive_num, axis_num)
    
    # determine if we want to move the arm relative to current position or to an absolute position
    if is_absolute == False:
        angle_check = return_joint_degrees(drive_num, axis_num, gear_ratio) + angle
    else:
        angle_check = angle
    
    if joint_num == 1:
        if angle_check > j1_theta_max or angle_check < j1_theta_min:
            error_string = 'joint angle 1 out of range'
            print(error_string)
            return
    elif joint_num == 2:
        if angle_check > j2_theta_max or angle_check < j2_theta_min:
            error_string = 'joint angle 2 out of range'
            print(angle_check)
            return
    elif joint_num == 3:
        if angle_check > j3_theta_max or angle_check < j3_theta_min:
            error_string = 'joint angle 3 out of range'
            print(error_string)
            return
    elif joint_num == 4:
        if angle_check > j4_theta_max or angle_check < j4_theta_min:
            error_string = 'joint angle 4 out of range'
            print(error_string)
            return
    
    move_axis(drive_num, axis_num, gear_ratio, angle, is_absolute)

def multi_angle_limit_check(angles):
    joint_1_theta = angles[0]
    joint_2_theta = angles[1]
    joint_3_theta = angles[2]
    joint_4_theta = angles[3]

    # wow this is ugly...
    if joint_1_theta > j1_theta_max or joint_1_theta < j1_theta_min \
    or joint_2_theta > j2_theta_max or joint_2_theta < j2_theta_min \
        or joint_3_theta > j3_theta_max or joint_3_theta < j3_theta_min \
            or joint_4_theta > j4_theta_max or joint_4_theta < j4_theta_min:
                print('Coordinate is reachable, but not within joint angle limits')
                return
    else:
        move_axis(0, 0, 5, joint_1_theta, True)
        move_axis(0, 1, 5, joint_2_theta, True)
        move_axis(1, 0, -5, joint_3_theta, True)
        move_axis(1, 1, 1, joint_4_theta, True)
        
        print('Valid solution angles')


def coordinate_limit_check(x, y, z):    
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
