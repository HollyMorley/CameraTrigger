from imutils.video import VideoStream
import numpy as np
import datetime
import imutils
import time
import glob
import cv2
from Stitcher import Stitcher
import tqdm.auto


'''
############ Workflow ###############

Read frames from both videos using the cv2.VideoCapture function.
Once have both frames, apply the stitching code (depending on performance, compare with https://towardsdatascience.com/image-panorama-stitching-with-opencv-2402bde6b46c).
Add stitched frame to new video using cv2.VideoWriter function.

|- Create video capture 

'''

# set up capture objects
cap1 = cv2.VideoCapture(r"C:\Experiment_development_and_testing\video_stitching_test\videos\20211020\HM-20211020stitch_test_travelator_cam0_1.avi")
cap2 = cv2.VideoCapture(r"C:\Experiment_development_and_testing\video_stitching_test\videos\20211020\HM-20211020stitch_test_travelator_cam1_1.avi")

# caps = [] ###################### eventually make caps a list dependent on left/right label in name
# videoList=glob.glob(r"C:\Experiment_development_and_testing\video_stitching_test\videos\20211006\*.avi")
# for path in videoList:
#     cap = cv2.VideoCapture(path)
#     if not cap.isOpened():
#         print("error opening", path)
#     else:
#         caps.append(cap)

# read metadata from (AT THE MOMENT ONE) file
fps = []
Frame_size = []
Frame_count = []
FPS = []
for c in [cap1, cap2]:
    if c.isOpened() == False:
        print("Error opening the video file")
    else:
        # Get frame rate information
        fps = int(c.get(5))
        FPS.append(fps)

        # Get frame count
        frame_count = c.get(7)
        Frame_count.append(frame_count)

        # Obtain frame size information using get() method
        frame_width = int(c.get(3))
        frame_height = int(c.get(4))
        frame_size = (frame_width, frame_height)
        Frame_size.append(frame_size)

if FPS[0] == FPS[1]:
    print("Frame rate : ", FPS[0], "frames per second")
else:
    print("Frame rates are different between videos")
if Frame_count[0] == Frame_count[1]:
    print("Frame count : ", Frame_count[0])
else:
    print("Frame counts are different between videos")
if Frame_size[0] == Frame_size[1]:
    print("Frame size : ", Frame_size[0])
else:
    print("Frame sizes are different between videos")


# initialize stitcher
stitcher = Stitcher()
total = 0

# iterate through videoframes
frames1 = []
frames2 = []
result = []
count = 0
Stch = []
with tqdm.tqdm(total=int(frame_count), position=0, leave=True) as pbar:
    while cap1.isOpened() or cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        frame1 = imutils.resize(frame1, width=600, height=109)
        frame2 = imutils.resize(frame2, width=600, height=109)
        if ret1 == True:
            frames1.append(frame1)
            #cv2.imshow('Frame1', frame1)
        if ret2 == True:
            frames2.append(frame2)
            #cv2.imshow('Frame2', frame2)
        if ret1 == True and ret2 == True:
            stch = stitcher.stitch([frame1, frame2])
            Stch.append(stch)
        # count+=1
        # print(count)
        if ret1 == False and ret2 == False:
            break
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        pbar.update(1)
cap1.release()
cap2.release()
cv2.destroyAllWindows()

# initialize video writer object
stch_shape = Stch[0].shape # get shape of new stitched image
stch_height = stch_shape[0]
stch_width = stch_shape[1]
new_frame = cv2.VideoWriter(r"C:\Experiment_development_and_testing\video_stitching_test\videos\20211006\test_stitch.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), FPS[0], [stch_width, stch_height])