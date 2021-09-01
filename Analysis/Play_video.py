import numpy as np
import cv2

#cap = cv2.VideoCapture('C:\\Users\\Holly Morley\\Dropbox (UCL - SWC)\\APA Project\\Data\\Behaviour\\Dual-belt_APAs\\videos\\Trimmed_videos\\20201001\\vlc-record-2020-10-01-19h00m08s-HM-20201001FLR_cam0_7.mp4')
cap = cv2.VideoCapture('Z:\\Holly\\vlc-record-2020-12-03-15h57m58s-20201203FLR_webcam.avi')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break
        break

cap.release()
cv2.destroyAllWindows()