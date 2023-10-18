import tkinter
from tkinter import ttk
from tkinter import messagebox
import sys
import os


def enter_data():

  patient = Patient(first_name_entry.get(), last_name_entry.get(), dni_entry.get())

  # User info
  firstname = first_name_entry.get()
  lastname = last_name_entry.get()

  if firstname and lastname:
    title = title_combobox.get()
    age = age_spinbox.get()
    dni = dni_entry.get()

    print("First name: ", firstname, "Last name: ", lastname)
    print("Title: ", title, "Edad: ", age, "DNI: ", dni)
    print("------------------------------------------")
  else:
    tkinter.messagebox.showwarning(title="Error",
                                   message="First name and last name are required.")


window = tkinter.Tk()
window.title("Alta de paciente")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text="Informacion de paciente")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(user_info_frame, text="Nombre")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Apellido")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

title_label = tkinter.Label(user_info_frame, text="Genero")
title_combobox = ttk.Combobox(user_info_frame, values=["", "M", "F", "X"])
title_label.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)

age_label = tkinter.Label(user_info_frame, text="Edad")
age_spinbox = tkinter.Spinbox(user_info_frame, from_=18, to=110)
age_label.grid(row=2, column=0)
age_spinbox.grid(row=3, column=0)

dni_label = tkinter.Label(user_info_frame, text="DNI")
dni_entry = tkinter.Entry(user_info_frame)
dni_label.grid(row=2, column=1)
dni_entry.grid(row=3, column=1)

description_frame = tkinter.LabelFrame(frame)
description_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

symptoms_label = tkinter.Label(description_frame, text="Sintomas")
symptoms_entry = tkinter.Entry(description_frame, width=67)
symptoms_label.grid(row=4, column=1)
symptoms_entry.grid(row=5, column=1)

"""
for widget in user_info_frame.winfo_children():
  widget.grid_configure(padx=10, pady=5)

# Saving Course Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

registered_label = tkinter.Label(courses_frame, text="Registration Status")

reg_status_var = tkinter.StringVar(value="Not Registered")
registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered",
                                       variable=reg_status_var, onvalue="Registered", offvalue="Not registered")

registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)

numcourses_label = tkinter.Label(courses_frame, text= "# Completed Courses")
numcourses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
numcourses_label.grid(row=0, column=1)
numcourses_spinbox.grid(row=1, column=1)

numsemesters_label = tkinter.Label(courses_frame, text="# Semesters")
numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=0, to="infinity")
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox.grid(row=1, column=2)

for widget in courses_frame.winfo_children():
  widget.grid_configure(padx=10, pady=5)

# Accept terms
terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text= "I accept the terms and conditions.",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)
"""
# Button
button = tkinter.Button(frame, text="Ingresar Paciente", command=enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()


class Patient:
  nombre = ""
  apellido = ""
  dni = 0

  def __init__(self, nombre, apellido, dni):
    self.nombre = nombre
    self.apellido = apellido
    self.dni = dni

  def encode(self, param):
    pass
