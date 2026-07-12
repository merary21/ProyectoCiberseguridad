# app.py - SISTEMA DE DETECCIÓN DE INTRUSOS
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import time
import requests

# Configuración de página
st.set_page_config(
    page_title="🛡️ CiberSeguridad - Monitoreo Puerto 80",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"  # ← Esto fuerza que esté abierto al iniciar
)

# --- ESTILOS CSS ---
# --- ESTILOS CSS ---
st.markdown("""
<style>

/* Fondo General */
.stApp{
    background: linear-gradient(135deg,#0f172a,#111827);
    color:white;
}

/* Eliminar línea azul superior y bordes */
.stApp > header {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

.stApp > .block-container {
    padding-top: 0rem !important;
    margin-top: 0 !important;
}

/* Eliminar cualquier borde o línea superior */
[data-testid="stAppViewContainer"] {
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stAppViewContainer"] > .stApp {
    border: none !important;
}

/* Eliminar línea azul del top */
#root > div:nth-child(1) > div > div > div > header {
    display: none !important;
}

/* Título Principal */
.main-header{
    font-size:2.8rem;
    font-weight:bold;
    text-align:center;
    color:#38bdf8;
    text-shadow:0 0 15px rgba(56,189,248,.6);
    margin-bottom:15px;
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Tarjetas */
.card{
    background:#1e293b;
    padding:20px;
    border-radius:15px;
    border:1px solid #334155;
    box-shadow:0 0 15px rgba(0,0,0,.4);
}
            section[data-testid="stSidebar"]{
    background:#0f172a;
}

/* Botones */
.stButton button{
    width:100%;
    background:#0ea5e9;
    color:white;
    border:none;
    border-radius:10px;
    padding:10px;
    font-weight:bold;
}

.stButton button:hover{
    background:#0284c7;
}

/* Métricas */
[data-testid="metric-container"]{
    background:#1e293b;
    border-radius:15px;
    padding:15px;
    border:1px solid #334155;
}

/* Alertas */
.alert-box{
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-size:20px;
    font-weight:bold;
}

.alert-danger{
    background:linear-gradient(135deg,#dc2626,#991b1b);
}

.alert-success{
    background:linear-gradient(135deg,#16a34a,#166534);
}

/* ========== OCULTAR ELEMENTOS DE STREAMLIT ========== */


/* Eliminar padding superior */
.block-container {
    padding-top: 0rem !important;
    margin-top: 0 !important;
}

/* Eliminar border-top azul */
[data-testid="stApp"] {
    border-top: none !important;
}

/* Eliminar cualquier línea o borde superior */
header[data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

/* Forzar eliminar línea azul */
.element-container > div {
    border-top: none !important;
}

/* Eliminar sombras y bordes del contenedor principal */
.main .block-container {
    padding-top: 0rem !important;
    margin-top: -1rem !important;
}

</style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.markdown('<div class="main-header">🛡️ SOC-AI</div>', unsafe_allow_html=True)
st.markdown("<center><h3>Security Operations Center con Inteligencia Artificial</h3></center>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align:center;
                background:#1e293b;
                padding:12px;
                border-radius:12px;
                border:1px solid #334155;
                margin-bottom:20px'>
        🟢 Monitoreo Activo
    </div>
    """, unsafe_allow_html=True)

# --- CARGA DEL MODELO ---
@st.cache_resource
def cargar_recursos():
    if not os.path.exists("modelo_guardado"):
        return None, None, None, None, "Error: No existe la carpeta modelo_guardado"
    try:
        modelo = joblib.load("modelo_guardado/isolation_forest_model.pkl")
        scaler = joblib.load("modelo_guardado/scaler.pkl")
        le_metodo = joblib.load("modelo_guardado/label_encoder_metodo.pkl")
        metadata = joblib.load("modelo_guardado/metadata.pkl")
        return modelo, scaler, le_metodo, metadata, None
    except Exception as e:
        return None, None, None, None, f"Error al cargar: {e}"

modelo, scaler, le_metodo, metadata, error_msg = cargar_recursos()

if error_msg:
    st.error(error_msg)
    st.stop()

# --- SIDEBAR: ENTRADA DE DATOS ---
with st.sidebar:
    st.header("📝 Ingresar Tráfico")
    st.markdown("Simula una conexión HTTP:")
    
    ip = st.text_input("IP Origen", "192.168.1.100")
    metodo = st.selectbox("Método", ["GET", "POST", "HEAD", "PUT"])
    url = st.text_input("URL", "/admin/login")
    estado = st.number_input("Estado HTTP", min_value=100, max_value=599, value=200, step=1)
    tamano = st.number_input("Tamaño (bytes)", min_value=0, value=1500, step=50)
    hora = st.slider("Hora del día", 0, 23, 12)
    
    btn_analizar = st.button("🔍 Analizar Tráfico", type="primary", use_container_width=True)

