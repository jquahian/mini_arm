import ik_solver as ik
import time
import odrive
from odrive.enums import *

# identify boards
odrv0 = '207D37A53548'
odrv1 = '387F37573437'

is_connected = False
oboard = [odrv0, odrv1]

# connect to boards
def connect_to_boards():
	global oboard
	global is_connected

	# find the odrives
	print('connecting to odrives')

	oboard[0] = odrive.find_any(serial_number=odrv0)
	oboard[1] = odrive.find_any(serial_number=odrv1)
	is_connected = True

	print('boards connected')

# calibrate odrives and set to closed loop control
def calibrate_all():
	global oboard
	global is_connected

	if is_connected == False:
		print('Boards not connected')
		return
	
	for board in oboard:
		print(f'Joint {oboard.index(board) + 1} Calibrating')

		board.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

		while board.axis0.current_state != AXIS_STATE_IDLE:
				time.sleep(0.1)

		board.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

		print(f'Joint {oboard.index(board) + 1} calibrated and in closed loop control')

		time.sleep(0.5)

		print(f'Joint {oboard.index(board) + 1} Calibrating')

		board.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

		while board.axis1.current_state != AXIS_STATE_IDLE:
				time.sleep(0.1)

		board.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

		print(f'Joint {oboard.index(board) + 1} calibrated and in closed loop control')

	print('Joint calibration complete!')

def move_axis_absolute(drive_num, axis_num, axis_gear_ratio, degrees):
	global oboard
	global is_connected

	degrees = float(degrees)
 
	if axis_num == 0:
		oboard[drive_num].axis0.controller.input_pos = calculate_motor_turns(
			axis_gear_ratio, degrees)
		if drive_num == 0:
			ik.joint_angles[0] = degrees
		elif drive_num == 1:
			ik.joint_angles[3] = degrees
	elif drive_num == 1:
		oboard[drive_num].axis1.controller.input_pos = calculate_motor_turns(
			axis_gear_ratio, degrees)
		if drive_num == 0:
			ik.joint_angles[1] = degrees
		elif drive_num == 1:
			ik.joint_angles[4] = degrees
	
	print(ik.joint_angles)	

def calculate_motor_turns(gear_ratio, input_degrees):
	# calculates the number of motor turns to get to degrees based on gear ratio
	required_turns = (input_degrees * gear_ratio)/360
	return required_turns

def move_to_point(j4_x, j4_y, j4_z):
	j4_x = float(j4_x)
	j4_y = float(j4_y)
	j4_z = float(j4_z)

	joint_angles = ik.limit_check(j4_x, j4_y, j4_z)

	print(
		f'for coordinates x: {j4_x}, y: {j4_y}, z: {j4_z}, joint 2 angle: {joint_angles[0]} degrees, joint 3 angle: {joint_angles[2]} degrees')

	# move joint 2
	move_axis_absolute(oboard[0], 1, 5, joint_angles[0])

	# move joint 3
	move_axis_absolute(oboard[1], 0, -5, joint_angles[1])

	print(f'Joint 4 now at coordinates x: {j4_x}, y: {j4_y}, z: {j4_z}')
 