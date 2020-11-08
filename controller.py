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

def move_axis(drive_num, axis_num, axis_gear_ratio, degrees, is_absolute):
	global oboard
	global is_connected
 
	if is_connected == False:
		print('Arm not connected')
		return

	degrees = float(degrees)
	
	if is_absolute:
		if axis_num == 0:
			oboard[drive_num].axis0.controller.input_pos = calculate_motor_turns(
				axis_gear_ratio, degrees)
		elif axis_num == 1:
			oboard[drive_num].axis1.controller.input_pos = calculate_motor_turns(
				axis_gear_ratio, degrees)
	elif is_absolute == False:
		if axis_num == 0:
			oboard[drive_num].axis0.controller.move_incremental(calculate_motor_turns(
				axis_gear_ratio, degrees), False)
		elif axis_num == 1:
			oboard[drive_num].axis1.controller.move_incremental(calculate_motor_turns(
				axis_gear_ratio, degrees), False)

	joint_num = return_joint_numer(drive_num, axis_num)
	new_joint_angle = round(return_joint_degrees(drive_num, axis_num, axis_gear_ratio), 3)

	if is_absolute:
		print(f'Moving {joint_num} to {new_joint_angle} degrees')
	else:

		print(f'Moving {joint_num} by {degrees} degrees.  Current angle of {joint_num} is now: {new_joint_angle} degrees')		

def calculate_motor_turns(axis_gear_ratio, input_degrees):
	# calculates the number of motor turns to get to degrees based on gear ratio
	required_turns = (input_degrees * axis_gear_ratio)/360
	return required_turns

# returns the current angle of requested joint
def return_joint_degrees(drive_num, axis_num, axis_gear_ratio):
	global oboard
	global is_connected

	if is_connected == False:
		print('Arm not connected')
		return 0

	if axis_num == 0:
		joint_angle = (oboard[drive_num].axis0.controller.input_pos * 360 / axis_gear_ratio)
	elif axis_num == 1:
		joint_angle = (oboard[drive_num].axis1.controller.input_pos * 360 / axis_gear_ratio)

	return joint_angle

# returns the current velocity of the requested joint
def return_joint_velocity(drive_num, axis_num):
	global oboard
	global is_connected

	if is_connected == False:
		print('Arm not connected')
		return 0

	if axis_num == 0:
		joint_vel_est = oboard[drive_num].axis0.encoder.vel_estimate
	elif axis_num == 1:
		joint_vel_est = oboard[drive_num].axis1.encoder.vel_estimate
	
	return joint_vel_est

# returns a joint number for human feedback
def return_joint_numer(drive_num, axis_num):
	if drive_num == 0 and axis_num == 0:
		joint_num = 1
	elif drive_num == 0 and axis_num == 1:
		joint_num = 2
	elif drive_num == 1 and axis_num == 0:
		joint_num = 3
	elif drive_num == 1 and axis_num == 1:
		joint_num = 4
  
	return joint_num
