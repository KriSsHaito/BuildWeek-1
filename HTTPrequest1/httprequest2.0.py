import requests
import json
import os
from datetime import datetime

# Funzione per salvare log di debug
def log_debug(message):
    folder_name = "http_debug_logs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    log_file = f"{folder_name}/debug_log.txt"
    with open(log_file, "a") as file:
        file.write(f"{datetime.now()}: {message}\n")

# Funzione per inviare richieste HTTP e gestire i cookie
def send_request(session, url, endpoint, method, headers=None, payload=None):
    full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
    try:
        # Invio richiesta
        if method == 'GET':
            response = session.get(full_url, headers=headers)
        elif method == 'POST':
            response = session.post(full_url, headers=headers, data=payload)
        elif method == 'PUT':
            response = session.put(full_url, headers=headers, data=payload)
        elif method == 'DELETE':
            response = session.delete(full_url, headers=headers)
        else:
            raise ValueError("Metodo HTTP non supportato.")

        # Log dettagli della richiesta
        log_debug(f"Request: {method} {full_url}")
        log_debug(f"Headers: {headers}")
        log_debug(f"Payload: {payload}")
        log_debug(f"Response Status Code: {response.status_code}")
        log_debug(f"Response Headers: {response.headers}")
        log_debug(f"Response Content: {response.text[:500]}")

        return response
    except requests.exceptions.RequestException as e:
        log_debug(f"Errore nella richiesta: {e}")
        print(f"Errore nella richiesta: {e}")
        return None

# Funzione per verificare se il login è riuscito
def is_logged_in(response):
    # Controlliamo se siamo effettivamente loggati (es. ricerca di parole chiave)
    if "Login failed" in response.text or response.status_code == 401:
        return False
    elif "security.php" in response.text or response.status_code == 200:
        return True
    return False

# Funzione principale
def main():
    session = requests.Session()  # Sessione persistente per gestire cookie
    url = input("Inserisci l'URL del web server (es: http://127.0.0.1/DVWA): ").strip()
    
    # Effettuiamo il login
    print("\n=== Login ===")
    login_endpoint = input("Inserisci l'endpoint di login (es: login.php): ").strip()
    username = input("Inserisci username: ").strip()
    password = input("Inserisci password: ").strip()

    # Payload del login
    payload = {
        "username": username,
        "password": password,
        "Login": "Submit"
    }

    # Headers opzionali
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Invio richiesta di login
    response = send_request(session, url, login_endpoint, "POST", headers, payload)

    # Verifica se il login è avvenuto
    if is_logged_in(response):
        print("\nLogin avvenuto con successo!")
    else:
        print("\nLogin fallito. Controlla le credenziali o i dettagli della richiesta.")
        return

    # Accesso a una pagina protetta
    print("\n=== Accesso a una pagina protetta ===")
    secure_endpoint = input("Inserisci l'endpoint della pagina protetta (es: security.php): ").strip()
    response = send_request(session, url, secure_endpoint, "GET")

    # Visualizziamo il contenuto della risposta
    print("\n=== Risposta ===")
    print(f"Status Code: {response.status_code}")
    print(response.text[:500])  # Stampiamo solo i primi 500 caratteri per evitare lunghi output

    # Salviamo la risposta in un file
    save_response(url, secure_endpoint, response)

# Funzione per salvare la risposta in un file
def save_response(url, endpoint, response):
    folder_name = "http_logs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{folder_name}/response_{timestamp}.txt"

    with open(file_name, "w") as file:
        file.write("=== Dettagli della richiesta ===\n")
        file.write(f"URL: {url}\n")
        file.write(f"Endpoint: {endpoint}\n")
        file.write("\n=== Dettagli della risposta ===\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers: {json.dumps(dict(response.headers), indent=4)}\n")
        file.write(f"Contenuto:\n{response.text}")

    print(f"Risposta salvata in: {file_name}")

if __name__ == "__main__":
    main()
