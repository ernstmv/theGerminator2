from customtkinter import CTkFrame, CTkLabel, CTkTextbox, CTkButton, CTkImage
from cv2 import cvtColor, COLOR_BGR2RGB, imread
from PIL import Image


class FileFrame(CTkFrame):
    def __init__(self, master, w, h):
        super().__init__(master)

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=0)

        self.frame_title = CTkLabel(self, text='Visualizer')
        self.frame_title.grid(
                row=0, column=0,
                columnspan=2, sticky='ew',
                padx=10, pady=10)

        self.image_label = CTkLabel(self)
        self.image_label.grid(
                row=1, column=0,
                padx=10, pady=10,
                columnspan=2)

        self.data_textbox = CTkTextbox(
                self,
                height=int(h/20),
                state='disabled')
        self.data_textbox.grid(
                row=2, column=0,
                columnspan=2,
                padx=10, pady=10,
                sticky='ew')

        self.next_button = CTkButton(self, text="", command=self.next)
        self.next_button.grid(
                row=3, column=0,
                pady=10, padx=10,
                sticky='ew')

        self.prev_button = CTkButton(self, text="", command=self.prev)
        self.prev_button.grid(
                row=3, column=1,
                pady=10, padx=10,
                sticky='ew')
        self.explorer_button = CTkButton(self, text='Browse', command=self.exp)
        self.explorer_button.grid(
                row=4, column=0,
                columnspan=2,
                padx=10, pady=10,
                sticky='ew')

        self.load_default_image()

    def next(self):
        pass

    def prev(self):
        pass

    def exp(self):
        pass

    def show_image(self, image):
        image = self.convert_image(image)
        self.image_label.configure(text='', image=image)

    def convert_image(self, image):
        img = cvtColor(image, COLOR_BGR2RGB)
        img_pil = Image.fromarray(image)
        img_ctk = CTkImage(
                light_image=img_pil,
                size=(int(img.shape[1]*0.3), int(img.shape[0]*0.3)))
        return img_ctk

    def load_default_image(self):
        img = imread('/home/leviathan/theGerminator2/.imgs/default3.jpg')
        self.show_image(img)
