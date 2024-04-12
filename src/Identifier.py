import cv2
import numpy as np

'''
This class finds the coordinates from each plant detected acording with the
input values (thresh_v, min_a).

Attributes:
    self.img
    self.green_layer
    self.green_threshed

Methods:
    __init__                            Void constructor
    set_image(image)                    Set self.img
    extract_green()                     Set self.green_layer
    process_image(thresh_v)             Set self.green_threshed
    extract_coordinates(min_a)          Find the x, y coordinates of each plant
    find_plants(img, thresh_v, min_a)   Consumes the above functions
'''


class Identifier:

    def __init__(self):
        pass

    def set_image(self, image):
        self.img = image

    def extract_green(self):
        img_lab = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)
        l_green = np.array([35, 60, 60], dtype=np.uint8)
        h_green = np.array([80, 255, 255], dtype=np.uint8)

        self.green_layer = cv2.inRange(img_lab, l_green, h_green)

    def process_image(self, thresh_v):
        img = cv2.GaussianBlur(self.green_layer, (11, 11), -1)
        self.green_threshed = cv2.threshold(
                img,
                thresh_v,
                255,
                cv2.THRESH_BINARY)

    def extract_coordinates(self, min_a):
        conts, _ = cv2.findContours(
                self.green_threshed,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)

        conts = [cont for cont in conts if cv2.contourArea(cont) > min_a]

        x_coord = []
        y_coord = []

        for cont in conts:
            x, y, w, h = cv2.boundingRect(cont)
            y_coord.append((y + h) / 2)
            x_coord((x + w) / 2)

        return x_coord, y_coord

    def find_plants(self, image, thresh_v, min_a):

        self.set_image(image)
        self.extract_green()
        self.process_image(thresh_v)
        x_coord, y_coord, = self.extract_coordinates(min_a)

        return x_coord, y_coord
