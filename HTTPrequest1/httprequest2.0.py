import requests
import os
import json
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

def is_valid_url(url):
    """Verifica che l'URL fornito sia valido."""
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)

def send_request(session, url, method, headers=None, data=None):
    """Invia una richiesta HTTP, salva il risultato e analizza la risposta."""
    try:
        if method == "GET":
            response = session.get(url, headers=headers)
        elif method == "POST":
            response = session.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = session.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = session.delete(url, headers=headers)
        else:
            print("[ERRORE] Metodo HTTP non supportato.")
            return None

        print(f"[RISPOSTA] Status Code: {response.status_code}")
        save_log(method, url, response)
        return response
    except requests.RequestException as e:
        print(f"[ERRORE] Richiesta {method} fallita: {e}")
        return None

def login(session, login_url, credentials):
    """Effettua il login utilizzando i dati forniti."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print("[INFO] Tentativo di login...")
    response = session.post(login_url, data=credentials, headers=headers)
    if "Login failed" in response.text:
        print("[ERRORE] Login fallito. Verifica le credenziali.")
    elif "Welcome" in response.text or "Dashboard" in response.text:
        print("[SUCCESSO] Login effettuato con successo!")
    else:
        print("[INFO] Risposta non chiara. Verifica manualmente.")
    return response

def main():
    # Inizializza la directory dei log
    initialize_log_directory()

    # Inserisci l'URL per il login
    login_url = input("Inserisci l'URL di login (es. http://127.0.0.1/DVWA/login.php): ").strip()
    if not is_valid_url(login_url):
        print("[ERRORE] L'URL fornito non è valido. Assicurati di includere http:// o https://.")
        return

    # Credenziali di login
    print("\nInserisci le credenziali di login:")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    credentials = {
        "username": username,
        "password": password
    }

    # Inizializza una sessione
    session = requests.Session()

    # Effettua il login
    login(session, login_url, credentials)

    # Inserisci l'URL della risorsa protetta
    url = input("\nInserisci l'URL completo della risorsa (es. http://127.0.0.1/DVWA/some_protected_page.php): ").strip()
    if not is_valid_url(url):
        print("[ERRORE] L'URL fornito non è valido.")
        return

    # Seleziona il tipo di richiesta HTTP
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

    # Header personalizzati
    headers = {}
    while input("\nVuoi aggiungere un header personalizzato? (s/n): ").lower() == "s":
        header_name = input("Inserisci il nome dell'header (es. Authorization): ").strip()
        header_value = input(f"Inserisci il valore per {header_name}: ").strip()
        headers[header_name] = header_value

    # Dati da inviare (solo per POST o PUT)
    data = None
    if method in ["POST", "PUT"]:
        print("\nSeleziona il formato dei dati:")
        print("[1] Parametri (es. chiave1=valore1&chiave2=valore2)")
        print("[2] JSON")
        data_format = input("Scegli il formato dei dati (1/2): ").strip()
        if data_format == "1":
            raw_data = input("Inserisci i dati (es. chiave1=valore1&chiave2=valore2): ").strip()
            data = dict(item.split("=") for item in raw_data.split("&"))
        elif data_format == "2":
            raw_data = input("Inserisci i dati JSON (es. {\"chiave\": \"valore\"}): ").strip()
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                print("[ERRORE] Il JSON fornito non è valido.")
                return

    # Invia la richiesta
    response = send_request(session, url, method, headers=headers, data=data)
    if response:
        print("[INFO] Contenuto della risposta:")
        print(response.text)

if __name__ == "__main__":
    main()

