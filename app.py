# ============================================================
# app.py - BACKEND FLASK DEL SISTEMA SOC-AI
# ============================================================

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS # Importante para evitar bloqueos locales
from flask_login import LoginManager, login_required
from dotenv import load_dotenv
import joblib
import os
import re
import time
from datetime import datetime
import requests

from models import db, Usuario
from auth import auth_bp

load_dotenv()

# ============================================================
# CONFIGURACIÓN DE FLASK
# ============================================================

app = Flask(__name__)
CORS(app) # Habilita CORS para evitar errores de conexión desde el frontend

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(auth_bp)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Inicia sesión para acceder a SOC-AI."
login_manager.login_message_category = "error"
login_manager.init_app(app)


@login_manager.user_loader
def cargar_usuario(usuario_id):
    return db.session.get(Usuario, int(usuario_id))


with app.app_context():
    db.create_all()

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
@login_required
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
@login_required
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
@login_required
def obtener_alertas():
    return jsonify({
        "total": len(alertas),
        "alertas": alertas
    })

# ============================================================
# 4. ANALIZAR TRÁFICO (Coincide con JS: /api/analyze)
# ============================================================

@app.route("/api/analyze", methods=["POST"])
@login_required
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

# ============================================================
# 5. ASISTENTES IA
# ============================================================

@app.route("/api/ai-analysis", methods=["POST"])
@login_required
def asistente_ia_unificado():

    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                "ok": False,
                "error": "No se recibieron datos."
            }), 400

        pregunta = str(datos.get("pregunta", "")).strip()
        tipo = str(datos.get("tipo", "ciberseguridad")).lower().strip()

        if not pregunta:
            return jsonify({
                "ok": False,
                "error": "Ingrese una pregunta."
            }), 400

        # ========================================================
        # ASISTENTE DE CIBERSEGURIDAD
        # ========================================================
        if tipo == "ciberseguridad":

            respuesta = consultar_llama(pregunta)

            return jsonify({
                "ok": True,
                "respuesta": respuesta,
                "asistente": "Llama 3.2"
            })

        # ========================================================
        # ANALISTA SOC
        # ========================================================
        if tipo == "soc":

            texto = pregunta.lower()

            # Estado general del sistema
            if any(p in texto for p in [
                "qué está pasando",
                "estado",
                "resumen",
                "qué pasa",
                "sistema"
            ]):

                respuesta = (
                    "📊 Estado del sistema:\n\n"
                    f"- Total de eventos: {total_eventos}\n"
                    f"- Tráfico normal: {total_normales}\n"
                    f"- Alertas detectadas: {total_alertas}"
                )

                return jsonify({
                    "ok": True,
                    "respuesta": respuesta,
                    "asistente": "Analista SOC"
                })

            # IP (se evalúa antes que "alertas/ataques" porque preguntas
            # naturales como "¿qué IP tiene más alertas?" contienen esa
            # palabra y antes caían siempre en la rama genérica)
            elif re.search(r"\bip\b", texto):

                conteo_ips = {}

                for alerta in alertas:
                    ip = alerta.get("ip", "N/A")
                    conteo_ips[ip] = conteo_ips.get(ip, 0) + 1

                top_ips = sorted(
                    conteo_ips.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]

                if top_ips:

                    respuesta = (
                        "🌐 IPs con más alertas:\n\n" +
                        "\n".join(
                            [
                                f"- {ip}: {cantidad} alertas"
                                for ip, cantidad in top_ips
                            ]
                        )
                    )

                else:

                    respuesta = (
                        "No existen alertas registradas "
                        "para analizar las IPs."
                    )

                return jsonify({
                    "ok": True,
                    "respuesta": respuesta,
                    "asistente": "Analista SOC"
                })

            # URL
            elif re.search(r"\burl\b", texto):

                conteo_urls = {}

                for alerta in alertas:
                    url = alerta.get("url", "N/A")
                    conteo_urls[url] = conteo_urls.get(url, 0) + 1

                top_urls = sorted(
                    conteo_urls.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:3]

                if top_urls:

                    respuesta = (
                        "🔗 URLs asociadas a alertas:\n\n" +
                        "\n".join(
                            [
                                f"- {url}: {cantidad} alertas"
                                for url, cantidad in top_urls
                            ]
                        )
                    )

                else:

                    respuesta = (
                        "No existen alertas registradas "
                        "para analizar las URLs."
                    )

                return jsonify({
                    "ok": True,
                    "respuesta": respuesta,
                    "asistente": "Analista SOC"
                })

            # Alertas / ataques (rama genérica, evaluada al final para
            # no capturar preguntas más específicas de IP o URL)
            elif any(p in texto for p in [
                "alerta",
                "ataque",
                "sospechoso",
                "intrusión",
                "intrusion"
            ]):

                respuesta = (
                    "🚨 Análisis de seguridad:\n\n"
                    f"Se han detectado {total_alertas} "
                    "posibles eventos sospechosos hasta el momento."
                )

                return jsonify({
                    "ok": True,
                    "respuesta": respuesta,
                    "asistente": "Analista SOC"
                })

            # Pregunta del SOC no reconocida
            else:

                respuesta = (
                    "No encontré información específica en los datos "
                    "actuales del SOC para responder esa pregunta."
                )

                return jsonify({
                    "ok": True,
                    "respuesta": respuesta,
                    "asistente": "Analista SOC"
                })

        # ========================================================
        # TIPO DESCONOCIDO
        # ========================================================

        return jsonify({
            "ok": False,
            "error": "Tipo de asistente no válido."
        }), 400

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": f"Error en el asistente IA: {str(e)}"
        }), 500

