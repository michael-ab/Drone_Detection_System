import argparse
import os
import shutil
import time
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, plot_one_box, strip_optimizer)
from utils.torch_utils import select_device, load_classifier, time_synchronized

# Our addons:
import cv2
import sys

import globs
import zoom_cam

from threading import Thread

#sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def PosXtoX():
    x = (globs.posX-globs.min_x)/globs.ratiow
    return x


def PosYtoY():
    y = -(globs.posY-globs.max_y)/globs.ratioh
    return y



def get_xmid_ymid(det):
    (xtl, ytl), (xbr, ybr) = get_tl_br(det)
    x_mid = int((xtl+xbr)/2)
    y_mid = int((ytl+ybr)/2)
    return x_mid, y_mid


def get_tl_br(det):
    x_top_left = int(det[0][0])
    y_top_left = int(det[0][1])
    x_btm_right = int(det[0][2])
    y_btm_right = int(det[0][3])
    return (x_top_left, y_top_left), (x_btm_right, y_btm_right)


def detect(opt, save_img=False):

    out, source, weights, view_img, save_txt, imgsz = \
        opt.output, opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size
    webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')

    # Initialize
    device = select_device(opt.device)
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'])  # load weights
        modelc.to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = True
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz)
    else:
        save_img = True
        dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
    for path, img, im0s, vid_cap in dataset:
        t00 = time.time()

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=opt.augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        t2 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
            else:
                p, s, im0 = path, '', im0s

            save_path = str(Path(out) / Path(p).name)
            txt_path = str(Path(out) / Path(p).stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                
                ### our code begin ###
                
                globs.x_mid, globs.y_mid = get_xmid_ymid(det)
                globs.label_sc2.configure(text="Drone recognized "+globs.detect_perc, font=("Calibri", 30, "bold"), bg='#034B5E',
                                        fg='#00ff15')

                globs.leader_cam = 1
                globs.leader_cam_count = 0
                zoom_cam.SetPositionZoom(globs.x_mid, globs.y_mid)
                #if (abs(globs.x_mid - 1280/2) < 120) & (abs(globs.y_mid - 720/2) < 60):
                x = PosXtoX()
                y = PosYtoY()
                center = (int(x),int(y))	
                globs.pts.appendleft(center)
                
                ### our code ends ###

                
                   
                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += '%g %ss, ' % (n, names[int(c)])  # add to string

                # Write results
                for *xyxy, conf, cls in det:
                

                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * 5 + '\n') % (cls, *xywh))  # label format

                    if save_img or view_img:  # Add bbox to image
                        label = '%s %.2f' % (names[int(cls)], conf)
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
             
            elif globs.leader_cam_count > 60:
                globs.leader_cam = 0
                globs.label_sc2.configure(text="Looking for drones...", font=("Calibri", 30, "bold"), bg='#034B5E',
                                    fg='red')
                globs.label_sc3.configure(text="", font=("Calibri", 30, "bold"), bg='#034B5E', fg='red')
                globs.label_sc4.configure(text="", font=("Calibri", 30, "bold"), bg='#034B5E', fg='red')

                globs.leader_cam_count = 0
            else:
                globs.leader_cam_count += 1
                globs.label_sc2.configure(text="Looking for drones...", font=("Calibri", 30, "bold"), bg='#034B5E',
                                    fg='red')
                globs.label_sc3.configure(text="", font=("Calibri", 30, "bold"), bg='#034B5E', fg='red')
                globs.label_sc4.configure(text="", font=("Calibri", 30, "bold"), bg='#034B5E', fg='red')
            
            
            # Print time (inference + NMS)
            # print('%sFPS: (%s)' % (s, int((1/(t2 - t1))/10)*10 ))

            # Stream results
            if True: #view_img:
                #cv2.imshow(p, im0)
                globs.frame_zoom = im0.copy()
               
                #if cv2.waitKey(1) == ord('q'):  # q to quit
                    #raise StopIteration


            t4 = time_synchronized()

            total_time = time.time() - t00

            #print('Total Loop Time: (%.3fs)' % (total_time))
            #print('Preprocess Time: (%.3fs)' % (t1 - t00))
            #print('DNN Time: (%.3fs)' % (t2 - t1))
            #print('Mid Time: (%.3fs)' % (t3 - t2))
            #print('GUI Time: (%.3fs)\n' % (t4 - t3))

    print('Done. (%.3fs)' % (time.time() - t0))


class init_detect(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)    
        
    
    def run(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('--weights', nargs='+', type=str, default='last.pt', help='model.pt path(s)')
        parser.add_argument('--source', type=str, default='0', help='source')  # file/folder, 0 for webcam
        parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
        parser.add_argument('--img-size', type=int, default=256, help='inference size (pixels)')
        parser.add_argument('--conf-thres', type=float, default=0.6, help='object confidence threshold')
        parser.add_argument('--iou-thres', type=float, default=0.6, help='IOU threshold for NMS')
        parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        parser.add_argument('--view-img', action='store_true', help='display results')
        parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
        parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
        parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
        parser.add_argument('--augment', action='store_true', help='augmented inference')
        parser.add_argument('--update', action='store_true', help='update all models')
        opt = parser.parse_args()
        print(opt)

        with torch.no_grad():
            if opt.update:  # update all models (to fix SourceChangeWarning)
                for opt.weights in ['yolov5s.pt', 'yolov5m.pt', 'yolov5l.pt', 'yolov5x.pt']:
                    detect(opt)
                    strip_optimizer(opt.weights)
            else:
                detect(opt)
