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
def extendSlope(pt1, pt2):
    distX = abs(pt2[0]-pt1[0])
    distY = abs(pt2[1]-pt1[1])
    pt3 = (pt2[0]+distX, pt2[1]+distY)
    pt4 = (pt3[0]+distX, pt3[1]+distY)
    pt5 = (pt4[0]+distX, pt4[1]+distY)
    return pt3, pt4, pt5


# ! VARIABLES
objects_tracked = []  # ? [frames (max = 5), [x, y], [x, y], ...]
frameCount = 0
previous_centers = []  # ? [[x, y]]
predicted_points = []  # ? []
max_distance = 30
display_points = []

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

    if frameCount == 1:
        previous_centers.append(current_centres)
    else:
        for cur_point in current_centres:                       # loop thru current points
            isTracked = False                                   # initialise tracking as false
            for prev_point in previous_centers:                 # loop through previous points
                distance = math.dist(cur_point, prev_point)     # find distance
                if distance <= max_distance:                    # if it is the same point
                    for obj in objects_tracked:                 # loop through objects being tracked
                        closestPoint = obj[obj[0]]
                        deviation = abs(prev_point[0]-closestPoint[0]) + abs(prev_point[1]-closestPoint[1])

                        if deviation < 5:                     # find object in objects_tracked
                            isTracked = True                            # confirm it is being tracked, set boolean
                            if obj[0]<=5:                                 # if algorithm loop applies
                                if obj[0] == 1:                     # if it is second frame of object
                                    pc1, pc2, pc3 = extendSlope(obj[1], cur_point)     # predict value for third loop
                                    obj.append(cur_point)
                                    obj.append(pc1)
                                    obj.append(pc2)
                                    obj.append(pc3)
                                    obj[0] += 1
                                    cv2.circle(frame, pc1, 5, (255, 0, 255), -1)           # prpl for predicted location
                                    cv2.circle(frame, pc2, 5, (255, 0, 255), -1)           # prpl for predicted location
                                    cv2.circle(frame, pc3, 5, (255, 0, 255), -1)           # prpl for predicted location
                                    cv2.circle(frame, cur_point, 3, (0, 255, 255), -1)      # ylo for current location
                                    print('second',obj)
                                elif obj[0] <5:                               # if it is third frame of object
                                    # TODO: draw circles at predicted and actual coordinates
                                    obj[0] += 1 
                                    cv2.circle(frame, obj[3], 5, (255, 0, 255), -1)           # prpl for predicted location
                                    cv2.circle(frame, obj[4], 5, (255, 0, 255), -1)           # prpl for predicted location
                                    cv2.circle(frame, obj[5], 5, (255, 0, 255), -1)           # prpl for predicted location
                                    cv2.circle(frame, cur_point, 3, (0, 255, 255), -1)      # ylo for current location
                    continue
            if not isTracked:
                # add object to being tracked if not tracked
                objects_tracked.append([1, cur_point])
                print('added new',objects_tracked)


    # # ! REMOVE/DEAL WITH OBJECTS WHOSE ITERATIONS HAVE ENDED
    for obj in objects_tracked:
        if obj[0]==5:
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
