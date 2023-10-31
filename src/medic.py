import sys
import socket as sock
from socket import socket
from threading import Thread, Condition
import tkinter as tk
from tkinter import ttk, messagebox
import libs.msg as lmsg
from libs.theme import Theme
import time

TURNOS_IP = "127.0.0.1"
TURNOS_PORT = 5000


class App(tk.Tk):
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    BORDER_WIDTH = 20
    APP_NAME = "Medico"
    FONT_NAME = "TkDefaultFont"

    def __init__(self):
        super().__init__()

        self.call_patient = Condition()
        self.connection_state = "Offline"

        self.str_patitentTitle = tk.StringVar()
        self.str_counterLabel = tk.StringVar(value="Pacientes Pendientes: 0")
        self.draw()

        self.connect_server()

        if self.socket is None:
            self.str_patitentTitle.set("Error!")
            self.patientDesc.insert(
                tk.END, "No se ha podido comunicar con la recepción..."
            )
            self.nextButton["state"] = tk.DISABLED
            self.patientDesc["state"] = tk.DISABLED
        else:
            self.str_patitentTitle.set("Bienvenido!")
            self.patientDesc.insert(
                tk.END, "Presione el boton de abajo para llamar a un paciente."
            )

        self.bind("<Escape>", self.exit)
        self.bind("<<New Patient>>", self.update_patient)
        self.bind("<<Inform Patient>>", self.notify_patient)

    def connect_server(self):
        try:
            self.socket = socket()
            self.socket.connect((TURNOS_IP, TURNOS_PORT))
            self.connection_state = "Online"
            self.login()
            Thread(target=self.wait_patient, args=(), daemon=True).start()
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
            msg_type=lmsg.MessageType.LOGIN, sender=lmsg.Role.MEDIC
        ).serialize()
        if self.socket.send(data) < len(data):
            messagebox.showwarning(title="Error", message="Fallo el Login.")
        else:
            Thread(target=self.ping_server, args=(), daemon=True).start()
            self.event_generate("<<New Patient>>")

    def ping_server(self):
        try:
            ping_socket = self.socket.dup()
        except:
            print("[Medic::Ping::Error] - Error al crear socket para ping.")
            return
        while True:
            try:
                data = ping_socket.recv(2048, sock.MSG_PEEK)
                if not data:
                    raise ConnectionResetError
                else:
                    msg = lmsg.deserialize(data)
                    if msg.msg_type == lmsg.MessageType.COUNTER:
                        ping_socket.recv(2048)
                        self.str_counterLabel.set(f"Pacientes Pendientes: {msg.counter}")

            except ConnectionResetError:
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

    def draw(self):
        self.geometry(f"{App.SCREEN_WIDTH}x{App.SCREEN_HEIGHT}")
        self.resizable(0, 0)
        self.title(App.APP_NAME)

        Theme.style(self, self.FONT_NAME)

        mainFrame = ttk.Frame(
            self, width=App.SCREEN_WIDTH, height=App.SCREEN_HEIGHT, style="Main.TFrame"
        )
        mainFrame.pack(fill="both", expand=True)

        self.conn_info_frame = tk.Frame(
            mainFrame,
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

        subFrame = ttk.Frame(
            mainFrame,
            width=App.SCREEN_HEIGHT - App.BORDER_WIDTH,
            height=App.SCREEN_HEIGHT - App.BORDER_WIDTH,
            style="Sub.TFrame",
        )
        subFrame.pack(
            fill="both",
            expand=True,
            anchor="center",
            padx=App.BORDER_WIDTH,
            pady=App.BORDER_WIDTH,
        )

        labelsFrame = ttk.Frame(subFrame, style="Sub.TFrame")
        labelsFrame.pack(fill="both", expand=True, anchor="center")

        patientTitle = ttk.Label(
            labelsFrame,
            textvariable=self.str_patitentTitle,
            background=Theme.BG,
            foreground=Theme.RED,
            font=(App.FONT_NAME, 22, "bold"),
        )
        patientTitle.pack(anchor="ne", padx=10, pady=10, side=tk.LEFT)

        counterLabel = ttk.Label(
            labelsFrame,
            textvariable=self.str_counterLabel,
            background=Theme.BG,
            foreground=Theme.RED,
            font=(App.FONT_NAME, 12, "bold"),
        )
        counterLabel.pack(anchor="nw", padx=10, pady=10, side=tk.RIGHT)

        scrollbar = ttk.Scrollbar(subFrame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.patientDesc = tk.Text(
            subFrame,
            background=Theme.BG,
            selectbackground=Theme.TEXT_SELECTED_BG,
            foreground=Theme.FG,
            selectforeground=Theme.BG,
            insertbackground=Theme.RED,
            font=(App.FONT_NAME, 14),
            wrap="word",
            yscrollcommand=scrollbar.set,
            height=20,
            spacing2=3,
        )
        self.patientDesc.pack(fill="both", padx=15, pady=5, expand=True)
        self.patientDesc.tag_configure("bold", font=(App.FONT_NAME, 14, "bold"))
        self.patientDesc.tag_configure("italic", font=(App.FONT_NAME, 14, "italic"))

        scrollbar.config(command=self.patientDesc.yview)

        self.nextButton = ttk.Button(
            subFrame, text="Siguiente Turno", command=self.request_patient
        )
        self.nextButton.pack(
            expand=True,
            anchor="se",
            padx=App.BORDER_WIDTH,
            pady=App.BORDER_WIDTH,
            ipadx=5,
            ipady=5,
        )

    def set_patient_description(self):
        self.patientDesc.delete("1.0", tk.END)
        self.patientDesc.insert(tk.END, "Nombre: ", "bold")
        self.patientDesc.insert(tk.END, f"{self.patient.name}")
        self.patientDesc.insert(tk.END, f"\nApellido: ", "bold")
        self.patientDesc.insert(tk.END, f"{self.patient.surname}")
        self.patientDesc.insert(tk.END, f"\nDNI: ", "bold")
        self.patientDesc.insert(tk.END, f"{self.patient.dni}")
        self.patientDesc.insert(tk.END, f"\nEdad: ", "bold")
        self.patientDesc.insert(tk.END, f"{self.patient.age}")
        self.patientDesc.insert(tk.END, f"\tSexo: ", "bold")
        self.patientDesc.insert(tk.END, f"{self.patient.sex}")
        self.patientDesc.insert(tk.END, f"\n\nSintomas:\n", "italic")
        self.patientDesc.insert(tk.END, f"{self.patient.symptoms}")

    def request_patient(self):
        self.str_patitentTitle.set("Esperando pacientes...")
        self.patientDesc.delete("1.0", tk.END)
        self.nextButton["state"] = tk.DISABLED

        with self.call_patient:
            self.call_patient.notify()

    def update_patient(self, _event):
        if self.patient is None:
            self.str_patitentTitle.set("Error!")
            self.patientDesc.insert(
                tk.END, "No se ha podido comunicar con el servidor..."
            )
            if self.connection_state == "Online":
                self.nextButton["state"] = tk.ACTIVE
            else:
                self.nextButton["state"] = tk.DISABLED

            self.patientDesc["state"] = tk.DISABLED
        else:
            self.str_patitentTitle.set(f"Paciente N°{self.patient.nro}")
            self.set_patient_description()
            self.nextButton["state"] = tk.NORMAL

    def get_patients(self):
        try:
            received_data = self.socket.recv(2048)
            msg = lmsg.deserialize(received_data)

            if msg == None:
                raise ConnectionResetError
            
            print("[Medic::Info] - Se recibio ", msg, " del servidor.")
            if msg.msg_type == lmsg.MessageType.PATIENT:
                self.patient = msg.patient
                self.event_generate("<<New Patient>>")
                self.event_generate("<<Inform Patient>>")
            elif msg.msg_type == lmsg.MessageType.COUNTER:
                self.str_counterLabel.set(f"Pacientes Pendientes: {msg.counter}")
                self.event_generate("<<New Patient>>")
                
        except ConnectionResetError:
            print("[Medic::Warning] - Se perdio la conexion con el sistema.")
            self.patient = None

    def wait_patient(self):
        while True:
            with self.call_patient:
                self.call_patient.wait()
            try:
                data: bytes = lmsg.Message(lmsg.MessageType.ASK).serialize()
                if self.socket.send(data) < len(data):
                    messagebox.showwarning(title="Error", message="No se pudo pedir paciente.")
                    print(
                        "[Medic::Error] - No se pudo pedir el paciente correctamente al sistema.",
                        file=sys.stderr,
                    )
                else:
                    self.get_patients()
            except ConnectionResetError:
                return

    def notify_patient(self, _event):
        data: bytes = lmsg.Message(lmsg.MessageType.GOT).serialize()
        if self.socket.send(data) < len(data):
            print(
                "[Medic::Error] - No se pudo confirmar el paciente correctamente al sistema.",
                file=sys.stderr,
            )

    def exit(self, _event):
        if self.socket != None:
            self.socket.shutdown(1)
            self.socket.close()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
