import customtkinter
import asyncio
import string

import websockets
from websockets.sync.client import connect
from threading import Thread
customtkinter.set_appearance_mode("dark")
websocket = None
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("CTk example")
        self.resizable(width=False, height=False)
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        # add widgets to app
        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.place(x=215,y=180)
        self.login_entry = customtkinter.CTkEntry(self.checkbox_frame, placeholder_text="Логин")
        self.login_entry.grid(row=0, column=0, padx=20, pady=11)
        self.registration_entry = customtkinter.CTkEntry(self.checkbox_frame, placeholder_text="Пароль")
        self.registration_entry.grid(row=1, column=0, padx=20, pady=11)
        self.login_button = customtkinter.CTkButton(self.checkbox_frame, command=self.login_button_click,text="Вход")
        self.login_button.grid(row=2, column=0, padx=20, pady=11)
        self.registration_button = customtkinter.CTkButton(self.checkbox_frame, command=self.register_button_click,text="Регистрация")
        self.registration_button.grid(row=3, column=0, padx=20, pady=11)
        self.version_text = customtkinter.CTkLabel(self, text="Version 0.1", fg_color="transparent",state="disabled")
        self.version_text.place(x=7, y=475)
        self.info_text = customtkinter.CTkLabel(self, text="", fg_color="transparent",anchor="center")
        self.info_text.place(x=217, y=385)
        Thread(target=self.hello).start()
    # add methods to app
    def login_button_click(self):
        if websocket:
            if app.login_entry.get() == "":
                self.info_text.configure(text="Имя пользователя не может быть пустым!")
                self.info_text.place(x=217, y=385)
            elif self.if_spaces(app.login_entry.get()):
                self.info_text.configure(text="Имя пользователя не может содержать пробелы и знаки(. | < >)!")
                self.info_text.place(x=115, y=385)
            else:
                websocket.send(f"login|{app.login_entry.get()}|{app.registration_entry.get()}")

    def register_button_click(self):
        if websocket:
            if app.login_entry.get() == "":
                self.info_text.configure(text="Имя пользователя не может быть пустым!")
                self.info_text.place(x=217, y=385)
            elif self.if_spaces(app.login_entry.get()):
                self.info_text.configure(text="Имя пользователя не может содержать пробелы и знаки(. | < >)!")
                self.info_text.place(x=115, y=385)
            else:
                websocket.send(f"registration|{app.login_entry.get()}|{app.registration_entry.get()}")

    def hello(self):
        global websocket
        try:
            with connect("ws://localhost:8765") as websocket:
                while True:
                    message = websocket.recv()
                    print(f"Received: {message}")
                    data = message.split("|")
                    if data[0] == "login_info":
                        if data[1] == "yes":
                            pass
                        elif data[1] == "no":
                            if data[2] == "no_user":
                                self.info_text.configure(text="Неизвестный пользователь!")
                                self.info_text.place(x=217, y=385)
                            elif data[2] == "incorrect_password":
                                self.info_text.configure(text="Неверный пароль!")
                                self.info_text.place(x=242, y=385)
                    if data[0] == "registration_info":
                        if data[1] == "yes":
                            pass
                        elif data[1] == "no":
                            if data[2] == "user_already_exits":
                                self.info_text.configure(text="Имя пользователя уже занято!")
                                self.info_text.place(x=211, y=385)
                                pass
        except ConnectionRefusedError:
            print("Сервер не доступен!")
            self.info_text.configure(text="Сервер не доступен!")
            self.info_text.place(x=242, y=385)
        except websockets.ConnectionClosedOK:
            print("Соединение успешно закрыто!")

    def on_close(self):
        if websocket:
            websocket.close()
            self.destroy()

    def if_spaces(self,text):
        for c in text:
            if c == " " or c == "|" or c == "." or c == "<" or c == ">":
                return True
        return False
app = App()
app.mainloop()