import libs.fifo as lf
import libs.patient as lp

lf.make_fifo()
fifo = lf.open_fifo("wb")
patient = lp.Patient(
    "Benito", "Camela", "78.456.321", 99, "B", "Le duele", 1230
).serialize(fifo)

fifo.close()
lf.remove_fifo()
