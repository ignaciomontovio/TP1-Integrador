import pickle, sys
from enum import Enum
import libs.patient as lp


class MessageType(Enum):
    PATIENT = 1
    COUNTER = 2
    ASK = 3
    GOT = 4


class Message:
    def __init__(
        self, msg_type: MessageType, patient: lp.Patient = None, counter: int = 0
    ):
        self.msg_type = msg_type
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
