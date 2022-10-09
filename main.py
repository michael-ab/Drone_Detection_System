import random
import sys
from threading import Thread
import time
import math
from ctypes import *
import keyboard  # using module keyboard
from zoom_cam import *
from wide_cam import *
from detect import *
from init_fun import *
import globs


# init threads
WideCam = WideCam()
ZoomCam = ZoomCam()
Init_detect = init_detect()

WideCam.start()
ZoomCam.start()
Init_detect.start()

globs.window.mainloop()
WideCam.join()
ZoomCam.join()
Init_detect.join()
