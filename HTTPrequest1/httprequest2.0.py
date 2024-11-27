import requests
import json
import os
from datetime import datetime

# Funzione per ottenere input utente in modo user-friendly
def user_friendly_input(prompt, allow_json=False):
    while True:
        user_input = input(prompt).strip()
        if allow_json and user_input:
            try:
                return json.loads(user_input)
            except json.JSONDecodeError:
                print("Errore: non è un JSON valido. Riprova.")
        else:
            return user_input

# Funzione per configurare la richiesta
def get_user_input():
    print("\n=== Configurazione della richiesta ===")
    url = input("Inserisci l'URL del web server (es: http://127.0.0.1/DVWA): ").strip()
    endpoint = input("Inserisci l'endpoint (es: login.php): ").strip()
    method = input("Inserisci il metodo HTTP (GET, POST, PUT, DELETE): ").strip().upper()
    headers = {}
    if input("Vuoi aggiungere headers personalizzati? (s/n): ").strip().lower() == 's':
        while True:
            key = input("Header key (lascia vuoto per terminare): ").strip()
            if not key:
                break
            value = input(f"Valore per {key}: ").strip()
            headers[key] = value

    payload = None
    if method in ['POST', 'PUT']:
        print("Inserisci il payload. Usa formato JSON (esempio: {\"username\": \"admin\", \"password\": \"password\"})")
        payload = user_friendly_input("Payload: ", allow_json=True)

    return url, endpoint, method, headers, payload

# Funzione per inviare richieste mantenendo la sessione
def send_request(session, url, endpoint, method, headers, payload):
    full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
    try:
        if method == 'GET':
            response = session.get(full_url, headers=headers)
        elif method == 'POST':
            response = session.post(full_url, headers=headers, data=payload)
        elif method == 'PUT':
            response = session.put(full_url, headers=headers, data=payload)
        elif method == 'DELETE':
            response = session.delete(full_url, headers=headers)
        else:
            print("Metodo HTTP non supportato.")
            return None

        return response
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")
        return None

# Funzione per salvare la risposta
def save_response(request_data, response):
    folder_name = "http_logs"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{folder_name}/log_{timestamp}.txt"

    with open(file_name, "w") as file:
        file.write("=== Dettagli della richiesta ===\n")
        file.write(f"URL: {request_data['url']}\n")
        file.write(f"Endpoint: {request_data['endpoint']}\n")
        file.write(f"Metodo HTTP: {request_data['method']}\n")
        file.write(f"Headers: {json.dumps(request_data['headers'], indent=4)}\n")
        if request_data['payload']:
            file.write(f"Payload: {json.dumps(request_data['payload'], indent=4)}\n")

        file.write("\n=== Dettagli della risposta ===\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Headers della risposta: {json.dumps(dict(response.headers), indent=4)}\n")
        try:
            file.write(f"Contenuto della risposta (JSON): {json.dumps(response.json(), indent=4)}\n")
        except ValueError:
            file.write(f"Contenuto della risposta (testo):\n{response.text}\n")

    print(f"Risposta salvata in: {file_name}")

# Funzione per analizzare la risposta
def parse_response(response):
    if not response:
        print("Nessuna risposta ricevuta.")
        return
    print("\n=== Risultato della richiesta ===")
    print(f"Status Code: {response.status_code}")
    print("Headers della risposta:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    print("\nContenuto della risposta:")
    try:
        print(response.json())
    except ValueError:
        print(response.text)

# Funzione principale
def main():
    session = requests.Session()  # Manteniamo una sessione per il cookie di autenticazione
    while True:
        user_input = get_user_input()
        if not user_input:
            continue
        url, endpoint, method, headers, payload = user_input
        response = send_request(session, url, endpoint, method, headers, payload)

        if response:
            request_data = {
                "url": url,
                "endpoint": endpoint,
                "method": method,
                "headers": headers,
                "payload": payload
            }
            save_response(request_data, response)

        parse_response(response)

        repeat = input("\nVuoi effettuare un'altra richiesta? (s/n): ").strip().lower()
        if repeat != 's':
            break

if __name__ == "__main__":
    main()
