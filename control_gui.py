import PySimpleGUI as sg
import controller
import limit_set as limit
import octoprint_listener as listener
import json
import instruction_parser as instruct
import clear_bed_detect

sg.theme('DarkBlack')
sg.SetOptions(font='Helvetica 12', auto_size_buttons=True)

# initial state of joint angles
joint_angles = [0, -35, 75, -150]

# zero'd position for joints 1, 2, 3, 4
home_angles = [0, 0, 0, 0]

# joint 4 zero position: want the option to control this independently of other joints
j4_angle = 0

# position of joint 4 in xyz space
point_coordinates = [0, 0, 0]

# initial status of connection to all printers
prusa_1_connected = False
prusa_6_connected = False

stream_data = False

# time in ms to poll octoprint/stream other data source
timeout = 2500

multi_point_instruction_num = 0

# set if we want printer(s) to keep printing indefinitely
p1_print_loop = False
p6_print_loop = False

# in case we ever need to stream data other than octoprint
# not sure how to do this if not all or nothing...
# once connected, how do we disconnect a specific printer?
def stream_data_toggle():
    global stream_data

    if not stream_data:
        stream_data = True
    else:
        stream_data = False

# pass in the ip + api key in external json file to octoprint
def connect_printer(printer_num):
    with open('printer_octoprint_data.txt') as json_file:
        data = json.load(json_file)
        printer_name = (data['printer_stats'][printer_num]['printer_name'])
        printer_api_key = (data['printer_stats'][printer_num]['api_key'])
        printer_data = (data['printer_stats'][printer_num]['printer_info'])
        
        printer_info_url = printer_data + f'?apikey={printer_api_key}'

    listener.get_printer_info(printer_info_url, printer_name)

    if listener.move_arm_to_pos == True:
        
        print('THE HARVEST HAS BEGUN')

        # instructions (joint angles) now stored in a separate text file as csv
        angle_instructions = instruct.parse_csv('test_test.txt')

        multi_point_control(angle_instructions, printer_num)
        
def loop_print(printer_num):
    # take picture of bed to check if the arm has actually gotten the print off
    clear_bed_detect.take_single_picture('check')
    
    if clear_bed_detect.print_detector():
        # needs popup to clear later...
        print('Clear bed before proceeding')
    else:
        with open('printer_octoprint_data.txt') as json_file:
            data = json.load(json_file)
            printer_name = (data['printer_stats'][printer_num]['printer_name'])
            printer_api_key = (data['printer_stats'][printer_num]['api_key'])
            printer_file_list = (data['printer_stats'][printer_num]['file_list'])

        # hard coded for now
        file_name = 'rectangle_vase_0.3mm_PET_MK3S.gcode'

        printer_file_list_url = printer_file_list + f'{file_name}' + f'?apikey={printer_api_key}'

        listener.send_print(printer_file_list_url, file_name, printer_name)

def multi_point_control(angle_instructions, printer_num):
    global multi_point_instruction_num

    # polls each joint to see if they are moving
    j1_current_vel = controller.return_joint_velocity(0, 0)
    j2_current_vel = controller.return_joint_velocity(0, 1)
    j3_current_vel = controller.return_joint_velocity(1, 0)
    j4_current_vel = controller.return_joint_velocity(1, 1)
    
    velocity_threshold = 0.05

    # if all of the joints are pretty much stationary, move to the instructed set
    if j1_current_vel < velocity_threshold and j2_current_vel < velocity_threshold\
        and j3_current_vel < velocity_threshold and j4_current_vel < velocity_threshold:
        limit.multi_angle_limit_check(angle_instructions[multi_point_instruction_num])

        # check to see where in the instruction set we are
        if multi_point_instruction_num == (len(angle_instructions) - 1):
            listener.move_arm_to_pos = False
            multi_point_instruction_num = 0
            print(f'Prusa {printer_num + 1} harvested!')
            
            if p1_print_loop or p6_print_loop:
                loop_print(printer_num)
        else:
            multi_point_instruction_num += 1
    else:
        print ('arm in motion')
        
