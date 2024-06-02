from customtkinter import CTkFrame, CTkTextbox


class MessageFrame(CTkFrame):
    def __init__(self, master, w, h):
        super().__init__(master, width=int(w/10), height=int(h/2))
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.message_textbox = CTkTextbox(self, state='disabled')

        self.message_textbox.grid(
                column=0, row=0,
                padx=10, pady=10,
                sticky='nsew')

    def set_message(self, mssg):
        self.message_textbox.configure(state='normal')
        self.message_textbox.delete('0.0', 'end')
        self.message_textbox.insert('0.0', mssg)
        self.message_textbox.configure(state='disabled')
