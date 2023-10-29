import sys
from threading import Thread
import socket as sock
from socket import socket
from queue import Queue
import libs.patient as lp
import libs.msg as lmsg

# import tkinter as tk

TURNOS_IP = "127.0.0.1"
TURNOS_PORT = 5000


class Server:
    def __init__(self):
        self.server_socket = socket()
        self.patient_queue = Queue()
        # Lista con todos los medicos para actualizar contador
        self.update_list = list()

        try:
            self.server_socket.bind((TURNOS_IP, TURNOS_PORT))
        except socket.error as err:
            print(f"[Server::Socket::Error] - {err}", file=sys.stderr)
            self.server_socket = None

        if self.server_socket is None:
            print("Cerrando el servidor...")
            return
            # self.str_patitentTitle.set("Error!")
            # self.patientDesc.insert(
        #     tk.END, "No se ha podido Inicializar el servidor..."
        # )
        else:
            self.server_socket.listen()

        #Thread(target=self.run_server, args=(), daemon=True).start()
        self.run_server()

        # self.bind("<Escape>", self.exit)
        # self.bind("<<New Patient>>", self.update_patient)
        # self.bind("<<Inform Patient>>", self.notify_patient)

    # Se acepta una conexion nueva y se pasa a ejecutar en un nuevo thread
    def run_server(self):
        while True:
            incoming_connection = self.server_socket.accept()
            Thread(target=self.login, args=(incoming_connection), daemon=True).start()

    # El login se encarga de categorizar cualquier conexion entrante y la lleva al flujo de ejecucion correspondiente
    def login(self, client_socket: sock.socket, client_address: sock.AddressInfo):
        while True:
            received_data = client_socket.recv(2048)
            msg = lmsg.deserialize(received_data)

            if msg == None:
                print(
                    "[Server::Warning] - Se perdio la conexion con "
                    + client_address
                    + " ."
                )
                client_socket.close()
                break

            if msg.msg_type == lmsg.MessageType.LOGIN:
                if msg.sender == lmsg.Role.MEDIC:
                    self.update_list.append(client_socket)
                    self.medic_conn(client_socket, client_address)
                else:
                    self.reception_conn(client_socket, client_address)
            else:
                print("[Server::Login::Warning] - Se recibio un MessageType invalido.")
                client_socket.close()
                break

    # Manejo de la conexion con usuarios medicos.
    def medic_conn(self, medic_socket: sock.socket, medic_address: sock.AddressInfo):
        while True:
            received_data = medic_socket.recv(2048)
            msg = lmsg.deserialize(received_data)

            if msg == None:
                print(
                    "[Server::Medic::Warning] - Se perdio la conexion con "
                    + medic_address
                    + " ."
                )
                self.update_list.remove(medic_socket)
                medic_socket.close()
                break

            if msg.msg_type == lmsg.MessageType.ASK:
                patient = self.patient_queue.get()
                medic_socket.send(
                    lmsg.Message(lmsg.MessageType.PATIENT, patient=patient).serialize()
                )
                self.patient_queue.task_done()

            received_data = medic_socket.recv(2048)
            msg = lmsg.deserialize(received_data)

            if msg == None:
                print(
                    "[Server::Medic::Warning] - Se perdio la conexion con "
                    + medic_address
                    + " ."
                )
                self.patient_queue.put(patient)
                self.update_list.remove(medic_socket)
                medic_socket.close()
                break

            if msg.msg_type == lmsg.MessageType.GOT:
                print("Paciente enviado exitosamente")
                patient = None
                Thread(target=self.medic_update, args=(), daemon=True).start()

            else:
                print("[Server::Login::Warning] - Se recibio un MessageType invalido.")
                self.patient_queue.put(patient)
                self.update_list.remove(medic_socket)
                medic_socket.close()
                break

    # Actualizacion de contador para los medicos, llamo a la funcion cada vez que alguien cambia la cola de pacientes
    # en vez de dejar un thread para ahorrar recursos.
    def medic_update(self):
        if self.update_queue.not_empty():
            data: bytes = lmsg.Message(
                lmsg.MessageType.COUNTER, counter=self.patient_queue.qsize()
            ).serialize()

            for medic in self.update_queue:
                if medic.send(data) < len(data):
                    print(
                        "[Server::Medic::Error] - No se pudo actualizar el conteo de pacientes.",
                        file=sys.stderr,
                    )

    # Manejo de la conexion con la/s recepcion/es, le responde con un mensaje si el paciente fue ingresado correctamente
    def reception_conn(
        self, recep_socket: sock.socket, recep_address: sock.AddressInfo
    ):
        while True:
            received_data = recep_socket.recv(2048)
            msg = lmsg.deserialize(received_data)

            if msg == None:
                print(
                    "[Server::Reception::Warning] - Se perdio la conexion con "
                    + recep_address
                    + " ."
                )
                recep_socket.close()
                break

            if msg.msg_type == lmsg.MessageType.PATIENT:
                data: bytes = lmsg.Message(lmsg.MessageType.GOT).serialize()
                try:
                    self.patient_queue.put()
                    recep_socket.send(data)
                    self.patient_queue.task_done()
                    if recep_socket.send(data) < len(data):
                        print(
                            "[Server::Reception::Error] - No se pudo confirmar el paciente correctamente al sistema.",
                            file=sys.stderr,
                        )
                except:
                    continue


if __name__ == "__main__":
    server = Server()