window_width = 1024
window_height = 600

col_1 = [[sg.Button('Connect'), sg.Button('Calibrate'), sg.Button('Home')],
        [sg.T('')],
        [sg.Text('Absolute Joint motion')],
        [sg.Text('J1 Angle: '),
        sg.Input('0', key='-J1-ABS-', size=(10, 10), justification='center'),
        sg.Button('Set J1')],
        [sg.Text('J2 Angle: '),
        sg.Input('0', key='-J2-ABS-', size=(10, 10), justification='center'),
        sg.Button('Set J2')],
        [sg.Text('J3 Angle: '),
        sg.Input('0', key='-J3-ABS-', size=(10, 10), justification='center'),
        sg.Button('Set J3')],
        [sg.Text('J4 Angle: '),
        sg.Input('0', key='-J4-ABS-', size=(10, 10), justification='center'),
        sg.Button('Set J4')],
        [sg.Button('Set All')],
        [sg.T('')],
        [sg.Text('Move to Point')],
        [sg.Text('x - Coordinate: '), sg.Input('0', key='-X-COORD-', size=(10, 10), justification='center')],
        [sg.Text('y - Coordinate: '), sg.Input('0', key='-Y-COORD-', size=(10, 10), justification='center')],
        [sg.Text('z - Coordinate: '), sg.Input('0', key='-Z-COORD-', size=(10, 10), justification='center')],
        [sg.Text('End-effector   : '), sg.Input('0', key='-E-COORD-', size=(10, 10), justification='center')],
        [sg.Button('Go')]]

col_2 = [[sg.Text('Relative Joint Motion')],
         [sg.Text('J1 Relative: '),
          sg.Input('10', key='-J1-REL-', size=(5, 10), justification='center'),
          sg.Button('-J1'),
          sg.Button('+J1')],
         [sg.Text('J2 Relative: '),
          sg.Input('10', key='-J2-REL-', size=(5, 10), justification='center'),
          sg.Button('-J2'),
          sg.Button('+J2')],
         [sg.Text('J3 Relative: '),
          sg.Input('10', key='-J3-REL-', size=(5, 10), justification='center'),
          sg.Button('-J3'),
          sg.Button('+J3')],
         [sg.Text('J4 Relative: '),
          sg.Input('10', key='-J4-REL-', size=(5, 10), justification='center'),
          sg.Button('-J4'),
          sg.Button('+J4')],
         [sg.T('')],
         [sg.Text('Connect to printers')],
         [sg.Button('Connect Prusa 1', key='-CONNECT_P1-DISCONNECT_P1-'), sg.Checkbox('Loop', enable_events=True, key='-LOOP-P1-PRINT-')],
         [sg.Button('Connect Prusa 6', key='-CONNECT_P6-DISCONNECT_P6-'), sg.Checkbox('Loop', enable_events=True, key='-LOOP-P6-PRINT-')]]

test_list = []

col_3 = [[sg.Text('Print Control')],
         [sg.T('')],
         [sg.Text('Printer File List')],
         [sg.Listbox(values=test_list, size=(int(10), 5))],
         [sg.T('')],
         [sg.Text('Print Queue')],
         [sg.Listbox(values=test_list, size=(int(10), 5))],
         [sg.Button('Add'), sg.Button('Remove')]]
   
col_4 = [[sg.Text('Output')],
         [sg.Output(size=(int(window_width/4), 10), key='OUTPUT')],
         [sg.Button('Exit')]]

layout = [[sg.Column(col_1, element_justification='r'), sg.VSeparator(),
           sg.Column(col_2, element_justification='r'), sg.VSeparator(), 
           sg.Column(col_3, element_justification='r'), sg.VSeparator(),
           sg.Column(col_4, element_justification='r')]]

window = sg.Window('Arm Control', layout, location=(0,0), size=(1024,600))

