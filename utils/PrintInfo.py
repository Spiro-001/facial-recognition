import os


def print_camera_settings(width, flip, window_name):
    os.system("cls")
    print("Starting camera...")
    os.system("cls")
    print(
        "Camera settings: \nWidth: {}, \nFlipped: {}, \nWindow Name: {}".format(
            width, flip, window_name
        )
    )


def print_info(self, camera):
    os.system("cls")
    print(
        "amount_of_people : {}\n".format(self.amount_of_people),
        "new_person? : {}\n".format(self.searching_active),
        "confidence_score : {}\n".format(self.faces[0]["confidence"]),
        "fps : {}\n".format(camera.getFPS()),
    )
