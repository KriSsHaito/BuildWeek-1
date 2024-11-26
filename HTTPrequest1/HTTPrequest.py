import requests
import os
from datetime import datetime
from urllib.parse import urlparse

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
        else:
            print("[ERRORE] Metodo HTTP non supportato.")
            return

        print(f"[RISPOSTA] Status Code: {response.status_code}")
        save_log(method, endpoint, response)
    except requests.RequestException as e:
        print(f"[ERRORE] Richiesta {method} fallita: {e}")

def is_valid_url(url):
    """Verifica se l'URL è valido."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def main():
    # Inizializza la directory dei log
    initialize_log_directory()

    # Inserisci l'URL della macchina host
    while True:
        ip_host = input("Inserisci l'indirizzo IP della macchina host o l'URL completo (es. http://192.168.1.100/DVWA): ").strip()
        if is_valid_url(ip_host):
            base_url = ip_host.rstrip("/")
            break
        print("[ERRORE] URL non valido. Riprova.")

    print(f"[INFO] URL base configurato: {base_url}")

    # Scelta del tipo di richiesta HTTP
    print("\nSeleziona il tipo di richiesta HTTP:")
    print("[1] GET")
    print("[2] POST")
    print("[3] PUT")
    print("[4] DELETE")
    method_choice = input("Inserisci il numero della scelta (1/2/3/4): ").strip()

    method = None
    if method_choice == "1":
        method = "GET"
    elif method_choice == "2":
        method = "POST"
    elif method_choice == "3":
        method = "PUT"
    elif method_choice == "4":
        method = "DELETE"
    else:
        print("[ERRORE] Scelta non valida.")
        return

    # Inserisci l'endpoint
    endpoint = input("Inserisci l'endpoint relativo (es. login.php): ").strip()
    if not endpoint:
        print("[ERRORE] L'endpoint non può essere vuoto.")
        return

    # Dati da inviare (solo per POST o PUT)
    data = None
    if method in ["POST", "PUT"]:
        data_input = input("Inserisci i dati da inviare in formato chiave=valore separati da '&', oppure JSON (es. {\"key\": \"value\"}), lascia vuoto per nessun dato: ").strip()
        if data_input:
            try:
                # Tenta di caricare i dati come JSON
                if data_input.startswith("{") and data_input.endswith("}"):
                    import json
                    data = json.loads(data_input)
                else:
                    # Interpreta come dati URL-encoded
                    data = dict(item.split("=") for item in data_input.split("&"))
            except Exception as e:
                print(f"[ERRORE] Formato dei dati non valido: {e}")
                return

    # Invia la richiesta
    send_request(base_url, method, endpoint, data)

if __name__ == "__main__":
    main()
