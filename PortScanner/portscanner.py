import socket
import threading
import queue

#Funzione Scan di una singola porta
def scanner_port(host, port, result_queue):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #oggetto socket
    sock.settimeout(1) #timeout di un secondo

    result = sock.connect_ex((host, port)) #Se la connessione è riuscita è 0

    if result == 0:
        #print(f"La Porta {port} è APERTA")
        result_queue.put(port)
        
    sock.close()

    


#Scansione di un range di porte
def scan_ports(host, start_port, end_port, result_queue):
    threads = [] #Creazione di un dizionario vuoto 
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scanner_port, args=(host, port, result_queue))
        threads.append(thread)
        thread.start()

    #Attesa termine thread
    for thread in threads:
        thread.join()

    
        

#Funzione Principale // viene esguita solo se portscanner.py funziona correttamente
if __name__ == "__main__":
    target_host = input("\n IP Host del target: ")
    inizio_port = int(input("Digita la porta iniziale: "))
    fine_port  = int(input("Digita la porta finale: "))

    print(f"Scansionando {target_host} da {inizio_port} a {fine_port}...")
    scan_ports(target_host, inizio_port, fine_port)
