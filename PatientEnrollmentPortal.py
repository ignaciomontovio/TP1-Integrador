import tkinter
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import pickle


class Patient:
  nombre = ""
  apellido = ""
  dni = 0
  genero = ""
  edad = 0
  sintomas = ""

  def __init__(self, nombre, apellido, dni, genero, edad, sintomas):
    self.nombre = nombre
    self.apellido = apellido
    self.dni = dni
    self.genero = genero
    self.edad = edad
    self.sintomas = sintomas

def enter_data():
  # User info
  firstname = first_name_entry.get()
  lastname = last_name_entry.get()

  if firstname and lastname:
    patient = Patient(first_name_entry.get(), last_name_entry.get(),
                      dni_entry.get(), gender_combobox.get(), age_spinbox.get(),
                      symptoms_entry.get())
    patientSerialized = pickle.dumps(patient)
    """
    try:
      os.mkfifo("./fifo", 0o600)

    except OSError as err:
      print(f"Error al crear fifo {err}")
      sys.exit(1)

    fifo = os.open("./fifo", os.O_WRONLY)

    os.write(fifo, patientSerialized)
    """
  else:
    tkinter.messagebox.showwarning(title="Error",
                                   message="First name and last name are required.")


window = tkinter.Tk()
window.title("Alta de paciente")
window.configure(bg="#457B9D")
frame = tkinter.Frame(window, background="#457B9D")
frame.pack()
# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text="Informacion de paciente",
                                     background="#457B9D")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)
user_info_frame.configure()

first_name_label = tkinter.Label(user_info_frame, text="Nombre",
                                 background="#457B9D")
first_name_label.grid(row=0, column=0)

first_name_entry = tkinter.Entry(user_info_frame, background="#F1FAEE")
first_name_entry.grid(row=1, column=0)

last_name_label = tkinter.Label(user_info_frame, text="Apellido",
                                background="#457B9D")
last_name_label.grid(row=0, column=1)

last_name_entry = tkinter.Entry(user_info_frame, background="#F1FAEE")
last_name_entry.grid(row=1, column=1)

combostyle = ttk.Style()

combostyle.theme_create('combostyle', parent='alt',
                        settings={'TCombobox':
                          {'configure':
                            {
                              'fieldbackground': '#F1FAEE',
                              'background': '#F1FAEE'
                            }}}
                        )
# ATTENTION: this applies the new style 'combostyle' to all ttk.Combobox
combostyle.theme_use('combostyle')


gender_label = tkinter.Label(user_info_frame, text="Genero",
                             background="#457B9D")
gender_combobox = ttk.Combobox(user_info_frame, values=["", "M", "F", "X"], )
gender_label.grid(row=0, column=2)
gender_combobox.grid(row=1, column=2)

age_label = tkinter.Label(user_info_frame, text="Edad", background="#457B9D")
age_spinbox = tkinter.Spinbox(user_info_frame, from_=0, to=110,
                              background="#F1FAEE")
age_label.grid(row=2, column=0)
age_spinbox.grid(row=3, column=0)

dni_label = tkinter.Label(user_info_frame, text="DNI", background="#457B9D")
dni_entry = tkinter.Entry(user_info_frame, background="#F1FAEE")
dni_label.grid(row=2, column=1)
dni_entry.grid(row=3, column=1)

description_frame = tkinter.LabelFrame(frame, background="#457B9D")
description_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

symptoms_label = tkinter.Label(description_frame, text="Sintomas",
                               background="#457B9D")
symptoms_entry = tkinter.Entry(description_frame, width=67,
                               background="#F1FAEE")
symptoms_label.grid(row=4, column=1)
symptoms_entry.grid(row=5, column=1)

# Button
button = tkinter.Button(frame, text="Ingresar Paciente", command=enter_data,
                        background="#A8DADC")
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
