import os
import requests
import json
from datetime import datetime

# Directory per salvare i log
LOG_DIR = "http_request_logs"

# Crea la cartella di log se non esiste
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def save_log(method, url, response):
    """Salva i dettagli della richiesta e della risposta in un file di log."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{LOG_DIR}/{method}_{url.replace('/', '_')}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Metodo HTTP: {method}\n")
        file.write(f"URL completo: {url}\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers:\n{response.headers}\n\n")
        
        if method not in ["HEAD"]:  # HEAD non ha un corpo nella risposta
            file.write("Risposta:\n")
            file.write(response.text)
    print(f"[LOG] Risposta salvata in: {filename}")

def send_request(url, method, data=None, headers=None):
    """Invia una richiesta HTTP e salva il risultato."""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, data=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, data=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        elif method == "HEAD":
            response = requests.head(url, headers=headers)
        elif method == "OPTIONS":
            response = requests.options(url, headers=headers)
        else:
            print("[ERRORE] Metodo HTTP non supportato.")
            return

        print(f"[RISPOSTA] Status Code: {response.status_code}")
        save_log(method, url, response)
    except requests.RequestException as e:
        print(f"[ERRORE] Richiesta {method} fallita: {e}")

def main():
    print("Benvenuto nello script di test delle richieste HTTP.")

    # Inserisci l'URL completo del server
    url = input("Inserisci l'URL completo del server (es. https://192.168.1.100/DVWA/login.php): ").strip()

    # Chiedi all'utente quale tipo di richiesta HTTP fare
    print("\nSeleziona il tipo di richiesta HTTP:")
    print("[1] GET")
    print("[2] POST")
    print("[3] PUT")
    print("[4] DELETE")
    print("[5] HEAD")
    print("[6] OPTIONS")
    method_choice = input("Inserisci il numero della scelta (1/2/3/4/5/6): ").strip()

    # Mappa della scelta dell'utente al metodo HTTP
    method = None
    if method_choice == "1":
        method = "GET"
    elif method_choice == "2":
        method = "POST"
    elif method_choice == "3":
        method = "PUT"
    elif method_choice == "4":
        method = "DELETE"
    elif method_choice == "5":
        method = "HEAD"
    elif method_choice == "6":
        method = "OPTIONS"
    else:
        print("[ERRORE] Scelta non valida.")
        return

    # Se il metodo è POST o PUT, chiedi all'utente se vuole inserire i dati (formato x-www-form-urlencoded o JSON)
    data = None
    headers = None
    if method in ["POST", "PUT"]:
        data_input = input("Vuoi inserire dei dati nel corpo della richiesta? (S/N): ").strip().upper()
        if data_input == "S":
            # Chiedi se si desidera usare JSON o x-www-form-urlencoded
            data_format = input("Scegli il formato dei dati (1) JSON, (2) x-www-form-urlencoded: ").strip()
            
            if data_format == "1":
                headers = {'Content-Type': 'application/json'}
                json_data_input = input("Inserisci i dati in formato JSON (es. {'key1':'value1', 'key2':'value2'}): ").strip()
                try:
                    data = json.loads(json_data_input)  # Converte la stringa JSON in un dizionario
                except json.JSONDecodeError:
                    print("[ERRORE] JSON non valido.")
                    return
            elif data_format == "2":
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                data = input("Inserisci i dati nel formato 'key1=value1&key2=value2': ").strip()
            else:
                print("[ERRORE] Scelta non valida per il formato dei dati.")
                return

    # Invia la richiesta
    send_request(url, method, data, headers)

if __name__ == "__main__":
    main()

