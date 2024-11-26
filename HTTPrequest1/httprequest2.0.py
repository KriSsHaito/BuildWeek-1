import requests
import os
from datetime import datetime
from urllib.parse import urlparse
import json

LOG_DIR = "http_request_logs"
session = requests.Session()

def initialize_log_directory():
    """Crea la directory per i log se non esiste già."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def save_log(method, url, response, data=None, headers=None):
    """Salva i dettagli della richiesta e della risposta in un file di log."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    sanitized_url = url.replace("/", "_").replace(":", "_")
    filename = f"{LOG_DIR}/{method}_{sanitized_url}_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Metodo HTTP: {method}\n")
        file.write(f"URL: {url}\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers di risposta:\n{response.headers}\n\n")
        if data:
            file.write(f"Dati inviati: {data}\n\n")
        if headers:
            file.write(f"Headers personalizzati:\n{headers}\n\n")
        file.write("Risposta:\n")
        file.write(response.text)
    print(f"[LOG] Risposta salvata in: {filename}")

def analyze_response(response):
    """Analizza la risposta per identificare eventuali problemi."""
    print("[DEBUG] Contenuto della risposta ricevuta:")
    print(response.text[:500])  # Stampa solo i primi 500 caratteri per il debug

    if "Login failed" in response.text or "Invalid username" in response.text:
        print("[INFO] Login fallito. Credenziali non valide.")
    elif "Welcome to the" in response.text or "Dashboard" in response.text:
        print("[INFO] Login riuscito.")
    else:
        print("[INFO] Nessun pattern riconosciuto nella risposta. Verifica manuale necessaria.")

def get_headers():
    """Permette all'utente di aggiungere header personalizzati."""
    headers = {}
    while True:
        add_header = input("Vuoi aggiungere un header personalizzato? (s/n): ").strip().lower()
        if add_header == "s":
            key = input("Inserisci il nome dell'header (es. Authorization): ").strip()
            value = input("Inserisci il valore dell'header: ").strip()
            headers[key] = value
        else:
            break
    return headers

def get_data():
    """Permette all'utente di inserire i dati in modo semplice."""
    print("\nSeleziona il formato dei dati:")
    print("[1] Parametri (es. chiave1=valore1&chiave2=valore2)")
    print("[2] JSON")
    choice = input("Scegli il formato dei dati (1/2): ").strip()
    
    data = None
    if choice == "1":
        data_input = input("Inserisci i dati (es. chiave=valore, separati da &): ").strip()
        try:
            data = dict(item.split("=") for item in data_input.split("&"))
        except ValueError:
            print("[ERRORE] Formato non valido! Riprova.")
            return get_data()
    elif choice == "2":
        json_input = input("Inserisci i dati JSON (es. {\"chiave\": \"valore\"}): ").strip()
        try:
            data = json.loads(json_input)
        except json.JSONDecodeError:
            print("[ERRORE] JSON non valido! Riprova.")
            return get_data()
    else:
        print("[ERRORE] Scelta non valida!")
        return get_data()
    
    return data

def send_request(url, method, data=None, headers=None):
    """Invia una richiesta HTTP, salva il risultato e analizza la risposta."""
    try:
        if method == "GET":
            response = session.get(url, headers=headers, allow_redirects=False)
        elif method == "POST":
            response = session.post(url, data=data, headers=headers, allow_redirects=False)
        elif method == "PUT":
            response = session.put(url, data=data, headers=headers, allow_redirects=False)
        elif method == "DELETE":
            response = session.delete(url, headers=headers, allow_redirects=False)
        else:
            print("[ERRORE] Metodo HTTP non supportato.")
            return

        # Debug dei reindirizzamenti
        if response.status_code in [301, 302]:
            print(f"[INFO] Reindirizzamento rilevato verso: {response.headers.get('Location')}")
        
        print(f"[RISPOSTA] Status Code: {response.status_code}")
        analyze_response(response)
        save_log(method, url, response, data, headers)
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

    # Dati e header da inviare
    data = None
    headers = None
    if method in ["POST", "PUT", "DELETE"]:
        headers = get_headers()
        if method != "DELETE":  # DELETE non richiede sempre dati
            data = get_data()

    # Invia la richiesta
    send_request(url, method, data, headers)

if __name__ == "__main__":
    main()
