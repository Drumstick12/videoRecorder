__author__ = 'Fabian Sinz'

import cv2
import cv
import cPickle as pickle

class VideoRecording:

    def __init__(self, filename, filename_metadata, resolution, fps, codec):
        self.filename_metadata = filename_metadata
        self.writer = cv2.VideoWriter(filename, cv.CV_FOURCC(*codec), int(fps), resolution, True)

    def write(self, frame):
        self.writer.write(frame)

    def write_metadata(self, current_datetime):
        with open(self.filename_metadata, 'ab') as f:
            pickle.dump(current_datetime, f)
            f.flush()

    def stop(self):
        pass