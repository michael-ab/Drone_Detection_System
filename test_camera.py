import cv2
import numpy as np


cams_test = 5
for i in range(0, cams_test):
    cap = cv2.VideoCapture(0)
    print("A")
    # cap.set(3, 800)
    # print("B")
    # cap.set(4, 600)
    # print("C")
    # cap.set(5, 10)
    print("D")
    test, frame = cap.read()
    if test:
        print("E")
        while 1:
            res, frame_small = cap.read()
            cv2.imshow("frame_small", frame_small)
            cv2.waitKey(10)

        cap.release()
        cv2.destroyAllWindows()


