import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import cv2
import imutils
import threading
from deepface import DeepFace


def start_webcam(a):
    videoCapture = cv2.VideoCapture(0)  # Setting the video stream
    if videoCapture.isOpened():
        while True:
            ret, frame = videoCapture.read()
            frame = imutils.resize(frame, width=900)
            frame = cv2.flip(frame, 1)

            if ret:
                cv2.imshow("Dev", frame)
                k = cv2.waitKey(1)
                if k == ord("q"):
                    break
        videoCapture.release()
        cv2.destroyAllWindows()


def checkFace(frame):
    result = DeepFace.verify(
        frame,
        "./test/daniel_img_1.png",
        model_name="Facenet",
        detector_backend="retinaface",
        enforce_detection=False,
    )
    print(result)


def main():
    person_detected = False
    amount_of_people = 0
    thread_started = False
    videoCapture = cv2.VideoCapture(0)  # Setting the video stream
    if videoCapture.isOpened():
        while True:
            ret, frame = videoCapture.read()
            frame = imutils.resize(frame, width=900)
            frame = cv2.flip(frame, 1)
            faces = DeepFace.extract_faces(
                frame, detector_backend="ssd", enforce_detection=False
            )

            def check_for_faces():
                threading.Timer(1.0, check_for_faces).start()
                nonlocal faces
                nonlocal person_detected
                nonlocal amount_of_people
                print(1)
                for idx, face in enumerate(faces):
                    if faces[0]["confidence"] * 100 > 90:
                        person_detected = True
                    else:
                        person_detected = False
                        amount_of_people = 0

            if not thread_started:
                check_for_faces()
                thread_started = True

            if person_detected and len(faces) > amount_of_people:
                result = DeepFace.verify(
                    frame,
                    "./test/daniel_img_1.png",
                    model_name="VGG-Face",
                    detector_backend="ssd",
                    enforce_detection=False,
                )
                amount_of_people = len(faces)
                person_detected = False
                print(result)

            if ret:
                cv2.imshow("Dev", frame)
                k = cv2.waitKey(1)
                if k == ord("q"):
                    break
        videoCapture.release()
        cv2.destroyAllWindows()


# a = []
# t1 = threading.Thread(target=start_webcam, args=(a,))  # Webcam
# t1.start()
# print(a)
# t2 = threading.Thread(target=checkFace, args=(a,))  # Facial Recognition
# t2.start()
# t1.join()
# t2.join()
# print(a)


main()

# objs = DeepFace.analyze(
#     img_path="./test/daniel_img_0.png", actions=["age", "gender", "race", "emotion"]
# )

# dfs = DeepFace.find(
#     img_path="./test/daniel_img_1.png", db_path="./test", enforce_detection=False
# )

# DeepFace.stream(db_path="./test")
