import cv2
import requests
import numpy as np
import imutils
import socket


class Camera():
    def __init__(self, ip):
        self.ip = ip
        self.url = f'http://{self.ip}:8080/shot.jpg'
        self.port = 80

    def check_conection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            result = sock.connect_ex((self.ip, self.port))
            if result == 0:
                return True
            else:
                return False
        except Exception:
            return False
        finally:
            sock.close()

    def get_image(self):
        img_resp = requests.get(self.url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        img = imutils.resize(img, width=800, height=600)
        return img

    def destroy_window():
        cv2.destroyAllWindows()
