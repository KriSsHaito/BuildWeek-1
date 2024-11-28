import requests

# URL del web server da testare
url = input("http://<indirizzo-web-server>: ") 

# Lista dei verbi HTTP da testare, inclusi OPTIONS
http_methods = ["OPTIONS", "GET", "POST", "PUT", "DELETE"]

# Dizionario per salvare i risultati
results = {}

for method in http_methods:
    try:
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
    except Exception as e:
        results[method] = {"error": str(e)}

# Output dei risultati
for method, result in results.items():
    print(f"\nMetodo: {method}")
    for key, value in result.items():
        print(f"{key}: {value}")
