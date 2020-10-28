import ik_solver as ik
import time
import odrive
from odrive.enums import *

# identify boards
odrv0 = '20873592524B'
odrv1 = '387F37573437'

oboard = [odrv0, odrv1]

is_connected = False

# connect to boards
def connect_to_boards():
	# find the odrives
	oboard[0] = odrive.find_any(serial_number=board_1_num)
	oboard[1] = odrive.find_any(serial_number=board_2_num)
	is_connected = True

# calibrate odrives and set to closed loop control
def calibrate_all():
	if is_connected == False:
		print('Boards not connected')
		return
	
	print('\n\nbeginning calibration...')
	
	for drive in oboard:
		print(f'\nnow calibrating {drive} axis 0')
		drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		
		while drive.axis0.current_state != AXIS_STATE_IDLE:
			time.sleep(0.1)
		
		print(f'\n{drive} axis 0 in CLOSED LOOP CONTROL')
		drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
		
		time.sleep(0.2)
		
		print(f'\nnow calibrating {drive} axis 1')
		drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		
		while drive.axis1.current_state != AXIS_STATE_IDLE:
			time.sleep(0.1)
			
		print(f'\n{drive} axis 1 in CLOSED LOOP CONTROL')
		drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

def move_axis_absolute(drive_num, axis_num, axis_gear_ratio, degrees):
	degrees = float(degrees)
	
	if axis_num == 0:
		drive_num.axis0.controller.input_pos = calculate_motor_turns(
		axis_gear_ratio, degrees)
	elif axis_num == 1:
		drive_num.axis1.controller.input_pos = calculate_motor_turns(
			axis_gear_ratio, degrees)

	print(f'moving {drive_num} {axis_num} to {degrees} degrees absolute')

def calculate_motor_turns(gear_ratio, input_degrees):
	# calculates the number of motor turns to get to degrees based on gear ratio
	required_turns = (input_degrees * gear_ratio)/360
	return required_turns

def move_to_point(j4_x, j4_y, j4_z):
	j4_x = float(j4_x)
	j4_y = float(j4_y)
	j4_z = float(j4_z)

	joint_angles = ik.limit_check(j4_x, j4_z)

	print(
		f'for coordinates x: {j4_x}, z: {j4_z}, joint 2 angle: {joint_angles[0]} degrees, joint 3 angle: {joint_angles[1]} degrees')

	# move joint 2
	move_axis_absolute(oboard[0], 1, 5, joint_angles[0])

	# move joint 3
	move_axis_absolute(oboard[1], 0, 5, joint_angles[1])

	print(f'Joint 4 now at coordinates x: {j4_x}, z: {j4_z}')


def reboot_all_odrive():
	if is_connected == False:
		print('Boards not connected')
		return

	for board in oboard:
		print(f'Rebooting {board}')
		board.reboot()

