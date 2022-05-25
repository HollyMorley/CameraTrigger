#from utils.constants import *
import time
import serial


# Define a config class with all the options for data acquisition and post-hoc analysis
class Config:
    """
        ############## EXPERIMENT CONFIG  ####################
    """
    date = time.strftime('%Y%m%d')
    experiment_setup = 'DualBelt'

    # ! Change these for every recording
    if experiment_setup == 'Treadmill':
        experiment_folder = "E:\\Data\\Behaviour\\Transparent_treadmill_Walking\\Videos\\" + date
    elif experiment_setup == 'DualBelt':
        #experiment_folder = "E:\\Data\\Behaviour\\DualTravellator\\Videos\\" + date
        experiment_folder = "C:\\Experiment_development_and_testing\\Side_overhead_front_test\\videos\\" + date

    #experiment_folder = "C:\\Users\\Holly Morley\\Dropbox (UCL - SWC)\\Videos" + date
    #experiment_folder = "C:\\Users\\Holly Morley\\Dropbox (UCL - SWC)\\APA Project\\Data\\Behaviour\\Transparent_treadmill_Walking\\test_videos\\" + date  # ? This should be changed for every experiment to avoid overwriting

    experiment_name = date + "250fps"  # YYMMDD_MOUSEID, all files for an experiment will start with this name
    trialnum_raw = 1
    trialnum = str(trialnum_raw)
    experiment_duration = None  # acquisition duration in seconds, alternatively set as None


    if experiment_setup == 'Treadmill':
        acquisition_framerate = 166 #330  # fps of camera triggering -> NEED TO SPECIFY SLEEP TIME IN ARDUINO for frame triggering
    elif experiment_setup == 'DualBelt':
        acquisition_framerate = 250


    overwrite_files = True # ! ATTENTION: this is useful for debug but could lead to overwriting experimental data
    save_to_video = True  # ! decide if you want to save the videos or not

    """
        ############## CAMERA CONFIG  ####################
    """
    # * These options should not be changed frequently unless  something changes in the experiment set up

    if experiment_setup == 'Treadmill':
        camera_config = {
            "video_format": ".avi",
            "n_cameras": 1,  # changed on 05/11/2019 to run only one camera
            "timeout": 100,   # frame acquisition timeout

            # ? Trigger mode and acquisition options -> needed for constant framerate
            "trigger_mode": True,  # hardware triggering
            "acquisition": {
                "exposure": "297", # treadmill= 297
                "frame_width": "992", # treadmill= 992; OLD "832",  # must be a multiple of 32
                "frame_height": "575", # treadmill= 575;  must be a multiple of 32
                "gain": "5.82685", #treadmill= 5.82685
                "frame_offset_y": "423", #treadmill = 423
                "frame_offset_x": "672", # treadmill = 672
            },


            # all commands and options  https://gist.github.com/tayvano/6e2d456a9897f55025e25035478a3a50
            # pixel formats https://ffmpeg.org/pipermail/ffmpeg-devel/2007-May/035617.html

            # "outputdict":{ # for ffmpeg
            #     "-vcodec": "mpeg4",   #   low fps high res
            #     '-crf': '0',
            #     '-preset': 'slow',  # TODO check this
            #     '-pix_fmt': 'gray',  # yuvj444p
            #     "-cpu-used": "1",  # 0-8. defailt 1, higher leads to higher speed and lower quality
            #     # "-r": "100", #   output video framerate
            #     "-flags":"gray",
            #     # "-ab":"0",
            #     # "-force_fps": "100"
            # },
            "outputdict":{
                "-c:v": 'libx264',   #   low fps high res
                "-crf": '17',
                "-preset": 'ultrafast',
                "-pix_fmt": 'yuv444p',
                "-r": str(acquisition_framerate),
            },

            "inputdict":{
                "-r": str(acquisition_framerate),
            }
        }

    elif experiment_setup == 'DualBelt':
        camera_config = {
            "video_format": ".avi",
            "n_cameras": 3,  # changed on 05/11/2019 to run only one camera
            "cam_names": ["overhead", "side", "front"],
            "timeout": 100,  # frame acquisition timeout

            # ? Trigger mode and acquisition options -> needed for constant framerate
            "trigger_mode": True,  # hardware triggering
            "acquisition_side": {
                "exposure": "300",
                "frame_width": "1984",
                "frame_height": "230",
                "gain": "0",
                "frame_offset_y": "454",
                "frame_offset_x": "0",
                "frame_reverse_x": "true",
                "frame_reverse_y": "true",
            },
            "acquisition_overhead": {
                "exposure": "300",
                "frame_width": "1664",
                "frame_height": "130",
                "gain": "0",
                "frame_offset_y": "383",
                "frame_offset_x": "288",
                "frame_reverse_x": "true",
                "frame_reverse_y": "false",
            },
            "acquisition_front": {
                "exposure": "300",
                "frame_width": "328",
                "frame_height": "400",
                "gain": "17",
                "frame_offset_y": "355",
                "frame_offset_x": "612",
                "frame_reverse_x": "false",
                "frame_reverse_y": "false",
            },
            # "acquisition": {
            #     # TEST
            #     "exposure": "300",
            #     "frame_width": "1696",  # "1984"
            #     "frame_height": "330",
            #     "gain": "0",
            #     "frame_offset_y": "454",
            #     "frame_offset_x": "0",
            #     "frame_reverse_x": "true",
            #     "frame_reverse_y": "true",
            # },

            # all commands and options  https://gist.github.com/tayvano/6e2d456a9897f55025e25035478a3a50
            # pixel formats https://ffmpeg.org/pipermail/ffmpeg-devel/2007-May/035617.html

            # "outputdict":{ # for ffmpeg
            #     "-vcodec": "mpeg4",   #   low fps high res
            #     '-crf': '0',
            #     '-preset': 'slow',  # TODO check this
            #     '-pix_fmt': 'gray',  # yuvj444p
            #     "-cpu-used": "1",  # 0-8. defailt 1, higher leads to higher speed and lower quality
            #     # "-r": "100", #   output video framerate
            #     "-flags":"gray",
            #     # "-ab":"0",
            #     # "-force_fps": "100"
            # },
            "outputdict": {
                "-c:v": 'libx264',  # low fps high res
                "-crf": '17',
                "-preset": 'ultrafast',
                "-pix_fmt": 'yuv444p',
                "-r": str(acquisition_framerate),
            },

            "inputdict": {
                "-r": str(acquisition_framerate),
            }
        }

    def __init__(self):
        return # don't need to do anything but we need this func