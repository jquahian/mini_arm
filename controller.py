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
	print('Connecting to arm')

	oboard[0] = odrive.find_any(serial_number=odrv0)
	oboard[1] = odrive.find_any(serial_number=odrv1)
	is_connected = True

	print('Arm connected')

# calibrate odrives and set to closed loop control
def calibrate_all():
	global oboard
	global is_connected

	if is_connected == False:
		print('Arm not connected')
		return
	
	for board in oboard:
		board.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

		while board.axis0.current_state != AXIS_STATE_IDLE:
				time.sleep(0.1)

		board.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

		time.sleep(0.5)

		board.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

		while board.axis1.current_state != AXIS_STATE_IDLE:
				time.sleep(0.1)

		board.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

	print('Joint calibration complete!')

def move_axis_absolute(drive_num, axis_num, axis_gear_ratio, degrees):
	global oboard
	global is_connected
 
	if is_connected == False:
		print('Arm not connected')
		return

	degrees = float(degrees)
 
	if axis_num == 0:
		oboard[drive_num].axis0.controller.input_pos = calculate_motor_turns(
			axis_gear_ratio, degrees)
	elif axis_num == 1:
		oboard[drive_num].axis1.controller.input_pos = calculate_motor_turns(
			axis_gear_ratio, degrees)

	if drive_num == 0 and axis_num == 0:
		joint_num = 1
	elif drive_num == 0 and axis_num == 1:
		joint_num = 2
	elif drive_num == 1 and axis_num == 0:
		joint_num = 3
	elif drive_num == 1 and axis_num == 1:
		joint_num = 4

	print(f'Moving joint {joint_num} to {degrees}')

def calculate_motor_turns(gear_ratio, input_degrees):
	# calculates the number of motor turns to get to degrees based on gear ratio
	required_turns = (input_degrees * gear_ratio)/360
	return required_turns
