import socket
import customtkinter
from PIL import Image
import threading

IP = "127.0.0.1"
PORT = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))


class frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs, ):
        super().__init__(master, **kwargs)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        def send():
            msg = self.entry.get()
            client_socket.send(msg.encode("utf-8"))
            self.entry.delete(0, 10000000)
            if 'dark-mode' in msg:
                customtkinter.set_appearance_mode('dark')
            if 'light-mode' in msg:
                customtkinter.set_appearance_mode('light')

        self.entry = customtkinter.CTkEntry(self, width=850)
        self.entry.grid(row=1, column=0, sticky=customtkinter.N, padx=5, pady=5)
        self.image = customtkinter.CTkImage(light_image=Image.open("send_button_light.png"),
                                            dark_image=Image.open("send_button.png"),
                                            size=(15, 15))

        self.button = customtkinter.CTkButton(self, text="", command=send, width=30, height=28, image=self.image)
        self.button.grid(row=1, column=1, sticky=customtkinter.N, pady=5, padx=2)
        send_thread = threading.Thread(target=send)
        send_thread.start()


class frame_label(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.frame = frame(master=self)

        def msgs():
            while True:
                msg_recv = client_socket.recv(1024).decode("utf-8")
                self.label = customtkinter.CTkLabel(self, text=msg_recv)
                self.label.pack(anchor=customtkinter.W, padx=10)
                if 'dark-mode' in msg_recv:
                    customtkinter.set_appearance_mode('dark')
                if 'light-mode' in msg_recv:
                    customtkinter.set_appearance_mode('light')

        msg_thread = threading.Thread(target=msgs)
        msg_thread.start()


class app(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode('system')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.geometry('600x600')
        self.frame = frame(master=self)
        self.frame.grid(row=1, column=0, sticky=customtkinter.S)
        self.frame_label = frame_label(master=self)
        self.frame_label.grid(row=0, column=0, ipadx=300, ipady=300)
        self.title("chat-box")
        self.iconbitmap("chat-box.ico")
        self.mainloop()


app()
