from threading import Thread
import time
import numpy as np
import PIL
from PIL import Image, ImageTk
import os
import cv2
from Phidget22.Devices.RCServo import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from PhidgetHelperFunctions import *
from init_fun import *
import globs

def SetPositionZoom(x, y):
    
    errY = abs(y - 720 / 2) / 4  # 4 is arbitrary val
    errX = abs(x - 1280 / 2) / 4

    count = 0
    stepY = (globs.ratio_zoom * errY) * (globs.ratio_zoom * errY) * 1.4  # last val is arbitrary val
    stepX = (globs.ratio_zoom * errX) * (globs.ratio_zoom * errX) * 1.4  # last val is arbitrary val

    if globs.leader_cam == 1:
        #print("setpositionzoom\n")
        if (x > 1280 / 2) & (globs.posX + stepX <= 175):
            count += 1
            globs.posX += stepX
        elif globs.posX - stepX >= 50:
            count += 1
            globs.posX -= stepX

        if (y > 720 / 2) & (globs.posY - stepX >= 50):
            globs.posY -= stepY
            count += 2
        elif globs.posY + stepY <= 175:
            globs.posY += stepY
            count += 2

        globs.label_sc3.configure(text='\u0394' + "x = " + str("{0:.2f}".format(errX)), font=("Calibri", 20), bg='#034B5E',
                            fg='#00ff15')
        globs.label_sc4.configure(text='\u0394' + "y = " + str("{0:.2f}".format(errY)), font=("Calibri", 20), bg='#034B5E',
                            fg='#00ff15')
    globs.label_angles.configure(text='\u03B8x = '+str("{0:.1f}".format(globs.posX)) +'\n\u03B8y = '+ str("{0:.1f}".format(globs.posY)), font=("Calibri", 20), bg='#034B5E', fg='white')
    return count


class ZoomCam(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)

    def run(self):

        globs.chY.setTargetPosition(100)
        globs.chX.setTargetPosition(100)

        while 1:

            #SetPositionZoom(globs.x_mid, globs.y_mid)  # ((x_mid_before + x_mid)/2, (y_mid_before + y_mid)/2)
            guiwidth = 700
            guiheight = 500
            dim = (guiwidth, guiheight)
            # resize image
            resized = cv2.resize(globs.frame_zoom, dim, interpolation=cv2.INTER_AREA)
            cv2.line(resized, (int(guiwidth/2 - 30), int(guiheight/2)), (int(guiwidth/2 + 30), int(guiheight/2)), (0, 0, 255), 3)
            cv2.line(resized, (int(guiwidth/2), int(guiheight/2 - 30)), (int(guiwidth/2), int(guiheight/2 + 30)), (0, 0, 255), 3)
            cv2imageS = cv2.cvtColor(resized, cv2.COLOR_BGR2RGBA)
            imgS = PIL.Image.fromarray(cv2imageS)
            imgtkS = ImageTk.PhotoImage(image=imgS)
            globs.main_sc.imgtkS = imgtkS
            globs.main_sc.configure(image=imgtkS)
            globs.main_sc._image_cache = imgtkS
            globs.window.update()

            bufY = globs.posY
            if not bufY:
                continue
            bufX = globs.posX
            if not bufX:
                continue

            try:
                targetPositionY = float(bufY)
                targetPositionX = float(bufX)

            except ValueError as e:
                print("Input must be a number, or Q to quit.")
                continue

            globs.chY.setTargetPosition(targetPositionY)
            globs.chX.setTargetPosition(targetPositionX)

            #frame_init_zoom = frame_zoom
            if globs.play == 0:
                break

        #capS.release()
        cv2.destroyAllWindows()
        print("\nExit ZoomCam")
        return 0



