import cv2
from sys import exit
from logging import warning, error

class Camera:
    def __init__(self, debug_mode, camera_index):
        self.debug_mode = debug_mode
        self.capture_device = cv2.VideoCapture(camera_index)
        self.capture_device.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    @property
    def is_open(self):
        if not self.capture_device.isOpened():
            error('The camera is not opened')
            exit()
        return True

    def close(self, warn=False):
        self.capture_device.release()
        if self.debug_mode: #if not in debug mode, there will be no window to destroy
            cv2.destroyAllWindows()
        if warn:
            warning('The camera has been closed')
            exit()

    def get_frame(self):
        frame = self.capture_device.read() #this returns a tuple, index 0 is True if the frame was grabbed, index 1 is the frame itself
        if type(frame) is bool or frame[1] is None: #if the camera failed to grab a frame, 'frame' is False instead of a tuple, or index 1 of the tuple is None
            self.close()
            error('The camera was unable to grab a frame')
            exit()
        return frame[1]

    def show_frame(self, frame):
        if not self.debug_mode: #only show the frame in debug mode
            return
        cv2.imshow('camera', frame)
        if cv2.waitKey(1) == 27: #27 is the 'Esc' (escape) key
            self.close(True) #'warn' is True, because the escape key is pressed with the intent to exit the program