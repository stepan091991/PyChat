import customtkinter
import textwrap
customtkinter.set_appearance_mode("dark")
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("PyChat by Stepan4ek")
        self.resizable(width=False, height=False)

        self.chat_menu_frame = customtkinter.CTkFrame(self, width=610, height=480, fg_color="transparent", border_width=0)
        self.chat_menu_frame.place(x=0, y=0)
        self.chats_frame = customtkinter.CTkScrollableFrame(self.chat_menu_frame, width=150, height=390, label_text="Чаты")
        self.chats_frame.place(x=7, y=35)
        self.messsages_frame = customtkinter.CTkScrollableFrame(self.chat_menu_frame, width=372, height=390, label_text="Сообщения")
        self.messsages_frame.place(x=200, y=35)
        self.message_entry = customtkinter.CTkEntry(self.chat_menu_frame, placeholder_text="Сообщение", width=280)
        self.message_entry.place(x=200, y=445)
        self.message_send_button = customtkinter.CTkButton(self.chat_menu_frame, command=self.new_message, text="Отправить", width=108)
        self.message_send_button.place(x=485, y=445)
        self.coint = 0
        self.messages = []
        self.chats = []
        for i in range(10):
            name = i
            self.chat = customtkinter.CTkButton(self.chats_frame, text=str(i+1),command=lambda idx = i: self.click3(idx))
            self.chat.grid(row=i, column=0, padx=0, pady=(10, 0), sticky="w")
            self.chats.append(self.chat)
    def click3(self,idx):
        print(self.chats[idx].cget("text"))
    def new_message(self):
        message = customtkinter.CTkLabel(self.messsages_frame, text=f"<Stepan4ek>\n{textwrap.fill(app.message_entry.get(), 40)}",fg_color="#3b3b3b",width=40,height=40,corner_radius=7,justify="left")
        message.grid(row=self.coint, column=1, padx=10, pady=(10, 0), sticky="w")
        self.messages.append(message)
        self.coint += 1

app = App()
app.mainloop()