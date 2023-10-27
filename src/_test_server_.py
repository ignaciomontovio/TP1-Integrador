import socket as soc
from socket import socket
from queue import Queue
import libs.patient as lp
import libs.msg as msg

TURNOS_IP = "127.0.0.1"
TURNOS_PORT = 5000

q = Queue()
ss = socket()
ss.bind((TURNOS_IP, TURNOS_PORT))


# ...recibe los pacientes por atender y los guarda
q.put(lp.Patient("Benito", "Camela", "78.456.321", 99, "B", "Le duele", 1230))
q.put(lp.Patient("Armando", "Barreras", "87.456.321", 99, "B", "Le duele algo", 1231))
q.put(lp.Patient("Esteban", "Quito", "58.456.321", 99, "B", "No le duele", 1232))


# ...en otro hilo aceptamos medicos
ss.listen(7)
(ms, mdir) = ss.accept()

# Enviamos al medico la cantidad de pacientes
ms.send(msg.Message(msg.MessageType.COUNTER, counter=q.qsize()).serialize())


# ...en otro hilo dedicado al medico esperamos a que nos pida pacientes
while not q.empty():
    rc = ms.recv(2048)
    mg = msg.deserialize(rc)

    if mg.msg_type == msg.MessageType.ASK:
        p = q.get()
        ms.send(msg.Message(msg.MessageType.PATIENT, patient=p).serialize())
        q.task_done()

    rc = ms.recv(2048)
    mg = msg.deserialize(rc)
    if mg.msg_type == msg.MessageType.GOT:
        print("Paciente fue pasado exitosamente")
        p = None  # Limpiamos...
        ms.send(msg.Message(msg.MessageType.COUNTER, counter=q.qsize()).serialize())


ss.close()
ms.close()
