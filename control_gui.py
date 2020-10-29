import PySimpleGUI as sg
import controller

sg.theme('DarkAmber')

# initial state of joint angles
joint_angles = [0, 50, 50, 0]

# position of joint 4 in xyz space
point_coordinates = [0, 0, 0]

layout = [[sg.Button('Connect'), sg.Button('Calibrate All'), sg.Button('Home All')],
          [sg.Text('Manual Joint Control')],
          [sg.Text('J1 Angle'), sg.Input(joint_angles[0]), sg.Button('Set J1'), sg.Text(
              'J2 Angle'), sg.Input(joint_angles[1]), sg.Button('Set J2')],
          [sg.Text('J3 Angle'), sg.Input(joint_angles[2]), sg.Button(
              'Set J3'), sg.Text('J4 Angle'), sg.Input(joint_angles[3]), sg.Button('Set J4')],
          [sg.Button('Set All')],
          [sg.Text('Move to Point')],
          [sg.Text('X:'), sg.Input(point_coordinates[0]), sg.Text('Y:'),
           sg.Input(point_coordinates[1]), sg.Text('Z:'), sg.Input(point_coordinates[2]), sg.Button('Go')],
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
        
        # move joints to initial known positions
        controller.move_axis_absolute(0, 0, 5, joint_angles[0])
        controller.move_axis_absolute(0, 1, 5, joint_angles[1])
        controller.move_axis_absolute(1, 0, -5, joint_angles[2])
        controller.move_axis_absolute(1, 1, 1, joint_angles[3])

    if event == 'Home All':
        controller.move_axis_absolute(0, 0, 5, 0)
        controller.move_axis_absolute(0, 1, 5, 0)
        controller.move_axis_absolute(1, 0, -5, 0)
        controller.move_axis_absolute(1, 1, 1, 0)
        
        # update known joint angles
        joint_angles[0] = 0
        joint_angles[1] = 0
        joint_angles[2] = 0
        joint_angles[3] = 0

    if event == 'Go':
        controller.move_to_point(values[4], values[5], values[6])
        
    if event == 'Set J1':
        controller.move_axis_absolute(0, 0, 5, values[0])
        
    if event == 'Set J2':
        controller.move_axis_absolute(0, 1, 5, values[1])
        
    if event == 'Set J3':
        controller.move_axis_absolute(1, 0, -5, values[2])

    if event == 'Set J4':
        controller.move_axis_absolute(1, 1, 1, values[3])

    if event == 'Set All':
        controller.move_axis_absolute(0, 0, 5, values[0])
        controller.move_axis_absolute(0, 1, 5, values[1])
        controller.move_axis_absolute(1, 0, -5, values[2])
        controller.move_axis_absolute(1, 1, 1, values[3])

window.close()
