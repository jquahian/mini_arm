import math
import limit_set as limit

# fixed joint lengths
j1_j2_length = 231.50
j2_j3_length = 77.279
j3_j4_length = 94.055
j4_tcp_length = 133.500
j3_tcp_length = j3_j4_length + j4_tcp_length

# has a div by zero error when entering xyz : 00z.  Needs exception for these coords
def solve_ik(x, y, z, joint_4):
    # projection of arm on xy plane
    xy_projection_length = math.sqrt(pow(x, 2) + pow(y, 2))
    
    # distance from j1_j2 to the end effector z position
    r3 = z - j1_j2_length
    
    j2_effector_length = math.sqrt(pow(xy_projection_length, 2) + pow(r3, 2))
    
    # find rotation of joint 1
    j1_theta = round(math.degrees(math.asin(x/xy_projection_length)), 3)
    
    # find angle between joint length 2 and joint length 3
    phi_3 = math.acos((pow(j2_effector_length, 2) - pow(j2_j3_length, 2) -
                       pow(j3_tcp_length, 2)) / (-2 * j2_j3_length * j3_tcp_length))
        
    # find rotation of joint 3
    j3_theta = round(math.degrees(math.radians(180) - phi_3), 3)
    
    # angle between the j2_effector_length and horizontal x-axis    
    phi_2 = math.acos((pow(j3_tcp_length, 2) - pow(j2_j3_length, 2) -
                       pow(j2_effector_length, 2)) / (-2 * j2_j3_length * j2_effector_length))
    
    # angle between the j2_effector_length and the vertical z-axis
    phi_1 = math.asin((z - j1_j2_length)/j2_effector_length)
    
    # find rotation of joint 2 -- relative to the horizontal axis
    j2_theta = round(math.degrees(phi_2 + phi_1 + math.radians(90)), 3)

    # need to correct which co-angle is chosen for each motor depending on motor configuration and ensure correct rotation direction
    if y < 0:
        j1_theta_motor = -(round(90 - j1_theta, 3))
    else:
        j1_theta_motor = (round(90 - j1_theta, 3))
    
    j2_theta_motor = round(180 - j2_theta, 3)
    j3_theta_motor = round(j3_theta, 3)
    
    # joint 4 (end effector) is independent from the IK solve, but must be passed in to check for limits
    joint_4_motor_theta = round(joint_4, 3)
    
    print(
        f'joint 1 target angle: {j1_theta} -- value to be passsed to motor is {j1_theta_motor}')
    print(
        f'joint 2 target angle: {j2_theta} -- value to be passsed to motor is {j2_theta_motor}')
    print(
        f'joint 3 target angle: {j3_theta} -- value to be passsed to motor is {j3_theta_motor}')
    print(
        f'joint 4 moving to {joint_4_motor_theta}')
    
    # angle checks
    limit.multi_angle_limit_check(
        [j1_theta_motor, j2_theta_motor, j3_theta_motor, joint_4_motor_theta])
    
    return (j1_theta_motor, j2_theta_motor, j3_theta_motor, x, y, z)

# # for tests
# solve_ik(106.066, 106.066, 130)
