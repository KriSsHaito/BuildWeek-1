import requests
import os
from datetime import datetime

# Creazione di una sessione persistente
def create_session():
    return requests.Session()

# Funzione per salvare log e risposte
def save_response(response, action=""):
    folder_name = "http_responses"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{folder_name}/{action}_{timestamp}.txt"

    with open(file_name, "w") as file:
        file.write("=== Dettagli della richiesta ===\n")
        file.write(f"URL: {response.url}\n")
        file.write(f"Metodo: {response.request.method}\n")
        file.write(f"Headers della richiesta: {response.request.headers}\n")
        file.write(f"Dati della richiesta: {response.request.body}\n\n")
        file.write("=== Dettagli della risposta ===\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers della risposta: {response.headers}\n")
        file.write(f"Contenuto della risposta:\n{response.text}")

    print(f"Risposta salvata in: {file_name}")

# Funzione generica per richieste HTTP
def send_request(session, method, url, headers=None, payload=None):
    try:
        if method == 'GET':
            response = session.get(url, headers=headers)
        elif method == 'POST':
            response = session.post(url, headers=headers, data=payload)
        elif method == 'PUT':
            response = session.put(url, headers=headers, data=payload)
        elif method == 'DELETE':
            response = session.delete(url, headers=headers)
        else:
            print("Metodo HTTP non valido.")
            return None

        # Salvataggio della risposta
        save_response(response, method)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta: {e}")
        return None

# Funzione per il login con POST
def login(session, base_url, login_endpoint):
    print("\n=== Login ===")
    url = f"{base_url.rstrip('/')}/{login_endpoint.lstrip('/')}"
    username = input("Inserisci username: ").strip()
    password = input("Inserisci password: ").strip()

    # Payload per il login
    payload = {
        "username": username,
        "password": password,
        "Login": "Submit"  # Questo dipende dal nome del pulsante HTML
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    print("\nEsempio di richiesta POST:")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"Payload: {payload}\n")

    # Invio della richiesta POST
    response = send_request(session, 'POST', url, headers=headers, payload=payload)

    # Verifica della risposta
    if response and "Login failed" not in response.text:
        print("Login avvenuto con successo!")
    else:
        print("Login fallito. Controlla le credenziali o i dettagli della richiesta.")

    return response

# Funzione per richiedere dati protetti
def access_protected_page(session, base_url, endpoint):
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    print(f"\nAccesso alla pagina protetta: {url}")
    response = send_request(session, 'GET', url)

    if response and response.status_code == 200:
        print("Accesso avvenuto con successo!")
        print("Contenuto della risposta:")
        print(response.text[:500])  # Mostra solo i primi 500 caratteri
    else:
        print("Accesso fallito. Controlla se il login è stato eseguito correttamente.")

# Menu per selezionare il tipo di richiesta
def user_menu(session, base_url):
    while True:
        print("\n=== Menu ===")
        print("1. Effettua una richiesta GET")
        print("2. Effettua una richiesta POST")
        print("3. Effettua una richiesta PUT")
        print("4. Effettua una richiesta DELETE")
        print("5. Effettua il login")
        print("6. Accedi a una pagina protetta")
        print("0. Esci")
        choice = input("Scegli un'opzione: ").strip()

        if choice == '1':
            endpoint = input("Inserisci l'endpoint: ").strip()
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            send_request(session, 'GET', url)
        elif choice == '2':
            endpoint = input("Inserisci l'endpoint: ").strip()
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            payload = input("Inserisci il payload (es. key=value&key2=value2): ").strip()
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            send_request(session, 'POST', url, headers=headers, payload=payload)
        elif choice == '3':
            endpoint = input("Inserisci l'endpoint: ").strip()
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            payload = input("Inserisci il payload (es. key=value&key2=value2): ").strip()
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            send_request(session, 'PUT', url, headers=headers, payload=payload)
        elif choice == '4':
            endpoint = input("Inserisci l'endpoint: ").strip()
            url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            send_request(session, 'DELETE', url)
        elif choice == '5':
            login_endpoint = input("Inserisci l'endpoint per il login (es: login.php): ").strip()
            login(session, base_url, login_endpoint)
        elif choice == '6':
            endpoint = input("Inserisci l'endpoint della pagina protetta: ").strip()
            access_protected_page(session, base_url, endpoint)
        elif choice == '0':
            print("Uscita...")
            break
        else:
            print("Scelta non valida. Riprova.")

# Funzione principale
def main():
    base_url = input("Inserisci l'URL del web server (es: http://127.0.0.1/DVWA): ").strip()
    session = create_session()
    user_menu(session, base_url)

if __name__ == "__main__":
    main()
