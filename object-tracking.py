import cv2
import numpy as np 
from object_detection import ObjectDetection
import math


# Init object detection
od = ObjectDetection()

cap = cv2.VideoCapture("los_angeles.mp4") # load the video element

#init count

frameCount = 0
centerPointsPrevious = []
trackingObjects = {}
trackId = 0

while True:  # read one frame at a time, with while loop until error exit.
    ret, frame = cap.read() # read the frame => boolean, frame
    frameCount+=1
    if not ret:
        break

    currentCenterPoints = []

    # * DETECT OBJECTS ON THE FRAME AND DRAW RECTANGLES
    (class_ids, scores, boxes) = od.detect(frame)
    for box in boxes:
        (x, y, w, h) = box
        cx = int((x+x+w)/2)
        cy = int((y+y+h)/2)
        currentCenterPoints.append((cx, cy))
        # print(f"frame {frameCount} box: ", x, y, w, h)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # frame, topleft, bottomright, color bgr, thickness

    if frameCount <= 2:
        for pt in currentCenterPoints:
            for pt2 in centerPointsPrevious:
                distance = math.hypot(pt2[0]-pt[0], pt[1]-pt[1])
                if distance<20:
                    trackingObjects[trackId] = pt
                    trackId+=1
    else: 
        currentCenterPointsCopy = currentCenterPoints.copy()
        for objectId, pt2 in trackingObjects.copy().items():
            objectExists = False
            for pt in currentCenterPointsCopy:
                distance = math.hypot(pt2[0]-pt[0], pt[1]-pt[1])
                if distance<20:
                    trackingObjects[objectId] = pt
                    objectExists = True
                    continue


            # remove id if outofframe
            if not objectExists:
                trackingObjects.pop(objectId)


    for objectId, pt in trackingObjects.items():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1) # frame, center coords, radius, color bgr, thickness (-1 means solid fill)
        cv2.putText(frame, str(objectId), (pt[0], pt[1]-7), 0, 1, (0, 0, 255), 2)

    print(trackingObjects)
    print('curr pts\n', currentCenterPoints)
    print('prev pts\n', centerPointsPrevious)

    centerPointsPrevious = currentCenterPoints.copy()

    # * CHANGING FRAMES HERE
    cv2.imshow("Frame", frame)  # show the frame in window 
    # cv2.waitKey(0) # wait for keydown to move to next iteration
    key = cv2.waitKey(0)
    if key==27:
        break

cap.release() #release file element
cv2.destroyAllWindows()