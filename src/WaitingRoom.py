import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import socket as sock
from socket import socket
import libs.msg as lmsg
import sys

TURNOS_PORT = 5000
TURNOS_IP = "127.0.0.1"


class WaitingRoomApp:
    def __init__(self, root):
        self.connect_server()
        self.process_interface(root)
    def connect_server(self):
        try:
            self.socket = socket()
            self.socket.connect((TURNOS_IP, TURNOS_PORT))
            self.connection_state = "Online"
            self.login()
        except sock.error as err:
            print(f"[Enrollment::Error] - {err}", file=sys.stderr)
            self.socket.close()
            self.connection_state = "Offline"
            messagebox.showerror(
                title="Error", message="No se pudo conectar con el servidor."
            )

    def process_interface(self, window):
        global listbox
        window.title("Sala de espera")
        window.configure(bg="#457B9D")
        window.attributes('-zoomed', True)
        frame = tk.Frame(window, background="#457B9D")
        frame.pack()
        listbox = tk.Listbox(window,width=45, height=10,font=("Helvetica", 50,"bold"))
        listbox.place(x=10,y=10)
        listbox.pack()

    def login(self):
        data: bytes = lmsg.Message(
            msg_type=lmsg.MessageType.LOGIN, sender=lmsg.Role.WAITINGROOM
        ).serialize()
        if self.socket.send(data) < len(data):
            messagebox.showwarning(title="Error", message="Fallo el Login.")
        else:
            Thread(target=self.ping_server, args=(), daemon=True).start()


    def ping_server(self):
        while True:
            try:
                received_data = self.socket.recv(2048)
                msg = lmsg.deserialize(received_data)

                if msg == None:
                    raise ConnectionResetError

                print("[Waiting Room::Info] - Se recibio ", msg, " del servidor.")
                if msg.msg_type == lmsg.MessageType.PATIENT:
                    self.patient = msg.patient
                    listbox.insert(tk.END,self.patient)
                    #data = ping_socket.recv(16, sock.MSG_PEEK)

            except ConnectionError:
                self.connection_state = "Offline"
                #self.update_conn_widget()
                break
            except BlockingIOError:
                continue
        return

if __name__ == "__main__":
    root = tk.Tk()
    app = WaitingRoomApp(root)
    root.mainloop()
