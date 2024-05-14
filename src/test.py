import cv2
import numpy as np

# Leer la imagen
imagen = cv2.imread('img.jpeg')

matrix = np.ones(imagen.shape) * 3

img_rgb_higher = np.uint8(np.clip(cv2.multiply(np.float64(imagen),matrix),0,255))
cv2.imshow('img', imagen)
cv2.waitKey(0)
cv2.imshow('img', img_rgb_higher)
cv2.waitKey(0)
