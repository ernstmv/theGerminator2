import cv2
import Identifier


def show(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)


def main():
    ide = Identifier.Identifier()
    img = cv2.imread('../imgs/img1.jpeg')
    dim = img.shape
    img = cv2.resize(img, (int(dim[1]*0.5), int(dim[0]*0.5)), cv2.INTER_AREA)
    ide.set_image(img)
    ide.identify_plants(200, 100)
    img = ide.get_image()
    show(img)


if __name__ == '__main__':
    main()
