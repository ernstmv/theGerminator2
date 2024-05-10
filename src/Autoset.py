import cv2
from math import dist, atan, degrees
from sklearn.cluster import KMeans
import numpy as np


class Auto:

    def __init__(self):
        self.kernel = 11
        self.margin = 2
        self.change = False

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
                1)
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

        self.centers = kmeans.cluster_self.centers_
        colors = []

        for i in range(-1, 3):

            c = self.centers[i]
            slope = []

            distances = {dist(c, cent): cent for cent in self.centers}

            for distance in distances:
                if distance == 0 or distance == max(distances.keys()):
                    continue
                x = [c[0], distances[distance][0]]
                y = [c[1], distances[distance][1]]

                m, _ = np.polyfit(x, y, 1)
                slope.append(m)

            angle = degrees(atan((slope[1] - slope[0])/(1+slope[1]*slope[0])))
            color = (0, 0, 0)
            angle = abs(angle)

            if angle < 90 + self.margin and angle > 90 - self.margin:
                color = (255, 0, 255)
                colors.append(510)

            cv2.circle(
                    self.mask,
                    (int(self.centers[i][0]), int(self.centers[i][1])),
                    5,
                    color,
                    3)

            cv2.putText(
                    self.mask,
                    f'{i+1}',
                    (int(self.centers[i][0]), int(self.centers[i][1])),
                    1,
                    2,
                    (255, 127, 127))

            cv2.line(
                    self.mask,
                    (int(self.centers[i-1][0]), int(self.centers[i-1][1])),
                    (int(self.centers[i][0]), int(self.centers[i][1])),
                    (255, 0, 0),
                    2)
        return sum(colors) == 510 * 4

    def auto_run(self):
        if self.autoset():
            return True
        elif self.change is False:
            if self.kernel < 35:
                self.kernel += 2
            else:
                self.kernel = 11
            self.change = True
        else:
            if self.margin < 5:
                self.margin += 1
            else:
                self.margin = 2
                self.change = False
