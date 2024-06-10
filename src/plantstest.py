from requests import get
from numpy import array, uint8
from imutils import resize
from Detector import Detector
import cv2


def main():
    ip = '192.168.0.127'
    url = 'http://' + ip + ':8080/shot.jpg'
    win_name = 'CAMARA'
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    auto = Detector()

    while True:
        img_resp = get(url)
        img_arr = array(bytearray(img_resp.content), dtype=uint8)
        img = cv2.imdecode(img_arr, -1)
        img = resize(img, width=700, height=1300)
        auto.set_images(img, img)
        try:
            auto.detect_plants()
        except Exception as e:
            print(e)
        _, img = auto.get_images()
        cv2.imshow(win_name, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow(win_name)


if __name__ == '__main__':
    main()
