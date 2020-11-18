import cv2 as cv
import os
from pathlib import Path

# hard-coded ROI for images from webcam

roi_width_min = 0
roi_width_max = 1280
roi_height_min = 450
roi_height_max = 720

# 1. check if we have a folder called 'images' make if not there
Path('images').mkdir(parents=True, exist_ok=True)

images = os.listdir('images')

# 2. take single picture of bed and store in images
#   a. picture before print: clear state
#   b. picture after arm picked up print: check state

def take_single_picture(bed_state):
    # 720 x 1280 x 3
    camera = cv.VideoCapture(0)

    for i in range(1):
        return_value, image = camera.read()
        
        if bed_state == 'initial':
            file_name = 'initial_state.jpg'
        elif bed_state == 'check':
            file_name = 'check_state.jpg'
        else:
            print('invalid bed state')
            break
        
        cv.imwrite(os.path.join('images', file_name), image)
        
    print(f'{bed_state} print bed picture recorded')

# 3. compare check vs. clear state
#   a. return True if clear, False if not clear
def print_detector():
    print_detected = True
    
    img_initial = cv.imread(os.path.join('images', 'initial_state.jpg'))
    img_check = cv.imread(os.path.join('images', 'check_state.jpg'))
    
    roi_initial = img_initial[roi_height_min: roi_height_max,
                            roi_width_min: roi_width_max]
    
    roi_check = img_check[roi_height_min: roi_height_max,
                          roi_width_min: roi_width_max]
    
    sub = cv.subtract(roi_initial, roi_check)
    new_threshold = cv.inRange(sub, (75, 75, 75), (255, 255, 255))
    
    if 255 in new_threshold:
        print(f'possible print on bed')
        print_detected = True
    else:
        print('bed clear')
        print_detected = False

    return print_detected

## for testing
# take_single_picture('check')
# print_detector()
        
    
    
    

