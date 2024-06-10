from customtkinter import CTk
from MessageFrame import MessageFrame
from FileFrame import FileFrame
from MVideoFrame import MVideoFrame
from SVideoFrame import SVideoFrame
from ControlsFrame import ControlsFrame
from Camera import Camera
from Detector import Detector
from BandControl import BandControl


class MainWindow(CTk):

    def __init__(self):
        super().__init__()

        self.stop_m = False
        self.stop_s = False
        self.stop_all = False

        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f'{w}x{h}')
        self.title('The Germinator')

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0), weight=1)
        self.grid_rowconfigure((1), weight=0)

        self.file_frame = FileFrame(self, w, h)  # TRABAJA SOLO?
        self.m_video_frame = MVideoFrame(self, w, h)
        self.s_video_frame = SVideoFrame(self, w, h)
        self.message_frame = MessageFrame(self, w, h)
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
        del camera
        self.stop_m = False

    def set_message(self, message):
        self.message_frame.set_message(message)

    def autoset(self, m_ip, s_ip):
        m_cam = Camera(m_ip)
        s_cam = Camera(s_ip)
        detector = Detector(self)
        self.band = BandControl()
        self.band.run()

        while not self.stop_all:

            m_img, s_img = m_cam.get_image(), s_cam.get_image()
            detector.set_images(m_img, s_img)
            detector.detect()
            m_img, s_img = detector.get_images()

            self.m_video_frame.set_image(m_img)
            self.s_video_frame.set_image(s_img)

            self.update()

        self.band.stop()
        del m_cam, s_cam, detector, self.band
        self.set_message("All resources released")
        self.stop_all = False

    def stop_auto(self):
        self.stop_all = True

    def m_disconnect(self):
        self.stop_m = True
        self.set_message("Main camera disconnected")

    def s_connect_camera(self, ip):
        camera = Camera(ip)
        while not self.stop_s:
            img = camera.get_image()
            self.s_video_frame.set_image(img)
            self.update()
        del camera
        self.stop_s = False

    def s_disconnect(self):
        self.stop_s = True
        self.set_message('Aux camera disconnected')
