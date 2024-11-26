import tkinter
from tkinter import scrolledtext
from portscanner import scan_ports
import threading
import queue 



finestra = tkinter.Tk()
finestra.title("Port Scanner")
finestra.geometry("400x600")
finestra.configure(bg="#e7cf8a")

frame = tkinter.Frame(bg="#e7cf8a") #Container

##################################################

#Script


def scansiona(): #Bottone
    target_host = inserisci_Host.get()

    port1 = inserisci_portainizio.get()
    inizio_port = int(port1)

    port2 = inserisci_portafine.get()
    fine_port = int(port2)

    result_queue = queue.Queue()

    scan_ports(target_host, inizio_port, fine_port, result_queue)

    result_text.delete(1.0, tkinter.END)
    result_text.insert(tkinter.END, f"Porte aperte su {target_host}\n")

    while not result_queue.empty():
        port = result_queue.get()
        result_text.insert(tkinter.END, f"Porta {port} aperta\n")



    
scan_thread = threading.Thread(target=scansiona)
scan_thread.start()
    


##################################################

#Creazione degli widget
spazio_titolo = tkinter.Label(frame, text="Port Scanner", bg="#e7cf8a", font=("Arial", 25, "bold"))
spazio_Host = tkinter.Label(frame, text="Host IP ", bg="#e7cf8a", font=("Arial", 12, "bold"))
inserisci_Host = tkinter.Entry(frame)
spazio_portainizio = tkinter.Label(frame, text= "Port range", bg="#e7cf8a", font=("Arial", 12, "bold") )
inserisci_portainizio = tkinter.Entry(frame)
inserisci_portafine = tkinter.Entry(frame)
bottone_scansiona = tkinter.Button(frame, text="SCANSIONA", bg="black", fg="#e7cf8a", font=("Arial", 12, "bold"), command=scansiona)
result_text = scrolledtext.ScrolledText(frame, width=30, height=17)

#Posizionamento degli Widget
spazio_titolo.grid(row=0, column=0, columnspan=2, sticky="news", pady=20) #columnspan sta a indicare che deve occupare 2 colonne
spazio_Host.grid(row=1, column=0)
inserisci_Host.grid(row=1, column=1, pady=10)
spazio_portainizio.grid(row=2, column=0)
inserisci_portainizio.grid(row=2, column=1, pady=0)
inserisci_portafine.grid(row=3, column=1, pady=10)
bottone_scansiona.grid(row=4, column=0, columnspan=2, pady=12)
result_text.grid(row=5,column=0, columnspan=2, pady=12)

frame.pack()




finestra.mainloop() #fino quando c'è questo loop l'app funzionerà
