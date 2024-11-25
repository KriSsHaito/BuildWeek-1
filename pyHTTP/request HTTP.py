import requests
import os
from datetime import datetime

# Directory per i log
LOG_DIR = "http_logs"

def initialize_log():
    """Crea la directory per i log se non esiste già."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def log_response(method, endpoint, response):
    """Salva la risposta HTTP in un file di log."""
    filename = f"{LOG_DIR}/{method}_{endpoint.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"URL: {response.url}\n")
        f.write(f"Status Code: {response.status_code}\n")
        f.write(f"Headers:\n{response.headers}\n\n")
        f.write("Response Content:\n")
        f.write(response.text)
    print(f"[LOG] Risposta salvata in: {filename}")

def print_status(response):
    """Mostra lo stato della risposta con colori per chiarezza."""
    status = response.status_code
    if 200 <= status < 300:
        print(f"\033[92m[SUCCESS] {status} - {response.url}\033[0m")  # Verde
    elif 400 <= status < 500:
        print(f"\033[93m[CLIENT ERROR] {status} - {response.url}\033[0m")  # Giallo
    elif 500 <= status:
        print(f"\033[91m[SERVER ERROR] {status} - {response.url}\033[0m")  # Rosso
    else:
        print(f"[INFO] {status} - {response.url}")

def test_server_reachability(base_url):
    """Controlla se il server è raggiungibile."""
    print(f"[DEBUG] Test della connessione a: {base_url}")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("\033[92m[INFO] Server raggiungibile.\033[0m")
            return True
        else:
            print(f"\033[91m[ERROR] Server non raggiungibile, status code: {response.status_code}\033[0m")
            return False
    except requests.RequestException as e:
        print(f"\033[91m[ERROR] Connessione fallita: {e}\033[0m")
        return False

def login(base_url, username, password, session):
    """Effettua il login al DVWA."""
    login_url = base_url + "login.php"
    try:
        login_data = {
            'username': username,
            'password': password,
            'Login': 'Login'
        }
        response = session.post(login_url, data=login_data)
        log_response("POST", "login.php", response)
        if "Welcome" in response.text:
            print_status(response)
            print("[+] Login avvenuto con successo.")
        else:
            print_status(response)
            print("[-] Login fallito.")
            exit()
    except requests.RequestException as e:
        print(f"[ERROR] Login fallito: {e}")

def send_request(method, base_url, endpoint, session, data=None):
    """Gestisce le richieste HTTP generiche."""
    url = base_url + endpoint
    try:
        if method == "GET":
            response = session.get(url)
        elif method == "POST":
            response = session.post(url, data=data)
        elif method == "PUT":
            response = session.put(url, data=data)
        elif method == "DELETE":
            response = session.delete(url)
        else:
            print(f"[ERROR] Metodo HTTP non supportato: {method}")
            return
        print_status(response)
        log_response(method, endpoint, response)
    except requests.RequestException as e:
        print(f"[ERROR] Richiesta {method} fallita: {e}")

if __name__ == "__main__":
    # Inizializza log
    initialize_log()

    # Input dinamico dell'indirizzo IP e credenziali
    metasploitable_ip = input("Inserisci l'indirizzo IP del server Metasploitable: ").strip()
    BASE_URL = f"https://{metasploitable_ip}/DVWA/"
    print(f"[INFO] URL base configurato: {BASE_URL}")

    # Controllo della raggiungibilità del server
    if not test_server_reachability(BASE_URL):
        exit()

    # Credenziali DVWA (possono essere parametrizzate)
    username = input("Inserisci il nome utente DVWA (default: admin): ") or "admin"
    password = input("Inserisci la password DVWA (default: password): ") or "password"

    # Sessione per le richieste
    session = requests.Session()

    # Login
    login(BASE_URL, username, password, session)

    # Seleziona il tipo di richiesta
    print("\nQuale tipo di richiesta vuoi fare?")
    print("[1] GET")
    print("[2] POST")
    print("[3] PUT")
    print("[4] DELETE")
    choice = input("Seleziona l'opzione (1/2/3/4): ").strip()

    if choice == "1":
        method = "GET"
    elif choice == "2":
        method = "POST"
        print("Endpoint disponibili per POST:")
        print(" 1. vulnerabilities/sqli/")
        print(" 2. vulnerabilities/brute/")
        print(" 3. vulnerabilities/csrf/")
        endpoint_choice = input("Seleziona l'endpoint (1/2/3): ").strip()
        if endpoint_choice == "1":
            endpoint = "vulnerabilities/sqli/"
        elif endpoint_choice == "2":
            endpoint = "vulnerabilities/brute/"
        elif endpoint_choice == "3":
            endpoint = "vulnerabilities/csrf/"
        data = input("Inserisci i dati da inviare (come dizionario, es. {'username': 'test', 'password': 'test'}): ")
        data = eval(data)  # Attenzione a questa funzione per motivi di sicurezza
    elif choice == "3":
        method = "PUT"
        print("Endpoint disponibili per PUT:")
        print(" 1. vulnerabilities/sqli/")
        endpoint_choice = input("Seleziona l'endpoint (1): ").strip()
        if endpoint_choice == "1":
            endpoint = "vulnerabilities/sqli/"
        data = input("Inserisci i dati da inviare (come dizionario, es. {'id': '1', 'name': 'test'}): ")
        data = eval(data)  # Attenzione a questa funzione per motivi di sicurezza
    elif choice == "4":
        method = "DELETE"
        print("Endpoint disponibili per DELETE:")
        print(" 1. vulnerabilities/sqli/?id=1")
        endpoint_choice = input("Seleziona l'endpoint (1): ").strip()
        if endpoint_choice == "1":
            endpoint = "vulnerabilities/sqli/?id=1"
        data = None
    else:
        print("[ERROR] Opzione non valida. Uscita...")
        exit()

    # Esegui la richiesta
    send_request(method, BASE_URL, endpoint, session, data)

