import pickle


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

    def __str__(self):
        return f"{self.name} {self.surname} - {self.dni}"

    def serialize(self, fifo):
        pickle.dump(self, fifo)


def serialize(fifo, patient):
    pickle.dump(patient, fifo)


def deserialize(fifo) -> Patient:
    return pickle.load(fifo)
