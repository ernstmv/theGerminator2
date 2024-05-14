import cv2
import Autoset

img = cv2.imread('img.jpeg')
h, w = img.shape[0], img.shape[1]
ratio = h / w
nw = int(w * 0.5)
nh = int(ratio * nw)
img = cv2.resize(img, (nw, nh))
cv2.imshow('img', img)
cv2.waitKey(0)
auto = Autoset.Auto()
auto.set_image(img)
auto.detect_plants()
img = auto.get_image()
img = cv2.GaussianBlur(img, (5, 5), 1)
cv2.imshow('img', img)
cv2.waitKey(0)
