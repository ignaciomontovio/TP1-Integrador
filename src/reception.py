import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import libs.fifo as lf
import libs.patient as lp
from libs.theme import Theme


class PatientEntryApp:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    def __init__(self, root):
        self.root = root
        self.root.title("Alta de paciente")
        self.root.geometry(f"{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}")
        self.root.resizable(0, 0)

        self.queue = queue.Queue()
        self.th = threading.Thread(target=self.write_data, args=(), daemon=True)
        self.th.start()

        self.create_widgets()

    def create_widgets(self):
        Theme.style(self.root)
        font = ("TkDefaultFont", 12)

        frame = ttk.Frame(self.root, style="Light.TFrame")
        frame.pack(fill="both", expand=True)

        user_info_frame = ttk.LabelFrame(frame, text="Información del paciente")
        user_info_frame.pack(fill="both", expand=True, side=tk.LEFT, padx=5, pady=5)

        self.first_name_label = ttk.Label(user_info_frame, text="Nombre")
        self.first_name_label.pack(fill="x", padx=5, pady=5)

        self.first_name_entry = ttk.Entry(user_info_frame, font=font)
        self.first_name_entry.pack(fill="x", padx=5, pady=5)

        self.last_name_label = ttk.Label(user_info_frame, text="Apellido")
        self.last_name_label.pack(fill="x", padx=5, pady=5)

        self.last_name_entry = ttk.Entry(user_info_frame, font=font)
        self.last_name_entry.pack(fill="x", padx=5, pady=5)

        self.sex_label = ttk.Label(user_info_frame, text="Género")
        self.sex_label.pack(fill="x", padx=5, pady=5)

        self.sex_combobox = ttk.Combobox(
            user_info_frame, values=["", "M", "F", "X"], font=font
        )
        self.sex_combobox.pack(fill="x", padx=5, pady=5)

        self.age_label = ttk.Label(user_info_frame, text="Edad", font=font)
        self.age_label.pack(fill="x", padx=5, pady=5)

        self.age_spinbox = ttk.Spinbox(user_info_frame, from_=0, to=110, font=font)
        self.age_spinbox.pack(fill="x", padx=5, pady=5)

        self.dni_label = ttk.Label(user_info_frame, text="DNI")
        self.dni_label.pack(fill="x", padx=5, pady=5)

        self.dni_entry = ttk.Entry(user_info_frame, font=font)
        self.dni_entry.pack(fill="x", padx=5, pady=5)

        description_frame = ttk.LabelFrame(frame, text="Síntomas")
        description_frame.pack(fill="both", expand=True, side=tk.TOP, padx=5, pady=5)

        self.symptoms_entry = tk.Text(
            description_frame,
            background=Theme.BG,
            selectbackground=Theme.TEXT_SELECTED_BG,
            foreground=Theme.FG,
            selectforeground=Theme.BG,
            insertbackground=Theme.RED,
            wrap="word",
            spacing2=3,
            height=10,
            font=font,
        )
        self.symptoms_entry.pack(fill="both", expand=True, pady=5, padx=5)

        button_send = ttk.Button(
            frame,
            text="Ingresar Paciente",
            command=self.enter_data,
            style="Sub.TButton",
        )
        button_send.pack(fill="both", expand=True, pady=5, padx=5)

        button_exit = ttk.Button(
            frame, text="Finalizar sesión", command=self.finish_session
        )
        button_exit.pack(fill="both", expand=True, pady=5, padx=5)

    def finish_session(self):
        self.queue.put(None)
        lf.remove_fifo()
        self.root.destroy()

    def show_message(self):
        messagebox.showinfo(
            title="Aceptado", message="Paciente agregado correctamente a la cola."
        )

    def enter_data(self):
        firstname = self.first_name_entry.get()
        lastname = self.last_name_entry.get()

        if firstname and lastname:
            patient = lp.Patient(
                nro=1,
                name=firstname,
                surname=lastname,
                dni=self.dni_entry.get(),
                age=self.age_spinbox.get(),
                sex=self.sex_combobox.get(),
                symptoms=self.symptoms_entry.get("1.0", "end"),
            )
            self.queue.put(patient)
        else:
            messagebox.showwarning(
                title="Error", message="Se requieren nombre y apellido."
            )

    def write_data(self):
        lf.make_fifo()
        fifo = lf.open_fifo("wb")

        while True:
            patient = self.queue.get()
            if patient == None:
                break

            patient.serialize(fifo)
            self.queue.task_done()


if __name__ == "__main__":
    root = tk.Tk()
    app = PatientEntryApp(root)
    root.mainloop()
