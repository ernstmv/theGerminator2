import customtkinter as ctk
from MainWindow import MainWindow

THEME_PATH = "/home/leviathan/theGerminator2/.theme/theme.json"

if __name__ == '__main__':
    ctk.set_default_color_theme(THEME_PATH)
    ctk.set_appearance_mode('dark')
    app = MainWindow()
    app.mainloop()
