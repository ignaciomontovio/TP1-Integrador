import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import os
import sys
import socket as sock
from socket import socket
import libs.patient as lp
import libs.msg as lmsg
import time

TURNOS_PORT = 5000
TURNOS_IP = "127.0.0.1"


class PatientEntryApp:
    def __init__(self, root):
        self.patient_counter = 0
        self.root = root
        root.title("Alta de paciente")
        root.configure(bg="#457B9D")
        self.connection_state = "Offline"

        self.create_widgets()
        self.connect_server()

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
        self.update_conn_widget()

    def login(self):
        data: bytes = lmsg.Message(
            msg_type=lmsg.MessageType.LOGIN, sender=lmsg.Role.RECEPTION
        ).serialize()
        if self.socket.send(data) < len(data):
            messagebox.showwarning(title="Error", message="Fallo el Login.")
        else:
            Thread(target=self.ping_server, args=(), daemon=True).start()

    def ping_server(self):
        try:
            ping_socket = socket()
            ping_socket.connect((TURNOS_IP, TURNOS_PORT))
            ping_socket.setblocking(False)
        except:
            print("[Enrollment::Ping::Error] - Error al crear socket para ping.")
            return
        while True:
            try:
                data = ping_socket.recv(16, sock.MSG_PEEK)
                if len(data) == 0:
                    raise ConnectionError
                
            except ConnectionError:
                self.connection_state = "Offline"
                self.update_conn_widget()
                break
            except BlockingIOError:
                continue
        return

    def update_conn_widget(self):
        self.connection_label.config(text=self.connection_state)
        if self.connection_state == "Online":
            self.connection_label.config(background="green")
            self.conn_info_frame.config(background="green")
            self.button_reconnect["state"] = tk.DISABLED

        else:
            self.connection_label.config(background="red")
            self.conn_info_frame.config(background="red")
            self.button_reconnect["state"] = tk.ACTIVE

    def create_widgets(self):
        self.conn_info_frame = tk.Frame(
            self.root,
            background="red",
        )

        self.button_reconnect = tk.Button(
            self.conn_info_frame,
            text="Reconectar",
            command=self.connect_server,
            background="#CCCCCC",
            state=tk.DISABLED,
        )
        self.button_reconnect.pack(side="right", ipadx=0, ipady=0)

        self.connection_label = tk.Label(
            self.conn_info_frame,
            text=self.connection_state,
            anchor="w",
            background="red",
        )
        self.connection_label.pack(side="left")

        self.conn_info_frame.pack(anchor="nw", fill="x", expand=True)

        frame = tk.Frame(self.root, background="#457B9D")
        frame.pack()

        user_info_frame = tk.LabelFrame(
            frame, text="Información del paciente", background="#457B9D"
        )
        user_info_frame.grid(row=1, column=0, padx=20, pady=10)

        self.first_name_label = tk.Label(
            user_info_frame, text="Nombre", background="#457B9D"
        )
        self.first_name_label.grid(row=0, column=0)

        self.first_name_entry = tk.Entry(user_info_frame, background="#F1FAEE")
        self.first_name_entry.grid(row=1, column=0)

        self.last_name_label = tk.Label(
            user_info_frame, text="Apellido", background="#457B9D"
        )
        self.last_name_label.grid(row=0, column=1)

        self.last_name_entry = tk.Entry(user_info_frame, background="#F1FAEE")
        self.last_name_entry.grid(row=1, column=1)

        self.combostyle = ttk.Style()
        self.combostyle.theme_create(
            "combostyle",
            parent="alt",
            settings={
                "TCombobox": {
                    "configure": {"fieldbackground": "#F1FAEE", "background": "#F1FAEE"}
                }
            },
        )
        self.combostyle.theme_use("combostyle")

        self.sex_label = tk.Label(user_info_frame, text="Género", background="#457B9D")
        self.sex_combobox = ttk.Combobox(user_info_frame, values=["", "M", "F", "X"])
        self.sex_label.grid(row=0, column=2)
        self.sex_combobox.grid(row=1, column=2)

        self.age_label = tk.Label(user_info_frame, text="Edad", background="#457B9D")
        self.age_spinbox = tk.Spinbox(
            user_info_frame, from_=0, to=110, background="#F1FAEE"
        )
        self.age_label.grid(row=2, column=0)
        self.age_spinbox.grid(row=3, column=0)

        self.dni_label = tk.Label(user_info_frame, text="DNI", background="#457B9D")
        self.dni_entry = tk.Entry(user_info_frame, background="#F1FAEE")
        self.dni_label.grid(row=2, column=1)
        self.dni_entry.grid(row=3, column=1)

        description_frame = tk.LabelFrame(frame, background="#457B9D")
        description_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

        self.symptoms_label = tk.Label(
            description_frame, text="Síntomas", background="#457B9D"
        )
        self.symptoms_entry = tk.Entry(
            description_frame, width=67, background="#F1FAEE"
        )
        self.symptoms_label.grid(row=4, column=1)
        self.symptoms_entry.grid(row=5, column=1)

        button_send = tk.Button(
            frame,
            text="Ingresar Paciente",
            command=self.enter_data,
            background="#90BE6D",
        )
        button_send.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        button_exit = tk.Button(
            frame,
            text="Finalizar sesión",
            command=self.finish_session,
            background="#E63946",
        )
        button_exit.grid(row=4, column=0, sticky="news", padx=20, pady=10)

    def finish_session(self):
        self.socket.close()
        self.root.quit()
        os._exit(0)

    def send_data(self, patient):
        try:
            if self.connection_state == "Online":
                data: bytes = lmsg.Message(
                    msg_type=lmsg.MessageType.PATIENT, patient=patient
                ).serialize()
                try:
                    if self.socket.send(data) < len(data):
                        print(
                            "[Enrollment::Error] - El paciente no puedo ser ingresado en el sistema.",
                            file=sys.stderr,
                        )
                        messagebox.showwarning(
                            title="Error",
                            message="El paciente no puedo ser ingresado en la cola.",
                        )

                except:
                    raise ConnectionResetError
            else:
                messagebox.showwarning(
                    title="Error", message="Se requiere una conexion con el servidor."
                )

            server_response = self.socket.recv(2048)
            msg = lmsg.deserialize(server_response)

            if msg == None:
                raise ConnectionResetError
                

            if msg.msg_type == lmsg.MessageType.GOT:
                Thread(
                    target=messagebox.showinfo,
                    kwargs={
                        "title": "Aceptado",
                        "message": "El paciente fue ingresado exitosamente.",
                    },
                )
        except ConnectionResetError:
            print("[Enrollment::Warning] - Se perdio la conexion con el servidor.")
            self.socket.close()
            self.connection_state = "Offline"
            self.update_conn_widget()

    def enter_data(self):
        firstname = self.first_name_entry.get()
        lastname = self.last_name_entry.get()

        if firstname and lastname:
            self.patient_counter += 1
            patient = lp.Patient(
                nro=self.patient_counter,
                name=firstname,
                surname=lastname,
                dni=self.dni_entry.get(),
                age=self.age_spinbox.get(),
                sex=self.sex_combobox.get(),
                symptoms=self.symptoms_entry.get(),
            )
            self.send_data(patient)
        else:
            messagebox.showwarning(
                title="Error", message="Se requieren nombre y apellido."
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = PatientEntryApp(root)
    root.mainloop()
