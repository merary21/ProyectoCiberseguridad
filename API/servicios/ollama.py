import os
import requests


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


def consultar_llama(pregunta):

    prompt = f"""
Eres CyberSOC AI, un asistente especializado en:

- Ciberseguridad
- Seguridad Web
- OWASP Top 10
- SQL Injection
- XSS
- DDoS
- Fuerza Bruta
- Monitoreo de tráfico web
- Detección de anomalías
- Seguridad de aplicaciones web

Tu trabajo es ayudar a administradores de sistemas.

Responde de forma profesional, clara y breve.

Pregunta:
{pregunta}
"""

    try:

        response = requests.post(

            f"{OLLAMA_URL}/api/generate",

            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },

            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except requests.RequestException as e:

        return (
            f"Error al conectar con "
            f"Ollama: {str(e)}"
        )