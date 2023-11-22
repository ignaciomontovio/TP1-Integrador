import pickle, sys


class Patient:
    def __init__(
        self,
        name="None",
        surname="None",
        dni="00.000.000",
        age=-1,
        sex="N",
        symptoms="...",
        nro=0,
    ):
        self.nro: int = nro
        self.age: int = age
        self.dni: str = dni
        self.sex: str = sex
        self.name: str = name
        self.surname: str = surname
        self.symptoms: str = symptoms
        self.room: str = ""

    def __str__(self):
        return f"{self.name} {self.surname} - {self.dni}"

    def serialize(self, fifo):
        pickle.dump(self, fifo)

    def serialize(self) -> bytes:
        return pickle.dumps(self)


def serialize(fifo, patient):
    pickle.dump(patient, fifo)


def serialize(patient) -> bytes:
    return pickle.dumps(patient)


def deserialize(fifo) -> Patient:
    try:
        patient = pickle.load(fifo)
    except EOFError as err:
        print(f"[Patient::Error] - {err}", file=sys.stderr)
        patient = None

    return patient


def deserialize(raw_bytes: bytes) -> Patient:
    try:
        patient = pickle.loads(raw_bytes)
    except EOFError as err:
        print(f"[Patient::Error] - {err}", file=sys.stderr)
        patient = None

    return patient
