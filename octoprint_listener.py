import requests
import json
import time

printer_ready_status = []

# toggles whether there is a print ready for pickup
# internal to script
harvest_ready = False

# toggles wheether arm needs to move to position
# only shuts off when the arm has completed all instruction sets given
# accessed by external script which sends commands to the arm
move_arm_to_pos = False

'''
TODOS
- check if not on same network
- check if server is accessible
- check to see if event was a print cancel or other print interrupt event
- make code scale to handle multiple printers
'''

# polls the requested printed via octoprint API
def get_printer_info(ip_address, printer_name):
    global printer_ready_status
    global harvest_ready
    global move_arm_to_pos
    
    r = requests.get(ip_address, timeout=5)
    info = r.json()
    
    printer_is_operational = info['state']['flags']['operational']
    printer_is_ready = info['state']['flags']['ready']
    printer_is_printing = info['state']['flags']['printing']
    printer_t0_temp = info['temperature']['tool0']['actual']
    printer_bed_temp = info['temperature']['bed']['actual']
    
    # to determine if we are to get the print or not, we need to see what state change the printer is in
    # if we have just connected to the printer and we don't know the past/future state, we initialize an emtpy list
    # the first and second ping to octoprint will return the ready status of the printer
    # if first entry in status goes from ready to not ready (which is printing), then when the status changes we get the print
    if len(printer_ready_status) < 2:
        printer_ready_status.append(printer_is_ready)
    else:
        printer_ready_status[0] = printer_ready_status[1]
        printer_ready_status[1] = printer_is_ready
        
        # 'ready' status (not printing -> printing)
        if printer_ready_status[0] == True and printer_ready_status[1] == False:
            print('PREPARING THE HARVEST')

        # 'ready' status changed (printing -> not printing) to standby and get print
        if printer_ready_status[0] == False and printer_ready_status[1] == True:
            harvest_ready = True

    # when bed temp is < 45 and other safety checks, we move to get the print
    if harvest_ready:
        if printer_bed_temp < 65 and printer_is_printing == False and printer_is_operational:
            harvest_ready = False
            move_arm_to_pos = True
            return move_arm_to_pos
    else:
        print('Not harvesting')

    # some status outpus
    print(f'{printer_name} operational: {printer_is_operational}')
    print(f'{printer_name} Nozzle Temp: {printer_t0_temp}')
    print(f'{printer_name} Bed Temp: {printer_bed_temp}')
    print(f'{printer_name} ready: {printer_is_ready}')
    print(f'{printer_name} printing: {printer_is_printing}')
    print('\n')

# starts print (file stored locally on octoprint)
def send_print(ip_address, file_name, printer_name):
    # print_command = {'command' : 'select', 'print': True}
    start_print = requests.post(ip_address, json={'command' : 'select', 'print' : True})

    print(start_print)
    
    print(f'starting print {file_name} on {printer_name}')
    
    