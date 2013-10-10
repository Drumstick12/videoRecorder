__author__ = 'Fabian Sinz'

import cv2
import cv
class VideoRecording:

    def __init__(self, filename, resolution, fps, codec):

        self.writer = cv2.VideoWriter(filename , cv.CV_FOURCC(*codec), int(fps), resolution, True)

    def write(self, frame):
        self.writer.write(frame)


    def stop(self):
        pass