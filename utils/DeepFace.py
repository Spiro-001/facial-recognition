import os
import cv2
import tkinter as tk

from tkinter import filedialog, Text

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
                    face_captured = camera.request_frame()[200:580, 500:780]
                    temp_database = "F:/python/faceMe/dev/test"
                    try:
                        person = DeepFace.find(
                            face_captured,
                            db_path=temp_database,
                            detector_backend="ssd",
                            enforce_detection=False,
                            silent=True,
                        )
                        extracted_faces = DeepFace.extract_faces(
                            face_captured,
                            detector_backend="ssd",
                            enforce_detection=False,
                        )
                        if extracted_faces[0]["confidence"] > 0.9:
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
                                    self.people_info = name
                                    camera.render_info(name)
                                    self.searching_active = False
                                    self.search_number = 0
                            else:  # Person not found in db create profile
                                root = tk.Tk()

                                def sendName():
                                    name = inputtxt.get(1.0, "end-1c")
                                    os.mkdir(f"{temp_database}/{name}")
                                    cv2.imwrite(
                                        f"{temp_database}/{name}/{name}.jpg",
                                        face_captured,
                                    )
                                    os.remove(
                                        f"{temp_database}/representations_vgg_face.pkl"
                                    )
                                    root.destroy()

                                inputtxt = tk.Text(root, height=5, width=20)
                                inputtxt.pack()
                                printButton = tk.Button(
                                    root, text="Confirm", command=sendName
                                )
                                printButton.pack()
                                root.mainloop()
                        else:  # No people present
                            print("No person found")
                            self.people_info = {}
                            camera.reset_info()
                    except (cv2.error, ValueError) as error:
                        if type(error) == cv2.error:  # Too Close
                            print("Too Close!!!")
                        if type(error) == ValueError:  # No Image
                            name = input("Name of Person")
                            os.mkdir(f"{temp_database/{name}}")
                            cv2.imwrite(
                                f"{temp_database}/{name}/{name}.jpg",
                                face_captured,
                            )

        deep_face_thread = Threads(thread_start_find_face)
        deep_face_thread.start()
        deep_face_thread.join()