# --- HISTORIAL (SESSION STATE) ---
if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- LÓGICA DE PREDICCIÓN ---
if btn_analizar:
    with st.spinner("Analizando patrones..."):
        time.sleep(0.5)
        
        try:
            # Feature Engineering
            url_length = len(url)
            request_rate = 5.0
            base = 1.5 if metodo == "POST" else 0.5
            duration = base if 200 <= estado < 300 else base * 2.0
            src_bytes = tamano * 0.1 if metodo == "POST" else tamano * 0.01
            dst_bytes = tamano
            num_packets = int((src_bytes + dst_bytes) / 1500) + 1
            metodo_enc = le_metodo.transform([metodo])[0] if metodo in le_metodo.classes_ else 0
            
            url_lower = url.lower()
            if 'admin' in url_lower or 'wp-admin' in url_lower: 
                service_enc = 0
            elif 'login' in url_lower or 'auth' in url_lower: 
                service_enc = 1
            elif 'api' in url_lower: 
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
                duration, src_bytes, dst_bytes, num_packets, 
                url_length, request_rate, estado, 
                metodo_enc, service_enc, flag_enc, hora
            ]]
            
            # Predicción
            input_scaled = scaler.transform(input_data)
            pred = modelo.predict(input_scaled)[0]
            score = modelo.decision_function(input_scaled)[0]
            es_anomalo = (pred == -1)
            
            # Guardar en historial
            registro = {
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Hora": datetime.now().strftime("%H:%M:%S"),
                "IP": ip,
                "Método": metodo,
                "URL": url,
                "Estado": estado,
                "Resultado": "🚨 ALERTA" if es_anomalo else "✅ OK",
                "Score": f"{score:.4f}"
            }
            st.session_state.historial.insert(0, registro)
            
            # Mostrar Resultado
            if es_anomalo:
                st.markdown(f'<div class="alert-box alert-danger">🚨 TRÁFICO ANÓMALO DETECTADO<br>Score: {score:.4f}</div>', unsafe_allow_html=True)
                st.warning(f"**Recomendación:** La IP `{ip}` presenta comportamiento sospechoso accediendo a `{url}`.")
            else:
                st.markdown(f'<div class="alert-box alert-success">✅ Tráfico Normal<br>Score: {score:.4f}</div>', unsafe_allow_html=True)
                st.success("El tráfico se encuentra dentro de los parámetros normales.")

        except Exception as e:
            st.error(f"Error en el análisis: {e}")

# ============================================
# IA LOCAL - LLAMA 3.2
# ============================================

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
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        return response.json()["response"]

    except Exception as e:

        return f"❌ Error al conectar con Llama 3.2: {str(e)}"

# --- TABLERO DE RESULTADOS ---
st.markdown("### 📊 Panel de Monitoreo")

total = len(st.session_state.historial)
alertas = len([x for x in st.session_state.historial if "ALERTA" in x["Resultado"]])
normales = total - alertas
riesgo = (alertas/total)*100 if total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Eventos Analizados", total)
col2.metric("🚨 Alertas Detectadas", alertas)
col3.metric("✅ Tráfico Normal", normales)
col4.metric("⚠️ Riesgo", f"{riesgo:.1f}%")

# --- REGISTRO DE ALERTAS ---
st.markdown("### 🚨 Registro de Alertas")

