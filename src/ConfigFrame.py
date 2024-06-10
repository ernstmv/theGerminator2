from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from random import choice
from string import ascii_letters, digits
from IPsManager import IPsManager
from customtkinter import (
        CTkToplevel,
        CTkOptionMenu,
        CTkEntry,
        CTkTextbox,
        CTkLabel,
        END,
        CTkButton)


class ConfigFrame(CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.manager = IPsManager()
        self.crops = [
                'Clavel', 'Cempasuchil',
                'Geranio', 'Pensamiento',
                'Others']
        self.sizes = ['14', '15', '21', '32', '50', '72', '128', '200']
        self.s = None
        self.c = None

        # MAIN CAMERA
        self.main_camera_l = CTkLabel(self, text='Main Camera')
        self.main_camera_l.grid(
                row=0, column=0,
                padx=10, pady=10,
                columnspan=5,
                sticky='ew')

        self.m_camera_fields = [None] * 4
        for i in range(4):
            self.m_camera_fields[i] = CTkEntry(self)
            self.m_camera_fields[i].grid(column=i, row=1, padx=5, pady=10)

        self.m_ip_menu = CTkOptionMenu(
                self,
                values=None,
                command=self.m_choose_ip)
        self.m_ip_menu.grid(column=4, row=1, padx=10, pady=10)

        self.m_save_button = CTkButton(
                self,
                text='Save IP',
                command=self.m_save_ip)
        self.m_test_button = CTkButton(
                self,
                text='Test IP',
                command=self.m_test_ip)
        self.m_delete_button = CTkButton(
                self,
                text='Delete IP',
                command=self.m_delete_ip)

        self.m_save_button.grid(row=2, column=0, padx=10, pady=10)
        self.m_test_button.grid(row=2, column=1, padx=10, pady=10)
        self.m_delete_button.grid(row=2, column=2, padx=10, pady=10)

        # SECONDARY CAMERA
        self.sec_camera_l = CTkLabel(self, text='Secondary Camera')
        self.sec_camera_l.grid(
                row=3, column=0,
                padx=10, pady=10,
                columnspan=5,
                sticky='ew')

        self.s_camera_fields = [None] * 4
        for i in range(4):
            self.s_camera_fields[i] = CTkEntry(self)
            self.s_camera_fields[i].grid(column=i, row=4, padx=5, pady=10)

        self.s_ip_menu = CTkOptionMenu(
                self,
                values=None,
                command=self.s_choose_ip)
        self.s_ip_menu.grid(column=4, row=4, padx=10, pady=10)

        self.s_save_button = CTkButton(
                self,
                text='Save IP',
                command=self.s_save_ip)
        self.s_test_button = CTkButton(
                self,
                text='Test IP',
                command=self.s_test_ip)
        self.s_delete_button = CTkButton(
                self,
                text='Delete IP',
                command=self.s_delete_ip)

        self.s_test_button.grid(row=5, column=1, padx=10, pady=10)
        self.s_save_button.grid(row=5, column=0, padx=10, pady=10)
        self.s_delete_button.grid(row=5, column=2, padx=10, pady=10)

        # APPLY CHANGES
        self.apply_button = CTkButton(
                self,
                text='Apply changes',
                command=self.apply)
        self.apply_button.grid(
                row=6, column=0,
                columnspan=5,
                padx=10, pady=10,
                sticky='ew')

        # QRs zone
        self.qr_zone_label = CTkLabel(self, text='QRs')
        self.qr_zone_label.grid(
                row=7, column=0,
                columnspan=5,
                pady=10,
                sticky='ew')

        self.green_label = CTkLabel(self, text="Greenhouse: ")
        self.green_label.grid(row=8, column=0, padx=10, pady=10)

        self.green_entry = CTkEntry(self)
        self.green_entry.grid(row=8, column=1, padx=10, pady=10)

        self.crop_label = CTkLabel(self, text="Crop in the tray: ")
        self.crop_label.grid(row=8, column=2, padx=10, pady=10)

        self.crop_menu = CTkOptionMenu(
                self,
                values=self.crops,
                command=self.choose_crop)
        self.crop_menu.grid(row=8, column=3, padx=10, pady=10)

        self.size_label = CTkLabel(self, text="Size of the tray:")
        self.size_label.grid(row=9, column=0, padx=10, pady=10)

        self.size_menu = CTkOptionMenu(
                self,
                values=self.sizes,
                command=self.choose_size)
        self.size_menu.grid(row=9, column=1, padx=10, pady=10)

        self.generate_qr_button = CTkButton(
                self,
                text='Generate QR',
                command=self.generate_qr)
        self.generate_qr_button.grid(row=8, column=4, padx=10, pady=10)

        self.message_textbox = CTkTextbox(self, state='disabled')
        self.message_textbox.grid(
                row=10, column=0,
                columnspan=5,
                padx=10, pady=10,
                sticky='nsew')

        self.load_ips()

    # MAIN CAMERA METHODS
    def m_read_ip(self):
        ip = [str(ip_field.get()) for ip_field in self.m_camera_fields]
        return '.'.join(ip)

    def m_write_ip_fields(self, ip):
        for ip_field in self.m_camera_fields:
            ip_field.delete(0, END)
        ip_parts = ip.split('.')
        for i in range(4):
            self.m_camera_fields[i].insert(0, ip_parts[i])

    def m_choose_ip(self, choice):
        self.m_write_ip_fields(choice)
        self.manager.m_insert_ip(choice)

    def m_save_ip(self):
        ip = self.m_read_ip()
        self.manager.m_insert_ip(ip)
        self.load_ips()

    def m_test_ip(self):
        ip = self.m_read_ip()
        if self.manager.test_ip(ip):
            self.set_message('Main camera is online')
        else:
            self.set_message('Main camera is offline')

    def m_delete_ip(self):
        ip = self.m_read_ip()
        self.manager.m_delete_ip(ip)
        self.load_ips()

    # SECONDARY CAMERA METHODS
    def s_read_ip(self):
        ip = [str(ip_field.get()) for ip_field in self.s_camera_fields]
        return '.'.join(ip)

    def s_write_ip_fields(self, ip):
        for ip_field in self.s_camera_fields:
            ip_field.delete(0, END)
        ip_parts = ip.split('.')
        for i in range(4):
            self.s_camera_fields[i].insert(0, ip_parts[i])

    def s_choose_ip(self, choice):
        self.s_write_ip_fields(choice)
        self.manager.s_insert_ip(choice)

    def s_save_ip(self):
        ip = self.s_read_ip()
        self.manager.s_insert_ip(ip)
        self.load_ips()

    def s_test_ip(self):
        ip = self.s_read_ip()
        if self.manager.test_ip(ip):
            self.set_message('Secondary camera is online')
        else:
            self.set_message('Secondary camera is offline')

    def s_delete_ip(self):
        ip = self.s_read_ip()
        self.manager.s_delete_ip(ip)
        self.load_ips()

    def choose_crop(self, choice):
        self.c = choice

    def choose_size(self, choice):
        self.s = choice

    # OTHER METHODS

    def load_ips(self):

        self.m_loaded_ips = self.manager.m_read_ip()
        self.s_loaded_ips = self.manager.s_read_ip()

        self.m_ip_menu.configure(values=self.m_loaded_ips)
        self.s_ip_menu.configure(values=self.s_loaded_ips)

        self.m_write_ip_fields(self.m_loaded_ips[0])
        self.s_write_ip_fields(self.s_loaded_ips[0])

    def generate_qr(self):
        gren = str(self.green_entry.get())
        if self.c is None or gren == '' or self.s is None:
            self.set_message("Error in data input, check crop and greenhouse")
            return None

        chars = ascii_letters + digits
        while True:
            ID = ''.join(choice(chars) for _ in range(16)).lower()
            if self.manager.is_available_ID(ID):
                break

        c = f'Identifier:{ID}\tGreenhouse:{gren}\tCrop:{self.c}\tSize:{self.s}'

        qr = QRCode(version=3, box_size=10, error_correction=ERROR_CORRECT_L)
        qr.add_data(c)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f'/home/leviathan/theGerminator2/QRCodes/{ID}.png')
        self.set_message(f'Qr code generated with name {ID}.png')

    def set_message(self, mssg):
        self.message_textbox.configure(state='normal')
        self.message_textbox.insert('0.0', '  : ' + mssg + '\n')
        self.message_textbox.configure(state='disabled')

    def apply(self):
        self.master.m_ip = self.m_read_ip()
        self.master.s_ip = self.s_read_ip()
        self.set_message('Ips updated')
