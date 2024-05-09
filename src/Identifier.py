import cv2
import numpy as np


class Identifier:

    def __init__(self):
        pass

    def identify(self, tray_t, plants_t, plants_min_a):
        self.identify_tray(tray_t)
        self.identify_plants(plants_t, plants_min_a)
        self.write_data()
        self.add_mask()

    def set_image(self, img):
        self.img = img
        self.mask = np.zeros_like(self.img)

    def get_image(self):
        return self.img

    def write_data(self):
        total_plants = len(self.plants) if self.plants is not None else 0
        cv2.putText(
                self.mask,
                f'Plants: {total_plants}',
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                1)

        cv2.putText(
                self.mask,
                'Tray size: PENDING',
                (100, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1)

    def identify_tray(self, thresh_v):

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, thresh_v, 255, cv2.THRESH_BINARY_INV)
        conts, _ = cv2.findContours(
                thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)

        conts = {cv2.contourArea(cont): cont for cont in conts}

        self.tray = conts[max(conts.keys())]

        cv2.drawContours(
                self.mask,
                self.tray,
                -1,
                (0, 0, 255),
                2)

    def identify_plants(self, thresh_value, min_area):

        if self.tray is None:
            return None

        x, y, w, h = cv2.boundingRect(self.tray)
        d_matrix = np.array([[1, 0, x],
                            [0, 1, y]], dtype=np.float32)
        img = self.img[y:y+h, x:x+w]

        _, green, _ = cv2.split(img)
        green_layer = cv2.medianBlur(green, 5)

        _, g_thresh = cv2.threshold(
                green_layer,
                thresh_value,
                255,
                cv2.THRESH_BINARY)

        plants, _ = cv2.findContours(
                g_thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)

        self.plants = [x for x in plants if cv2.contourArea(x) > min_area]

        if self.plants is None:
            return None

        self.plants = [cv2.transform(p, d_matrix) for p in self.plants]

        cv2.drawContours(
                self.mask,
                self.plants,
                -1,
                (0, 255, 0),
                -1)

    def add_mask(self):
        self.img = cv2.addWeighted(self.img, 0.6, self.mask, 0.8, 0)
