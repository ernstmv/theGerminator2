import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('../imgs/green.jpg')

# Convertir la imagen de BGR a HSV
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Definir el rango de colores verde en HSV
verde_bajo = np.array([40, 40, 40])  # Umbral mínimo para verde
verde_alto = np.array([80, 255, 255])  # Umbral máximo para verde

# Crear una máscara utilizando el rango de colores verde
mascara = cv2.inRange(imagen_hsv, verde_bajo, verde_alto)

# Aplicar la máscara a la imagen original
imagen_con_mascara = cv2.bitwise_and(imagen, imagen, mask=mascara)

# Mostrar la imagen original, la máscara y la imagen con la máscara aplicada
cv2.imshow('Imagen con Mascara', imagen_con_mascara)
cv2.waitKey(0)
cv2.destroyAllWindows()

