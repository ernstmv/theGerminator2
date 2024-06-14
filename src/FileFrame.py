from customtkinter import (
        CTkFrame,
        CTkLabel,
        CTkTextbox,
        CTkButton,
        CTkImage)
from cv2 import cvtColor, COLOR_BGR2RGB, imread, resize, INTER_AREA
from PIL import Image


class FileFrame(CTkFrame):
    def __init__(self, master, w, h):
        super().__init__(master, width=int(3*w/10), height=int(h/3))

        self.columnconfigure((0), weight=1)
        self.rowconfigure((0, 1), weight=0)

        self.frame_title = CTkLabel(self, text='Visualizer')
        self.frame_title.grid(
                row=0, column=0,
                columnspan=2, sticky='ew',
                padx=10, pady=10)

        self.image_label = CTkLabel(self, height=int(h/4))
        self.image_label.grid(
                row=1, column=0,
                padx=10, pady=10,
                columnspan=2)

        self.load_default_image()

    def show_image(self, image):
        image = self.convert_image(image)
        self.image_label.configure(text='', image=image)

    def convert_image(self, image):
        img = cvtColor(image, COLOR_BGR2RGB)
        img_pil = Image.fromarray(image)
        img_ctk = CTkImage(
                light_image=img_pil,
                size=(int(img.shape[1]*1), int(img.shape[0]*1)))
        return img_ctk

    def load_default_image(self):
        img = imread('/home/leviathan/theGerminator2/.theme/default.jpeg')
        h, w = img.shape[:2]
        scale = 0.5
        new_size = (int(w*scale), int(h*scale))
        img = resize(img, new_size, interpolation=INTER_AREA)
        self.show_image(img)
