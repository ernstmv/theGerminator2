from TraysManager import TraysManager
from customtkinter import CTkImage
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from math import dist
import numpy as np


def g_radius(cont):
    ((x, y), radius) = cv2.minEnclosingCircle(cont)
    return radius


class Detector:

    def __init__(self, master):
        self.tray_id = None
        self.tray_greenhouse = None
        self.tray_crop = None
        self.tray_size = None
        self.tray_plants = []
        self.plants_coordinates = []
        self.plants_areas = []
        self.plants_colors = []
        self.tray_n_plants = None
        self.tray_germination = None
        self.master = master

        self.QRdetector = cv2.QRCodeDetector()

    def set_images(self, m_img, s_img):
        self.m_img = m_img
        self.s_img = s_img
        self.m_mask = np.zeros_like(m_img)
        self.s_mask = np.zeros_like(s_img)

    def get_images(self):
        m_img = cv2.addWeighted(self.m_img, 0.6, self.m_mask, 0.8, 0)
        s_img = cv2.addWeighted(self.s_img, 0.6, self.s_mask, 0.8, 0)
        return m_img, s_img

    def detect(self):
        if self.tray_id is None:
            self.detectQR()
            self.old_hist = self.get_frame_hist()
            return None
        self.detect_plants()
        if len(self.tray_plants) != 0:
            self.new_hist = self.get_frame_hist()
            r = cv2.compareHist(
                    self.old_hist,
                    self.new_hist,
                    cv2.HISTCMP_CORREL)

            if r > 0.9:

                self.put_message(f'Crop = {self.tray_crop}')
                self.put_message(f'Greenhouse = {self.tray_greenhouse}')
                self.put_message(f'Total plants = {self.tray_n_plants}')
                self.put_message(f'Tray size = {self.tray_size}')
                self.put_message(f'Germination = {self.tray_germination}')

                self.add_tray()
                self.show_graphics()

                self.tray_id = None
                self.tray_crop = None
                self.tray_size = None
                self.tray_plants = []
                self.plants_areas = []
                self.plants_coordintes = []
                self.plants_colors = []
                self.tray_n_plants = None
                self.tray_greenhouse = None
                self.tray_germination = None

    def show_graphics(self):
        fig, ax = plt.subplots()
        ax.plot(self.plants_areas)
        ax.set_xlabel('Plants')
        ax.set_ylabel('Areas')
        ax.set_title('Areas plot')

        fig.canvas.draw()

        imagen_np = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        imagen_np = imagen_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        plt.close(fig)

        imagen_bgr = cv2.cvtColor(imagen_np, cv2.COLOR_RGB2BGR)

        self.master.file_frame.show_image(imagen_bgr)

    def detectQR(self):

        data = None
        points = None

        x = 400
        cv2.line(self.s_mask, (x, 0), (x, 1300), (0, 255, 0), 2)
        gray_image = cv2.cvtColor(self.s_img, cv2.COLOR_BGR2GRAY)
        data, points, _ = self.QRdetector.detectAndDecode(gray_image)

        if points is not None:

            dists = []
            points = points[0].astype(int)
            for i in range(len(points)):
                p1 = tuple(points[i])
                p2 = tuple(points[(i+1) % len(points)])
                cv2.line(
                        self.s_mask,
                        p1, p2,
                        (0, 255, 0), 4)
                dists.append(dist(p1, p2))

            lado = dists[0]
            for d in dists:
                if d <= lado*0.9 or d >= lado*1.1:
                    return None

            max_x = max([points[i][0] for i in range(len(points))])

            if x >= max_x:
                return None
            elif max_x >= x:
                self.master.band.stop()
            values = [
                    data.split()[i].split(':')[1]
                    for i in range(len(data.split()))]
            try:
                self.tray_id = values[0]
                self.tray_greenhouse = values[1]
                self.tray_crop = values[2]
                self.tray_size = int(values[3])
                self.put_message(f'Tray identified with ID: {self.tray_id}')
                self.master.band.run()
            except Exception:
                return None

    def detect_plants(self):

        #  "SCANNER" LINE DEFINITION
        cv2.line(self.m_mask, (200, 0), (200, 1000), (255, 0, 255), 1)

        # DEFINITION OF GREEN MASK
        hsv = cv2.cvtColor(self.m_img, cv2.COLOR_RGB2HSV)
        hsv[:, :, 2] = hsv[:, :, 2] * 1.2
        green_l = np.array([25, 40, 72])
        green_h = np.array([102, 255, 255])
        plants_mask = cv2.inRange(hsv, green_l, green_h)

        # FIND PLANTS
        conts, _ = cv2.findContours(
                plants_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE)

        plants = [cont for cont in conts if cv2.contourArea(cont) > 300]

        for plant in plants:
            x, y, w, h = cv2.boundingRect(plant)
            if (x+w) >= 200 and (x+w) < 230:
                cv2.rectangle(
                        self.m_mask,
                        (x, y),
                        (x+w, y+h),
                        (0, 255, 0),
                        2)
                self.tray_plants.append(plant)
                plant_center, _ = cv2.minEnclosingCircle(plant)
                self.plants_coordinates.append(plant_center)
                self.plants_areas.append(cv2.contourArea(plant))
                cont_mask = np.zeros_like(self.m_img[:, :, 0])
                cv2.drawContours(cont_mask, [plant], -1, 255, -1)
                self.plants_colors.append(cv2.mean(self.m_img, mask=cont_mask))
        self.tray_n_plants = len(self.tray_plants)
        self.tray_germination = self.tray_n_plants / self.tray_size * 100

    def put_message(self, mssg):
        self.master.set_message(mssg)

    def add_tray(self):
        manager = TraysManager()
        content = [
                self.tray_id,
                self.tray_crop,
                self.tray_greenhouse,
                self.tray_size,
                self.tray_n_plants,
                self.tray_germination]
        manager.add_tray(content)
        manager.add_coordinates(self.tray_id, self.plants_coordinates)
        manager.add_areas(self.tray_id, self.plants_areas)
        del manager

    def get_frame_hist(self):
        gray = cv2.cvtColor(self.m_img, cv2.COLOR_BGR2RGB)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist)
        return hist
