import warnings

__author__ = 'fabee'
import cv2


class Camera:
    def __init__(self, post_processor= None):
        """
        Initializes a new camera

        :param post_processor: function that is applies to the frame after grabbing
        """
        self.capture = None
        if post_processor is None:
            self.post_processor = lambda x: x

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def open(self):
        capture = cv2.VideoCapture(0)
        self.capture = capture

    def get_properties(self):
        """

        :returns: the properties (cv2.cv.CV_CAP_PROP_*) from the camera
        :rtype: dict
        """
        if self.capture is not None:
            properties = [e for e in dir(cv2.cv) if "CV_CAP_PROP" in e]
            ret = {}
            for e in properties:
                ret[e[12:].lower()] = self.capture.get(getattr(cv2.cv,e))
            return ret
        else:
            warnings.warn("Camera needs to be opened first!")
            return None

    def grab_frame(self):
        flag, frame = self.capture.read()

        if not flag:
            warnings.warn("Coulnd't grab frame from camera!")
            return None
        else:
            return self.post_processor(frame)
        return


    def close(self):
        pass

