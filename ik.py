import math
from controller import move_to_point

# fixed joint lengths
j1_j2_length = 100
j2_j3_length = 100
j3_j4_length = 100

def solve_ik(x, y, z):
    # projection of arm on xy plane
    xy_projection_length = math.sqrt(pow(x, 2) + pow(y, 2))
    
    # distance from j1_j2 to the end effector z position
    r3 = z - j1_j2_length
    
    j2_effector_length = math.sqrt(pow(xy_projection_length, 2) + pow(r3, 2))
    
    # find rotation of joint 1
    j1_theta = math.degrees(math.atan(r3/xy_projection_length))
    
    # find angle between joint length 2 and joint length 3
    phi_3 = math.acos((pow(j2_effector_length, 2) - pow(j2_j3_length, 2) -
                       pow(j3_j4_length, 2)) / (-2 * j2_j3_length * j3_j4_length))
        
    # find rotation of joint 3
    j3_theta = math.degrees(math.radians(180) - phi_3)
    
    # angle between the j2_effector_length and horizontal x-axis    
    phi_2 = math.acos((pow(j3_j4_length, 2) - pow(j2_j3_length, 2) -
                       pow(j2_effector_length, 2)) / (-2 * j2_j3_length * j2_effector_length))
    
    # angle between the j2_effector_length and the vertical z-axis
    phi_1 = math.asin((z - j1_j2_length)/j2_effector_length)
    
    # find rotation of joint 2 -- relative to the horizontal axis
    j2_theta = math.degrees(phi_2 + phi_1 + math.radians(90))
    
    print(f'joint 1 target angle: {j1_theta}')
    print(f'joint 2 target angle: {j2_theta}')
    print(f'joint 3 target angle: {j3_theta}')
    
    move_to_point(j1_theta, j2_theta, j3_theta, x, y, z)
    return (j1_theta, j2_theta, j3_theta, x, y, z)

# # testing only!
# solve_ik(106.066, 106.066, 130)
