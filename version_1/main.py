import textwrap
import rsa
import customtkinter
import asyncio
import string
from PIL import Image
import websockets
from websockets.sync.client import connect
from threading import Thread
customtkinter.set_appearance_mode("dark")
websocket = None
server_pub_key = None
(my_pub_key, my_priv_key) = rsa.newkeys(2048)
#Класс приложения
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("PyChat by Stepan4ek")
        self.resizable(width=False, height=False)
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        self.myname = ""
        self.messages_list = ()
        self.selected_chat = ""
        #Окно меню регистрации и входа
        self.logo_image = customtkinter.CTkImage(light_image=Image.open("logo.png"), size=(193, 58))
        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.place(x=215,y=180)
        self.login_entry = customtkinter.CTkEntry(self.checkbox_frame, placeholder_text="Логин")
        self.login_entry.grid(row=0, column=0, padx=20, pady=11)
        self.registration_entry = customtkinter.CTkEntry(self.checkbox_frame, placeholder_text="Пароль",show='*')
        self.registration_entry.grid(row=1, column=0, padx=20, pady=11)
        self.login_button = customtkinter.CTkButton(self.checkbox_frame, command=self.login_button_click,text="Вход")
        self.login_button.grid(row=2, column=0, padx=20, pady=11)
        self.registration_button = customtkinter.CTkButton(self.checkbox_frame, command=self.register_button_click,text="Регистрация")
        self.registration_button.grid(row=3, column=0, padx=20, pady=11)
        self.version_text = customtkinter.CTkLabel(self, text="Version: beta 0.0.1", fg_color="transparent",state="disabled")
        self.version_text.place(x=7, y=475)
        self.info_text = customtkinter.CTkLabel(self, text="", fg_color="transparent",anchor="center")
        self.info_text.place(x=217, y=385)
        self.logo_text = customtkinter.CTkLabel(self, text="", fg_color="transparent", anchor="center",image=self.logo_image)
        self.logo_text.place(x=207, y=100)
        self.info_menu_button = customtkinter.CTkButton(self, text="Информация", command=self.info_menu_button_event)
        self.info_menu_button.place(x=10, y=10)
        #Окно меню информации
        self.info_menu_all_frame = customtkinter.CTkFrame(self, width=600, height=400,fg_color="transparent",border_width=0)
        self.info_menu_all_frame.place(x=-1000, y=10)
        self.info_menu_frame = customtkinter.CTkFrame(self.info_menu_all_frame,width=550,height=135)
        self.info_menu_frame.place(x=10, y=0)
        self.menu_info_text = customtkinter.CTkLabel(self.info_menu_frame, text="Информация о программе:\nПрограмма полностью написана на python\nПередача данных и сообщений сделана на WebSocket\nПрограмма находится в процессе разработки\nПрограмма была написана в одиночку\nАвтор программы Stepan4ek", fg_color="transparent", anchor="s",justify="left",font=("",17))
        self.menu_info_text.place(x=10, y=10)
        self.info_menu_frame1 = customtkinter.CTkScrollableFrame(self.info_menu_all_frame,width=550,height=135)
        self.info_menu_frame1.place(x=10, y=143)
        self.menu_info_text1 = customtkinter.CTkLabel(self.info_menu_frame1, text="Дополнительная информация\n――――――――――――――――――――――――――――――――――――――――――――――――――――――\nЛицензия:\nПроект полность открытый, код доступен для всех, пожалуйста не \nворуйте и не выдавайте себя за его автора.\nЕсли вы хотите помочь в развитии проекта пишите в дискорд, \nник stepan4ek\n――――――――――――――――――――――――――――――――――――――――――――――――――――――\nШифровние:\nВсе данные шифруются с помощью асиметричного шифрования,\nМодуль шифрования python: rsa", fg_color="transparent", anchor="s",justify="left",font=("",17))
        self.menu_info_text1.grid(row=0, column=0, padx=0, pady=(10, 20), sticky="w")
        #Окно меню чата
        self.chat_menu_frame = customtkinter.CTkFrame(self, width=610, height=480,fg_color="transparent",border_width=0)
        self.chat_menu_frame.place(x=-1000, y=0)
        self.chats_frame = customtkinter.CTkScrollableFrame(self.chat_menu_frame, width=150, height=390,label_text="Чаты")
        self.chats_frame.place(x=7, y=35)
        self.messsages_frame = customtkinter.CTkScrollableFrame(self.chat_menu_frame, width=372, height=350,label_text="Сообщения")
        self.messsages_frame.place(x=200, y=35)
        self.message_entry = customtkinter.CTkEntry(self.chat_menu_frame, placeholder_text="Сообщение",width=280)
        self.message_entry.place(x=200, y=445)
        self.message_send_button = customtkinter.CTkButton(self.chat_menu_frame, command=self.send_new_message, text="Отправить",width=108)
        self.message_send_button.place(x=485, y=445)
        self.chats = []
        chat = customtkinter.CTkButton(self.chats_frame, text="Общий чат")
        chat.grid(row=0, column=0, padx=0, pady=(10, 0), sticky="w")
        self.chats.append(chat)
        self.message_coint = 0
        self.messages = []
        #for i in range(50):
            #chat = customtkinter.CTkButton(self.chats_frame, text=str(i))
            #chat.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            #self.checkboxes.append(chat)
        #Подключение к серверу
        Thread(target=self.hello).start()
    #Событие при нажатии на логин
    def login_button_click(self):
        if websocket:
            if app.login_entry.get() == "":
                self.info_text.configure(text="Имя пользователя не может быть пустым!")
                self.info_text.place(x=175, y=385)
            elif app.registration_entry.get() == "":
                self.info_text.configure(text="Пароль не может быть пустым!")
                self.info_text.place(x=211, y=385)
            elif self.if_spaces(app.login_entry.get()):
                self.info_text.configure(text="Имя пользователя не может содержать пробелы и знаки(. | < >)!")
                self.info_text.place(x=115, y=385)
            else:
                websocket.send(self.encript(f"login|{app.login_entry.get()}|{app.registration_entry.get()}"))
    #Событие при нажатии на регистрацию
    def register_button_click(self):
        if websocket:
            if app.login_entry.get() == "":
                self.info_text.configure(text="Имя пользователя не может быть пустым!")
                self.info_text.place(x=175, y=385)
            elif app.registration_entry.get() == "":
                self.info_text.configure(text="Пароль не может быть пустым!")
                self.info_text.place(x=211, y=385)
            elif self.if_spaces(app.login_entry.get()):
                self.info_text.configure(text="Имя пользователя не может содержать пробелы и знаки(. | < >)!")
                self.info_text.place(x=115, y=385)
            elif self.if_slesh(app.registration_entry.get()):
                self.info_text.configure(text="Пароль не может содержать знак |!")
                self.info_text.place(x=197, y=385)
            else:
                websocket.send(self.encript(f"registration|{app.login_entry.get()}|{app.registration_entry.get()}"))
    #Событие при нажатии на информацию
    def info_menu_button_event(self):
        self.open_chat()
        if self.info_menu_button.cget("text") == "Информация":
            self.info_menu_button.configure(text="Назад")
            self.close_reglog_menu()
            self.open_info_menu()
        elif self.info_menu_button.cget("text") == "Назад":
            self.info_menu_button.configure(text="Информация")
            self.open_reglog_menu()
            self.close_info_menu()
    #Срабатывает при получении сообщения
    def new_message(self,name,message,to,access):
        if name == self.myname:
            message = customtkinter.CTkLabel(self.messsages_frame, text=f"<{name}>\n{textwrap.fill(message, 40)}",fg_color="#5d5d5d", width=40, height=40, corner_radius=7, justify="left")
            message.grid(row=self.message_coint, column=1, padx=10, pady=(10, 0), sticky="w")
        else:
            message = customtkinter.CTkLabel(self.messsages_frame, text=f"<{name}>\n{textwrap.fill(message, 40)}",fg_color="#3b3b3b", width=40, height=40, corner_radius=7, justify="left")
            message.grid(row=self.message_coint, column=1, padx=10, pady=(10, 0), sticky="w")
        self.messages.append(message)
        self.message_coint += 1
    def select_chat(self,idx):
        print(self.messages[idx].cget("text"))
    def send_new_message(self):
        if len(app.message_entry.get()) > 200:
            print("Слишком большое сообщение!")
            pass
        else:
            websocket.send(self.encript(f"message|{self.myname}|public|all|{app.message_entry.get()}"))
            app.message_entry.delete(0, last_index=None)
        pass
    #Функция обмена данными
    def hello(self):
        global websocket,server_pub_key
        try:
            with connect("ws://stepan4ek.servegame.com:8765") as websocket:
                websocket.send(f"key|{my_pub_key.n}|{my_pub_key.e}")
                while True:
                    message = websocket.recv()
                    print(f"Получено зашифрованое сообщение: {message}")
                    try:
                        if message.split("|",1)[0] == "key":
                            server_pub_key = rsa.PublicKey(int(message.split("|")[1]),int(message.split("|")[2]))
                    except TypeError as err:
                        data_decript = rsa.decrypt(message, my_priv_key)
                        print(f"Сообщение расшифровано: {data_decript.decode('utf8')}")
                        data = data_decript.decode("utf8").split("|")
                        if data[0] == "login_info":
                            if data[1] == "yes":
                                self.myname = app.login_entry.get()
                                self.open_chat()
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
                                self.info_text.configure(text="Успешная регистрация!")
                                self.info_text.place(x=211, y=385)
                                pass
                            elif data[1] == "no":
                                if data[2] == "user_already_exits":
                                    self.info_text.configure(text="Имя пользователя уже занято!")
                                    self.info_text.place(x=211, y=385)
                                    pass
                        if data[0] == "message":
                            self.new_message(data[1],data[4],data[3],data[2])
        except ConnectionRefusedError:
            print("Сервер не доступен!")
            self.info_text.configure(text="Сервер не доступен!")
            self.info_text.place(x=242, y=385)
            self.registration_button.configure(state="disabled")
            self.login_button.configure(state="disabled")
            self.registration_entry.configure(state="disabled")
            self.login_entry.configure(state="disabled")
        except websockets.ConnectionClosedOK:
            print("Соединение успешно закрыто!")
    #Функция закрытия приложения
    def on_close(self):
        if websocket:
            websocket.close()
        self.destroy()
    #Функция проверки на пробелы
    def if_spaces(self,text):
        for c in text:
            if c == " " or c == "|" or c == "." or c == "<" or c == ">" or c == "(" or c == ")" or c == "!":
                return True
        return False
    #Функция проверки на слеш
    def if_slesh(self,text):
        for c in text:
            if c == "|":
                return True
        return False
    def encript(self,text):
        return rsa.encrypt(text.encode("utf8"), server_pub_key)
    #функция закрытия меню регистрации и входа
    def close_reglog_menu(self):
        self.checkbox_frame.place(x=-215, y=180)
        self.logo_text.place(x=-2207, y=100)
        self.info_text.place(x=self.info_text.winfo_x()+1000, y=385)
    #функция открытия меню регистрации и входа
    def open_reglog_menu(self):
        self.checkbox_frame.place(x=215, y=180)
        self.logo_text.place(x=207, y=100)
        self.info_text.place(x=self.info_text.winfo_x()-1000, y=385)
    #функция открытия меню информации
    def open_info_menu(self):
        self.info_menu_all_frame.place(x=10, y=50)
    #функция закрытия меню информации
    def close_info_menu(self):
        self.info_menu_all_frame.place(x=-1000, y=10)
    def open_chat(self):
        self.chat_menu_frame.place(x=0, y=0)
app = App()
app.mainloop()