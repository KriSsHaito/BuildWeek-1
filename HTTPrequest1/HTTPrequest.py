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

def save_log(method, url, response):
    """Salva i dettagli della richiesta e della risposta in un file di log."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{LOG_DIR}/{method}_{url.replace('/', '_')}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Metodo HTTP: {method}\n")
        file.write(f"URL: {url}\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers:\n{response.headers}\n\n")
        file.write("Risposta:\n")
        file.write(response.text)
    print(f"[LOG] Risposta salvata in: {filename}")

def send_request(url, method, data=None):
    """Invia una richiesta HTTP e salva il risultato."""
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
        save_log(method, url, response)
    except requests.RequestException as e:
        print(f"[ERRORE] Richiesta {method} fallita: {e}")

def is_valid_url(url):
    """Verifica che l'URL fornito sia valido."""
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

def main():
    # Inizializza la directory dei log
    initialize_log_directory()

    # Inserisci l'URL completo
    url = input("Inserisci l'URL completo della richiesta (es. http://192.168.1.100/DVWA/login.php): ").strip()
    if not is_valid_url(url):
        print("[ERRORE] L'URL fornito non è valido. Assicurati di includere http:// o https://.")
        return

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

    # Dati da inviare (solo per POST o PUT)
    data = None
    if method in ["POST", "PUT"]:
        data_input = input("Inserisci i dati da inviare (es. username=admin&password=password), lascia vuoto per nessun dato: ").strip()
        if data_input:
            data = dict(item.split("=") for item in data_input.split("&"))

    # Invia la richiesta
    send_request(url, method, data)

if __name__ == "__main__":
    main()
