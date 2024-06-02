from customtkinter import (
        CTkButton,
        CTkEntry,
        CTkScrollableFrame,
        CTkLabel,
        CTkOptionMenu,
        END
        )
from IPsManager import IPsManager


class ConfigFrame(CTkScrollableFrame):
    def __init__(self, master, w, h):
        super().__init__(master, width=int(3*w/10), height=int(h/3))

        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.master = master
        self.manager = IPsManager()

        self.reload_ips()

        # MAIN CAMERA
        self.m_ip_label = CTkLabel(self, text='MAIN CAMERA')
        self.m_ip_label.grid(
                row=0, column=0,
                columnspan=5,
                padx=10, pady=10)

        self.m_camera_fields = [None] * 4
        for i in range(4):
            self.m_camera_fields[i] = CTkEntry(self)
            self.m_camera_fields[i].grid(column=i, row=1, padx=5, pady=10)

        self.m_ip_menu = CTkOptionMenu(
                self,
                values=self.m_loaded_ips,
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
        self.m_test_button.grid(
                row=2, column=1,
                columnspan=3,
                padx=10, pady=10)
        self.m_delete_button.grid(row=2, column=4, padx=10, pady=10)

        self.m_connect_button = CTkButton(
                self,
                text='Connect',
                command=self.m_connect_camera)
        self.autoset_button = CTkButton(
                self,
                text='Autoset',
                command=self.autoset)
        self.m_disconnect_button = CTkButton(
                self,
                text='Disconnect',
                command=self.m_disconnect)

        self.m_connect_button.grid(column=0, row=3, padx=10, pady=10)
        self.autoset_button.grid(
                column=1, row=3,
                columnspan=3,
                padx=10, pady=10)
        self.m_disconnect_button.grid(column=4, row=3, padx=10, pady=10)

        # SECONDARY CAMERA
        self.s_ip_label = CTkLabel(self, text='SECONDARY CAMERA')
        self.s_ip_label.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

        self.s_camera_fields = [None] * 4
        for i in range(4):
            self.s_camera_fields[i] = CTkEntry(self)
            self.s_camera_fields[i].grid(column=i, row=5, padx=5, pady=10)

        self.s_ip_menu = CTkOptionMenu(
                self,
                values=self.s_loaded_ips,
                command=self.s_choose_ip)
        self.s_ip_menu.grid(column=4, row=5, padx=10, pady=10)

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
        self.s_save_button.grid(row=6, column=0, padx=10, pady=10)
        self.s_test_button.grid(
                row=6, column=1,
                columnspan=3,
                padx=10, pady=10)
        self.s_delete_button.grid(row=6, column=4, padx=10, pady=10)

        self.s_connect_button = CTkButton(
                self,
                text='Connect',
                command=self.s_connect_camera)
        self.s_disconnect_button = CTkButton(
                self,
                text='Disconnect',
                command=self.s_disconnect)

        self.s_connect_button.grid(column=0, row=7, padx=10, pady=10)
        self.s_disconnect_button.grid(column=4, row=7, padx=10, pady=10)

    def m_read_ip(self):
        ip = [str(ip_field.get()) for ip_field in self.m_camera_fields]
        return '.'.join(ip)

    def s_read_ip(self):
        ip = [str(ip_field.get()) for ip_field in self.s_camera_fields]
        return '.'.join(ip)

    def m_write_ip_fields(self, ip):
        ip_parts = ip.split('.')
        for i in range(4):
            self.m_camera_fields[i].insert(0, ip_parts[i])

    def s_write_ip_fields(self, ip):
        ip_parts = ip.split('.')
        for i in range(4):
            self.s_camera_fields[i].insert(0, ip_parts[i])

    def m_delete_ip_fields(self):
        for ip_field in self.m_camera_fields:
            ip_field.delete(0, END)

    def s_delete_ip_fields(self):
        for ip_field in self.s_camera_fields:
            ip_field.delete(0, END)

    def m_choose_ip(self, choice):
        self.m_delete_ip_fields()
        self.m_write_ip_fields(choice)

    def s_choose_ip(self, choice):
        self.s_delete_ip_fields()
        self.s_write_ip_fields(choice)

    def m_save_ip(self):
        ip = self.m_read_ip()
        self.manager.m_write_ip(ip)
        self.reload_ips()

    def m_test_ip(self):
        ip = self.m_read_ip()
        self.manager.test_ip(ip)

    def m_delete_ip(self):
        ip = self.m_read_ip()
        self.manager.m_delete_ip(ip)
        self.m_delete_ip_fields()
        self.reload_ips()

    def m_connect_camera(self):
        ip = self.m_read_ip()
        self.master.m_connect_camera(ip)

    def autoset(self):
        ip = self.m_read_ip()
        self.master.autoset(ip)

    def m_disconnect(self):
        self.master.m_dissconect()

    def s_save_ip(self):
        ip = self.s_read_ip()
        self.manager.s_write_ip(ip)
        self.reload_ips()

    def s_test_ip(self):
        ip = self.s_read_ip()
        self.manager.test_ip(ip)

    def s_delete_ip(self):
        ip = self.s_read_ip()
        self.manager.s_delete_ip(ip)
        self.s_delete_ip_fields()
        self.reload_ips()

    def s_connect_camera(self):
        ip = self.s_read_ip()
        self.master.s_connect_camera(ip)

    def s_disconnect(self):
        self.master.s_dissconect()

    def reload_ips(self):
        self.m_loaded_ips = self.manager.m_read_ip()
        self.s_loaded_ips = self.manager.s_read_ip()
        try:
            self.m_ip_menu.configure(values=self.m_loaded_ips)
            self.s_ip_menu.configure(values=self.s_loaded_ips)
        except Exception:
            pass
