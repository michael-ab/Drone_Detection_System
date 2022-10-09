from threading import Thread
import time
import numpy as np
import PIL
from PIL import Image, ImageTk
import os
import cv2
from init_fun import *
import globs
import gi
gi.require_version('Gtk', '2.0')
import matplotlib.pyplot as plt
import pyrealsense2 as rs

pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
profile = pipe.start(config)

frameset = pipe.wait_for_frames()
color_frame = frameset.get_color_frame()
color_init = np.asanyarray(color_frame.get_data())

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2


def SetPositionWide(x, y):
    count = 0

    if globs.leader_cam == 0:
        if ((globs.min_x + x * globs.ratiow) >= globs.min_x) & ((globs.min_x + x * globs.ratiow) <= globs.max_x):
            globs.posX = globs.min_x + x * globs.ratiow
            count += 1
        if(globs.max_x - x * globs.ratiow < globs.min_x):
            globs.posX = globs.min_x
        if((globs.max_x - x * globs.ratiow) > globs.max_x):
            globs.posX = globs.max_x
        if ((globs.max_y - y * globs.ratioh) >= globs.min_y) & ((globs.max_y - y * globs.ratioh) <= globs.max_y):
            globs.posY = globs.max_y - y * globs.ratioh
            count += 2
        if(globs.max_y - y * globs.ratioh < globs.min_y):
            globs.posY = globs.min_y
        if((globs.max_y - y * globs.ratioh) > globs.max_y):
             globs.posY = globs.max_y
    globs.label_angles.configure(text='\u03B8x = '+ str("{0:.1f}".format(globs.posX)) +'\n\u03B8y = '+ str("{0:.1f}".format(globs.posY)), font=("Calibri", 20), bg='#034B5E', fg='white')
    return count


DIM=(3264, 2448)
K=np.array([[1282.0387271196444, 0.0, 1670.4818003835164], [0.0, 1264.8223767238137, 1221.5199038892504], [0.0, 0.0, 1.0]])
D=np.array([[-0.02794047631602407], [0.007431072061745044], [-0.004890265066026917], [0.00022694907838545974]])



class WideCam(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)

    def run(self):
        #globs.capW.set(3, 3264)
        #globs.capW.set(4, 2448)
        #_, frame_init = globs.capW.read()
        frameset = pipe.wait_for_frames()

        align = rs.align(rs.stream.color)
        frameset = align.process(frameset)

        color_frame_init = frameset.get_color_frame()
        frame_depth = frameset.get_depth_frame()

        frame_init = np.asanyarray(color_frame_init.get_data())

        while 1:
            frameset = pipe.wait_for_frames()
            color_frame = frameset.get_color_frame()
            frame_depth = frameset.get_depth_frame()

            frame = np.asanyarray(color_frame.get_data())
            depth = np.asanyarray(frame_depth.get_data())
            #map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
            #frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            fram_cp = frame.copy()
	
            ### motion detector
            d = cv2.absdiff(frame_init, frame)
            gray = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=3)
            (c, _) = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if c:
                for contour in c:
                    if cv2.contourArea(contour) < 100:
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    if h / w > 0.9 or h / w < 0.3:
                        continue
                    else:
                        label_lc2.configure(text="h/w = " + str("{0:.2f}".format(h / w)), font=("Calibri", 20), bg='#034B5E', fg='white')
                        bottomLeftCornerOfText = (x, y)
                        # Crop depth data:
                        depth = depth[x:x+w, y:y+h].astype(float)
                        depth_crop = depth.copy()
                        if depth_crop.size == 0:
                            continue
                        depth_res = depth_crop[depth_crop != 0]
                        # Get data scale from the device and convert to meters
                        depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
                        depth_res = depth_res * depth_scale
                        if depth_res.size == 0:
                            continue
                        dist = min(depth_res)
                        cv2.rectangle(fram_cp, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        text = "Distance: " + str("{0:.2f}").format(dist)
                        cv2.putText(fram_cp,
                                    text,
                                    bottomLeftCornerOfText,
                                    font,
                                    fontScale,
                                    fontColor,
                                    lineType)
                        if (globs.lastX != x + w / 2) | (globs.lastY != y + h / 2):  # wide camera
                            pos = SetPositionWide(x + w / 2, y + h / 2)
            resized = cv2.resize(fram_cp, (700,500), interpolation=cv2.INTER_AREA)
            overlay = resized.copy()
            if globs.leader_cam == 0:
                globs.pts.clear()
            else:
                center_deque = globs.pts.copy()
                for elem in center_deque:
                    if elem is None:
                        continue
                    cv2.circle(resized, elem, 5, (0, 255, 0), -1)
            alpha = 0.6
            res = cv2.addWeighted(overlay, alpha, resized, 1 - alpha, 0)
            cv2imageL = cv2.cvtColor(res, cv2.COLOR_BGR2RGBA)
            imgL = PIL.Image.fromarray(cv2imageL)
            imgtkL = ImageTk.PhotoImage(image=imgL)
           
            globs.main_lc.imgtkL = imgtkL
            globs.main_lc.configure(image=imgtkL)
            globs.main_lc._image_cache = imgtkL
            globs.window.update()

            frame_init = frame

            if globs.play == 0:
                break

        print("\nExit WideCam")
        globs.capW.release()
        cv2.destroyAllWindows()
        pipe.stop()


