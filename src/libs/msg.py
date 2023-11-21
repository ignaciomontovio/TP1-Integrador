import pickle, sys
from enum import Enum
import libs.patient as lp


class MessageType(Enum):
    PATIENT = 1
    """ Envia un paciente """
    COUNTER = 2
    """ Pide la cantidad de pacientes pendientes """
    ASK = 3
    """ Pide el proximo paciente """
    GOT = 4
    """ Informa que recibio el paciente """
    LOGIN = 5
    """ Pide conectarse al Servidor """


class Role(Enum):
    MEDIC = 1
    RECEPTION = 2
    WAITINGROOM = 3


class Message:
    def __init__(
        self,
        msg_type: MessageType,
        sender: Role = None,
        patient: lp.Patient = None,
        counter: int = 0,
    ):
        self.msg_type = msg_type
        self.sender = sender
        self.patient = patient
        self.counter = counter

    def __str__(self):
        return f"{self.msg_type.name} - {self.patient} - {self.counter}"

    def serialize(self) -> bytes:
        return pickle.dumps(self)


def deserialize(raw_bytes: bytes) -> Message:
    try:
        msg = pickle.loads(raw_bytes)
    except EOFError as err:
        print(f"[Msg::Error] - {err}", file=sys.stderr)
        msg = None

    return msg
