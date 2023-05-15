import cv2
import numpy as np
from object_detection import ObjectDetection
import math
import os

od = ObjectDetection()


videoPath = os.path.join(os.getcwd() + "/video1.mp4")
print(videoPath)
cap = cv2.VideoCapture(videoPath)


# ! FUNCTIONS
def extendSlope(pt1, pt2, pt3):
    dev_x = ((pt2[0]-pt1[0])+(pt3[0]-pt2[0]))/2
    dev_y = ((pt2[1]-pt1[1])+(pt3[1]-pt2[1]))/2
    pred_dev = [int(dev_x), int(dev_y)]
    return pred_dev


# ! VARIABLES
objects_tracked = []  # ? [frames (max = 5), [x, y], [x, y], ...]
frameCount = 0
previous_centers = []  # ? [[x, y]]
predicted_points = []  # ? []
max_distance = 30
display_points = []
pos1 = []
pos2 = []
pos3 = []
dev = [0, 0]
values = []

while True:
    ret, frame = cap.read()
    current_centres = []
    frameCount += 1

    # * DETECT OBJECTS ON THE FRAME AND DRAW RECTANGLES
    (class_ids, scores, boxes) = od.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        cx = int((x+x+w)/2)
        cy = int((y+y+h)/2)
        current_centres.append((cx, cy))
        # frame, topleft, bottomright, color bgr, thickness
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(frame, (cx,cy), 5, (255, 0, 255), -1)
    #print(current_centres)
    run = True
    if frameCount == 1:
        pos1 = list(current_centres[0])
    elif frameCount == 2:
        pos2 = list(current_centres[0])
    elif frameCount == 3:
        pos3 = list(current_centres[0])

    if frameCount <= 8 and frameCount > 3:
        dev = extendSlope(pos1, pos2, pos3)
        cx += dev[0]
        cy += dev[1]
        value = [cx, cy]
        values.append(value)
        pos1[0] += dev[0]
        pos2[0] += dev[0]
        pos3[0] += dev[0]
        pos1[1] += dev[1]
        pos2[1] += dev[1]
        pos3[1] += dev[1]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        
    elif frameCount == 9:
        pos1 = []
        pos2 = []
        pos3 = []
        frameCount = 0
        dev = []
        
    for i in values:
        cx1, cy1 = i
        cv2.circle(frame, (cx1,cy1), 5, (0, 0, 0), -1)
        values.remove(i)

    
    print(pos1, pos2, pos3)


    # ! REMOVE/DEAL WITH OBJECTS WHOSE ITERATIONS HAVE ENDED
    for obj in objects_tracked:
        if obj[0]==3:
            objects_tracked.remove(obj)

    # * CHANGING FRAMES HERE
    cv2.imshow("Frame", frame)  # show the frame in window
    # cv2.waitKey(0) # wait for keydown to move to next iteration
    key = cv2.waitKey(1)
    if key == 27:
        break

    previous_centers = current_centres

cap.release()  # release file element
cv2.destroyAllWindows()