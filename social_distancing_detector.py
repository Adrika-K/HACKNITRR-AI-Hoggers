# imports

import numpy as np
from configs import config as cng
from configs.detection import detect_people
import argparse
import imutils as transposetools
import cv2
import os
from scipy.spatial import distance as length
x = 2

def calldetection(i , y):
    if i in y:
        __BOX__ = (104, 85, 205)
        return __BOX__


# construct evrything from new
aptsz = argparse.ArgumentParser()
aptsz.add_argument("-i", "--input", type=str, default="", help="path to (optional) input video file")
aptsz.add_argument("-o", "--output", type=str, default="", help="path to (optional) output video file")
aptsz.add_argument("-d", "--display", type=int, default=1, help="whether or not output frame should be displayed")
artgys = vars(aptsz.parse_args())

# initializing YOLO
Pathlabels_name = os.path.sep.join([cng.MODEL_PATH, "coco.names"])
LABELS = open(Pathlabels_name).read().strip().split("\n")

# finding paths
pathweightsinitialize = os.path.sep.join([cng.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([cng.MODEL_PATH, "yolov3.cfg"])


print("IF you see this that means code is working ....")
TrackerPY = cv2.dnn.readNetFromDarknet(configPath, pathweightsinitialize)

# you need gpu for good performance
if cng.Needtheuseofgpu:
    TrackerPY.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    TrackerPY.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

notlt = TrackerPY.getLayerNames()
notlt = [notlt[i - 1] for i in TrackerPY.getUnconnectedOutLayers()]

# loading video stream
print("if you see this that means everything is working fine")
# no video ?!! no problem it loads webcam also
vs = cv2.VideoCapture(artgys["input"] if artgys["input"] else 0)
VideoWriter = None


while True:
    (gand, ftrrate) = vs.read()
    if not gand:
        break


    ftrrate = transposetools.resize(ftrrate, width=800)
    solutionsss = detect_people(ftrrate, TrackerPY, notlt, personIdx=LABELS.index("person"))


    violationdeetector = set()
    y = violationdeetector


    if len(solutionsss) >= x:
        # calculation euclidian distance

        centroids = np.array([r[2] for r in solutionsss])
        D = length.cdist(centroids, centroids, metric="euclidean")

        for i in range(0, D.shape[0]):
            for j in range(i+1, D.shape[1]):

                if D[i, j] < cng.distanceminimum:
                    y.add(i)
                    y.add(j)
    

    for (i, (prob, bbox, centroid)) in enumerate(solutionsss):

        (TX, TY, EX, EY) = bbox
        (cX, cY) = centroid
        __BOX__ = (0, 255, 0)

        #Changing the box colour if violation detected
        colourto = calldetection(i , y)
        if i in y:
            __BOX__ = (0, 0, 255)


        cv2.rectangle(ftrrate, (TX, TY), (EX, EY), __BOX__, 2)
        cv2.circle(ftrrate, (cX, cY), 5, __BOX__, 1)


    TextToShow = "Number of violation: {}".format(len(y))
    cv2.putText(ftrrate, TextToShow, (10, ftrrate.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 3)


    if artgys["display"] > 0:
        # show the output maynot properly work for everyone
        cv2.imshow("Output", ftrrate)
        key = cv2.waitKey(1) & 0xFF

        # press 'u' to [exit / break loop] press if video is too long and dont have time to wait
        if key == ord("u"):
            break
    

    if artgys["output"] != "" and VideoWriter is None:
        # initialize the video writer
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        VideoWriter = cv2.VideoWriter(artgys["output"], fourcc, 25, (ftrrate.shape[1], ftrrate.shape[0]), True)


    if VideoWriter is not None:
        print("Writing Video , ya!!!! wait some time to see the output video")
        VideoWriter.write(ftrrate)

