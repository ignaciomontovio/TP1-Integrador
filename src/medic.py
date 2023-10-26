import sys
import socket as soc
from socket import socket
from threading import Thread, Condition
import tkinter as tk
from tkinter import ttk
import libs.msg as lmsg
from libs.theme import Theme

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

        self.cs = socket()
        self.call_patient = Condition()

        try:
            self.cs.connect((TURNOS_IP, TURNOS_PORT))
        except soc.error as err:
            print(f"[Medic::Error] - {err}", file=sys.stderr)
            self.cs = None

        self.str_patitentTitle = tk.StringVar()
        self.str_counterLabel = tk.StringVar(value="Pacientes Pendientes: 0")
        self.draw()

        if self.cs is None:
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

            Thread(target=self.get_patients, args=(), daemon=True).start()
            Thread(target=self.wait_patient, args=(), daemon=True).start()

        self.bind("<Escape>", self.exit)
        self.bind("<<New Patient>>", self.update_patient)
        self.bind("<<Inform Patient>>", self.notify_patient)

    def draw(self):
        self.geometry(f"{App.SCREEN_WIDTH}x{App.SCREEN_HEIGHT}")
        self.resizable(0, 0)
        self.title(App.APP_NAME)

        Theme.style(self, self.FONT_NAME)

        mainFrame = ttk.Frame(
            self, width=App.SCREEN_WIDTH, height=App.SCREEN_HEIGHT, style="Main.TFrame"
        )
        mainFrame.pack(fill="both", expand=True)

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
                tk.END, "No se ha podido comunicar con la recepción..."
            )
            self.nextButton["state"] = tk.DISABLED
            self.patientDesc["state"] = tk.DISABLED
        else:
            self.str_patitentTitle.set(f"Paciente N°{self.patient.nro}")
            self.set_patient_description()
            self.nextButton["state"] = tk.NORMAL
            self.event_generate("<<Inform Patient>>")

    def get_patients(self):
        while True:
            rc = self.cs.recv(2048)
            msg = lmsg.deserialize(rc)

            if msg == None:
                print("[Medic::Warning] - Se perdio la conexion con el sistema.")
                break

            if msg.msg_type == lmsg.MessageType.PATIENT:
                self.patient = msg.patient
                self.event_generate("<<New Patient>>")
            elif msg.msg_type == lmsg.MessageType.COUNTER:
                self.str_counterLabel.set(f"Pacientes Pendientes: {msg.counter}")
            else:
                print("[Medic::Warning] - Se recibio un MessageType invalido.")

    def wait_patient(self):
        while True:
            with self.call_patient:
                self.call_patient.wait()
                data: bytes = lmsg.Message(lmsg.MessageType.ASK).serialize()
                if self.cs.send(data) < len(data):
                    print(
                        "[Medic::Error] - No se pudo pedir el paciente correctamente al sistema.",
                        file=sys.stderr,
                    )

    def notify_patient(self, _event):
        data: bytes = lmsg.Message(lmsg.MessageType.GOT).serialize()
        if self.cs.send(data) < len(data):
            print(
                "[Medic::Error] - No se pudo confirmar el paciente correctamente al sistema.",
                file=sys.stderr,
            )

    def exit(self, _event):
        if self.cs != None:
            self.cs.close()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
