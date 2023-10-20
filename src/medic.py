import tkinter as tk
from tkinter import ttk
import libs.fifo as lf
import libs.patient as lp


class Theme:
    BG = "#F1FAEE"
    FG = "#1D3557"
    RED = "#E63946"
    BORDER_BG = "#1D3557"
    BORDER_BG_N = "#E63946"
    BORDER_BG_A = "#457B9D"
    BORDER_BG_P = "#1D3557"
    TEXT_SELECTED_BG = "#457B9D"


class App(tk.Tk):
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    BORDER_WIDTH = 20
    APP_NAME = "Medico"
    FONT_NAME = "TkDefaultFont"

    def __init__(self):
        super().__init__()

        self.fifo = lf.open_fifo("rb")
        self.patient = lp.Patient()
        self.str_patitentTitle = tk.StringVar(value="Paciente N°XYZ")

        self.draw()
        self.set_patient_description()

        self.bind("<Escape>", lambda e: self.destroy())

    def draw(self):
        self.geometry(f"{App.SCREEN_WIDTH}x{App.SCREEN_HEIGHT}")
        self.resizable(0, 0)
        self.title(App.APP_NAME)

        self.style = ttk.Style(self)
        self.style.configure("Main.TFrame", background=Theme.BORDER_BG)
        self.style.configure("Sub.TFrame", background=Theme.BG)
        self.style.configure(
            "TButton",
            font=(App.FONT_NAME, 14),
            background=Theme.BORDER_BG_N,
            foreground=Theme.BG,
        )
        self.style.map(
            "TButton",
            background=[("pressed", Theme.BORDER_BG_P), ("active", Theme.BORDER_BG_A)],
        )

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

        patientTitle = ttk.Label(
            subFrame,
            textvariable=self.str_patitentTitle,
            background=Theme.BG,
            foreground=Theme.RED,
            font=(App.FONT_NAME, 24, "bold"),
        )
        patientTitle.pack(anchor="nw", padx=10, pady=10)

        scrollbar = ttk.Scrollbar(subFrame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

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
            height=22,
            spacing2=3,
        )
        self.patientDesc.pack(fill="y", anchor="nw", padx=15, pady=5)
        self.patientDesc.tag_configure("bold", font=(App.FONT_NAME, 14, "bold"))
        self.patientDesc.tag_configure("italic", font=(App.FONT_NAME, 14, "italic"))

        scrollbar.config(command=self.patientDesc.yview)

        nextButton = ttk.Button(
            subFrame, text="Siguiente Turno", command=self.update_patient
        )
        nextButton.pack(
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

    def update_patient(self):
        self.patient = lp.deserialize(self.fifo)
        self.str_patitentTitle.set(f"Paciente N°{self.patient.nro}")
        self.patientDesc.delete("1.0", tk.END)
        self.set_patient_description()


if __name__ == "__main__":
    app = App()
    app.mainloop()
