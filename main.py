import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("CTk example")
        self.configure(fg_color="red")

        # add widgets to app
        self.login_button = customtkinter.CTkButton(self, command=self.button_click)
        self.login_button.grid(row=0, column=0, padx=20, pady=10)
        self.registration_button = customtkinter.CTkButton(self, command=self.button_click)
        self.registration_button.grid(row=1, column=0, padx=20, pady=30)

    # add methods to app
    def button_click(self):
        print("button click")


app = App()
app.mainloop()