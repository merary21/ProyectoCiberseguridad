import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.2",
    "prompt": "Explica qué es un ataque DDoS en una sola frase.",
    "stream": False
}

respuesta = requests.post(url, json=payload)

print(respuesta.json()["response"])