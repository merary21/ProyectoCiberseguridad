# ============================================================
# metricas.py - MÉTRICAS Y EVOLUCIÓN DEL SOC-AI
# ============================================================

import streamlit as st
import pandas as pd

from metricas import MetricasSOC
from linea_base import guardar_linea_base, cargar_linea_base
from historial import cargar_historial


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="📊 Métricas - SOC-AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#111827);
    color:white;
}

.stApp > header {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

.block-container {
    padding-top: 1rem !important;
}

[data-testid="stAppViewContainer"] {
    border: none !important;
    box-shadow: none !important;
}

.main-header{
    font-size:2.8rem;
    font-weight:bold;
    text-align:center;
    color:#38bdf8;
    text-shadow:0 0 15px rgba(56,189,248,.6);
    margin-bottom:15px;
}

[data-testid="metric-container"]{
    background:#1e293b;
    border-radius:15px;
    padding:15px;
    border:1px solid #334155;
}

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

</style>
""", unsafe_allow_html=True)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="main-header">📊 SOC-AI - Métricas y Evolución</div>',
    unsafe_allow_html=True
)

st.markdown(
    "<center><h3>Observabilidad, línea base e indicadores de seguridad</h3></center>",
    unsafe_allow_html=True
)

st.markdown("""
<div style='text-align:center;
            background:#1e293b;
            padding:12px;
            border-radius:12px;
            border:1px solid #334155;
            margin-bottom:20px'>
    📊 Panel de medición y evolución del riesgo
</div>
""", unsafe_allow_html=True)


# ============================================================
# BOTÓN PARA REGRESAR AL MONITOREO
# ============================================================

if st.button("⬅️ Volver al Monitoreo SOC-AI", use_container_width=True):
    st.switch_page("app.py")


# ============================================================
# MÉTRICAS DEL SOC-AI
# ============================================================

if "metricas_soc" not in st.session_state:
    st.session_state.metricas_soc = MetricasSOC()

metricas = st.session_state.metricas_soc

resumen_metricas = metricas.obtener_resumen()


# ============================================================
# OBTENER HISTORIAL PERMANENTE
# ============================================================

historial_metricas = cargar_historial()

if historial_metricas:
    df_metricas = pd.DataFrame(historial_metricas)
else:
    df_metricas = pd.DataFrame()


# ============================================================
# CÁLCULO DE DATOS ACTUALES
# ============================================================

total = 0
alertas = 0
normales = 0
riesgo = 0

if "historial" in st.session_state:
    total = len(st.session_state.historial)

    alertas = len([
        x for x in st.session_state.historial
        if "ALERTA" in x.get("Resultado", "")
    ])

    normales = total - alertas

    riesgo = (
        (alertas / total) * 100
        if total > 0
        else 0
    )

porcentaje_anomalias = resumen_metricas.get(
    "porcentaje_anomalias",
    0
)

porcentaje_normales = resumen_metricas.get(
    "porcentaje_normales",
    0
)

tiempo_promedio = resumen_metricas.get(
    "tiempo_promedio",
    0
)

p50 = resumen_metricas.get("p50", 0)
p95 = resumen_metricas.get("p95", 0)
tiempo_maximo = resumen_metricas.get("tiempo_maximo", 0)
tasa_error = resumen_metricas.get("tasa_error", 0)


# ============================================================
# RESUMEN ACTUAL
# ============================================================

st.markdown("## 📊 Resumen Actual")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📊 Eventos Analizados",
    total
)

col2.metric(
    "🚨 Alertas Detectadas",
    alertas
)

col3.metric(
    "✅ Tráfico Normal",
    normales
)

col4.metric(
    "⚠️ Riesgo",
    f"{riesgo:.1f}%"
)

col5.metric(
    "⏱️ Tiempo Promedio",
    f"{tiempo_promedio:.6f}s"
)


# ============================================================
# INDICADORES DE DETECCIÓN
# ============================================================

st.markdown("---")
st.markdown("## 📈 Indicadores de Detección")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Porcentaje de anomalías",
        f"{porcentaje_anomalias:.2f}%"
    )

with col2:
    st.metric(
        "Porcentaje de tráfico normal",
        f"{porcentaje_normales:.2f}%"
    )


# ============================================================
# MÉTRICAS DE RENDIMIENTO
# ============================================================

st.markdown("## ⚡ Métricas de Rendimiento")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "P50",
    f"{p50:.6f}s"
)

col2.metric(
    "P95",
    f"{p95:.6f}s"
)

col3.metric(
    "Tiempo máximo",
    f"{tiempo_maximo:.6f}s"
)

col4.metric(
    "Tasa de error",
    f"{tasa_error:.2f}%"
)


# ============================================================
# LÍNEA BASE
# ============================================================

st.markdown("---")
st.markdown("## 📏 Línea Base del SOC-AI")

base_actual = cargar_linea_base()

if base_actual:

    st.info(
        f"📌 Línea base registrada el "
        f"{base_actual['fecha']}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Anomalías base",
        f"{base_actual['porcentaje_anomalias']:.2f}%"
    )

    col2.metric(
        "Riesgo base",
        f"{base_actual['riesgo']:.2f}%"
    )

    col3.metric(
        "Tiempo base",
        f"{base_actual['tiempo_promedio']:.6f}s"
    )

else:

    st.warning(
        "⚠️ Todavía no existe una línea base."
    )


# ============================================================
# ESTABLECER LÍNEA BASE
# ============================================================

st.markdown("### 📌 Gestión de Línea Base")

if st.button(
    "📌 Establecer / Actualizar línea base",
    use_container_width=True
):

    if total == 0:

        st.warning(
            "Debe analizar tráfico antes "
            "de establecer la línea base."
        )

    else:

        base = guardar_linea_base(
            resumen_metricas
        )

        st.success(
            "✅ Línea base establecida correctamente."
        )

        st.json(base)


# ============================================================
# COMPARACIÓN CON LÍNEA BASE
# ============================================================

base_actual = cargar_linea_base()

if base_actual and total > 0:

    st.markdown("### 📊 Comparación con Línea Base")

    diferencia_anomalias = (
        porcentaje_anomalias
        - base_actual["porcentaje_anomalias"]
    )

    diferencia_riesgo = (
        riesgo
        - base_actual["riesgo"]
    )

    diferencia_tiempo = (
        tiempo_promedio
        - base_actual["tiempo_promedio"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Cambio en anomalías",
        f"{diferencia_anomalias:+.2f}%"
    )

    col2.metric(
        "Cambio en riesgo",
        f"{diferencia_riesgo:+.2f}%"
    )

    col3.metric(
        "Cambio en tiempo",
        f"{diferencia_tiempo:+.6f}s"
    )


# ============================================================
# HISTORIAL DE MEDICIONES
# ============================================================

st.markdown("---")
st.markdown("## 📚 Historial de Mediciones")

if historial_metricas:

    st.dataframe(
        df_metricas,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Todavía no existen mediciones históricas."
    )


# ============================================================
# EVOLUCIÓN DEL RIESGO
# ============================================================

st.markdown("---")
st.markdown("## 📈 Evolución del Riesgo")

if historial_metricas and "fecha" in df_metricas.columns:

    st.line_chart(
        df_metricas.set_index("fecha")["riesgo"]
    )

    st.caption(
        "La gráfica muestra cómo ha evolucionado "
        "el porcentaje de riesgo registrado en las mediciones."
    )

else:

    st.info(
        "No hay suficientes mediciones para mostrar "
        "la evolución del riesgo."
    )


# ============================================================
# EVOLUCIÓN DE ANOMALÍAS
# ============================================================

st.markdown("---")
st.markdown("## 📈 Evolución de Anomalías")

if (
    historial_metricas
    and "fecha" in df_metricas.columns
    and "porcentaje_anomalias" in df_metricas.columns
):

    st.line_chart(
        df_metricas.set_index("fecha")["porcentaje_anomalias"]
    )

    st.caption(
        "La gráfica muestra la evolución del porcentaje "
        "de anomalías detectadas."
    )

else:

    st.info(
        "No hay suficientes mediciones para mostrar "
        "la evolución de anomalías."
    )


# ============================================================
# CONCLUSIÓN DEL PANEL
# ============================================================

st.markdown("---")
st.markdown("## 🧠 Interpretación")

if total == 0:

    st.info(
        "El sistema todavía no tiene eventos analizados. "
        "Regresa al monitoreo, analiza tráfico y luego "
        "consulta nuevamente este panel."
    )

elif riesgo >= 50:

    st.error(
        f"🚨 El nivel de riesgo actual es de {riesgo:.2f}%. "
        "Se recomienda revisar las alertas y comparar "
        "los indicadores con la línea base."
    )

elif riesgo > 0:

    st.warning(
        f"⚠️ El sistema presenta un nivel de riesgo de "
        f"{riesgo:.2f}%. Se recomienda continuar con el "
        "monitoreo de las anomalías."
    )

else:

    st.success(
        "✅ Actualmente no se han registrado anomalías "
        "en los eventos analizados."
    )


st.caption(
    "SOC-AI | Sistema Inteligente de Ciberseguridad Preventiva | "
    "Observabilidad y detección de anomalías con Isolation Forest"
)