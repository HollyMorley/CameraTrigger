## code to stitch frames from 2 cameras together **AFTER VIDEOS HAVE BEEN SAVED***

import numpy as np
import cv2
import imutils

class Stitcher:
    def __init__(self):
        # determine if we are using OpenCV v3.X and initialise the cached homography matrix
        self.isv3 = imutils.is_cv3()
        self.cachedH = None

    def stitch(self, images, ratio=0.75, reprojThresh=4.0): # images is the list of two images
        # unpack the images
        (imageB, imageA) = images

        # if the cached homography matrix is None, then need to apply keypoint matching to construct it.
        # The frames should not change across the videos so only need to keypoint match once at the start.
        if self.cachedH is None:
            # detect keypoints and extract
            (kpsA, featuresA) = self.detectAndDescribe(imageA)
            (kpsB, featuresB) = self.detectAndDescribe(imageB)

            # match features between the two images
            M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)

            # if the match is None, then there aren't enough matched keypoints to create a panorama
            if M is None:
                return None

            # cache the homography matrix
            self.cachedH = M[1]

        # apply a perspective transform to stitch the images together using the cached homography matrix
        result = cv2.warpPerspective(imageA, self.cachedH, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        # return the stitched image
        return result

    def detectAndDescribe(self, image):
        # convert image to greyscale
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # check to see if we are using OpenCV 3.X
        if self.isv3:
            # detect and extract features from the image
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)

        # otherwise, we are using OpenCV 2.4.X
        else:
            # detect keypoints in the image
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(grey)

            # extract features from the image
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps,features) = extractor.compute(grey, kps)

        # convert the keypoints from KeyPoint objects to NumPy arrays
        kps = np.float32([kp.pt for kp in kps])

        # return a tuple of keypoints and features
        return (kps, features)

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        # compute the raw matches and initialize the list of actual matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []

        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        # computing homography requires at least 4 matches
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (_,i) in matches])
            ptsB = np.float32([kpsB[i] for (i,_) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

            # return the matches along with the homography matrix and status of each matched point
            return (matches, H, status)

        # otherwise, no homography could be computed
        return None

    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # initialise the output visualisation image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB

        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully matched
            if s == 1:
                # draw the match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

        # return the visualisation
        return vis







# # Create video capture object
# vid_capture = cv2.VideoCapture(r"C:\Experiment_development_and_testing\video_stitching_test\videos\20211006\HM-20211006stitch_test_cam0_1.avi")
# #vid_captureR = cv2.VideoCapture(r"C:\Experiment_development_and_testing\video_stitching_test\videos\20211006\HM-20211006stitch_test_cam1_1.avi")
#
#
# # Read metadata from file
# fps = []
# frame_size = []
# if vid_capture.isOpened() == False:
#     print("Error opening the video file")
# else:
#     # Get frame rate information
#     fps = int(vid_capture.get(5))
#     print("Frame Rate : ", fps, "frames per second")
#
#     # Get frame count
#     frame_count = vid_capture.get(7)
#     print("Frame count : ", frame_count)
#
#     # Obtain frame size information using get() method
#     frame_width = int(vid_capture.get(3))
#     frame_height = int(vid_capture.get(4))
#     frame_size = (frame_width,frame_height)
#     print("Frame size : ", frame_size)
#
# # Initialise video writer object
# output = cv2.VideoWriter(r"D:\APA_Project\Data\Behaviour\Dual-belt_APAs\videos\Raw_videos\20201130\test_video.avi",
#                          cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, frame_size)
#
# # Read each image frame from file
# print("Writing video...")
# while vid_capture.isOpened():
#     # vCapture.read() methods returns a tuple, first element is a bool and the second is frame
#
#     ret, frame = vid_capture.read()
#     if ret == True:
#         # Write the frame to the output files
#         output.write(frame)
#     else:
#         print("Stream disconnected")
#         break
#
# # Release the objects
# vid_capture.release()
# output.release()