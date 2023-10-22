import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import libs.fifo as lf
import libs.patient as lp

class PatientEntryApp:
  def __init__(self, root):
    self.root = root
    root.title("Alta de paciente")
    root.configure(bg="#457B9D")

    # Creación de FIFO
    lf.make_fifo()
    self.fifo = lf.open_fifo("wb")

    self.create_widgets()

  def create_widgets(self):
    frame = tk.Frame(self.root, background="#457B9D")
    frame.pack()

    user_info_frame = tk.LabelFrame(frame, text="Información del paciente", background="#457B9D")
    user_info_frame.grid(row=0, column=0, padx=20, pady=10)

    self.first_name_label = tk.Label(user_info_frame, text="Nombre", background="#457B9D")
    self.first_name_label.grid(row=0, column=0)
    self.first_name_entry = tk.Entry(user_info_frame, background="#F1FAEE")
    self.first_name_entry.grid(row=1, column=0)

    self.last_name_label = tk.Label(user_info_frame, text="Apellido", background="#457B9D")
    self.last_name_label.grid(row=0, column=1)
    self.last_name_entry = tk.Entry(user_info_frame, background="#F1FAEE")
    self.last_name_entry.grid(row=1, column=1)

    self.combostyle = ttk.Style()
    self.combostyle.theme_create('combostyle', parent='alt', settings={'TCombobox':
                                                                         {'configure': {'fieldbackground': '#F1FAEE', 'background': '#F1FAEE'}}})
    self.combostyle.theme_use('combostyle')

    self.sex_label = tk.Label(user_info_frame, text="Género", background="#457B9D")
    self.sex_combobox = ttk.Combobox(user_info_frame, values=["", "M", "F", "X"])
    self.sex_label.grid(row=0, column=2)
    self.sex_combobox.grid(row=1, column=2)

    self.age_label = tk.Label(user_info_frame, text="Edad", background="#457B9D")
    self.age_spinbox = tk.Spinbox(user_info_frame, from_=0, to=110, background="#F1FAEE")
    self.age_label.grid(row=2, column=0)
    self.age_spinbox.grid(row=3, column=0)

    self.dni_label = tk.Label(user_info_frame, text="DNI", background="#457B9D")
    self.dni_entry = tk.Entry(user_info_frame, background="#F1FAEE")
    self.dni_label.grid(row=2, column=1)
    self.dni_entry.grid(row=3, column=1)

    description_frame = tk.LabelFrame(frame, background="#457B9D")
    description_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    self.symptoms_label = tk.Label(description_frame, text="Síntomas", background="#457B9D")
    self.symptoms_entry = tk.Entry(description_frame, width=67, background="#F1FAEE")
    self.symptoms_label.grid(row=4, column=1)
    self.symptoms_entry.grid(row=5, column=1)

    button_send = tk.Button(frame, text="Ingresar Paciente", command=self.enter_data, background="#90BE6D")
    button_send.grid(row=3, column=0, sticky="news", padx=20, pady=10)

    button_exit = tk.Button(frame, text="Finalizar sesión", command=self.finish_session, background="#E63946")
    button_exit.grid(row=4, column=0, sticky="news", padx=20, pady=10)

  def finish_session(self):
    lf.remove_fifo()
    self.root.quit()
    os._exit(0)

  def show_message(self):
    messagebox.showinfo(title="Aceptado", message="Paciente agregado correctamente a la cola.")

  def enter_data(self):
    firstname = self.first_name_entry.get()
    lastname = self.last_name_entry.get()

    if firstname and lastname:
      patient = lp.Patient(nro=1, name=firstname, surname=lastname, dni=self.dni_entry.get(),
                           age=self.age_spinbox.get(), sex=self.sex_combobox.get(),
                           symptoms=self.symptoms_entry.get())
      threading.Thread(target=self.show_message).start()
      os.write(self.fifo, patient.serialize(self.fifo))
    else:
      messagebox.showwarning(title="Error", message="Se requieren nombre y apellido.")

if __name__ == "__main__":
  root = tk.Tk()
  app = PatientEntryApp(root)
  root.mainloop()