while True:
    # if connected to the printer, ping the printer for status every 15 s
    if stream_data == True:
        event, values = window.read(timeout=timeout)
        if prusa_1_connected:
            connect_printer(0)

        if prusa_6_connected:
            connect_printer(1)
    else:
        event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Connect':
        controller.connect_to_boards()
    
    if event == 'Calibrate':
        controller.calibrate_all()
        
        # move joints to initial pose
        limit.multi_angle_limit_check(joint_angles)
        for i in range(len(joint_angles)):
            values[i] = joint_angles[i]

    if event == 'Home':
        
        # moves arm back to zero pose
        limit.multi_angle_limit_check(home_angles)
        for i in range(len(home_angles)):
            values[i] = home_angles[i]

    if event == 'Set J1':
        limit.single_angle_limit_check(0, 0, 5, float(values['-J1-ABS-']), True)
        
    if event == 'Set J2':
        limit.single_angle_limit_check(0, 1, 5, float(values['-J2-ABS-']), True)
        
    if event == 'Set J3':
        limit.single_angle_limit_check(1, 0, -5, float(values['-J3-ABS-']), True)

    if event == 'Set J4':
        limit.single_angle_limit_check(1, 1, 1, float(values['-J4-ABS-']), True)
    
    if event == 'Set All':
        limit.multi_angle_limit_check(
            [float(values[0]), float(values[1]), float(values[3]), float(values[4])])
    
    if event == 'Go':
        limit.coordinate_limit_check(float(values['-X-COORD-']), float(values['-Y-COORD-']), float(values['-Z-COORD-']), float(values['-E-COORD-']))
        
    if event == '-J1':
        limit.single_angle_limit_check(0, 0, 5, -float(values['-J1-REL-']), False)
    
    if event == '+J1':
        limit.single_angle_limit_check(0, 0, 5, float(values['-J1-REL-']), False)
    
    if event == '-J2':
        limit.single_angle_limit_check(0, 1, 5, -float(values['-J2-REL-']), False)

    if event == '+J2':
        limit.single_angle_limit_check(0, 1, 5, float(values['-J2-REL-']), False)

    if event == '-J3':
        limit.single_angle_limit_check(1, 0, -5, -float(values['-J3-REL-']), False)

    if event == '+J3':
        limit.single_angle_limit_check(1, 0, -5, float(values['-J3-REL-']), False)

    if event == '-J4':
        limit.single_angle_limit_check(1, 1, 1, -float(values['-J4-REL-']), False)

    if event == '+J4':
        limit.single_angle_limit_check(1, 1, 1, float(values['-J4-REL-']), False)

    if event == '-CONNECT_P1-DISCONNECT_P1-':
        stream_data_toggle()
        
        if not prusa_1_connected:            
            prusa_1_connected = True                
        else:
            prusa_1_connected = False

        window['-CONNECT_P1-DISCONNECT_P1-'].Update('Disconnect Prusa 1' if prusa_1_connected else 'Connect Prusa 1')
    
    if event =='-LOOP-P1-PRINT-':
        p1_print_loop = not p1_print_loop
        window['-LOOP-P1-PRINT-'].update(p1_print_loop)
        print(f'Prusa 1 print loop: {p1_print_loop}')

    if event == '-CONNECT_P6-DISCONNECT_P6-':
        # prusa 6 currently using printer index of 1 since others arent in the json file yet
        stream_data_toggle()

        if not prusa_6_connected:
            # take picture of the clear bed to set ground truth for 'clear' initial state
            clear_bed_detect.take_single_picture('initial')
            prusa_6_connected = True
        else:
            prusa_6_connected = False

        window['-CONNECT_P6-DISCONNECT_P6-'].Update(
            'Disconnect Prusa 6' if prusa_6_connected else 'Connect Prusa 6')

    if event == '-LOOP-P6-PRINT-':
        p6_print_loop = not p6_print_loop
        window['-LOOP-P6-PRINT-'].update(p6_print_loop)
        print(f'Prusa 6 print loop: {p6_print_loop}')

window.close()
