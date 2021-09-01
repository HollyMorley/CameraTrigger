import sys
sys.path.append("./")
from Config import Config
from fcutils.video.video_editing import Editor

class TrimVideos(Editor):
    def __init__(self, video_to_edit):
        Editor.__init__(video_to_edit)

        trim_clip(videopath, savepath)


if __name__ == "__main__":
    videopath = "C:\\Users\\Holly Morley\\Dropbox (UCL - SWC)\\APA Project\\Data\\Behaviour\\Transparent_treadmill_Walking\\Raw_Videos\\20200923\\HM-20200923FR_cam0_2-copy.avi"  # <--- path to the video to edit
    savepath = "C:\\Users\\Holly Morley\\Dropbox (UCL - SWC)\\APA Project\\Data\\Behaviour\\Transparent_treadmill_Walking\\Trimmed_Videos\\HM-20200923FR_cam0_2-copyCLIP1.avi"
    #trimvideos = TrimVideos(videopath,savepath,start=100,stop=200)