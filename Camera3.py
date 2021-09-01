# VERSION 3
# Script to record videos after and until an IR sensor is activated.
# IR sensor and camera triggering is controlled by an Arduino. The Arduino communicates the beginning and end of
# recording via the serial port.

import subprocess as sp
import os
import datetime
import serial
import pypylon.pylon as py

VideoPath = r"C:\Users\Holly Morley\Dropbox (UCL - SWC)\APA Project\videos\Test_triggeredCamera"
FramesPerSecond = 200
ser = serial.Serial('COM5', 9600)  # connect to com port


# Class to
class FFMPEGVideoWriter:

    def __init__(
            self, filename, size, fps, codec="libx264", audiofile=None, preset="medium", bitrate=None, pixfmt="rgba",
            logfile=None, threads=None, ffmpeg_params=None):

        if logfile is None:
            logfile = sp.PIPE
        self.filename = filename
        self.codec = codec
        self.ext = self.filename.split(".")[-1]

        # order is important
        cmd = [
            r"C:\Users\Holly Morley\PycharmProjects\Packages\ffmpeg\bin\ffmpeg",
            '-y',
            '-loglevel',
            'error' if logfile == sp.PIPE else 'info',
            '-f',
            'rawvideo',
            '-vcodec',
            'rawvideo',
            '-s',
            '%dx%d' % (size[1], size[0]),
            '-pix_fmt',
            pixfmt,
            '-r',
            '%.02f' % fps,
            '-i',
            '-',
            '-an',
        ]
        cmd.extend([
            '-vcodec', codec,
            '-preset', preset,
        ])
        if ffmpeg_params is not None:
            cmd.extend(ffmpeg_params)
        if bitrate is not None:
            cmd.extend([
                '-b', bitrate
            ])
        if threads is not None:
            cmd.extend(["-threads", str(threads)])

        if ((codec == 'libx264') and
                (size[0] % 2 == 0) and
                (size[1] % 2 == 0)):
            cmd.extend([
                '-pix_fmt', 'yuv420p'
            ])
        cmd.extend([
            filename
        ])

        popen_params = {"stdout": sp.DEVNULL,
                        "stderr": logfile,
                        "stdin": sp.PIPE}

        # This was added so that no extra unwanted window opens on windows
        # when the child process is created
        if os.name == "nt":
            popen_params["creationflags"] = 0x08000000  # CREATE_NO_WINDOW

        self.proc = sp.Popen(cmd, **popen_params)

    def write_frame(self, img_array):
        """ Writes one frame in the file."""
        try:
            self.proc.stdin.write(img_array.tobytes()) # note on lit that says use communicate instead of stdin.write
        except IOError as err:
            _, ffmpeg_error = self.proc.communicate()
            error = (str(err) + ("\n\nMoviePy error: FFMPEG encountered "
                                 "the following error while writing file %s:"
                                 "\n\n %s" % (self.filename, str(ffmpeg_error))))

            if b"Unknown encoder" in ffmpeg_error:

                error = error+("\n\nThe video export "
                  "failed because FFMPEG didn't find the specified "
                  "codec for video encoding (%s). Please install "
                  "this codec or change the codec when calling "
                  "write_videofile. For instance:\n"
                  "  >>> clip.write_videofile('myvid.webm', codec='libvpx')")%(self.codec)

            elif b"incorrect codec parameters ?" in ffmpeg_error:

                 error = error+("\n\nThe video export "
                  "failed, possibly because the codec specified for "
                  "the video (%s) is not compatible with the given "
                  "extension (%s). Please specify a valid 'codec' "
                  "argument in write_videofile. This would be 'libx264' "
                  "or 'mpeg4' for mp4, 'libtheora' for ogv, 'libvpx for webm. "
                  "Another possible reason is that the audio codec was not "
                  "compatible with the video codec. For instance the video "
                  "extensions 'ogv' and 'webm' only allow 'libvorbis' (default) as a"
                  "video codec."
                  )%(self.codec, self.ext)

            elif  b"encoder setup failed" in ffmpeg_error:

                error = error+("\n\nThe video export "
                  "failed, possibly because the bitrate you specified "
                  "was too high or too low for the video codec.")

            elif b"Invalid encoder type" in ffmpeg_error:

                error = error + ("\n\nThe video export failed because the codec "
                  "or file extension you provided is not a video")

            raise IOError(error)

    def close(self):
        if self.proc:
            self.proc.stdin.close()
            if self.proc.stderr is not None:
                self.proc.stderr.close()
            self.proc.wait()

        self.proc = None

    # Support the Context Manager protocol, to ensure that resources are cleaned up.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def cam_setup():

    camera = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())
    print("Using device ", camera.GetDeviceInfo().GetSerialNumber())

    # reset to default config before all other settings
    camera.UserSetSelector = "Default"
    camera.UserSetLoad.Execute()

    # HARDWARE SETUP
    camera.LineSelector = "Line4"  # Select GPIO line Line 4
    camera.LineMode = "Input"  # Set the line mode for the selected GPIO line

    # IMAGE ACQUISITION CONTROL
    # below settings are from page 153 of manual
    camera.AcquisitionMode = "Continuous"  # Set the acquisition mode to continuous
    camera.TriggerSelector = "FrameBurstStart"  # Select the frame burst start trigger
    camera.TriggerMode = "Off"  # Set the mode for the selected trigger
    camera.AcquisitionFrameRateEnable = False  # Disable the acquisition frame rate parameter (this will disable the
    # camera’s internal frame rate control and allow you to control the frame rate with external frame start trigger
    # signals)
    camera.TriggerSelector = "FrameStart"  # Select the frame start trigger
    camera.TriggerMode = "On"  # Set the mode for the selected trigger
    camera.TriggerSource = "Line4"  # Set the source for the selected trigger
    camera.TriggerActivation = "RisingEdge"  # Set the trigger activation mode to rising edge
    camera.TriggerDelay = 1  # Set the trigger delay for one millisecond (1000us == 1ms == 0.001s) *NOT SURE ABOUT THIS*
    camera.ExposureMode = "TriggerWidth"  # Set for the trigger width exposure mode
    # camera.ExposureOverlapTimeMax = 500.0
    camera.SensorReadoutMode = "Fast"  # Set and read the sensor readout mode parameter value

    # FEATURES
    camera.Gain = 12.0  # set gain - max is 12
    camera.Width = 992  # Set width, height and offsets # increments of 32
    # camera.OffsetX = 0  # increments of 32
    camera.Height = 300
    # camera.OffsetY = 0
    camera.CenterX = True
    camera.CenterY = True
    # camera.ReverseX = "true"
    # camera.ReverseY = "true"
    # camera.Gamma = 1.2

    return camera


if __name__ == '__main__':
    cam = cam_setup()
    while True:
        SerialMonitor = ser.readline(20)
        if True:
        #if SerialMonitor == b'Camera Start\r\n':
            time_initiated_chunk = datetime.datetime.now()  # start time of recording
            chunk_formatted_time = time_initiated_chunk.strftime("%d-%m-%Y-%H-%M-%S")  # formatting the time

            with FFMPEGVideoWriter(VideoPath + '\\' + chunk_formatted_time + '.avi', (cam.Height(), cam.Width()), fps=FramesPerSecond, pixfmt="rgba") as writer:
                SerialMonitor = ser.readline(20)
                cam.StartGrabbing(py.GrabStrategy_OneByOne)
                while cam.IsGrabbing() and SerialMonitor != 'Camera Finished':  # checks if camera is grabbing
                    res = cam.RetrieveResult(1000, py.TimeoutHandling_ThrowException)
                    writer.write_frame(res.Array)
                    print(res.BlockID)
                    res.Release()
                    SerialMonitor = ser.readline(20)
        break
