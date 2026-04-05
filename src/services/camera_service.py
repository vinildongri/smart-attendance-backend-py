import cv2
from src.config.settings import settings

class CameraService:
    def __init__(self):
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(settings.CAMERA_ID)
        return self.cap.isOpened()

    def get_frame(self):
        ret, frame = self.cap.read()
        return ret, frame

    def stop(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()

camera_service = CameraService()