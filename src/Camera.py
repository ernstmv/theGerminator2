from cv2 import cvtColor, COLOR_BGR2RGB, imdecode
from requests import get
from numpy import array, uint8
from imutils import resize


class Camera():
    def __init__(self, ip):
        self.ip = ip
        self.url = 'http://' + self.ip + ':8080/shot.jpg'
        self.port = 80

    def get_image(self):
        img_resp = get(self.url)
        img_arr = array(bytearray(img_resp.content), dtype=uint8)
        img = imdecode(img_arr, -1)
        img = resize(img, width=700, height=1300)
        return cvtColor(img, COLOR_BGR2RGB)
