import json
import os
import platform
import sys
from datetime import datetime


ARCHIVO_BASE = "linea_base.json"


def guardar_linea_base(metricas):

    # ============================================================
    # CALCULAR PORCENTAJE DE ANOMALÍAS
    # ============================================================

    total_analizado = metricas.get(
        "total_analizado",
        0
    )

    anomalias = metricas.get(
        "anomalias",
        0
    )

    porcentaje_anomalias = (
        (anomalias / total_analizado) * 100
        if total_analizado > 0
        else 0
    )


    # ============================================================
    # CALCULAR PORCENTAJE DE TRÁFICO NORMAL
    # ============================================================

    normales = metricas.get(
        "normales",
        0
    )

    porcentaje_normales = (
        (normales / total_analizado) * 100
        if total_analizado > 0
        else 0
    )


    # ============================================================
    # CREAR LÍNEA BASE
    # ============================================================

    datos = {

        "fecha":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),


        # ========================================
        # AMBIENTE
        # ========================================

        "ambiente": {

            "sistema_operativo":
                platform.system()
                + " "
                + platform.release(),

            "python":
                sys.version.split()[0],

            "framework":
                "Streamlit",

            "modo":
                "Ejecución local"
        },


        # ========================================
        # ENDPOINT
        # ========================================

        "endpoint": {

            "tipo":
                "Interfaz Streamlit",

            "ruta":
                "SOC-AI / Analizar Tráfico",

            "metodo":
                "Simulación de solicitud HTTP"
        },


        # ========================================
        # PAYLOAD
        # ========================================

        "payload": {

            "ip":
                "192.168.1.100",

            "metodo":
                "GET",

            "url":
                "/index.html",

            "estado":
                200,

            "tamano":
                1500,

            "hora":
                12
        },


        # ========================================
        # VERSIONES
        # ========================================

        "version_codigo":
            "SOC-AI v1.0",

        "componente_ia":
            "Isolation Forest",

        "version_componente_ia":
            "Modelo entrenado - isolation_forest_model.pkl",


        # ========================================
        # EJECUCIÓN
        # ========================================

        "herramienta":
            "Streamlit + Python",

        "cantidad_solicitudes":
            total_analizado,


        # ========================================
        # MÉTRICAS
        # ========================================

        "anomalias":
            anomalias,

        "normales":
            normales,

        "alertas":
            metricas.get(
                "alertas",
                0
            ),

        "errores":
            metricas.get(
                "errores",
                0
            ),

        "porcentaje_anomalias":
            porcentaje_anomalias,

        "porcentaje_normales":
            porcentaje_normales,

        "tiempo_promedio":
            metricas.get(
                "tiempo_promedio",
                0
            ),

        "p50":
            metricas.get(
                "p50",
                0
            ),

        "p95":
            metricas.get(
                "p95",
                0
            ),

        "tiempo_maximo":
            metricas.get(
                "tiempo_maximo",
                0
            ),

        "tasa_error":
            metricas.get(
                "tasa_error",
                0
            ),

        "riesgo":
            metricas.get(
                "riesgo",
                0
            )
    }


    # ============================================================
    # GUARDAR ARCHIVO JSON
    # ============================================================

    with open(
        ARCHIVO_BASE,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )


    return datos


def cargar_linea_base():

    # ============================================================
    # VERIFICAR SI EXISTE EL ARCHIVO
    # ============================================================

    if not os.path.exists(
        ARCHIVO_BASE
    ):

        return None


    # ============================================================
    # CARGAR JSON
    # ============================================================

    with open(
        ARCHIVO_BASE,
        "r",
        encoding="utf-8"
    ) as archivo:

        datos = json.load(
            archivo
        )


    # ============================================================
    # COMPATIBILIDAD CON LÍNEAS BASE ANTIGUAS
    # ============================================================

    if "porcentaje_anomalias" not in datos:

        total = datos.get(
            "cantidad_solicitudes",
            0
        )

        anomalias = datos.get(
            "anomalias",
            0
        )

        datos["porcentaje_anomalias"] = (
            (anomalias / total) * 100
            if total > 0
            else 0
        )


    if "porcentaje_normales" not in datos:

        total = datos.get(
            "cantidad_solicitudes",
            0
        )

        normales = datos.get(
            "normales",
            0
        )

        datos["porcentaje_normales"] = (
            (normales / total) * 100
            if total > 0
            else 0
        )


    return datos