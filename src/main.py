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

        self.registered_ips = None

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

        self.ip1_entry = ctk.CTkEntry(
                self,
                fg_color='transparent',
                text_color=BLUE)
        self.ip2_entry = ctk.CTkEntry(
                self,
                fg_color='transparent',
                text_color=BLUE)
        self.ip3_entry = ctk.CTkEntry(
                self,
                fg_color='transparent',
                text_color=BLUE)
        self.ip4_entry = ctk.CTkEntry(
                self,
                fg_color='transparent',
                text_color=BLUE)
        self.ip5_entry = ctk.CTkEntry(
                self,
                fg_color='transparent',
                text_color=BLUE)

        self.ip_menu = ctk.CTkOptionMenu(
                self,
                button_color=BLUE,
                button_hover_color=DARK_BLUE,
                text_color=BLUE,
                command=self.load_ip,
                values=self.registered_ips
                )

        self.ip_label.grid(
                column=1,
                row=0,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=6)

        self.ip1_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')
        self.ip2_entry.grid(column=2, row=1, padx=10, pady=10, sticky='ew')
        self.ip3_entry.grid(column=3, row=1, padx=10, pady=10, sticky='ew')
        self.ip4_entry.grid(column=4, row=1, padx=10, pady=10, sticky='ew')
        self.ip5_entry.grid(column=5, row=1, padx=10, pady=10, sticky='ew')
        self.ip_menu.grid(column=6, row=1, padx=10, pady=10, sticky='ew')

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
                columnspan=3)

        self.area_label.grid(
                column=4,
                row=2,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=3)

        self.thresh_slider.grid(
                column=1,
                row=3,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=3)

        self.area_slider.grid(
                column=4,
                row=3,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=3)

    def set_thresh_value(self):
        pass

    def set_area_value(self):
        pass

    def load_ip(self):
        pass

    def save_ip(self):
        pass

    def connect_camera(self):
        pass

    def capture_image(self):
        pass

    def test_connection(self):
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


def main():
    ctk.set_appearance_mode("dark")

    app = MainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()
