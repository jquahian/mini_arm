import PySimpleGUI as sg
import controller

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Button('Connect'), sg.Button('Calibrate All'), sg.Button('Home All')],
          [sg.Text('Manual Joint Control')],
          [sg.Text('J1 Angle'), sg.Input(), sg.Button('Set J1'), sg.Text('J2 Angle'), sg.Input(), sg.Button('Set J2')], [
    sg.Text('J3 Angle'), sg.Input(), sg.Button('Set J3'), sg.Text('J4 Angle'), sg.Input(), sg.Button('Set J4')],
          [sg.Text('Move to Point')],
    [sg.Text('X:'), sg.Input(), sg.Text('Y:'), sg.Input(),
     sg.Text('Z:'), sg.Input(), sg.Button('Go')],
          [sg.Button('Exit')]]

# Create the Window
window = sg.Window('Arm Control', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
        break
    
    if event == 'Connect':
        controller.connect_to_boards()
    
    if event == 'Calibrate All':
        controller.calibrate_all()
        
    if event == 'Home All':
        controller.move_axis_absolute(controller.oboard[0], 0, 5, 0)
        controller.move_axis_absolute(controller.oboard[0], 1, 5, 0)
        controller.move_axis_absolute(controller.oboard[1], 0, 5, 0)
        controller.move_axis_absolute(controller.oboard[1], 1, 1, 0)

    if event == 'Go':
        controller.move_to_point(values[4], values[6])
        
    if event == 'Set J1':
        controller.move_axis_absolute(controller.oboard[0], 0, 5, values[0])
        
    if event == 'Set J2':
        controller.move_axis_absolute(controller.oboard[0], 1, 5, values[1])
        
    if event == 'Set J3':
        controller.move_axis_absolute(controller.oboard[1], 0, -5, values[2])

    if event == 'Set J4':
        controller.move_axis_absolute(controller.oboard[1], 1, 1, values[3])

window.close()
