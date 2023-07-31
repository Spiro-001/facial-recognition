import cv2
import imutils
import numpy as np
import os
import math

from VerifyCam import verify_camera
from Threads import Threads
from PrintInfo import print_camera_settings


class WebCam:
    def __init__(self, device=0) -> None:
        self.video = cv2.VideoCapture(device)  # Connect to camera device
        self.video = verify_camera(self.video)  # Verify camera device is working
        self.people_info = {}

    def start(self, width=1280, flip=True, window_name="Development", fps=True):
        def thread_start_camera(self, width, flip, window_name):
            # print_camera_settings(width, flip, window_name)
            while True:
                ret, self.frame = self.video.read()
                self.frame = imutils.resize(self.frame, width=width)
                if flip:
                    self.frame = cv2.flip(self.frame, 1)
                if ret:
                    cv2.rectangle(
                        self.frame,
                        [500, 200],
                        [780, 580],
                        (255, 0, 0),
                        2,
                    )

                    if self.people_info:
                        try:
                            shapes = np.zeros_like(self.frame, np.uint8)
                            cv2.rectangle(
                                shapes,
                                [780, 200],  # 200 800
                                [1080, 580],  # 580 1080
                                (255, 255, 255),
                                -1,
                            )
                            output = self.frame
                            alpha = 0.8
                            mask = shapes.astype(bool)
                            output[mask] = cv2.addWeighted(
                                self.frame, alpha, shapes, 1 - alpha, 0
                            )[mask]

                            img = cv2.imread(
                                f"F:/python/faceMe/dev/test/{self.people_info}/{self.people_info}.jpg",
                                1,
                            )
                            img = imutils.resize(img, width=140, height=140)
                            self.frame[210:350, 860:1000] = img[0:140, 0:140]

                            cv2.putText(
                                self.frame,
                                self.people_info,
                                [800, 200],
                                cv2.FONT_HERSHEY_DUPLEX,
                                1,
                                (255, 0, 0),
                                2,
                                cv2.LINE_4,
                            )

                        except Exception as error:
                            print(error)

                    cv2.imshow(window_name, self.frame)

                    k = cv2.waitKey(1)
                    if k == ord("q"):  # Q to terminate camera process
                        break
            self.video.release()
            cv2.destroyAllWindows()
            print("Camera has been closed")

        webCam_thread = Threads(
            thread_start_camera,
            args=(
                self,
                width,
                flip,
                window_name,
            ),
        )

        webCam_thread.start()  # Initialize threading for webcam
        webCam_thread.join()  # Clean up threads

    def request_frame(self):
        if hasattr(self, "frame"):
            return self.frame
        else:
            return False

    def open(self):
        return self.video.isOpened()

    def getFPS(self):
        return self.video.get(cv2.CAP_PROP_FPS)

    def render_info(self, person):
        self.people_info = person

    def reset_info(self):
        self.people_info = {}
