import threading


class Threads:
    def __init__(self, function, args=[]) -> None:
        self.new_thread = threading.Thread(target=function, args=(*args,))

    def start(self):
        self.new_thread.start()

    def join(self):
        self.new_thread.join()
