import sys

sys.path.append("./")

import os
import numpy as np
import time
import csv

import Camera
import Config
from fcutils.file_io import utils


class Main(Camera.Camera, Config.Config):

    def __init__(self):
        super().__init__()
        #Config.__init__(self)  # load the config paramaters
        #Camera.__init__(self)

    def setup_experiment_files(self):
        # Takes care of creating a folder to keep the files of this experiment
        # Checks if files exists already in that folder
        # Checks if we are overwriting anything
        # Check if exp folder exists and if it's empty
        utils.check_create_folder(self.experiment_folder)
        if not utils.check_folder_empty(self.experiment_folder):
            print("\n\n!!! experiment folder is not empty, might risk overwriting stuff !!!\n\n")

        # Create files for videos
        if self.save_to_video:
            self.video_files_names = [os.path.join(self.experiment_folder, "HM-" + self.experiment_name + "_cam{}".format(i) + "_" + self.trialnum + "{}".format(self.camera_config["video_format"])) for i in np.arange(self.camera_config["n_cameras"])]
            #self.video_files_names = [os.path.join(self.experiment_folder, self.experiment_name + "_cam{}{}".format(i, self.camera_config["video_format"])) for i in np.arange(self.camera_config["n_cameras"])]
            self.video_data_files_names = [os.path.join(self.experiment_folder, "HM-" + self.experiment_name + "_cam{}".format(i) + "_" + self.trialnum + "_VideoData") for i in np.arange(self.camera_config["n_cameras"])]
            self.video_data_fps_files_names = [os.path.join(self.experiment_folder, "HM-" + self.experiment_name + "_cam{}".format(i) + "_" + self.trialnum + "_FPSData") for i in np.arange(self.camera_config["n_cameras"])]

            # Check if they exist already
            for vid in self.video_files_names:
                if utils.check_file_exists(vid) and not self.overwrite_files: raise FileExistsError(
                    "Cannot overwrite video file: ", vid)

    def terminate_experiment(self):
        """
            This function gets called when the user interrupts the execution of the experiments.
            It takes care of printing a summary, plotting stuff, closing the ffmpeg writers etc etc
        """
        exp_duration = round(time.time() - self.exp_start_time / 1000, 2)
        print("""\n\n\nTerminating experiment. Acquired {} frames in {}s.
                {}s / {}fps -> {} frames, 
                {} frames acquired, actual framerate: {}""".format(self.frame_count, exp_duration, exp_duration,
                                                                   self.acquisition_framerate,
                                                                   int(exp_duration * self.acquisition_framerate),
                                                                   self.frame_count,
                                                                   round(self.frame_count / exp_duration, 2)))


        with open(self.video_data_files_names[0] + ".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Total frames acquired", "Total recording time", "acquisition framerate", "frames acquired",
                 "actual framerate"])
            writer.writerow([self.frame_count, exp_duration, self.acquisition_framerate,
                             int(exp_duration * self.acquisition_framerate), round(self.frame_count / exp_duration, 2)])


        start_again = input("\n\nTo record another trial with this mouse, press 'y'.\nTo stop the experiment, press 'n'.")
        start_again = start_again.strip().lower()
        if start_again == 'y':
            print("next trial starting...")
            os.system('clear')
            self.trialnum_raw += 1
            self.trialnum = str(self.trialnum_raw)
            m.setup_experiment_files()
            self.frame_count = 0
            m.start_experiment()
        elif start_again == 'n':
            print("exp closed")
            # Close pylon windows and ffmpeg writers
            os.system('clear')
            #self.close_pylon_windows()
            self.close_ffmpeg_writers()


    def start_experiment(self):
        self.parallel_processes = []  # store all the parallel processes

        # Start cameras and set them up`
        self.start_cameras()

        # Start streaming videos
        self.exp_start_time = time.time() * 1000  # experiment starting time in milliseconds # ** MOVED TO CAMERA.PY INTO STREAM_VIDEOS AND STREAM_VIDEOS_KEYBOARD BECAUSE RECORDING IS NOW CONDITIONAL

        self.stream_videos_keyboard()  # choose between stream_videos() or stream_videos_keyboard()
        self.terminate_experiment()
        '''except Exception as e:
                print("Acquisition terminated with error: ", e)
                self.terminate_experiment()'''


if __name__ == "__main__":
    m = Main()
    m.setup_experiment_files()
    m.start_experiment()
