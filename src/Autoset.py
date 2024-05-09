import cv2
from sklearn.cluster import KMeans
import numpy as np


class Auto:

    def __init__(self):
        self.kernel = 11
        pass

    def set_image(self, img):
        self.img = img
        self.mask = np.zeros_like(img)

    def get_image(self):
        self.img = cv2.addWeighted(self.img, 0.6, self.mask, 0.8, 0)
        return self.img

    def autoset(self):

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY_INV,
                self.kernel,
                2)

        conts, _ = cv2.findContours(
                thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)

        conts = {cv2.contourArea(cont): cont for cont in conts}
        try:
            self.tray = conts[max(conts.keys())]
        except Exception:
            return None

        mask = np.zeros_like(self.img)
        cv2.drawContours(
                self.mask,
                self.tray,
                -1,
                (0, 0, 255),
                10)
        cv2.drawContours(
                mask,
                self.tray,
                -1,
                (0, 0, 255),
                10)

        _, _, b = cv2.split(mask)
        edges = cv2.Canny(b, 50, 150)
        lines = cv2.HoughLinesP(
                edges,
                1,
                np.pi/180,
                100,
                minLineLength=300,
                maxLineGap=200)

        if lines is None:
            return None

        pos = []
        for line in lines:
            x, y, x1, y1 = line[0]
            pos.append([x, y])
            pos.append([x1, y1])
            cv2.circle(
                    self.mask,
                    (x, y),
                    5,
                    (0, 255, 0),
                    3)

            cv2.circle(
                    self.mask,
                    (x1, y1),
                    5,
                    (0, 255, 0),
                    3)

        if len(pos) < 4 or pos is None:
            return None

        kmeans = KMeans(n_clusters=4)
        kmeans.fit(np.array(pos))

        centers = kmeans.cluster_centers_
        dif = 40

        RED = []
        BLUE = []

        for i in range(-1, 3):

            p2 = centers[i-2]
            p1 = centers[i-1]
            c = centers[i]
            n = centers[i+1]

            xok = []
            if abs(c[0] - p2[0]) < dif:
                xok.append(True)
            if abs(c[0] - p1[0]) < dif:
                xok.append(True)
            if abs(c[0] - n[0]) < dif:
                xok.append(True)

            yok = []
            if abs(c[1] - p2[1]) < dif:
                yok.append(True)
            if abs(c[1] - p1[1]) < dif:
                yok.append(True)
            if abs(c[1] - n[1]) < dif:
                yok.append(True)

            red = 255 if sum(1 for x in xok if x) == 1 else 0
            blue = 255 if sum(1 for y in yok if y) == 1 else 0

            color = (red, 0, blue)

            cv2.circle(
                    self.mask,
                    (int(centers[i][0]), int(centers[i][1])),
                    5,
                    color,
                    3)

            cv2.putText(
                    self.mask,
                    f'{i+1}',
                    (int(centers[i][0]), int(centers[i][1])),
                    1,
                    5,
                    (255, 127, 127))

            cv2.line(
                    self.mask,
                    (int(centers[i-1][0]), int(centers[i-1][1])),
                    (int(centers[i][0]), int(centers[i][1])),
                    (255, 0, 0),
                    2)
            RED.append(red)
            BLUE.append(blue)
        return all(RED) and all(BLUE)

    def auto_run(self):
        if self.autoset():
            return True
        else:
            if self.kernel < 25:
                self.kernel += 2
            else:
                self.kernel = 11
