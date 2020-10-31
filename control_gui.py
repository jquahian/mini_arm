import PySimpleGUI as sg
import controller
import limit_set as limit

sg.theme('DarkAmber')

# initial state of joint angles
joint_angles = [0, 50, 50, 0]

# zero'd position
home_angles = [0, 0, 0, 0]

# position of joint 4 in xyz space
point_coordinates = [0, 0, 0]

layout = [[sg.Button('Connect')],
          [sg.Button('Calibrate All'), sg.Button('Home All')],
          [sg.Text('Manual Joint Control')],
          [sg.Text('J1 Angle: '), sg.Input(joint_angles[0]), sg.Button('Set J1')],
          [sg.Text('J2 Angle: '), sg.Input(joint_angles[1]), sg.Button('Set J2')],
          [sg.Text('J3 Angle: '), sg.Input(joint_angles[2]), sg.Button('Set J3')],
          [sg.Text('J4 Angle: '), sg.Input(joint_angles[3]), sg.Button('Set J4')],
          [sg.Button('Set All')],
          [sg.Text('Move to Point')],
          [sg.Text('x - Coordinate: '), sg.Input('0')],
          [sg.Text('y - Coordinate: '), sg.Input('0')],
          [sg.Text('z - Coordinate: '), sg.Input('0')],
          [sg.Button('Go')],
          [sg.Text('Output')],
          [sg.Output(size=(65, 15), key='OUTPUT')],
          [sg.Button('Exit')]]

window = sg.Window('Arm Control', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Connect':
        controller.connect_to_boards()
    
    if event == 'Calibrate All':
        controller.calibrate_all()
        
        # # move joints to initial known positions
        limit.multi_angle_limit_check(joint_angles)

    if event == 'Home All':
        limit.multi_angle_limit_check(home_angles)

    if event == 'Go':
        limit.coordinate_limit_check(values[4], values[5], values[6])
        
    if event == 'Set J1':
        limit.single_angle_limit_check(1, values[0])
        
    if event == 'Set J2':
        limit.single_angle_limit_check(2, values[1])
        
    if event == 'Set J3':
        limit.single_angle_limit_check(3, values[2])

    if event == 'Set J4':
        limit.single_angle_limit_check(4, values[3])

    if event == 'Set All':
        limit.multi_angle_limit_check(
            [values[0], values[1], values[2], values[3]])

window.close()
