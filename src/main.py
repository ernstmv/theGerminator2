import customtkinter as ctk


def button(window, tx, function):
    button = ctk.CTkButton(
            window,
            text=tx,
            command=function,
            anchor=ctk.N)
    return button


def pos_widget(widget, row, col, px, py, s):
    widget.grid(
            row=row,
            column=col,
            padx=px,
            pady=py,
            sticky=s)


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('500x500')
        self.title('The Germinator')
        self.grid_columnconfigure((0), weight=1)


def main():
    ctk.set_appearance_mode("dark")

    app = MainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()
