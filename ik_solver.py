import math

# test joint 4 coords
# j4_x = 155.6
# j4_y = 0
# j4_z = 210.5

# legnth offset for added tools
effector_length = 0

# fixed joint lengths
j1_j2_length = 231.5
j2_j3_length = 77.279
j3_j4_length = 94.054 + effector_length

# set joint 2 and joint 3 angle minimums and maximums
j2_theta_min = 90
j2_theta_max = 270

j3_theta_min = 90
j3_theta_max = 180

# inverse kin
def solve_joint_2_3_angles(j4_x, j4_z):
    # determine length from base to end effector
    j1_effector_length = math.sqrt(pow(j4_x, 2) + pow(j4_z, 2))
    
    # angle between j1 and effector on the xz plane relative to the (horizontal) x axis
    j1_effector_xz_theta = math.acos(j4_x/j1_effector_length)

    # angle between j1 and effector on the xz plane relative to the (vertical) z axis
    j1_effector_xz_cotheta = math.radians(90) - j1_effector_xz_theta

    # determine distance between j2 and end effector using cosine law
    j2_effector_length = (math.sqrt(pow(j1_j2_length, 2) + pow(j1_effector_length, 2) 
                                    - 2 * j1_j2_length * j1_effector_length * math.cos(j1_effector_xz_cotheta)))
    
    # determine joint angle for joint 3
    j3_theta = (math.acos((pow(j2_effector_length, 2) - pow(j2_j3_length, 2) -pow(j3_j4_length, 2)) 
                          / (-2 * j2_j3_length * j3_j4_length)))
    
    # determine the first component angle for theta 2
    j2_theta_alpha = math.asin((j1_effector_length * math.sin(j1_effector_xz_cotheta)) / j2_effector_length)
    
    # check if there are other possible angles
    possible_angles = sin_ambiguity_check(j2_theta_alpha, j1_effector_xz_cotheta)
    
    if len(possible_angles) > 1:
        j2_theta_alpha = verify_ambiguious_angle(j1_effector_xz_cotheta, j1_j2_length, j2_effector_length, j1_effector_length)
        
        for angles in possible_angles:
            angles = math.degrees(angles)
            print(f'joint 2 theta alpha possible angle is: {angles} degrees')
    else:
        print('no ambiguity for j2_theta_alpha')
    
    # determine the second component angle for theta 2
    j2_theta_beta = math.asin((j3_j4_length * math.sin(j3_theta)) / j2_effector_length)
    
    # check if there are other possible angles
    possible_angles = sin_ambiguity_check(j2_theta_beta, j3_theta)
    
    if len(possible_angles) > 1:
        j2_theta_beta = verify_ambiguious_angle(j3_theta, j2_effector_length, j2_j3_length, j3_j4_length)
    
        for angles in possible_angles:
            angles = math.degrees(angles)
            print(f'joint 2 theta beta possible angle is: {angles} degrees')
    else:
        print('no ambiguity for j2_theta_beta')
    
    # determnine joint angle for joint 2
    j2_theta = j2_theta_alpha + j2_theta_beta
    
    j2_theta = round(math.degrees(j2_theta), 3)
    j3_theta = round(math.degrees(j3_theta), 3)
    
    joint_angles = [j2_theta, j3_theta]
    
    return joint_angles

# check if the supplied coordinates are within the reach of the robot and within safety limits
def limit_check(j4_x, j4_z):
    full_robot_radius = round(j1_j2_length + j2_j3_length + j3_j4_length, 3)
    minimum_z = round(j1_j2_length - j3_j4_length, 3)
    maximum_x_y = round(j2_j3_length + j3_j4_length, 3)
    
    if j4_x > maximum_x_y:
        return print(f'x and/or y-coordinate(s) outside of bounds.  Must be below x or y = {maximum_x_y}')
        
    if j4_z > full_robot_radius or j4_z < minimum_z:
        return print(
            f'z coordinate outside of bounds.  Must be below z = {full_robot_radius} and above z = {minimum_z}')

    return solve_joint_2_3_angles(j4_x, j4_z)

# determine if we have inputs with multiple angle solution
def sin_ambiguity_check(solved_angle, known_angle):
    ambiguous_angle = math.radians(180) - solved_angle
    possible_angles = [solved_angle]
    
    if ambiguous_angle + known_angle < math.radians(180):
        possible_angles.append(ambiguous_angle)
        return possible_angles
    else:
        return possible_angles

# if there are any ambiguous angles, determine which one is correct
def verify_ambiguious_angle(verified_angle, verified_edge_length_1, verified_edge_length_2, ambiguous_edge_length):
    verified_angle = (math.acos((pow(ambiguous_edge_length, 2) - pow(verified_edge_length_1, 2) - pow(verified_edge_length_2, 2))
                                / (-2 * verified_edge_length_1 * verified_edge_length_2)))
    
    return verified_angle
