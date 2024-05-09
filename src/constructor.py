import customtkinter as ctk

COLORS = ['#038C8C', '#014040', '#D90404', '#400101', '#262626', '#0D0D0D']


def menu(master, color, method, values_):
    return ctk.CTkOptionMenu(
                master,
                button_color=COLORS[color],
                font=('ProFont Windows Nerd Font', 15),
                button_hover_color=COLORS[color+1],
                text_color='#ffffff',
                command=method,
                values=values_)


def entrys(master, color):
    return ctk.CTkEntry(
            master,
            fg_color='transparent',
            font=('ProFont Windows Nerd Font', 20),
            text_color=COLORS[color])


def label(master, tx, color):
    return ctk.CTkLabel(
            master,
            text=tx,
            fg_color='transparent',
            font=('ProFont Windows Nerd Font', 20),
            text_color=COLORS[color],
            anchor='center')


def slider(master, method, fro_, t, color):
    return ctk.CTkSlider(
            master,
            command=method,
            from_=fro_,
            to=t,
            fg_color=COLORS[color+1],
            button_color=COLORS[color],
            button_hover_color=COLORS[color+1],
            progress_color=COLORS[color]
            )


def button(master, color, tx, method):
    return ctk.CTkButton(
            master,
            border_width=2,
            fg_color='transparent',
            hover_color=COLORS[color+1],
            font=('ProFont Windows Nerd Font', 20),
            border_color=COLORS[color],
            text_color=COLORS[color],
            text=tx,
            command=method)
