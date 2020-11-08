import requests
import json
import time
import limit_set as limit

p1_ready_status = []
harvest_ready = False

'''
TODOS
- check if not on same network
- check to see if event was a print cancel
- decide where harvest_prints should go??
'''

# polls the requested printed via octoprint API
def get_printer_info(ip_address):
    global p1_ready_status
    global harvest_ready
    
    r = requests.get(ip_address, timeout=5)
    info = r.json()

    p1_is_operational = info['state']['flags']['operational']
    p1_is_ready = info['state']['flags']['ready']
    p1_is_printing = info['state']['flags']['printing']
    p1_t0_temp = info['temperature']['tool0']['actual']
    p1_bed_temp = info['temperature']['bed']['actual']
    
    # to determine if we are to get the print or not, we need to see what state change the printer is in
    # if we have just connected to the printer and we don't know the past/future state, we initialize an emtpy list
    # the first and second ping to octoprint will return the ready status of the printer
    # if first entry in status goes from ready to not ready (which is printing), then when the status changes we get the print
    if len(p1_ready_status) < 2:
        p1_ready_status.append(p1_is_ready)
    else:
        p1_ready_status[0] = p1_ready_status[1]
        p1_ready_status[1] = p1_is_ready
        
        if p1_ready_status[0] == True and p1_ready_status[1] == False:
            print("PREPARING FOR THE HARVEST")

        # 'ready' status changed (printing -> not printing) get ready to pick the print
        if p1_ready_status[0] == False and p1_ready_status[1] == True:
            harvest_ready = True
    
    # when bed temp is < 45 and other safety checks, we move to get the print
    if harvest_ready:
        if p1_bed_temp < 45 and p1_is_printing == False and p1_is_operational:
            harvest_prints()
            harvest_ready = False
    else:
        print('Nothing to harvest')

    # some status outpus
    print(f'Prusa 1 operational: {p1_is_operational}')
    print(f'Prusa 1 Nozzle Temp: {p1_t0_temp}')
    print(f'Prusa 1 Bed Temp: {p1_bed_temp}')
    print(f'Prusa 1 ready: {p1_is_ready}')
    print(f'Prusa 1 printing: {p1_is_printing}')
    print('\n')
    
# should this be here?    
def harvest_prints():
    # test coords to 'pickup' print
    limit.multi_angle_limit_check([0, 40, 50, -250])
    print('Prusa 1 harvested!')
