import cv2
import numpy as np 
from object_detection import ObjectDetection
import math

od = ObjectDetection()

cap = cv2.VideoCapture("idk.mp4")
objects_tracked = [] # TODO: [[x, y], frameOccurenceNumberInLoop]

while True:
    ret, frame = cap.read()

    current_centres = []

    # * DETECT OBJECTS ON THE FRAME AND DRAW RECTANGLES
    (class_ids, scores, boxes) = od.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        cx = int((x+x+w)/2)
        cy = int((y+y+h)/2)
        current_centres.append((cx, cy))
        # print(f"frame {frameCount} box: ", x, y, w, h)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # frame, topleft, bottomright, color bgr, thickness
    print(current_centres)
        

    # * CHANGING FRAMES HERE
    cv2.imshow("Frame", frame)  # show the frame in window 
    # cv2.waitKey(0) # wait for keydown to move to next iteration
    key = cv2.waitKey(1)
    if key==27:
        break

cap.release() #release file element
cv2.destroyAllWindows()