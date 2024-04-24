import cv2


class Identifier:

    def __init__(self):
        pass

    def set_image(self, img):
        self.img = img

    def get_image(self):
        return self.img

    def get_plants_coordinates(self):
        return self.plants_centers

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

        self.plants_centers = []

        for plant in plants:
            center, _ = cv2.minEnclosingCircle(plant)
            self.plants_centers.append(tuple(map(int, center)))

        cv2.drawContours(
                self.img,
                plants,
                -1,
                (0, 255, 0),
                2)
