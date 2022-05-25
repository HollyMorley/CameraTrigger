import sys
sys.path.append("./")

import subprocess as sp
import os
import datetime
import serial
import pypylon.pylon as py
import skvideo.io
import cv2
import time
import numpy as np
import keyboard
import csv
import Config
import re


class Camera():
    def __init__(self):
        self.frame_count = 0
        self.cam_writers = {}
        self.grabs = {}
        self.display_frames = {}

    def start_cameras(self):
        self.get_cameras()  # get the detected cameras
        self.get_camera_writers()  # set up a video grabber for each
        self.setup_cameras()  # set up camera parameters (triggering... )

    def get_cameras(self):
        # Get detected cameras
        self.tlFactory = py.TlFactory.GetInstance()
        self.devices = self.tlFactory.EnumerateDevices()
        if not self.devices:
            raise ValueError("Could not find any camera")
        else:
            self.cameras = py.InstantCameraArray(self.camera_config["n_cameras"])

    def get_camera_writers(self):
        # Open FFMPEG camera writers if we are saving to video
        if self.save_to_video:
            for i, file_name in enumerate(self.video_files_names):
                w, h = self.camera_config["acquisition_{}".format(os.path.basename(file_name).split("_")[-2].split(".")[0])]['frame_width'], self.camera_config["acquisition_{}".format(os.path.basename(file_name).split("_")[-2].split(".")[0])][
                    'frame_height']
                indict = self.camera_config['inputdict'].copy()
                indict['-s'] = '{}x{}'.format(w, h)
                self.cam_writers[i] = skvideo.io.FFmpegWriter(file_name, outputdict=self.camera_config["outputdict"],
                                                              inputdict=indict)

                print("Writing to: {}".format(file_name))
        else:
            self.cam_writers = {str(i): None for i in np.arange(self.camera_config["n_cameras"])}

    def setup_cameras(self):
        # set up cameras
        for i, cam in enumerate(self.cameras):
            cam.Attach(self.tlFactory.CreateDevice(self.devices[i]))
            print("Using camera: ", cam.GetDeviceInfo().GetFriendlyName())
            cam.Open()
            cam.RegisterConfiguration(py.ConfigurationEventHandler(),
                                      py.RegistrationMode_ReplaceAll,
                                      py.Cleanup_Delete)

            # Set up Exposure and frame size etc
            if "side" in cam.GetDeviceInfo().GetFriendlyName() :
                cam.OffsetX.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_offset_x"])
                cam.Width.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_width"])
            else:
                cam.Width.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_width"])
                cam.OffsetX.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_offset_x"])
            cam.ExposureTime.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["exposure"])
           # cam.Width.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_width"])
            cam.Height.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_height"])
            cam.Gain.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["gain"])
            cam.OffsetY.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_offset_y"])
         #   cam.OffsetX.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_offset_x"])
            cam.ReverseX.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_reverse_x"])
            cam.ReverseX.FromString(self.camera_config["acquisition_{}".format(re.sub('[^a-zA-Z]+', '', cam.GetDeviceInfo().GetFriendlyName()[3:]))]["frame_reverse_x"])
            '''
            if "side" in cam.GetDeviceInfo().GetFriendlyName():
                cam.ExposureTime.FromString(self.camera_config["acquisition"]["exposureSIDE"])
                cam.Width.FromString(self.camera_config["acquisition"]["frame_widthSIDE"])
                cam.Height.FromString(self.camera_config["acquisition"]["frame_heightSIDE"])
                cam.Gain.FromString(self.camera_config["acquisition"]["gainSIDE"])
                cam.OffsetY.FromString(self.camera_config["acquisition"]["frame_offset_ySIDE"])
                cam.OffsetX.FromString(self.camera_config["acquisition"]["frame_offset_xSIDE"])
                cam.ReverseX.FromString(self.camera_config["acquisition"]["frame_reverse_xSIDE"])
            if "overhead" in cam.GetDeviceInfo().GetFriendlyName():
                cam.ExposureTime.FromString(self.camera_config["acquisition"]["exposureOVERHEAD"])
                cam.Width.FromString(self.camera_config["acquisition"]["frame_widthSIDE"])
                cam.Height.FromString(self.camera_config["acquisition"]["frame_heightSIDE"])
                cam.Gain.FromString(self.camera_config["acquisition"]["gainOVERHEAD"])
                cam.OffsetY.FromString(self.camera_config["acquisition"]["frame_offset_yOVERHEAD"])
                cam.OffsetX.FromString(self.camera_config["acquisition"]["frame_offset_xOVERHEAD"])
                cam.ReverseX.FromString(self.camera_config["acquisition"]["frame_reverse_xOVERHEAD"])
            if "front" in cam.GetDeviceInfo().GetFriendlyName():
                cam.ExposureTime.FromString(self.camera_config["acquisition"]["exposureFRONT"])
                cam.Width.FromString(self.camera_config["acquisition"]["frame_widthSIDE"])
                cam.Height.FromString(self.camera_config["acquisition"]["frame_heightSIDE"])
                cam.Gain.FromString(self.camera_config["acquisition"]["gainFRONT"])
                cam.OffsetY.FromString(self.camera_config["acquisition"]["frame_offset_yFRONT"])
                cam.OffsetX.FromString(self.camera_config["acquisition"]["frame_offset_xFRONT"])
                cam.ReverseX.FromString(self.camera_config["acquisition"]["frame_reverse_xFRONT"])
            '''


            # ? Trigger mode set up
            if self.camera_config["trigger_mode"]:
                print('camera is triggering')
                # Triggering
                if "front" in cam.GetDeviceInfo().GetFriendlyName():
                    cam.LineSelector.FromString('Line2')
                    cam.TriggerSource.FromString('Line2')
                else:
                    cam.LineSelector.FromString('Line4')
                    cam.TriggerSource.FromString('Line4')
                cam.TriggerSelector.FromString('FrameStart')
                cam.TriggerMode.FromString('On')
                #cam.LineSelector.FromString('Line4')
                cam.LineMode.FromString('Input')
                #cam.TriggerSource.FromString('Line4')
                #cam.TriggerActivation.FromString('RisingEdge')

                # ! Settings to make sure framerate is correct
                # https://github.com/basler/pypylon/blob/master/samples/grab.py
                cam.OutputQueueSize = 10
                cam.MaxNumBuffer = 50  # Default is 10
            else:
                print('camera is not triggering')
                cam.TriggerMode.FromString("Off")

            # Start grabbing + GRABBING OPTIONS
            cam.Open()
            cam.StartGrabbing(py.GrabStrategy_LatestImageOnly)

            # ! if you want to extract timestamps for the frames: https://github.com/basler/pypylon/blob/master/samples/grabchunkimage.py

    def print_current_fps(self, start):
        now = time.time()
        elapsed = now - start
        start = now

        # Given that we did 500 frames in elapsedtime, what was the framerate
        time_per_frame = (elapsed / 500) * 1000
        fps = round(1000 / time_per_frame, 2)

        print("     tot frames: {}, current fps: {}".format(self.frame_count, fps))
        return start

    def grab_frames(self):
        for i, (writer, cam) in enumerate(zip(self.cam_writers.values(), self.cameras)):
            try:
                grab = cam.RetrieveResult(self.camera_config["timeout"])
            except:
                raise ValueError("Grab failed for {}".format(cam.GetDeviceInfo().GetFriendlyName()))

            if not grab.GrabSucceeded():
                break
            else:
                if self.save_to_video:
                    writer.writeFrame(grab.Array)
                pass
        return grab

    def stream_videos(self, max_frames=None):
        ser = serial.Serial('COM5', 9600)  # connect to com port
        global start
        start = None
        # # Set up display windows
        # if self.live_display:
        #     image_windows = [py.PylonImageWindow() for i in self.cameras]
        #     self.pylon_windows = image_windows
        #     for i, window in enumerate(image_windows): window.Create(i)

        # ? Keep looping to acquire frames
        # self.grab.GrabSucceeded is false when a camera doesnt get a frame -> exit the loop

        while True:
            serialmonitor = ser.readline(20)
            print(serialmonitor)
            if serialmonitor == b'Camera Running\r\n':
                self.exp_start_time = time.time() * 1000  # experiment starting time in milliseconds
                try:
                    if self.frame_count % 500 == 0:  # Print the FPS in the last 100 frames
                        if self.frame_count == 0:
                            start = time.time()
                        else:
                            start = self.print_current_fps(start)

                    # ! Loop over each camera and get frames
                    grab = self.grab_frames()
                    print('frame grabbed')

                    # Update frame count
                    self.frame_count += 1

                    # Stop if sensor no longer detects mouse is running
                    '''serialmonitor = ser.readline(20)
                    if serialmonitor != b'Camera Running\r\n':
                        print(serialmonitor)
                        print('mouse gone')
                        break'''

                    # Stop if reached max frames
                    if max_frames is not None:
                        if self.frame_count >= max_frames:
                            print("Reached the end of the experiment.")
                            break

                    # stop if enough time has elapsed
                    if self.experiment_duration is not None:
                        if time.time() - self.exp_start_time / 1000 > self.experiment_duration:
                            print("Terminating acquisition - reached max time")
                            raise KeyboardInterrupt("terminating")  # need to raise an error here to be cached in main

                except py.TimeoutException as e:
                    print("Pylon timeout Exception")
                    raise ValueError("Could not grab frame within timeout")

            elif serialmonitor == b'Camera Finished\r\n':
                print('end of loop')
                print(serialmonitor)
                break

        # Close camera
        for cam in self.cameras: cam.Close()
        print("camera was closed")

    def stream_videos_keyboard(self, max_frames=None):
        global start
        initiate_recording = input("Press 'y' to start recording. Press '#' to stop")
        initiate_recording = initiate_recording.strip().lower()
        if initiate_recording == 'y':
            print('RECORDING STARTED')
            self.exp_start_time = time.time() * 1000  # experiment starting time in milliseconds
            while True:
                #perf_start = time.time()
                try:
                    '''loop_start = time.time()'''
                    if self.frame_count % 500 == 0:  # Print the FPS in the last 100 frames
                        if self.frame_count == 0:
                            start = time.time()
                        else:
                            start = self.print_current_fps(start)

                    # ! Loop over each camera and get frames
                    grab = self.grab_frames()
                    #print('frame grabbed')

                    # Update frame count
                    self.frame_count += 1

                    # stop if key is pressed
                    if keyboard.is_pressed('#'):
                        break

                    '''# Stop if reached max frames
                    if max_frames is not None:
                        if self.frame_count >= max_frames:
                            print("Reached the end of the experiment.")
                            break

                    # stop if enough time has elapsed
                    if self.experiment_duration is not None:
                        if time.time() - self.exp_start_time / 1000 > self.experiment_duration:
                            print("Terminating acquisition - reached max time")
                            raise KeyboardInterrupt("terminating")  # need to raise an error here to be cached in main
                            '''

                    '''
                    loop_end = (time.time() - loop_start) * 1000
                    print("frame {} took {} milliseconds".format(self.frame_count, loop_end))

                    #create a csv file showing time taken to complete loop for each frame
                    with open(self.video_data_fps_files_names[0] + ".csv", 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            ["Frame number", "Loop time (ms)"])
                        writer.writerow([self.frame_count, loop_end])
                        '''

                except py.TimeoutException as e:
                    print("Pylon timeout Exception")
                    raise ValueError("Could not grab frame within timeout")

                #perf_end = time.time()
                #loop_perf = perf_end - perf_start
                #print(loop_perf)

            # Close camera
            for cam in self.cameras: cam.Close()
            print("camera was closed")

        else:
            print("something went wrong")

    def close_ffmpeg_writers(self):
        if self.save_to_video:
            for writer in self.cam_writers.values():
                writer.close()