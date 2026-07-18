from fastapi import FastAPI
from schemas import WebRequest

import joblib
from datetime import datetime


# ==============================
# CARGA DEL MODELO
# ==============================

modelo = joblib.load(
    "../modelo_guardado/isolation_forest_model.pkl"
)

scaler = joblib.load(
    "../modelo_guardado/scaler.pkl"
)

le_metodo = joblib.load(
    "../modelo_guardado/label_encoder_metodo.pkl"
)


# ==============================
# APLICACIÓN
# ==============================

app = FastAPI(
    title="SOC-AI API",
    description="API de detección inteligente de anomalías en tráfico web",
    version="2.0.0"
)


# ==============================
# HEALTH
# ==============================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "SOC-AI API"
    }


# ==============================
# METADATA
# ==============================

@app.get("/metadata")
def metadata():

    return {
        "project": "SOC-AI",
        "version": "2.0.0",
        "model": "Isolation Forest",
        "assistant": "Llama 3.2 mediante Ollama",
        "purpose": "Detección de anomalías en tráfico web"
    }


# ==============================
# ANÁLISIS INTELIGENTE
# ==============================

@app.post("/analyze")
def analyze(request: WebRequest):

    ip = request.ip
    metodo = request.method
    url = request.url
    estado = request.status_code
    tamano = request.response_size

    hora = datetime.now().hour

    url_length = len(url)

    request_rate = 5.0

    base = 1.5 if metodo == "POST" else 0.5

    duration = (
        base
        if 200 <= estado < 300
        else base * 2.0
    )

    src_bytes = (
        tamano * 0.1
        if metodo == "POST"
        else tamano * 0.01
    )

    dst_bytes = tamano

    num_packets = int(
        (src_bytes + dst_bytes) / 1500
    ) + 1

    metodo_enc = (
        le_metodo.transform([metodo])[0]
        if metodo in le_metodo.classes_
        else 0
    )

    url_lower = url.lower()

    if "admin" in url_lower or "wp-admin" in url_lower:
        service_enc = 0

    elif "login" in url_lower or "auth" in url_lower:
        service_enc = 1

    elif "api" in url_lower:
        service_enc = 2

    else:
        service_enc = 4

    if estado == 200:
        flag_enc = 0

    elif estado in [301, 302, 304]:
        flag_enc = 1

    elif estado in [401, 403]:
        flag_enc = 2

    elif estado == 404:
        flag_enc = 3

    else:
        flag_enc = 4

    input_data = [[
        duration,
        src_bytes,
        dst_bytes,
        num_packets,
        url_length,
        request_rate,
        estado,
        metodo_enc,
        service_enc,
        flag_enc,
        hora
    ]]

    input_scaled = scaler.transform(input_data)

    pred = modelo.predict(input_scaled)[0]

    score = modelo.decision_function(input_scaled)[0]

    es_anomalo = pred == -1

    if es_anomalo:

        return {
            "resultado": "ALERTA",
            "nivel_riesgo": "ALTO",
            "anomalia": True,
            "score": round(float(score), 4),
            "ip": ip,
            "url": url,
            "mensaje": "Se detectó un comportamiento anómalo"
        }

    else:

        return {
            "resultado": "NORMAL",
            "nivel_riesgo": "BAJO",
            "anomalia": False,
            "score": round(float(score), 4),
            "ip": ip,
            "url": url,
            "mensaje": "El tráfico se encuentra dentro de los parámetros normales"
        }