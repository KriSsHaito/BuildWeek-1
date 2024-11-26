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
    # Sostituisci caratteri non validi negli URL per il nome file
    sanitized_url = url.replace("/", "_").replace(":", "_")
    filename = f"{LOG_DIR}/{method}_{sanitized_url}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Metodo HTTP: {method}\n")
        file.write(f"URL: {url}\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers:\n{response.headers}\n\n")
        file.write("Risposta:\n")
        file.write(response.text)
    print(f"[LOG] Risposta salvata in: {filename}")

def analyze_response(response):
    """Analizza la risposta per identificare successi o fallimenti logici."""
    # Modifica i messaggi di verifica in base alla tua applicazione
    if "Login failed" in response.text or "Invalid credentials" in response.text:
        print("[INFO] Login fallito. Verifica le credenziali.")
    elif "Welcome" in response.text or "Login successful" in response.text:
        print("[INFO] Login riuscito.")
    else:
        print("[INFO] Risposta analizzata, nessun pattern specifico identificato.")

def send_request(url, method, data=None):
    """Invia una richiesta HTTP, salva il risultato e analizza la risposta."""
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
        # Analizza il contenuto della risposta
        analyze_response(response)
        # Salva la risposta nei log
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
    url = input("Inserisci l'URL completo della richiesta (es. http://127.0.0.1/DVWA/login.php): ").strip()
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
            try:
                data = dict(item.split("=") for item in data_input.split("&"))
            except ValueError:
                print("[ERRORE] I dati forniti non sono in un formato valido (es. chiave=valore).")
                return

    # Invia la richiesta
    send_request(url, method, data)

if __name__ == "__main__":
    main()
