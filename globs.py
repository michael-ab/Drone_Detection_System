from init_fun import *
from collections import deque

chY = None
chX = None
label_sc2 = None
label_sc3 = None
label_sc4 = None
label_angles = None
leader_cam = None
play = None
main_sc = None
main_lc = None
window = None
lastX = None
lastY = None
leader_cam_count = 0

posX = 90
posY = 90
leader_cam = 0
play = 1
lastX = 0
lastY = 0

min_y = 83.8
max_y = 128.9	

min_x = 61.1
max_x = 133.3

#capW = cv2.VideoCapture("/dev/video0")

#width = capW.get(cv2.CAP_PROP_FRAME_WIDTH)
#height = capW.get(cv2.CAP_PROP_FRAME_HEIGHT)

#print("Wide frame = (", width, ",", height, ")" )
ratiow = abs(max_x - min_x) / 700
ratioh = abs(max_y - min_y) / 500
y_mid = 500 / 2
x_mid = 700 / 2

ratio_zoom = 13 / 1280


frame_zoom = cv2.imread('/home/nvidia/Desktop/project_code_2/images_gui/logo_drone.jpg')

pts = deque(maxlen=64)

detect_perc = ""
