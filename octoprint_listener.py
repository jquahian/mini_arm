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
    
    if len(p1_ready_status) < 2:
        p1_ready_status.append(p1_is_ready)
    else:
        p1_ready_status[0] = p1_ready_status[1]
        p1_ready_status[1] = p1_is_ready
        
        if p1_ready_status[0] == True and p1_ready_status[1] == False:
            print("PREPARING FOR THE HARVEST")

        if p1_ready_status[0] == False and p1_ready_status[1] == True:
            harvest_ready = True
        
    if harvest_ready:
        if p1_bed_temp < 30 and p1_is_printing == False and p1_is_operational:
                harvest_prints()
                harvest_ready == False
    else:
        print('Nothing to harvest')

    print(f'Prusa 1 operational status: {p1_is_operational}')
    print(f'Prusa 1 Nozzle Temp: {p1_t0_temp}')
    print(f'Prusa 1 Bed Temp: {p1_bed_temp}')
    print(f'Prusa 1 printing status: {p1_is_ready}')
    print(f'Prusa 1 operational status: {p1_is_printing}')
    
# should this be here?    
def harvest_prints():
    # test coords to 'pickup' print
    limit.multi_angle_limit_check([0, 40, 50, -250])
    print('Prusa 1 harvested!')

def start_listener(is_connected):
    with open('octoprint_data.txt') as json_file:
        data = json.load(json_file)
        prusa_1_data = (data['prusa_1'][0]['printer_address'])

    while is_connected:
        print('Connected to Prusa 1')
        get_printer_info(prusa_1_data)
        time.sleep(60)
    else:
        print('Disconnected from Prusa 1')
