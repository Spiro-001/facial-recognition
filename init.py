import sys
import os

sys.path.insert(0, "./utils")

from WebCam import WebCam
from Threads import Threads
from DeepFace import DeepFaceObject


def main():
    face_me = DeepFaceObject()  # Create DeepFace Object
    camera = WebCam()  # Camera default device 0
    camera_thread = Threads(camera.start)  # New thread for opening and rendering camera
    find_face_thread = Threads(face_me.find_face, args=(camera,))
    camera_thread.start()
    find_face_thread.start()
    camera_thread.join()
    find_face_thread.join()


main()
