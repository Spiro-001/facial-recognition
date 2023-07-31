import cv2


def verify_camera(video):  # Verify camera device is working
    while not video.isOpened():
        print("Attempting to connect to another camera...")
        for deviceNumber in range(0, 4):  # Trying different devices
            video = cv2.VideoCapture(deviceNumber)
            print(f"Trying for camera device {deviceNumber}")
            if video.isOpened():
                print("Camera successfully connected!")
                return video
        if not video.isOpened():
            print("Unable to connect to a camera device.")
            return video
    return video
