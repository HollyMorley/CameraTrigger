import skvideo.measure
import numpy as np


outputfile = "C:\\Users\\Holly Morley\\Dropbox (UCL - SWC)\\APA Project\\Data\\Behaviour\\Transparent_treadmill_Walking\\Trimmed_Videos\\HM-20200929FL1034186_cam0_1_Run1.avi"

# first produce a yuv for demonstration
vid = skvideo.io.vread(outputfile)
T, M, N, C = vid.shape

# start the FFmpeg writing subprocess with following parameters
writer = skvideo.io.FFmpegWriter(outputfile, outputdict={
  '-vcodec': 'libx264', '-b': '300000000'
})

for i in range(30):
  writer.writeFrame(outputdata[i])
writer.close()

inputdata = skvideo.io.vread(outputfile)

# test each frame's SSIM score
mSSIM = 0
for i in range(30):
  mSSIM += skvideo.measure.ssim(np.mean(inputdata[i], axis=2), np.mean(outputdata[i], axis=2))

mSSIM /= 30.0
print(mSSIM