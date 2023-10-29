import multiprocessing
import time
import tkinter as tk
from tkinter import Frame, ttk, messagebox
import threading
import os
import libs.fifo as lf
import libs.patient as lp

lista_strings = ["123","123123"]

class WaitingRoom:
    def __init__(self, root):
        self.root = root
        root.title("Sala de espera")
        root.configure(bg="#457B9D")
        self.create_widgets()

    def create_widgets(self):
        self.root.attributes('-zoomed', True)
        self.frame = Frame(self.root)
        self.frame.pack()
        self.state = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)
        frame = tk.Frame(self.root, background="#457B9D")
        frame.pack()
        listbox = tk.Listbox(self.root,width=45, height=10,font=("Helvetica", 50,"bold"))
        listbox.place(x=10,y=10)
        listbox.pack()
        for item in lista_strings:
            listbox.insert(tk.END, item)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state 
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
    
def launch_graphic():
    root = tk.Tk()
    app = WaitingRoom(root)
    root.mainloop()

def waiting_msg():
    while True:
        thread_logic=threading.Thread(target=process_msg())
        thread_logic.daemon=True
        thread_logic.start()
        time.sleep(10)

def process_msg():
    print("procesando msg")

def main():
    process_graphic=os.fork()
    if(process_graphic==-1):
        print("Error")
        return -1
    send, recive = multiprocessing.Pipe()
    if(process_graphic==0):
        launch_graphic()
    else:
        waiting_msg()

if __name__ == "__main__":
    main()
 
