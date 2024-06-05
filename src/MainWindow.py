import customtkinter as ctk
from MessageFrame import MessageFrame
from FileFrame import FileFrame
from MVideoFrame import MVideoFrame
from SVideoFrame import SVideoFrame
from ControlsFrame import ControlsFrame
from Camera import Camera


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.stop_m = False
        self.stop_s = False

        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f'{w}x{h}')
        self.title('The Germinator')

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=0)

        self.m_video_frame = MVideoFrame(self, w, h)
        self.s_video_frame = SVideoFrame(self, w, h)
        self.message_frame = MessageFrame(self, w, h)
        self.file_frame = FileFrame(self, w, h)  # TRABAJA SOLO?
        self.controls_frame = ControlsFrame(self, w, h)

        self.m_video_frame.grid(
                row=0, column=0,
                padx=10, pady=10,
                columnspan=2,
                sticky='nsew')
        self.s_video_frame.grid(
                row=1, column=0,
                padx=10, pady=10,
                sticky='nsew')
        self.message_frame.grid(
                row=1, column=1,
                padx=10, pady=10,
                sticky='nsew')
        self.file_frame.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')
        self.controls_frame.grid(
                row=1, column=2,
                padx=10, pady=10,
                sticky='nsew')

    def m_connect_camera(self, ip):
        camera = Camera(ip)
        while not self.stop_m:
            img = camera.get_image()
            self.m_video_frame.set_image(img)
            self.update()
        self.stop_m = False

    def set_message(self, message):
        self.message_frame.set_message(message)

    def autoset(self, ip):
        pass

    def m_disconnect(self):
        self.stop_m = True

    def s_connect_camera(self, ip):
        camera = Camera(ip)
        while not self.stop_s:
            img = camera.get_image()
            self.s_video_frame.set_image(img)
            self.update()
        self.stop_s = False

    def s_disconnect(self):
        self.stop_s = True
