import customtkinter as ctk
import Camera


BLUE = '#04BFAD'
DARK_BLUE = '#014040'

RED = '#D90404'
DARK_RED = '#400101'

GREEN = '#558C03'
DARK_GREEN = '#014017'


class UpperFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.main_label = ctk.CTkLabel(
                self,
                text='The Germinator',
                font=('ProFont Nerd Font', 30),
                fg_color='transparent')
        self.main_label.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.main_label2 = ctk.CTkLabel(
                self,
                text='by AGROMACH',
                fg_color='transparent')
        self.main_label2.grid(row=1, column=0, padx=10, pady=10, sticky='ew')


class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.reload_ips()
        self.ip = None
        self.ip_fields = [None] * 4

        self.save_ip_button = ctk.CTkButton(
                self,
                border_width=2,
                fg_color='transparent',
                hover_color=DARK_BLUE,
                border_color=BLUE,
                text_color=BLUE,
                text='SAVE IP',
                command=self.save_ip)

        self.connect_button = ctk.CTkButton(
                self,
                border_width=2,
                fg_color='transparent',
                hover_color=DARK_RED,
                border_color=RED,
                text_color=RED,
                text='RUN',
                command=self.connect_camera)

        self.capture_button = ctk.CTkButton(
                self,
                border_width=2,
                fg_color='transparent',
                hover_color=DARK_RED,
                border_color=RED,
                text_color=RED,
                text='CAPTURE',
                command=self.capture_image)

        self.test_connection_button = ctk.CTkButton(
                self,
                border_width=2,
                fg_color='transparent',
                hover_color=DARK_GREEN,
                border_color=GREEN,
                text_color=GREEN,
                text='TEST',
                command=self.test_connection)

        self.save_ip_button.grid(column=0, row=0, padx=10, pady=10)
        self.test_connection_button.grid(column=0, row=1, padx=10, pady=10)
        self.capture_button.grid(column=0, row=2, padx=10, pady=10)
        self.connect_button.grid(column=0, row=3, padx=10, pady=10)

        self.ip_label = ctk.CTkLabel(
                self,
                text='IP DIRECTION',
                fg_color='transparent',
                text_color=BLUE)

        self.ip_label.grid(
                column=1,
                row=0,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=5)

        for i in range(len(self.ip_fields)):
            self.ip_fields[i] = ctk.CTkEntry(
                    self,
                    fg_color='transparent',
                    text_color=BLUE)

            self.ip_fields[i].grid(
                    column=i+1,
                    row=1,
                    padx=10,
                    pady=10,
                    sticky='ew')

        self.ip_menu = ctk.CTkOptionMenu(
                self,
                button_color=BLUE,
                button_hover_color=DARK_BLUE,
                text_color=BLUE,
                command=self.load_ip,
                values=self.registered_ips
                )

        self.ip_menu.grid(column=5, row=1, padx=10, pady=10, sticky='ew')

        self.thresh_label = ctk.CTkLabel(
                self,
                text='Theshold value',
                fg_color='transparent',
                text_color=GREEN,
                anchor='center')

        self.area_label = ctk.CTkLabel(
                self,
                text='Minium area',
                fg_color='transparent',
                text_color=GREEN,
                anchor='center')

        self.thresh_slider = ctk.CTkSlider(
                self,
                command=self.set_thresh_value,
                from_=0,
                to=255,
                fg_color=DARK_GREEN,
                progress_color=GREEN)

        self.area_slider = ctk.CTkSlider(
                self,
                command=self.set_area_value,
                from_=0,
                to=1000,
                fg_color=DARK_GREEN,
                progress_color=GREEN)

        self.thresh_label.grid(
                column=1,
                row=2,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=2)

        self.area_label.grid(
                column=4,
                row=2,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=2)

        self.thresh_slider.grid(
                column=1,
                row=3,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=2)

        self.area_slider.grid(
                column=4,
                row=3,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=2)

    # SETTERs

    def set_thresh_value(self, value):
        self.thresh = value

    def set_area_value(self, value):
        self.min_area = value

    def set_ip(self):
        self.ip = self.read_ip_fields()

    # WIDGETs ACTIONS

    def save_ip(self):
        ip = self.read_ip_fields()
        with open('../data/ips.txt', 'a') as file:
            file.write(ip+'\n')
        self.reload_ips()

    def connect_camera(self):
        pass

    def capture_image(self):
        pass

    def test_connection(self):
        self.set_ip()
        try:
            self.master.connect_camera(self.ip)
            self.master.test_connection()
            self.master.disconnect_camera()
        except Exception:
            self.master.test_connection(False)

    def load_ip(self, choice):
        self.set_ip()
        self.update_ip_fields(choice)

    # AUXILIAR METHODS

    def update_ip_fields(self, choice):
        ip_parts = []
        ip = ''
        for char in choice:
            if char == '.':
                ip_parts.append(ip)
                ip = ''
                continue
            ip += char
        ip_parts.append(ip)
        self.delete_ip_fields()
        self.write_ip_fields(ip_parts)

    def write_ip_fields(self, ip_parts):
        for i in range(4):
            self.ip_fields[i].insert(0, ip_parts[i])

    def delete_ip_fields(self):
        for ip_field in self.ip_fields:
            ip_field.delete(0, ctk.END)

    def read_ip_fields(self):
        ip = [str(ip_field.get()) for ip_field in self.ip_fields]
        return '.'.join(ip)

    def reload_ips(self):
        with open('../data/ips.txt', 'r') as file:
            ips = file.readlines()
        self.registered_ips = [ip.strip() for ip in ips]
        try:
            self.ip_menu.configure(values=self.registered_ips)
        except Exception:
            pass


class ImageFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width=2, border_color=GREEN)

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.image_label = ctk.CTkLabel(
                self,
                text='~ Please connect the camera ~',
                fg_color='transparent',
                text_color='GREEN',
                anchor='center'
                )
        self.image_label.grid(
                column=0,
                row=0,
                padx=10,
                pady=10,
                sticky='nesw')

    def show_image(self, image):
        pass

    def set_message(self, val):
        if val:
            message = 'Test done, the camera is ready to use'
        else:
            message = 'Test uncomplete, the camera is not available\nCheck ip'
        self.image_label.configure(text=message)


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry('1000x1000')
        self.resizable(width=False, height=False)
        self.title('The Germinator')
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure((2), weight=1)

        self.upper_frame = UpperFrame(self)
        self.upper_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.buttons_frame = ButtonsFrame(self)
        self.buttons_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.image_frame = ImageFrame(self)
        self.image_frame.grid(row=2, column=0, padx=30, pady=30, sticky='nesw')

    def connect_camera(self, ip):
        self.camera = Camera.Camera(ip)

    def test_connection(self, is_ip=True):
        val = self.camera.check_connection() if is_ip else False
        self.image_frame.set_message(val)

    def disconnect_camera(self):
        del self.camera


def main():
    ctk.set_appearance_mode("dark")

    app = MainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()
