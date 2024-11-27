import requests
import os
from datetime import datetime

def save_log(method, url, response):
    """Salva i dettagli della richiesta e della risposta in un file di log."""
    log_dir = "request_logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(log_dir, f"log_{timestamp}.txt")
    
    with open(filename, "w") as f:
        f.write(f"Method: {method}\n")
        f.write(f"URL: {url}\n")
        f.write(f"Status Code: {response.status_code}\n")
        f.write("Response Headers:\n")
        for key, value in response.headers.items():
            f.write(f"{key}: {value}\n")
        f.write("\nResponse Body:\n")
        f.write(response.text)

    print(f"[INFO] Log salvato in: {filename}")


def login(session, base_url, username, password):
    """Effettua il login al server."""
    login_url = f"{base_url}/login.php"
    payload = {
        "username": username,
        "password": password,
        "Login": "Login"
    }
    response = session.post(login_url, data=payload)
    
    # Controllo se il login è andato a buon fine
    if "Login failed" in response.text or response.status_code != 200:
        print("[ERRORE] Login fallito. Controlla le credenziali.")
        return False
    print("[SUCCESSO] Login effettuato con successo.")
    return True


def send_request(session, base_url, endpoint, method, data=None):
    """Invia una richiesta HTTP mantenendo la sessione."""
    url = f"{base_url}/{endpoint}"
    
    try:
        if method == "GET":
            response = session.get(url)
        elif method == "POST":
            response = session.post(url, data=data)
        elif method == "PUT":
            response = session.put(url, data=data)
        elif method == "DELETE":
            response = session.delete(url)
        elif method == "HEAD":
            response = session.head(url)
        elif method == "OPTIONS":
            response = session.options(url)
        else:
            print("[ERRORE] Metodo HTTP non supportato.")
            return

        print(f"[RISPOSTA] Status Code: {response.status_code}")
        print(f"[RISPOSTA] Contenuto: {response.text[:200]}...")  # Mostra solo i primi 200 caratteri
        save_log(method, url, response)
    except requests.RequestException as e:
        print(f"[ERRORE] Richiesta {method} fallita: {e}")


def main():
    base_url = input("Inserisci l'URL del web server (es. https://<IP_HOST>/DVWA): ").strip()
    username = input("Inserisci il nome utente: ").strip()
    password = input("Inserisci la password: ").strip()
    
    # Crea una sessione
    session = requests.Session()
    
    # Effettua il login
    if not login(session, base_url, username, password):
        return
    
    # Menu interattivo per le richieste
    while True:
        print("\nScegli il tipo di richiesta HTTP:")
        print("1. GET")
        print("2. POST")
        print("3. PUT")
        print("4. DELETE")
        print("5. HEAD")
        print("6. OPTIONS")
        print("7. Esci")
        choice = input("Scelta: ").strip()
        
        if choice == "7":
            print("Uscita dal programma.")
            break
        
        methods = {"1": "GET", "2": "POST", "3": "PUT", "4": "DELETE", "5": "HEAD", "6": "OPTIONS"}
        method = methods.get(choice)
        
        if not method:
            print("[ERRORE] Scelta non valida.")
            continue
        
        endpoint = input("Inserisci l'endpoint (es. login.php, security.php): ").strip()
        data = None
        if method in ["POST", "PUT"]:
            data = input("Inserisci i dati da inviare (in formato JSON): ").strip()
        
        send_request(session, base_url, endpoint, method, data)


if __name__ == "__main__":
    main()
