import sys
sys.path.append("./")
from Config import Config
from fcutils.video.video_editing import Editor as VideoUtils
from fcutils.video.utils import manual_video_inspect


# ? To manually inspect a video frame by frame:
# 1) Specify the path to the video you want to analyse
# 2) Run this script

class Inspector(Config, VideoUtils):
    def __init__(self, video_to_inspect):
        Config.__init__(self)
        VideoUtils.__init__(self)

        #self.manual_video_inspect(video_to_inspect, rescale=4)
        manual_video_inspect(video_to_inspect)


if __name__ == "__main__":
    videofile = "C:\\Users\\Holly Morley\\Dropbox (UCL - SWC)\\APA Project\\Data\\Behaviour\\Transparent_treadmill_Walking\\Videos\\20200923\\HM-20200923FR_cam0_2.avi"  # * <--- path to the video to analyse
    inspector = Inspector(videofile)