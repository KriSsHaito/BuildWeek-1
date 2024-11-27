import requests
import os
from datetime import datetime
from urllib.parse import urlparse
import json

# Configurazione della directory per i log
LOG_DIR = "http_request_logs"

def initialize_log_directory():
    """Crea la directory per i log se non esiste già."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def save_log(method, url, response):
    """Salva i dettagli della richiesta e della risposta in un file di log."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    sanitized_url = url.replace('/', '_').replace(':', '_').replace('?', '_')
    filename = f"{LOG_DIR}/{method}_{sanitized_url}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Metodo HTTP: {method}\n")
        file.write(f"URL completo: {response.url}\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers:\n{response.headers}\n\n")
        file.write("Risposta:\n")
        file.write(response.text)
    print(f"[LOG] Risposta salvata in: {filename}")

def send_request(url, method, json_data=None):
    """Invia una richiesta HTTP e salva il risultato."""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=json_data)
        elif method == "PUT":
            response = requests.put(url, json=json_data)
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
    url = input("Inserisci l'URL completo (es. http://192.168.1.100/DVWA/login.php): ").strip()
    if not is_valid_url(url):
        print("[ERRORE] URL non valido. Assicurati di includere http:// o https:// e un dominio valido.")
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

    # Dati in formato JSON da inviare (solo per POST o PUT)
    json_data = None
    if method in ["POST", "PUT"]:
        print("\nInserisci i dati da inviare in formato JSON.")
        print("Esempio (richiesta di login):")
        print('{"username": "admin", "password": "password123"}')
        json_input = input("Inserisci i dati JSON: ").strip()
        try:
            json_data = json.loads(json_input) if json_input else None
        except json.JSONDecodeError:
            print("[ERRORE] Formato JSON non valido. Assicurati di utilizzare una sintassi corretta.")
            return

    # Invia la richiesta
    send_request(url, method, json_data)

if __name__ == "__main__":
    main()


