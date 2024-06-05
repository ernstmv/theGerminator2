from customtkinter import (
        CTkButton,
        CTkScrollableFrame,
        CTkLabel
        )
from ConfigFrame import ConfigFrame
from IPsManager import IPsManager


class ControlsFrame(CTkScrollableFrame):
    def __init__(self, master, w, h):
        super().__init__(master, width=int(3*w/10), height=int(h/3))

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.master = master

        # MAIN CAMERA
        self.main_label = CTkLabel(self, text='The Germinator')
        self.main_label.grid(
                row=0, column=0,
                padx=10, pady=10,
                columnspan=2,
                sticky='ew')

        self.config_button = CTkButton(
                self,
                text='',
                command=self.launch_config_window)
        self.config_button.grid(row=0, column=2, padx=10, pady=10)

        self.m_camera_label = CTkLabel(self, text='Main camera')
        self.m_camera_label.grid(
                row=1, column=0,
                sticky='ew',
                padx=10, pady=10)

        self.m_connect_button = CTkButton(
                self,
                text='Connect',
                fg_color="#0CABA8",
                text_color="#025940",
                command=self.m_connect_camera)
        self.m_disconnect_button = CTkButton(
                self,
                text='Disconnect',
                command=self.m_disconnect)

        self.m_connect_button.grid(row=1, column=1, padx=10, pady=10)
        self.m_disconnect_button.grid(row=1, column=2, padx=10, pady=10)

        self.s_camera_label = CTkLabel(self, text='Secondary camera')
        self.s_camera_label.grid(
                row=2, column=0,
                padx=10, pady=10,
                sticky='ew')

        self.s_connect_button = CTkButton(
                self,
                text='Connect',
                text_color="#025940",
                command=self.s_connect_camera)
        self.s_disconnect_button = CTkButton(
                self,
                text='Disconnect',
                command=self.s_disconnect)

        self.s_connect_button.grid(row=2, column=1, padx=10, pady=10)
        self.s_disconnect_button.grid(row=2, column=2, padx=10, pady=10)

        self.others_label = CTkLabel(self, text='Band')
        self.others_label.grid(
                row=4, column=0,
                sticky='ew',
                padx=10, pady=10)

        self.run_band_button = CTkButton(
                self,
                text='Run',
                fg_color="#bf1515",
                text_color="#590404",
                hover_color="#8D5A56",
                command=self.run_band)
        self.stop_band = CTkButton(
                self,
                text='Stop',
                fg_color="#bf1515",
                text_color="#590404",
                hover_color="#8D5A56",
                command=self.stop_band)

        self.run_band_button.grid(
                row=4, column=1,
                padx=10, pady=10)
        self.stop_band.grid(
                row=4, column=2,
                sticky='ew',
                padx=10, pady=10)

        self.work_label = CTkLabel(self, text='Work area')
        self.work_label.grid(
                row=5, column=0,
                columnspan=3,
                sticky='ew',
                padx=10, pady=10)

        self.autoset_button = CTkButton(
                self,
                text='Autoset',
                fg_color="#bf1515",
                text_color="#590404",
                hover_color="#8D5A56",
                command=self.autoset)
        self.autoset_button.grid(
                row=6, column=0,
                columnspan=2,
                sticky='ew',
                padx=10, pady=10)

        self.launch_button = CTkButton(
                self,
                text='Launch',
                fg_color="#bf1515",
                text_color="#590404",
                hover_color="#8D5A56",
                command=self.launch)
        self.launch_button.grid(
                row=6, column=2,
                padx=10, pady=10)

        self.load_ips()

    def launch_config_window(self):
        self.config_window = ConfigFrame(self)

    def run_band(self):
        pass

    def stop_band(self):
        pass

    def launch(self):
        pass

    def m_connect_camera(self):
        self.master.set_message('Connecting to camera with ip: ' + self.m_ip)
        manager = IPsManager()
        if manager.test_ip(self.m_ip):
            self.master.set_message('Connection done')
            self.master.m_connect_camera(self.m_ip)
        else:
            self.master.set_message('Connection refused')
        del manager

    def autoset(self):
        ip = self.m_read_ip()
        self.master.autoset(ip)

    def m_disconnect(self):
        self.master.m_disconnect()

    def s_connect_camera(self):
        self.master.set_message('Connecting to camera with ip: ' + self.m_ip)
        manager = IPsManager()
        if manager.test_ip(self.s_ip):
            self.master.set_message('Connection done')
            self.master.s_connect_camera(self.s_ip)
        else:
            self.master.set_message('Connection refused')
        del manager

    def s_disconnect(self):
        self.master.s_disconnect()

    def load_ips(self):
        self.master.set_message('Loading ips..')
        manager = IPsManager()
        self.m_ip = manager.get_m_ip()
        self.master.set_message('Main camera ip: ' + self.m_ip)
        self.s_ip = manager.get_s_ip()
        self.master.set_message('Second camera ip: ' + self.s_ip)
        self.master.set_message('Ips correctly loaded')
        del manager
