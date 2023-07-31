import os
import cv2

from deepface import DeepFace
from Threads import Threads
from WebCam import WebCam
from PrintInfo import print_info


class DeepFaceObject:
    def __init__(self) -> None:
        self.faces = []
        self.person = []
        self.people_info = {}
        self.amount_of_people = 0
        self.searching_active = False
        self.searched_person = None
        self.search_number = 0

    def find_face(self, camera):
        def thread_start_find_face():
            while camera.open():
                frame = camera.request_frame()
                if type(frame) is bool and frame == False:
                    print("Starting up.")
                    os.system("cls")
                    print("Starting up..")
                    os.system("cls")
                    print("Starting up...")
                    os.system("cls")
                else:
                    face_captured = camera.request_frame()
                    temp_database = "F:/python/faceMe/dev/test"
                    try:
                        person = DeepFace.find(
                            face_captured[100:680, 400:880],
                            db_path=temp_database,
                            detector_backend="ssd",
                            enforce_detection=False,
                            silent=True,
                        )
                    except:
                        print("Too Close!")
                    if len(person[0]) != 0:
                        verify = DeepFace.verify(
                            img1_path=face_captured,
                            img2_path=person[0]["identity"][0],
                            detector_backend="ssd",
                            enforce_detection=False,
                        )
                        if verify["verified"] and person:
                            name = (
                                person[0]["identity"][0]
                                .split("\\")[-1]
                                .split("/")[-1]
                                .replace(".jpg", "")
                            )
                            self.people_info[name] = verify["facial_areas"]["img1"]
                            self.searching_active = False
                            self.search_number = 0
                    else:
                        self.people_info = {}
                    if self.people_info:
                        camera.render_info(
                            person="daniel",
                            xy_start=[
                                self.people_info["daniel"]["x"] + 300,
                                self.people_info["daniel"]["y"],
                            ],
                            xy_end=[
                                self.people_info["daniel"]["x"] + 600,
                                self.people_info["daniel"]["y"] + 400,
                            ],
                        )
                    else:
                        camera.reset_info()

        deep_face_thread = Threads(thread_start_find_face)
        deep_face_thread.start()
        deep_face_thread.join()
