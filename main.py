import customtkinter
customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("CTk example")
        self.resizable(width=False, height=False)

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
    # add methods to app
    def login_button_click(self):
        self.info_text.configure(text="Неверный логин или пароль!")
        self.info_text.place(x=217, y=385)

    def register_button_click(self):
        self.info_text.configure(text="Сервер не доступен!")
        self.info_text.place(x=242, y=385)
app = App()
app.mainloop()