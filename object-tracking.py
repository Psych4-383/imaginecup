import cv2
import numpy as np 
from object_detection import ObjectDetection
import math


# Init object detection
od = ObjectDetection()

cap = cv2.VideoCapture("idk.mp4") # load the video element

#init count

frameCount = 0
centerPointsPrevious = []
trackingObjects = {}
trackId = 0

def extendSlope(){
    distX = pt1[0]-pt2[0]
    distY = pt1[1]-pt2[1]
    pt3 = (pt2[0]+distX, pt2[1]+distY)
    return pt3
}


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
        for objectId, pt2 in trackingObjects.copy().items():
            currentCenterPointsCopy = currentCenterPoints.copy()
            objectExists = False
            for pt in currentCenterPointsCopy:
                distance = math.hypot(pt2[0]-pt[0], pt[1]-pt[1])
                if distance<20:
                    trackingObjects[objectId] = pt
                    objectExists = True
                    currentCenterPoints.remove(pt)
                    continue


            # remove id if outofframe
            if not objectExists:
                trackingObjects.pop(objectId)


    for pt in currentCenterPoints:
        trackingObjects[trackId] = pt
        trackId+=1


    for objectId, pt in trackingObjects.items():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1) # frame, center coords, radius, color bgr, thickness (-1 means solid fill)
        cv2.putText(frame, str(objectId), (pt[0], pt[1]-7), 0, 1, (0, 0, 255), 2)

    print(trackingObjects)
    print('current frame left pts\n', currentCenterPoints)

    centerPointsPrevious = currentCenterPoints.copy()

    # * CHANGING FRAMES HERE
    cv2.imshow("Frame", frame)  # show the frame in window 
    # cv2.waitKey(0) # wait for keydown to move to next iteration
    key = cv2.waitKey(1)
    if key==27:
        break

cap.release() #release file element
cv2.destroyAllWindows()