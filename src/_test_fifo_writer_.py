import libs.fifo as lf
import libs.patient as lp

lf.make_fifo()
fifo = lf.open_fifo("wb")

patient = lp.Patient(
    "Benito", "Camela", "78.456.321", 99, "B", "Le duele", 1230
).serialize(fifo)

patient = lp.Patient(
    "Armando", "Barreras", "87.456.321", 99, "B", "Le duele algo", 1231
).serialize(fifo)


patient = lp.Patient(
    "Esteban", "Quito", "58.456.321", 99, "B", "No le duele", 1232
).serialize(fifo)

nro = 1232
while True:
    name = input("Ingrese el nombre del paciente: ")
    if name == "kill":
        break

    nro += 1
    patient = lp.Patient(
        name, "Quito", "58.456.321", 99, "B", "No le duele", nro
    ).serialize(fifo)

fifo.close()
lf.remove_fifo()
