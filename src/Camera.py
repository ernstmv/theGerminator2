import cv2
import requests
import numpy as np
import imutils
import subprocess


class Camera():
    def __init__(self, ip):
        self.ip = ip
        self.url = 'http://' + self.ip + ':8080/shot.jpg'
        self.port = 80

    def check_connection(self):
        process = subprocess.Popen(
                ['ping', '-c', '1', self.ip],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            return True
        else:
            return False

    def get_image(self):
        img_resp = requests.get(self.url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = imutils.resize(img, width=800, height=600)
        return img

    def destroy_window():
        cv2.destroyAllWindows()
