import customtkinter as ctk
import Autoset
import Camera
from constructor import menu, entrys, label, button, COLORS


class DialogFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, border_width=2, border_color=COLORS[1])
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.configure(fg_color='#000000')

        self.dialog_textbox = ctk.CTkTextbox(
                self,
                border_width=2,
                fg_color='#000000',
                border_color=COLORS[-1],
                text_color=COLORS[0],
                font=('ProFont Windows Nerd Font', 20),
                height=90,
                state='disabled'
                )

        self.dialog_textbox.grid(
                column=0,
                row=0,
                padx=10,
                pady=10,
                sticky='ew')

    def show_message(self, n_message=-1, mssg=None, np=0, ts=0, ptg=0):
        messages = [
                'Welcome, please connect a camera',
                'Test OK, the device is online',
                'Device unavailable, please check the IP direction',
                'Connecting...',
                'Identifying tray ...',
                'Identifying plants...',
                f'Plants: {np}\nTray size: {ts}\nPercentage: {ptg}',
                'Loading...',
                'Done'
                ]
        message = mssg if mssg else messages[n_message]
        self.dialog_textbox.configure(state='normal')
        self.dialog_textbox.delete('0.0', 'end')
        self.dialog_textbox.insert('0.0', message)
        self.dialog_textbox.configure(state='disabled')


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
                'LAUNCH']

        m = [
                self.save_ip,
                self.connect,
                self.disconnect,
                self.test,
                self.launch]

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

    def launch(self):
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
                text=None,
                fg_color='transparent',
                text_color=COLORS[1],
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


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry('800x900')
        self.resizable(width=False, height=False)
        self.title('The Germinator')
        self.configure(fg_color=COLORS[-1])

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0, 2), weight=0)
        self.grid_rowconfigure((1), weight=1)

        self.buttons_frame = ButtonsFrame(self)
        self.buttons_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.image_frame = ImageFrame(self)
        self.image_frame.grid(row=1, column=0, padx=30, pady=30, sticky='nesw')

        self.dialog_frame = DialogFrame(self)
        self.dialog_frame.grid(row=2, column=0, padx=10, pady=10, sticky='esw')

        self.dialog_frame.show_message(0)

    def connect_camera(self, ip):
        self.dialog_frame.show_message(3)
        self.camera = Camera.Camera(ip)
        self.dialog_frame.show_message()

    def test_connection(self, is_ip=True):
        n = 1 if self.camera.check_connection() else 2
        self.dialog_frame.show_message(n)

    def run_video(self):
        self.stop = False
        while 1:
            try:
                image = self.camera.get_image()
            except Exception as e:
                self.dialog_frame.show_message(mssg=e)
                break
            image = self.camera.convert_image(image)
            self.image_frame.show_image(image)
            self.update()

            if self.stop:
                break

    def autoset(self):
        self.auto = Autoset.Auto()
        self.stop = False
        while 1:
            try:
                image = self.camera.get_image()
            except Exception as e:
                self.dialog_frame.show_message(mssg=e)
                break
            self.auto.set_image(image)
            if self.auto.detect_tray():
                self.auto.detect_plants()
                np, ts, ptg = self.auto.process_data()
                self.dialog_frame.show_message(
                        n_message=-3,
                        np=np,
                        ts=ts,
                        ptg=ptg)
                self.stop = True
            image = self.auto.get_image()
            image = self.camera.convert_image(image)
            self.image_frame.show_image(image)
            self.update()

            if self.stop:
                del (self.auto)
                break

    def disconnect_camera(self):
        self.stop = True
        del self.camera


if __name__ == '__main__':
    ctk.set_appearance_mode("dark")
    app = MainWindow()
    app.mainloop()
