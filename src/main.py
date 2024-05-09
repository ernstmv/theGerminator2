import customtkinter as ctk
import Autoset
import Camera
import Identifier
from constructor import menu, entrys, label, slider, button, COLORS


class SlidersFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width=2, border_color=COLORS[-2])
        self.configure(fg_color=COLORS[-1])

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=0)

        self.plants_thresh = 127
        self.tray_thresh = 127
        self.plants_min_area = 1000

        self.labels = [None] * 3
        self.sliders = [None] * 3

        s = [
                'Plants threshold',
                'Plants area',
                'Tray threshold'
                ]

        methods = [
                self.set_plants_thresh,
                self.set_plants_min_area,
                self.set_tray_thresh]

        to_list = [255, 2000, 255]

        for i in range(3):
            self.labels[i] = label(self, s[i], 0)
            self.sliders[i] = slider(self, methods[i], 0, to_list[i], 2)

        self.labels[0].grid(column=0, row=0, padx=10, pady=10, sticky='ew')
        self.labels[1].grid(column=1, row=0, padx=10, pady=10, sticky='ew')
        self.labels[2].grid(
                column=0,
                row=2,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=2)

        self.sliders[0].grid(column=0, row=1, padx=10, pady=10, sticky='ew')
        self.sliders[1].grid(column=1, row=1, padx=10, pady=10, sticky='ew')
        self.sliders[2].grid(
                column=0,
                row=3,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=2)

    def set_plants_thresh(self, value):
        self.plants_thresh = value

    def set_plants_min_area(self, value):
        self.plants_min_area = value

    def set_tray_thresh(self, value):
        self.tray_thresh = value


class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width=2, border_color=COLORS[-2])

        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.configure(fg_color='#0D0D0D')

        self.reload_ips()
        self.ip = None

        self.fields = [None] * 4
        self.buttons = [None] * 5

        sb = [
                'SAVE IP',
                'CONNECT',
                'DISCONNECT',
                'TEST',
                'BUILD']

        m = [
                self.save_ip,
                self.connect,
                self.disconnect,
                self.test,
                self.build]

        for i in range(5):
            self.buttons[i] = button(self, 0, sb[i], m[i])
            self.buttons[i].grid(column=i, row=2, padx=10, pady=10)

        self.auto_button = button(self, 0, 'AUTOSET', self.autoset_img)
        self.auto_button.grid(
                column=0,
                row=3,
                padx=10,
                pady=10,
                sticky='ew',
                columnspan=5)

        self.label = label(self, 'IP DIRECTION', 0)
        self.label.grid(column=2, row=0, padx=10, pady=10, sticky='ew')

        for i in range(4):
            self.fields[i] = entrys(self, 0)
            self.fields[i].grid(column=i, row=1, padx=10, pady=10, sticky='ew')

        self.ip_menu = menu(self, 0, self.load_ip, self.registered_ips)
        self.ip_menu.grid(column=4, row=1, padx=10, pady=10, sticky='ew')

    # SETTERS

    def set_ip(self):
        self.ip = self.read_ip_fields()

    # WIDGETs ACTIONS
    #
    def autoset_img(self):
        self.set_ip()
        self.master.connect_camera(self.ip)
        self.master.autoset()

    def save_ip(self):
        ip = self.read_ip_fields()
        with open('/home/sword/theGerminator/data/ips.txt', 'a') as file:
            file.write(ip+'\n')
        self.reload_ips()

    def connect(self):
        self.set_ip()
        self.master.connect_camera(self.ip)
        self.master.run_video()

    def disconnect(self):
        self.master.disconnect_camera()

    def test(self):
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

    def build(self):
        pass

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
            self.fields[i].insert(0, ip_parts[i])

    def delete_ip_fields(self):
        for ip_field in self.fields:
            ip_field.delete(0, ctk.END)

    def read_ip_fields(self):
        ip = [str(ip_field.get()) for ip_field in self.fields]
        return '.'.join(ip)

    def reload_ips(self):
        with open('/home/sword/theGerminator/data/ips.txt', 'r') as file:
            ips = file.readlines()
        self.registered_ips = [ip.strip() for ip in ips]
        try:
            self.ip_menu.configure(values=self.registered_ips)
        except Exception:
            pass


class ImageFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width=2, border_color=COLORS[-2])
        self.configure(fg_color=COLORS[-1])

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.image_label = ctk.CTkLabel(
                self,
                text='~ Please connect the camera ~',
                fg_color='transparent',
                text_color=COLORS[1],
                font=('ProFont Windows Nerd Font', 20),
                anchor='center'
                )
        self.image_label.grid(
                column=0,
                row=0,
                padx=10,
                pady=10,
                sticky='nesw')

    def show_image(self, image):
        self.image_label.configure(text='', image=image)

    def set_message(self, val):
        if val:
            message = 'Test done, the camera is ready to use'
        else:
            message = 'Test uncomplete, the camera is not available\nCheck ip'
        self.image_label.configure(text=message)


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry('800x900')
        self.resizable(width=False, height=False)
        self.title('The Germinator')
        self.configure(fg_color=COLORS[-1])

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure((2), weight=1)

        self.buttons_frame = ButtonsFrame(self)
        self.buttons_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.sliders_frame = SlidersFrame(self)
        self.sliders_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.image_frame = ImageFrame(self)
        self.image_frame.grid(row=2, column=0, padx=30, pady=30, sticky='nesw')

    def connect_camera(self, ip):
        self.camera = Camera.Camera(ip)

    def test_connection(self, is_ip=True):
        val = self.camera.check_connection() if is_ip else False
        self.image_frame.set_message(val)

    def run_video(self):
        ide = Identifier.Identifier()
        self.stop = False
        while 1:
            image = self.camera.get_image()
            ide.set_image(image)
            ide.identify(
                    self.sliders_frame.tray_thresh,
                    self.sliders_frame.plants_thresh,
                    self.sliders_frame.plants_min_area)
            image = ide.get_image()
            image = self.camera.convert_image(image)
            self.image_frame.show_image(image)
            self.update()

            if self.stop:
                break

    def autoset(self):
        auto = Autoset.Auto()
        self.stop = False
        while 1:
            image = self.camera.get_image()
            auto.set_image(image)
            if auto.auto_run():
                self.stop = True
            image = auto.get_image()
            image = self.camera.convert_image(image)
            self.image_frame.show_image(image)
            self.update()

            if self.stop:
                break

    def disconnect_camera(self):
        self.stop = True
        del self.camera


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    app = MainWindow()
    app.mainloop()
