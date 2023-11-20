import tkinter as tk
from tkinter import messagebox, CENTER, W, Label
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

    def format_string(self, text):
        long = 20
        return text.center(long)[:long].upper()

    def process_interface(self, window):
        global listbox
        window.title("Sala de espera")
        window.configure(bg="#457B9D")
        window.attributes('-zoomed', True)

        frame = tk.Frame(window, background="#457B9D")
        frame.pack()

        title = Label(text=self.format_string("paciente") + "|" + self.format_string("consultorio"))
        title.config(fg="#1D3557",bg="#A8DADC",width=45,height=1,font=("Monospace",50,"bold"),anchor=W)
        title.pack(anchor=CENTER,pady=20,ipady=20)


        listbox = tk.Listbox(window,width=45, height=9,font=("Monospace", 50,"bold"))
        listbox.config(bg="#1D3557")
        listbox.pack(anchor=CENTER)


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
                    patients=listbox.get(0, tk.END)
                    listbox.delete(0,tk.END)
                    self.patient = msg.patient
                    patient = self.patient.name+" "+self.patient.surname
                    room = self.patient.room
                    listbox.insert(tk.END,self.format_string(patient)+"| "+self.format_string("consultorio "+room))
                    listbox.itemconfig(0, {'fg': '#E63946'})
                    cont=0
                    for p in patients:
                        listbox.insert(tk.END,p)
                        cont=cont+1
                        listbox.itemconfig(cont, {'fg': 'white'})

            except ConnectionError:
                self.connection_state = "Offline"
                break
            except BlockingIOError:
                continue
        return

if __name__ == "__main__":
    root = tk.Tk()
    app = WaitingRoomApp(root)
    root.mainloop()
