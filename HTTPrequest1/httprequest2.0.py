import os
import json
import requests

# Creazione della cartella per salvare le risposte
output_dir = "http_responses"
os.makedirs(output_dir, exist_ok=True)

# Configurare una sessione persistente
session = requests.Session()
session.headers.update({"User-Agent": "CybersecurityScript/1.0"})

# Funzione per eseguire una richiesta HTTP
def perform_request(method, url, data=None):
    try:
        if method == "GET":
            response = session.get(url)
        elif method == "POST":
            response = session.post(url, json=data)
        elif method == "PUT":
            response = session.put(url, json=data)
        elif method == "DELETE":
            response = session.delete(url)
        else:
            print(f"Metodo {method} non supportato")
            return None

        # Stampa la risposta in modo leggibile
        print_response_details(response)

        # Salva la risposta in un file
        save_response(url, method, response)
        return response
    except requests.RequestException as e:
        print(f"Errore durante la richiesta {method} a {url}: {e}")
        return None

# Funzione per stampare la risposta in modo leggibile
def print_response_details(response):
    print("\n--- Dettagli della Risposta HTTP ---")
    print(f"URL: {response.url}")
    print(f"Metodo: {response.request.method}")
    print(f"Codice di Stato: {response.status_code}")
    print(f"Intestazioni:\n{json.dumps(dict(response.headers), indent=4)}")
    print(f"Contenuto della risposta:")
    print(response.text)  # Non formattiamo il corpo come JSON, lo mostriamo direttamente

# Funzione per salvare la risposta in un file
def save_response(url, method, response):
    file_name = f"{method}_{url.replace('/', '_').replace(':', '')}.json"
    file_path = os.path.join(output_dir, file_name)

    # Contenuto da salvare
    response_content = {
        "url": response.url,
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "content": response.text,
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(response_content, f, indent=4)
    print(f"Risposta salvata in {file_path}\n")

# Funzione per ottenere i dati da inviare (per POST e PUT)
def get_data_for_method(method):
    if method in ["POST", "PUT"]:
        data_input = input(f"Inserisci i dati in formato JSON per la richiesta {method}: ")
        try:
            data = json.loads(data_input)
            return data
        except json.JSONDecodeError:
            print("Errore nel formato JSON. Assicurati di fornire un JSON valido.")
            return None
    return None

# Funzione per scegliere la richiesta
def choose_request():
    print("Scegli il tipo di richiesta HTTP:")
    print("1. GET")
    print("2. POST")
    print("3. PUT")
    print("4. DELETE")
    method_choice = input("Inserisci il numero corrispondente alla richiesta (1-4): ")

    method_mapping = {
        "1": "GET",
        "2": "POST",
        "3": "PUT",
        "4": "DELETE",
    }

    method = method_mapping.get(method_choice)
    if not method:
        print("Scelta non valida.")
        return

    url = input("Inserisci l'URL della richiesta: ")

    # Se la richiesta è POST o PUT, chiedi i dati
    data = get_data_for_method(method)

    # Esegui la richiesta
    perform_request(method, url, data)

# Esegui il programma
if __name__ == "__main__":
    choose_request()


