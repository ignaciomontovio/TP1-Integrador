import libs.fifo as lf
import libs.patient as lp

fifo = lf.open_fifo("rb")

patient = lp.deserialize(fifo)
print("Patient read: ")
print(patient)

fifo.close()
