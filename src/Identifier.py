import cv2
import numpy as np


class Identifier:

    def __init__(self):
        pass

    def set_image(self, img):
        self.img = img

    def get_image(self):
        return self.img

    def get_plants_coordinates(self):
        return self.plants_centers

    def identify_lines(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 220, 250, apertureSize=3)

        lines = cv2.HoughLinesP(
                edges,
                1,
                np.pi/180,
                100,
                minLineLength=100,
                maxLineGap=10)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(
                    self.img,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA)

    def identify_plants(self, thresh_value, min_area):

        green_layer = self.img[:, :, 1]
        _, g_thresh = cv2.threshold(
                green_layer,
                thresh_value,
                255,
                cv2.THRESH_BINARY)
        plants, _ = cv2.findContours(
                g_thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)
        plants = [x for x in plants if cv2.contourArea(x) > min_area]

        mask = np.zeros_like(self.img)
        cv2.drawContours(
                mask,
                plants,
                -1,
                (22, 224, 36),
                -1)

        self.img = cv2.addWeighted(self.img, 0.6, mask, 0.8, 0)

        self.plants_centers = []

        for plant in plants:
            center, _ = cv2.minEnclosingCircle(plant)
            self.plants_centers.append(tuple(map(int, center)))
