import sys
from threading import Thread
import socket as sock
from socket import socket
from queue import SimpleQueue
import libs.msg as lmsg


TURNOS_IP = "127.0.0.1"
TURNOS_PORT = 5000


class Server:
    def __init__(self):
        self.server_socket = socket()
        self.patient_queue = SimpleQueue()
        # Lista con todos los medicos para actualizar contador
        self.medic_update_list = list()
        # Lista con todas las pantallas para actualizar los turnos
        self.waiting_room_update_list = list()
        try:
            self.server_socket.bind((TURNOS_IP, TURNOS_PORT))
        except sock.error as err:
            print(f"[Server::Socket::Error] - {err}", file=sys.stderr)
            self.server_socket = None

        if self.server_socket is None:
            print("Cerrando el servidor...")
            return
        else:
            self.server_socket.listen()
        # Thread(target=self.run_server, args=(), daemon=True).start()
        self.run_server()

    # Se acepta una conexion nueva y se pasa a ejecutar en un nuevo thread
    def run_server(self):
        while True:
            incoming_connection = self.server_socket.accept()
            Thread(target=self.login, args=(incoming_connection), daemon=True).start()

    # El login se encarga de categorizar cualquier conexion entrante y la lleva al flujo de ejecucion correspondiente
    def login(self, client_socket: sock.socket, client_address: sock.AddressInfo):
        try:
            while True:
                received_data = client_socket.recv(2048)
                msg = lmsg.deserialize(received_data)

                if msg == None:
                    raise ConnectionResetError

                if msg.msg_type == lmsg.MessageType.LOGIN:
                    if msg.sender == lmsg.Role.MEDIC:
                        print(
                            f"[Server::info] - Nueva conexion desde ",
                            client_address,
                            " , tipo: MEDICO",
                        )
                        self.medic_update_list.append(client_socket)
                        self.medic_conn(client_socket, client_address)
                    if msg.sender == lmsg.Role.RECEPTION:
                        print(
                            f"[Server::info] - Nueva conexion desde ",
                            client_address,
                            " , tipo: RECEPCION",
                        )
                        self.reception_conn(client_socket, client_address)
                    if msg.sender == lmsg.Role.WAITINGROOM:
                        print(
                            f"[Server::info] - Nueva conexion desde ",
                            client_address,
                            " , tipo: WAITING_ROOM",
                        )
                        self.waiting_room_update_list.append(client_socket)
                        self.waiting_room_conn(client_socket, client_address)
                else:
                    print(
                        "[Server::Login::Warning] - Se recibio un MessageType invalido."
                    )
                    raise ConnectionResetError
        except ConnectionResetError:
            print(
                "[Server::Warning] - Se perdio la conexion con ",
                client_address,
                " .",
            )
            client_socket.close()

    # Manejo de la conexion con usuarios medicos.
    def medic_conn(self, medic_socket: sock.socket, medic_address: sock.AddressInfo):
        try:
            while True:
                received_data = medic_socket.recv(2048)
                msg = lmsg.deserialize(received_data)

                if msg == None:
                    raise ConnectionResetError
                print(msg)
                try:
                    if msg.msg_type == lmsg.MessageType.ASK:
                        patient = self.patient_queue.get(block=True, timeout=None)
                        patient.room = str(msg.counter)
                        data: bytes = lmsg.Message(
                            msg_type=lmsg.MessageType.PATIENT, patient=patient
                        ).serialize()
                        if medic_socket.send(data) < len(data):
                            print(
                                "[Server::Error] - El paciente no puedo ser enviado.",
                                file=sys.stderr,
                            )
                            raise ConnectionAbortedError
                        for waiting_room in self.waiting_room_update_list:
                            waiting_room.send(data)
                    elif msg.msg_type == lmsg.MessageType.GOT:
                        print("[Server::info] - Paciente enviado exitosamente")
                        patient = None
                        Thread(target=self.medic_update, args=(), daemon=True).start()
                    else:
                        print("[Server::Warning] - Se recibio un MessageType invalido.")
                        raise ConnectionError
                except ConnectionAbortedError:
                    self.patient_queue.put(patient)

        except ConnectionResetError:
            print(
                "[Server::Medic::Warning] - Se perdio la conexion con ",
                medic_address,
                " .",
            )
            self.medic_update_list.remove(medic_socket)
            medic_socket.close()
        return

    # Actualizacion de contador para los medicos, llamo a la funcion cada vez que alguien cambia la cola de pacientes
    # en vez de dejar un thread para ahorrar recursos.
    def medic_update(self):
        if len(self.medic_update_list) > 0:
            data: bytes = lmsg.Message(
                lmsg.MessageType.COUNTER, counter=self.patient_queue.qsize()
            ).serialize()

            for medic in self.medic_update_list:
                if medic.send(data) < len(data):
                    print(
                        "[Server::Medic::Error] - No se pudo actualizar el conteo de pacientes.",
                        file=sys.stderr,
                    )
        return

    # Manejo de la conexion con la/s recepcion/es, le responde con un mensaje si el paciente fue ingresado correctamente
    def reception_conn(
        self, recep_socket: sock.socket, recep_address: sock.AddressInfo
    ):
        try:
            while True:
                received_data = recep_socket.recv(2048)
                msg = lmsg.deserialize(received_data)
                print("[Server::info] - Recived ", msg, " from ", recep_address)
                if msg == None:
                    raise ConnectionResetError

                if msg.msg_type == lmsg.MessageType.PATIENT:
                    data: bytes = lmsg.Message(
                        msg_type=lmsg.MessageType.GOT
                    ).serialize()
                    try:
                        self.patient_queue.put(msg.patient)
                        if recep_socket.send(data) < len(data):
                            print(
                                "[Server::Reception::Error] - No se pudo confirmar el paciente correctamente al sistema.",
                                file=sys.stderr,
                            )
                        Thread(target=self.medic_update, args=(), daemon=True).start()
                    except:
                        continue
        except ConnectionResetError:
            print(
                "[Server::Reception::Warning] - Se perdio la conexion con ",
                recep_address,
                " .",
            )
            recep_socket.close()

    # Manejo de la conexion con la/s sala/s de espera. Al romperse el enlace se saca la recepción de la lista.
    def waiting_room_conn(
        self, waiting_room_socket: sock.socket, waiting_room_address: sock.AddressInfo
    ):
        try:
            while True:
                data = waiting_room_socket.recv(1)
                if not data:
                    self.close_waiting_room_socket(
                        waiting_room_address, waiting_room_socket
                    )
                    return
        except ConnectionResetError:
            self.close_waiting_room_socket(waiting_room_address, waiting_room_socket)

    def close_waiting_room_socket(self, waiting_room_address, waiting_room_socket):
        print(
            "[Server::Reception::Warning] - Se perdio la conexion con ",
            waiting_room_address,
            " . Se quitará de la lista de salas de espera.",
        )
        self.waiting_room_update_list.remove(waiting_room_socket)
        waiting_room_socket.close()

    def waiting_room_update(self):
        if len(self.waiting_room_update_list) > 0:
            data: bytes = lmsg.Message(
                lmsg.MessageType.COUNTER, counter=self.patient_queue.qsize()
            ).serialize()

            for medic in self.medic_update_list:
                if medic.send(data) < len(data):
                    print(
                        "[Server::Medic::Error] - No se pudo actualizar el conteo de pacientes.",
                        file=sys.stderr,
                    )
        return


if __name__ == "__main__":
    server = Server()
