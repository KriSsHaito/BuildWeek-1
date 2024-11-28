import os
import requests

# URL del web server da testare
url = input("http://<indirizzo-web-server>": )

# Lista dei verbi HTTP da testare, inclusi OPTIONS
http_methods = ["OPTIONS", "GET", "POST", "PUT", "DELETE"]

# Cartella per salvare i log
log_directory = "http_logs"

# Creazione della cartella se non esiste
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Dizionario per salvare i risultati
results = {}

for method in http_methods:
    try:
        # Invia la richiesta corrispondente al metodo
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, data={"key": "value"})
        elif method == "PUT":
            response = requests.put(url, data={"key": "value"})
        elif method == "DELETE":
            response = requests.delete(url)
        elif method == "OPTIONS":
            response = requests.options(url)
        
        # Salvataggio del risultato
        results[method] = {
            "status_code": response.status_code,
            "reason": response.reason,
            "headers": dict(response.headers),
            "allowed_methods": response.headers.get("Allow", "Non specificati") if method == "OPTIONS" else "N/A"
        }
        
        # Preparazione del contenuto del log
        log_content = f"Metodo: {method}\n"
        log_content += f"Status Code: {response.status_code}\n"
        log_content += f"Reason: {response.reason}\n"
        log_content += f"Headers: {response.headers}\n"
        if method == "OPTIONS":
            log_content += f"Allowed Methods: {results[method]['allowed_methods']}\n"
        
        # Salvataggio in un file separato per ogni verbo HTTP
        log_file_path = os.path.join(log_directory, f"{method}_log.txt")
        with open(log_file_path, "w") as log_file:
            log_file.write(log_content)
    
    except Exception as e:
        # Gestione degli errori
        results[method] = {"error": str(e)}
        log_file_path = os.path.join(log_directory, f"{method}_error_log.txt")
        with open(log_file_path, "w") as log_file:
            log_file.write(f"Errore durante il metodo {method}: {str(e)}\n")

# Output dei risultati (per la console)
for method, result in results.items():
    print(f"\nMetodo: {method}")
    for key, value in result.items():
        print(f"{key}: {value}")
