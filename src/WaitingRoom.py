import os
import tkinter as tk

def recv_msg():
    global window, listbox
    fifo = "internal_msg"
    with open(fifo, "r") as fifo:
        datos = fifo.read()
        listbox.insert(tk.END,datos)
    window.after(1000,recv_msg)
    window.update()

def send_msg(mensaje):
    fifo = "internal_msg"
    with open(fifo, "w") as fifo:
        fifo.write(mensaje)

def process_interface():
    global window, listbox
    window = tk.Tk()
    window.title("Sala de espera")
    window.configure(bg="#457B9D")
    window.attributes('-zoomed', True)

    frame = tk.Frame(window, background="#457B9D")
    frame.pack()

    title = Label(text=" TURNO\t\t\t CONSULTORIO")
    title.config(fg="#1D3557",bg="#A8DADC",width=45,height=1,font=("Helvetica",50,"bold"),anchor=W) 
    title.pack(anchor=CENTER,pady=20,ipady=20)
    

    listbox = tk.Listbox(window,width=45, height=10,font=("Helvetica", 50,"bold"))
    listbox.config(bg="#1D3557")
    listbox.pack(anchor=CENTER)
    
    window.after(1000,recv_msg)
    window.mainloop()

def process_logic():
    while True:
        msg = input("Escribe un mensaje (o 'q' para salir): ")
        if msg.lower() == 'q':
            send_msg('q')  # Enviar un mensaje de salida
            break
        send_msg(msg)

def main():
    fifo = "internal_msg"
    if not os.path.exists(fifo):
        os.mkfifo(fifo)
    pidL=os.fork()
    if pidL==-1:
        print("ERROR")
        exit -1
    if pidL == 0:
        process_logic()
    pidI = os.fork()
    if pidI==-1:
        print("ERROR")
        exit -1
    if pidI == 0:  # Proceso hijo para la interfaz gráfica
        process_interface()
    
    os.wait()  # Esperar a que el proceso hijo termine
    os.wait()  # Esperar a que el proceso hijo termine


if __name__ == "__main__":
    main()