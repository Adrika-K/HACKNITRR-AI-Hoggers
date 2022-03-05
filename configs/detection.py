# imports
from .config import Threshold
from .config import Conf
import numpy as np
import cv2

def detect_people(frame, net, ln, personIdx=0):

    (H, W) = frame.shape[:2]
    results = []


    helloblob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(helloblob)
    nameoflayer = net.forward(ln)


    boxes = []
    centroids = []
    confidences = []

    for output in nameoflayer:
        for detection in output:
            scores = detection[5:]
            IDoftheclasses = np.argmax(scores)
            confidence = scores[IDoftheclasses]



            if IDoftheclasses == personIdx and confidence > Conf:

                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")



                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))


                boxes.append([x, y, int(width), int(height)])
                centroids.append((centerX, centerY))
                confidences.append(float(confidence))


    indexesxt = cv2.dnn.NMSBoxes(boxes, confidences, Conf, Threshold)


    if len(indexesxt) > 0:

        for i in indexesxt.flatten():

            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])


            r = (confidences[i], (x, y, x + w, y + h), centroids[i])
            results.append(r)


    return results