if st.session_state.historial:
    df = pd.DataFrame(st.session_state.historial)
    
    # Filtrar solo alertas
    alertas_df = df[df["Resultado"].str.contains("ALERTA", na=False)]
    
    if not alertas_df.empty:
        st.dataframe(
            alertas_df[["Fecha", "IP", "URL", "Estado", "Score"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay alertas registradas aún. ¡El sistema está funcionando correctamente!")
    
    # Tabla completa con colores
    st.markdown("### 📋 Historial Completo")
    
    def colorear_alerta(valor):
        if "ALERTA" in str(valor):
            return "background-color:#dc2626;color:white"
        return "background-color:#16a34a;color:white"

    st.dataframe(
        df.style.map(colorear_alerta, subset=["Resultado"]),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("📭 No hay datos en el historial. Usa el panel lateral para analizar tráfico.")

# --- ASISTENTE VIRTUAL ---
st.markdown("### 🤖 Analista SOC Virtual")

with st.expander("💬 Haz una pregunta al sistema"):
    st.markdown("""
    **Ejemplos de preguntas:**
    - ¿Qué está pasando en el sistema?
    - ¿Hay tráfico sospechoso?
    - ¿Cuántas alertas hay?
    - ¿Qué IPs son las más activas?
    - ¿Resumen del tráfico?
    """)

    pregunta = st.text_input("Escribe tu pregunta:")

    if st.button("Consultar asistente"):
        if not st.session_state.historial:
            st.warning("No hay datos aún para analizar.")
        else:
            df = pd.DataFrame(st.session_state.historial)
            texto = pregunta.lower()
            
            alertas_count = len(df[df["Resultado"].str.contains("ALERTA", na=False)])
            total_reg = len(df)
            normales_count = total_reg - alertas_count
            
            top_ips = df["IP"].value_counts().head(3)
            top_urls = df["URL"].value_counts().head(3)

            if any(x in texto for x in ["qué está pasando", "estado", "resumen", "qué pasa", "sistema"]):
                respuesta = (f"📊 **Estado del sistema:**\n\n"
                           f"- Total de eventos: {total_reg}\n"
                           f"- Tráfico normal: {normales_count}\n"
                           f"- Alertas detectadas: {alertas_count}\n")

            elif any(x in texto for x in ["alerta", "ataque", "sospechoso", "intrusión"]):
                respuesta = (f"🚨 **Análisis de seguridad:**\n\n"
                           f"Se han detectado **{alertas_count} posibles eventos sospechosos**.\n"
                           f"Revisa las IPs con mayor actividad anómala.")

            elif "ip" in texto:
                respuesta = "🌐 **IPs más activas:**\n\n" + "\n".join(
                    [f"- {ip}: {count} eventos" for ip, count in top_ips.items()])

            elif "url" in texto:
                respuesta = "🔗 **URLs más consultadas:**\n\n" + "\n".join(
                    [f"- {url}: {count} veces" for url, count in top_urls.items()])

            elif any(x in texto for x in ["ayuda", "qué puedo preguntar", "como usar"]):
                respuesta = ("🧠 **Puedes preguntarme:**\n\n"
                           "- Estado del sistema\n"
                           "- Alertas detectadas\n"
                           "- IPs más activas\n"
                           "- URLs más consultadas")
            else:
                respuesta = (f"🤖 **¡Hola! Soy SOC-AI, tu asistente virtual de ciberseguridad.**\n\n"
                            f"Soy una inteligencia artificial diseñada para ayudarte a:\n"
                          f"💡 **Puedes preguntarme cosas como:**\n"
                            "- *¿Qué está pasando en el sistema?*\n"
                            "- *¿Hay tráfico sospechoso?*\n"
                            "- *¿Cuántas alertas hay?*\n"
                            "- *¿Qué IPs son las más activas?*\n"
                            "- *¿Qué URLs han sido más consultadas?*\n"
                            "- *¿Hay ataques detectados?*\n\n"
                            "¡Estoy aquí para ayudarte a mantener tu red segura! 🔒"
                        )


            st.chat_message("user").write(pregunta)
            st.chat_message("assistant").write(respuesta)
# ============================================
# ASISTENTE DE CIBERSEGURIDAD IA
# ============================================

st.markdown("---")

st.subheader("🤖 Asistente de Ciberseguridad IA")

st.info(
    "Consulta sobre URLs, IPs, ataques, vulnerabilidades y eventos sospechosos."
)

pregunta_ia = st.text_area(
    "Escribe tu consulta:",
    height=120,
    placeholder="Ejemplo: ¿La URL /wp-admin.php puede indicar un ataque?"
)

if st.button("Consultar IA"):

    if pregunta_ia.strip() == "":

        st.warning("Ingrese una pregunta.")

    else:

        with st.spinner("Analizando consulta..."):

            respuesta = consultar_llama(pregunta_ia)

        st.chat_message("user").write(pregunta_ia)

        st.chat_message("assistant").write(respuesta)

# --- FOOTER ---
st.markdown("---")
st.markdown("## 🧠 Información del Sistema")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("Modelo IA\n\nIsolation Forest")
with col2:
    st.info("Dataset\n\n3,000 registros")
with col3:
    st.info("Objetivo\n\nDetección de anomalías")

st.caption("SOC-AI | Sistema Inteligente de Ciberseguridad Preventiva | Detección de Anomalías con Isolation Forest")