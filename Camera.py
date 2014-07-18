import warnings
from datetime import datetime

__author__ = 'fabee'
import cv2

def brg2rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def brg2grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

class Camera:
    def __init__(self, device_no=0, post_processor=None):
        """
        Initializes a new camera

        :param post_processor: function that is applies to the frame after grabbing
        """
        self.capture = None
        self.device_no = device_no
        self.post_processor = post_processor
        if post_processor is None:
            self.post_processor = lambda x, y: (x, y)

        self.open()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def open(self):
        capture = cv2.VideoCapture(self.device_no)
        self.capture = capture
        
        # try to increase the resolution of the frame capture; default is 640x480
        #~ self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 864)
        #~ self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        #~ self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
        #~ self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)

    def is_working(self):
        return self.capture.isOpened()


    def get_properties(self):
        """
        :returns: the properties (cv2.cv.CV_CAP_PROP_*) from the camera
        :rtype: dict
        """
        if self.capture is not None:
            properties = [e for e in dir(cv2.cv) if "CV_CAP_PROP" in e]
            ret = {}
            for e in properties:
                ret[e[12:].lower()] = self.capture.get(getattr(cv2.cv, e))
            return ret
        else:
            warnings.warn("Camera needs to be opened first!")
            return None

    def get_resolution(self):
        if self.capture is not None:
            return int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), \
                   int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        else:
            raise ValueError("Camera is not opened or not functional! Capture is None")

    def grab_frame(self):
        dtime = datetime.now()
        flag, frame = self.capture.read()

        if not flag:
            warnings.warn("Coulnd't grab frame from camera!")
            return None
        else:
            return self.post_processor(frame, dtime)
        return


    def close(self):
        pass

