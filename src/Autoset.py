import cv2
from math import dist, atan, degrees
from sklearn.cluster import KMeans
import numpy as np


def g_radius(cont):
    ((x, y), radius) = cv2.minEnclosingCircle(cont)
    return radius


class Auto:

    def __init__(self):
        self.kernel = 11
        self.r = 0
        self.c = 2
        self.change = False
        self.p_coordinates = []

    def set_image(self, img):
        self.img = img
        self.mask = np.zeros_like(img)

    def get_image(self):
        self.img = cv2.addWeighted(self.img, 0.6, self.mask, 0.8, 0)
        return self.img

    def autoset_tray(self):

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (31, 31), 0)

        thresh = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY_INV,
                self.kernel,
                self.c)

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
                20)

        _, _, b = cv2.split(mask)
        edges = cv2.Canny(b, 50, 150)
        lines = cv2.HoughLinesP(
                edges,
                1,
                np.pi/180,
                100,
                minLineLength=500,
                maxLineGap=300)

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
                    (0, 255, 255),
                    3)

            cv2.circle(
                    self.mask,
                    (x1, y1),
                    5,
                    (0, 255, 255),
                    3)

        if len(pos) < 4 or pos is None:
            return None

        kmeans = KMeans(n_clusters=4)
        kmeans.fit(np.array(pos))

        self.centers = kmeans.cluster_centers_
        colors = []

        for i in range(-1, 3):

            c = self.centers[i]
            slope = []

            dists = {dist(c, cent): cent for cent in self.centers}

            for distance in dists:
                if distance == 0 or distance == max(dists.keys()):
                    continue
                x = [c[0], dists[distance][0]]
                y = [c[1], dists[distance][1]]

                m, _ = np.polyfit(x, y, 1)
                slope.append(m)

                cv2.line(
                        self.mask,
                        (int(c[0]), int(c[1])),
                        (int(dists[distance][0]), int(dists[distance][1])),
                        (255, 0, 0),
                        2)
            if len(slope) < 2:
                return None

            angle = degrees(atan((slope[1] - slope[0])/(1+slope[1]*slope[0])))
            color = (0, 0, 0)
            angle = abs(angle)

            if angle < 95 and angle > 85:
                color = (255, 0, 255)
                colors.append(510)

            cv2.circle(
                    self.mask,
                    (int(self.centers[i][0]), int(self.centers[i][1])),
                    5,
                    color,
                    3)

        return sum(colors) == 510 * 4

    def detect_tray(self):
        if self.autoset_tray():
            return True
        elif self.change is False:
            if self.kernel < 51:
                self.kernel += 2
            else:
                self.kernel = 3
            self.change = True
        else:
            if self.c < 5:
                self.c += 0.1
            else:
                self.c = 2
                self.change = False

    def autoset_plants(self):
        conts, _ = cv2.findContours(
                self.plants_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)

        rads = [g_radius(c) for c in conts if g_radius(c) > 0.1]
        median = (max(rads) + min(rads)) / 2

        self.p = [p for p in conts if g_radius(p) > median * 0.4]

        plants = []
        for p in self.p:
            ((x, y), _) = cv2.minEnclosingCircle(p)
            center = (int(x), int(y))
            if cv2.pointPolygonTest(self.tray, center, False) > 0:
                plants.append(p)
                self.p_coordinates.append(center)
        self.p = plants
        print(self.p_coordinates)

    def set_plants_mask(self):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_RGB2HSV)
        hsv[:, :, 2] = hsv[:, :, 2] * 1.2

        green_l = np.array([25, 40, 72])
        green_h = np.array([102, 255, 255])

        self.plants_mask = cv2.inRange(hsv, green_l, green_h)

        img, _, _ = cv2.split(self.mask)
        conts, _ = cv2.findContours(
                img,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)
        conts = {cv2.contourArea(cont): cont for cont in conts}
        try:
            self.tray = conts[max(conts.keys())]
        except Exception:
            return None
        cv2.drawContours(
                self.mask,
                self.tray,
                -1,
                (255, 0, 255),
                1)

    def draw_plants(self):
        for center in self.p_coordinates:
            cv2.circle(self.mask, center, 1, (0, 255, 0), 2)

    def detect_plants(self):
        self.set_plants_mask()
        self.autoset_plants()
        self.draw_plants()
        return 'Done'

    def process_data(self):
        return len(self.p_coordinates), 200, len(self.p)/200

    def get_plants_coordinates(self):
        return self.p_coordinates
