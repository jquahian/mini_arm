import PySimpleGUI as sg
import controller
import limit_set as limit
import octoprint_listener as listener
import json

sg.theme('DarkAmber')

# initial state of joint angles
joint_angles = [0, -35, 35, 0]

# zero'd position for joints 1, 2, 3, 4
home_angles = [0, 0, 0, 0]

# joint 4 zero position: want the option to control this independently of other joints
j4_angle = 0

# position of joint 4 in xyz space
point_coordinates = [0, 0, 0]

# initial status of connection to first printer
prusa_1_connected = False

stream_data = False

# time in ms to poll octoprint/stream other data source
timeout = 2500

multi_point_instruction_num = 0

# in case we ever need to stream data other than octoprint
def stream_data_toggle():
    global stream_data

    if not stream_data:
        stream_data = True
    else:
        stream_data = False

# pass in the ip + api key in external json file to octoprint
def connect_prusa_1():
    with open('octoprint_data.txt') as json_file:
        data = json.load(json_file)
        prusa_1_data = (data['prusa_1'][0]['printer_address'])

    listener.get_printer_info(prusa_1_data)
    
    if listener.move_arm_to_pos == True:
        print('THE HARVEST HAS BEGUN')

        # test coords to 'pickup' print
        # need better system to program the arm for specific moves
        angle_set_1 = [0, 40, 50, 0]
        angle_set_2 = [0, 40, 50, -310]
        angle_set_3 = [90, 30, 30, -310]
        angle_set_4 = [0, 30, 30, -310]
        angle_set_5 = [0, 40, 50, 0]
        angle_set_6 = [0, 40, 50, 0]
        angle_set_7 = [0, 0, 0, 0]

        multi_point_control(angle_set_1, angle_set_2, angle_set_3, angle_set_4, angle_set_5, angle_set_6, angle_set_7)

# need to convert this to args or load from a preconfigured jsonn file
# eww
def multi_point_control(angle_set_1, angle_set_2, angle_set_3, angle_set_4, angle_set_5, angle_set_6, angle_set_7):
    global multi_point_instruction_num
    
    # ewwwwwwwww
    angle_instructions = [angle_set_1, angle_set_2, angle_set_3, angle_set_4, angle_set_5, angle_set_6, angle_set_7]
    
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
            print('Prusa 1 harvested!')
        else:
            multi_point_instruction_num += 1
    else:
        print ('arm in motion')

layout = [[sg.Button('Connect')],
          [sg.Button('Calibrate All'), sg.Button('Home All')],
          [sg.Text('Manual Joint Control')],
          [sg.Text('J1 Angle: '), 
           sg.Input('0', size=(10, 10), justification='center'),
           sg.Button('Set J1'), 
           sg.Text('Relative: '), 
           sg.Input('10', size=(5,10), justification='center'), 
           sg.Button('-J1'), 
           sg.Button('+J1')],
          [sg.Text('J2 Angle: '), 
           sg.Input('0', size=(10, 10), justification='center'), 
           sg.Button('Set J2'), 
           sg.Text('Relative: '), 
           sg.Input('10', size=(5,10), justification='center'),
           sg.Button('-J2'), 
           sg.Button('+J2')],
          [sg.Text('J3 Angle: '), 
           sg.Input('0', size=(10, 10), justification='center'), 
           sg.Button('Set J3'), 
           sg.Text('Relative: '), 
           sg.Input('10', size=(5,10), justification='center'),
           sg.Button('-J3'), 
           sg.Button('+J3')],
          [sg.Text('J4 Angle: '), 
           sg.Input('0', size=(10, 10), justification='center'), 
           sg.Button('Set J4'), 
           sg.Text('Relative: '), 
           sg.Input('10', size=(5,10), justification='center'),
           sg.Button('-J4'), 
           sg.Button('+J4')],
          [sg.Button('Set All')],
          [sg.Text('Move to Point')],
          [sg.Text('x - Coordinate: '), sg.Input('0', size=(10, 10), justification='center')],
          [sg.Text('y - Coordinate: '), sg.Input('0', size=(10, 10), justification='center')],
          [sg.Text('z - Coordinate: '), sg.Input('0', size=(10, 10), justification='center')],
          [sg.Text('End-effector   : '), sg.Input('0', size=(10, 10), justification='center')],
          [sg.Button('Go')],
          [sg.Text('Output')],
          [sg.Output(size=(65,15), key='OUTPUT')],
          [sg.Button('Connect to Prusa 1', key='-CONNECT_P1-DISCONNECT_P1-')],
          [sg.Button('Exit')]]

window = sg.Window('Arm Control', layout)

while True:
    # if connected to the printer, ping the printer for status every 15 s
    if stream_data == True:
        event, values = window.read(timeout=timeout)
        if connect_prusa_1:
            connect_prusa_1()
    else:
        event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Connect':
        controller.connect_to_boards()
    
    if event == 'Calibrate All':
        controller.calibrate_all()
        
        # move joints to initial pose
        limit.multi_angle_limit_check(joint_angles)
        for i in range(len(joint_angles)):
            values[i] = joint_angles[i]

    if event == 'Home All':
        
        # moves arm back to zero pose
        limit.multi_angle_limit_check(home_angles)
        for i in range(len(home_angles)):
            values[i] = home_angles[i]

    if event == 'Go':
        limit.coordinate_limit_check(float(values[8]), float(values[9]), float(values[10]), float(values[11]))
        
    if event == 'Set J1':
        limit.single_angle_limit_check(0, 0, 5, float(values[0]), True)
        
    if event == 'Set J2':
        limit.single_angle_limit_check(0, 1, 5, float(values[2]), True)
        
    if event == 'Set J3':
        limit.single_angle_limit_check(1, 0, -5, float(values[4]), True)

    if event == 'Set J4':
        limit.single_angle_limit_check(1, 1, 1, float(values[6]), True)
        
    if event == '-J1':
        limit.single_angle_limit_check(0, 0, 5, -float(values[1]), False)
    
    if event == '+J1':
        limit.single_angle_limit_check(0, 0, 5, float(values[1]), False)
    
    if event == '-J2':
        limit.single_angle_limit_check(0, 1, 5, -float(values[3]), False)

    if event == '+J2':
        limit.single_angle_limit_check(0, 1, 5, float(values[3]), False)

    if event == '-J3':
        limit.single_angle_limit_check(1, 0, -5, -float(values[5]), False)

    if event == '+J3':
        limit.single_angle_limit_check(1, 0, -5, float(values[5]), False)

    if event == '-J4':
        limit.single_angle_limit_check(1, 1, 1, -float(values[7]), False)

    if event == '+J4':
        limit.single_angle_limit_check(1, 1, 1, float(values[7]), False)

    if event == 'Set All':
        limit.multi_angle_limit_check(
            [float(values[0]), float(values[2]), float(values[4]), float(values[6])])
    
    if event == '-CONNECT_P1-DISCONNECT_P1-':
        stream_data_toggle()
        
        if not prusa_1_connected:            
            prusa_1_connected = True
        else:
            prusa_1_connected = False

        window['-CONNECT_P1-DISCONNECT_P1-'].Update('Disconnect Prusa 1' if prusa_1_connected else 'Connect Prusa 1')

window.close()
