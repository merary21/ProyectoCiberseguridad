# ============================================================
# app.py - BACKEND FLASK DEL SISTEMA SOC-AI
# ============================================================

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS # Importante para evitar bloqueos locales
import joblib
import os
import time
from datetime import datetime
import requests

# ============================================================
# CONFIGURACIÓN DE FLASK
# ============================================================

app = Flask(__name__)
CORS(app) # Habilita CORS para evitar errores de conexión desde el frontend

# ============================================================
# CONFIGURACIÓN DE RUTAS DE MODELOS
# ============================================================

MODEL_PATH = "modelo_guardado/isolation_forest_model.pkl"
SCALER_PATH = "modelo_guardado/scaler.pkl"
ENCODER_PATH = "modelo_guardado/label_encoder_metodo.pkl"
METADATA_PATH = "modelo_guardado/metadata.pkl"

# ============================================================
# VARIABLES DEL SISTEMA
# ============================================================

modelo = None
scaler = None
le_metodo = None
metadata = None
modelo_error = None

# Contadores básicos del sistema
total_eventos = 0
total_alertas = 0
total_normales = 0

# Lista únicamente de alertas detectadas
alertas = []

# ============================================================
# CARGAR MODELO
# ============================================================

def cargar_recursos():
    global modelo, scaler, le_metodo, metadata, modelo_error

    try:
        if not os.path.exists("modelo_guardado"):
            modelo_error = "Error: No existe la carpeta modelo_guardado"
            return

        modelo = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        le_metodo = joblib.load(ENCODER_PATH)
        metadata = joblib.load(METADATA_PATH)

        modelo_error = None
        print("============================================")
        print("SOC-AI: Modelo cargado correctamente")
        print("============================================")

    except Exception as e:
        modelo_error = f"Error al cargar el modelo: {str(e)}"
        print("============================================")
        print("ERROR AL CARGAR EL MODELO")
        print(modelo_error)
        print("============================================")

# Cargar los recursos al iniciar Flask
cargar_recursos()

# ============================================================
# RUTAS DEL FRONTEND
# ============================================================

@app.route("/")
def inicio():
    return render_template("index.html")

# ============================================================
# 1. HEALTH CHECK (Coincide con JS: /api/health)
# ============================================================

@app.route("/api/health", methods=["GET"])
def health():
    if modelo_error:
        return jsonify({
            "status": "error",
            "modelo": "no disponible",
            "error": modelo_error
        }), 500

    return jsonify({
        "status": "ok",
        "servicio": "SOC-AI",
        "modelo": "Isolation Forest"
    })

# ============================================================
# 2. MÉTRICAS (Coincide con JS: /api/metrics)
# ============================================================

@app.route("/api/metrics", methods=["GET"])
def obtener_metricas():
    return jsonify({
        "total": total_eventos,
        "alertas": total_alertas,
        "modelo": "Isolation Forest"
    })

# ============================================================
# 3. ALERTAS (Coincide con JS: /api/alerts)
# ============================================================

@app.route("/api/alerts", methods=["GET"])
def obtener_alertas():
    return jsonify({
        "total": len(alertas),
        "alertas": alertas
    })

# ============================================================
# 4. ANALIZAR TRÁFICO (Coincide con JS: /api/analyze)
# ============================================================

@app.route("/api/analyze", methods=["POST"])
def analizar_trafico():
    global total_eventos, total_alertas, total_normales

    if modelo_error:
        return jsonify({"ok": False, "error": modelo_error}), 500

    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"ok": False, "error": "No se recibieron datos."}), 400

        # Obtener campos
        ip = str(datos.get("ip", "192.168.1.100")).strip()
        metodo = str(datos.get("metodo", "GET")).upper().strip()
        url = str(datos.get("url", "/admin/login")).strip()
        
        try:
            estado = int(datos.get("estado", 200))
            tamano = int(datos.get("tamano", 1500))
            hora = int(datos.get("hora", 12))
        except (ValueError, TypeError):
            return jsonify({"ok": False, "error": "Los valores numéricos son inválidos."}), 400

        # Feature Engineering (Tu lógica original intacta)
        url_length = len(url)
        request_rate = 5.0
        base = 1.5 if metodo == "POST" else 0.5
        duration = base if 200 <= estado < 300 else base * 2.0
        src_bytes = tamano * 0.1 if metodo == "POST" else tamano * 0.01
        dst_bytes = tamano
        num_packets = int((src_bytes + dst_bytes) / 1500) + 1

        # Codificación del método
        metodo_enc = le_metodo.transform([metodo])[0] if metodo in le_metodo.classes_ else 0

        # Codificación del servicio
        url_lower = url.lower()
        if "admin" in url_lower or "wp-admin" in url_lower:
            service_enc = 0
        elif "login" in url_lower or "auth" in url_lower:
            service_enc = 1
        elif "api" in url_lower:
            service_enc = 2
        else:
            service_enc = 4

        # Codificación del estado HTTP
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

        # Datos para el modelo
        input_data = [[duration, src_bytes, dst_bytes, num_packets, url_length, request_rate, estado, metodo_enc, service_enc, flag_enc, hora]]
        input_scaled = scaler.transform(input_data)

        # Predicción
        inicio_proceso = time.perf_counter()
        pred = modelo.predict(input_scaled)[0]
        score = modelo.decision_function(input_scaled)[0]
        fin_proceso = time.perf_counter()
        tiempo_procesamiento = fin_proceso - inicio_proceso

        es_anomalo = (pred == -1)
        total_eventos += 1

        # RESULTADO NORMAL
        if not es_anomalo:
            total_normales += 1
            return jsonify({
                "ok": True,
                "alerta": False,          # Clave que espera el JS
                "sospechoso": False,      # Clave que espera el JS
                "mensaje": "El tráfico se encuentra dentro de los parámetros normales.",
                "score": round(float(score), 4),
                "tiempo_procesamiento": round(tiempo_procesamiento, 6),
                "ip": ip,
                "url": url
            })

        # RESULTADO ANÓMALO
        total_alertas += 1
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        nueva_alerta = {
            "id": len(alertas) + 1,
            "fecha": fecha,
            "timestamp": fecha,         # Clave que espera el JS para la tabla
            "ip": ip,
            "metodo": metodo,
            "url": url,
            "estado": estado,
            "nivel": "high",            # Clave que espera el JS para el badge
            "tipo": "Anomalía detectada",
            "descripcion": f"Comportamiento sospechoso accediendo a {url}",
            "score": round(float(score), 4)
        }

        alertas.insert(0, nueva_alerta)

        return jsonify({
            "ok": True,
            "alerta": True,             # Clave que espera el JS
            "sospechoso": True,         # Clave que espera el JS
            "mensaje": f"Tráfico anómalo detectado. La IP {ip} presenta comportamiento sospechoso accediendo a {url}.",
            "score": round(float(score), 4),
            "tiempo_procesamiento": round(tiempo_procesamiento, 6),
            "ip": ip,
            "url": url
        })

    except Exception as e:
        return jsonify({"ok": False, "error": f"Error en el análisis: {str(e)}"}), 500

