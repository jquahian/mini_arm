import ik_solver
import time
# import odrive
# from odrive.enums import *

# identify boards
j1_j2_drive = '20873592524B'
j3_j4_drive = '387F37573437'

board_array = [j1_j2_drive, j3_j4_drive]

# connect to boards
def connect_to_boards():
	# find the odrives
	board_array[0] = odrive.find_any(serial_number=board_1_num)
	board_array[1] = odrive.find_any(serial_number=board_2_num)

# calibrate odrives and set to closed loop control
def calibrate_all():
	print('\n\nbeginning calibration...')

	for board in board_array:

		print(f'\nnow calibrating {board} axis 0')
		board.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		while board.axis0.current_state != AXIS_STATE_IDLE:
			time.sleep(0.1)

		print(f'\n{board} axis 0 in CLOSED LOOP CONTROL')
		board.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

		time.sleep(0.5)

		print(f'\nnow calibrating {board} axis 1')
		board.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
		while board.axis1.current_state != AXIS_STATE_IDLE:
			time.sleep(0.1)

		print(f'\n{board} axis 1 in CLOSED LOOP CONTROL')
		board.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# set control

# input positions
