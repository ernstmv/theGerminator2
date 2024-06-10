from customtkinter import CTkFrame, CTkLabel, CTkImage
from cv2 import cvtColor, COLOR_BGR2RGB, imread
from PIL import Image


class SVideoFrame(CTkFrame):
    def __init__(self, master, w, h):
        super().__init__(master, height=int(3*h/10))

        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=0)
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)

        self.frame_title = CTkLabel(self, text="SECONDARY CAMERA")
        self.frame_title.grid(
                row=0, column=0,
                padx=10, pady=10,
                sticky='ew',
                columnspan=2)

        self.image_label = CTkLabel(self, text=None)
        self.image_label.grid(column=0, row=1)

        self.load_default_image()

    def set_image(self, image):
        image = self.convert_image(image)
        self.image_label.configure(text='', image=image)

    def convert_image(self, image):
        img = cvtColor(image, COLOR_BGR2RGB)
        img_pil = Image.fromarray(image)
        img_ctk = CTkImage(
                light_image=img_pil,
                size=(int(img.shape[1]*0.5), int(img.shape[0]*0.5)))
        return img_ctk

    def load_default_image(self):
        img = imread('/home/leviathan/theGerminator2/.theme/default2.jpg')
        self.set_image(img)