# ============================================================
# FUNCIÓN AUXILIAR: LLAMA 3.2
# ============================================================

def consultar_llama(pregunta):

    prompt = f"""
Eres CyberSOC AI, un asistente especializado en ciberseguridad.

Tu función es responder preguntas relacionadas con:

- Ciberseguridad
- Seguridad web
- OWASP Top 10
- SQL Injection
- XSS
- DDoS
- Fuerza Bruta
- Ataques web
- Vulnerabilidades
- Seguridad de servidores
- Redes
- HTTP y HTTPS
- Protección de aplicaciones web
- Detección de anomalías

IMPORTANTE:

Responde directamente la pregunta del usuario.

No inventes alertas del sistema.

No digas que no existen alertas a menos que la pregunta
específicamente solicite información sobre las alertas del SOC.

Si el usuario pregunta por un concepto de ciberseguridad,
explícalo claramente.

Si pregunta por riesgos, menciona los principales riesgos
y después proporciona recomendaciones de seguridad.

Si la pregunta del usuario NO está relacionada con
ciberseguridad, seguridad informática o los temas listados
arriba, NO la respondas. En su lugar, indica claramente que
eres CyberSOC AI, un asistente especializado únicamente en
ciberseguridad, que ese tema está fuera de tu enfoque, y
sugiere que reformule su pregunta hacia temas de seguridad
informática.

Responde en español.

Pregunta del usuario:

{pregunta}

Respuesta:
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",

            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },

            timeout=60
        )

        response.raise_for_status()

        resultado = response.json()

        return resultado.get(
            "response",
            "No se recibió respuesta de Llama 3.2."
        )

    except requests.exceptions.ConnectionError:

        return (
            "❌ No se pudo conectar con Ollama. "
            "Verifique que Ollama esté ejecutándose "
            "en localhost:11434."
        )

    except requests.exceptions.Timeout:

        return (
            "❌ La consulta a Llama 3.2 "
            "superó el tiempo de espera."
        )

    except Exception as e:

        return f"❌ Error al conectar con Llama 3.2: {str(e)}"

# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)