import cv2
import requests
import numpy as np
import imutils
import subprocess
from PIL import Image
import customtkinter as ctk


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
        img = imutils.resize(img, width=700, height=1300)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def convert_image(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(image)
        img_ctk = ctk.CTkImage(
                light_image=img_pil,
                size=(img.shape[1], img.shape[0]))
        return img_ctk
