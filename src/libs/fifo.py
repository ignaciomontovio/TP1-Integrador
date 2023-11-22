import os, sys

FIFO_FILENAME = "./turnos.fifo"

def make_fifo(filename=FIFO_FILENAME, mode=0o600):
    try:
        if not os.path.exists(filename):
            os.mkfifo(FIFO_FILENAME, mode)
    except OSError as err:
        print(f"[Fifo::Error] - {err}", file=sys.stderr)
        print(f"<<-- Ocurrio un error, terminando proceso... -->>")
        sys.exit(1)

def open_fifo(mode, filename=FIFO_FILENAME):
    try:
        fifo = open(filename, mode, buffering=0)
    except IOError as err:
        print(f"[Fifo::Error] - {err}", file=sys.stderr)
        fifo = None

    return fifo

def remove_fifo(filename=FIFO_FILENAME):
    os.unlink(filename)

def delete_fifo(filename=FIFO_FILENAME):
    if os.path.exists(filename):
        os.remove(filename)
