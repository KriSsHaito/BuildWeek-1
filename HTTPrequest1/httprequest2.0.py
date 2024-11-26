import requests
import os
from datetime import datetime

# Configurazione della directory per i log
LOG_DIR = "http_request_logs"

def initialize_log_directory():
    """Crea la directory per i log se non esiste già."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def save_log(method, endpoint, response):
    """Salva i dettagli della richiesta e della risposta in un file di log."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{LOG_DIR}/{method}_{endpoint.replace('/', '_')}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Metodo HTTP: {method}\n")
        file.write(f"Endpoint: {endpoint}\n")
        file.write(f"URL completo: {response.url}\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers:\n{response.headers}\n\n")
        file.write("Risposta:\n")
        if method not in ["HEAD"]: #HEAD non ha un corpo nella risposta
            file.write("Risposta:\n")
            file.write(response.text)
    print(f"[LOG] Risposta salvata in: {filename}")

def send_request(base_url, method, endpoint, data=None):
    """Invia una richiesta HTTP e salva il risultato."""
    url = f"{base_url}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, data=data)
        elif method == "PUT":
            response = requests.put(url, data=data)
        elif method == "DELETE":
            response = requests.delete(url)
        elif method == "HEAD":
            response = requests.head(url)
        elif method == "OPTIONS":
            response = requests.options(url)
        else:
            print("[ERRORE] Metodo HTTP non supportato.")
            return

        print(f"[RISPOSTA] Status Code: {response.status_code}")
        save_log(method, endpoint, response)
    except requests.RequestException as e:
        print(f"[ERRORE] Richiesta {method} fallita: {e}")

def main():
    # Inizializza la directory dei log
    initialize_log_directory()

    # Inserisci l'IP della macchina host
    ip_host = input("Inserisci l'indirizzo IP della macchina host (es. 192.168.1.100): ").strip()
    base_url = f"http://{ip_host}/DVWA"
    print(f"[INFO] URL base configurato: {base_url}")

    # Scelta del tipo di richiesta HTTP
    print("\nSeleziona il tipo di richiesta HTTP:")
    print("[1] GET")
    print("[2] POST")
    print("[3] PUT")
    print("[4] DELETE")
    print("[5] HEAD")
    print("[6] OPTIONS")
    method_choice = input("Inserisci il numero della scelta (1/2/3/4/5/6): ").strip()

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

    # Inserisci l'endpoint
    endpoint = input("Inserisci l'endpoint relativo (es. login.php): ").strip()

    # Dati da inviare (solo per POST o PUT)
    data = None
    if method in ["POST", "PUT"]:
        data_input = input("Inserisci i dati da inviare (es. username=admin&password=password), lascia vuoto per nessun dato: ").strip()
        if data_input:
            data = dict(item.split("=") for item in data_input.split("&"))

    # Invia la richiesta
    send_request(base_url, method, endpoint, data)

if __name__ == "__main__":
    main()