# ============================================================
# 5. ASISTENTE IA / ANALISTA (Coincide con JS: /api/ai-analysis)
# ============================================================

@app.route("/api/ai-analysis", methods=["POST"])
def asistente_ia_unificado():
    try:
        datos = request.get_json()
        pregunta = str(datos.get("pregunta", "")).strip()

        if not pregunta:
            return jsonify({"ok": False, "error": "Ingrese una pregunta."}), 400

        texto = pregunta.lower()

        # Lógica del Analista SOC (Respuestas rápidas basadas en reglas)
        if any(p in texto for p in ["qué está pasando", "estado", "resumen", "qué pasa", "sistema"]):
            respuesta = (
                f"📊 Estado del sistema:\n\n"
                f"- Total de eventos: {total_eventos}\n"
                f"- Tráfico normal: {total_normales}\n"
                f"- Alertas detectadas: {total_alertas}\n"
            )
            return jsonify({"ok": True, "respuesta": respuesta})

        elif any(p in texto for p in ["alerta", "ataque", "sospechoso", "intrusión"]):
            respuesta = f"🚨 Análisis de seguridad:\n\nSe han detectado {total_alertas} posibles eventos sospechosos hasta el momento."
            return jsonify({"ok": True, "respuesta": respuesta})

        elif "ip" in texto:
            conteo_ips = {}
            for a in alertas:
                conteo_ips[a["ip"]] = conteo_ips.get(a["ip"], 0) + 1
            top_ips = sorted(conteo_ips.items(), key=lambda x: x[1], reverse=True)[:3]
            
            if top_ips:
                respuesta = "🌐 IPs con más alertas:\n\n" + "\n".join([f"- {ip}: {cantidad} alertas" for ip, cantidad in top_ips])
            else:
                respuesta = "No existen alertas registradas para analizar las IPs."
            return jsonify({"ok": True, "respuesta": respuesta})

        elif "url" in texto:
            conteo_urls = {}
            for a in alertas:
                conteo_urls[a["url"]] = conteo_urls.get(a["url"], 0) + 1
            top_urls = sorted(conteo_urls.items(), key=lambda x: x[1], reverse=True)[:3]
            
            if top_urls:
                respuesta = "🔗 URLs asociadas a alertas:\n\n" + "\n".join([f"- {url}: {cantidad} alertas" for url, cantidad in top_urls])
            else:
                respuesta = "No existen alertas registradas para analizar las URLs."
            return jsonify({"ok": True, "respuesta": respuesta})

        # Si no es una pregunta de estado, consultar a Llama 3.2
        respuesta = consultar_llama(pregunta)
        return jsonify({"ok": True, "respuesta": respuesta})

    except Exception as e:
        return jsonify({"ok": False, "error": f"Error en el asistente IA: {str(e)}"}), 500

# ============================================================
# FUNCIÓN AUXILIAR: LLAMA 3.2
# ============================================================

def consultar_llama(pregunta):
    prompt = f"""
Eres CyberSOC AI, un asistente especializado en ciberseguridad, OWASP Top 10, 
SQL Injection, XSS, DDoS, Fuerza Bruta y detección de anomalías.
Responde de forma profesional, clara y breve a la siguiente consulta de un administrador de sistemas:

Pregunta: {pregunta}
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "No se recibió respuesta de Llama.")
    except requests.exceptions.ConnectionError:
        return "❌ No se pudo conectar con Ollama. Verifique que Ollama esté ejecutándose en localhost:11434."
    except requests.exceptions.Timeout:
        return "❌ La consulta a Llama 3.2 superó el tiempo de espera."
    except Exception as e:
        return f"❌ Error al conectar con Llama 3.2: {str(e)}"

# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)