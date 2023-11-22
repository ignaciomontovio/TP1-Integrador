## Patient Lib
Datos de la clase **Paciente**:
- nro: int
- name: str
- surname: str
- dni: str
- age: int
- sex: str
- symptoms: str

> Puede serializarse y deserializarse atraves de la libreria [_pickle_](https://docs.python.org/3/library/pickle.html).

## Fifo Lib

> Por default y para que se mantenga concistencia entre los procesos el nombre del fifo es **'turnos.fifo'**.

### Writer example

```python
import libs.fifo as lf
import libs.patient as lp

lf.make_fifo()
fifo = lf.open_fifo("wb")
patient = lp.Patient("Benito", "Camela", "78.456.321", 99, "B", "Le duele", 1230).serialize(fifo)

fifo.close()
lf.remove_fifo()
```

### Reader example

```python
import libs.fifo as lf
import libs.patient as lp

fifo = lf.open_fifo("rb")

patient = lp.deserialize(fifo)
print("Patient read: ")
print(patient)

fifo.close()
```

## Bibliografia:
- [**Fifo - Named pipes**](https://es.wikipedia.org/wiki/Tuber%C3%ADa_(inform%C3%A1tica))
- [**Pickle - A python lib**](https://docs.python.org/3/library/pickle.html).
