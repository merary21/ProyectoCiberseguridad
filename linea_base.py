import json
import os
import platform
import sys
from datetime import datetime


ARCHIVO_BASE = "linea_base.json"


def guardar_linea_base(metricas):

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
            metricas["total_analizado"],


        # ========================================
        # MÉTRICAS
        # ========================================

        "anomalias":
            metricas["anomalias"],

        "normales":
            metricas["normales"],

        "alertas":
            metricas["alertas"],

        "errores":
            metricas["errores"],

        "tiempo_promedio":
            metricas["tiempo_promedio"],

        "p50":
            metricas["p50"],

        "p95":
            metricas["p95"],

        "tiempo_maximo":
            metricas["tiempo_maximo"],

        "tasa_error":
            metricas["tasa_error"],

        "riesgo":
            metricas["riesgo"]
    }


    with open(
        ARCHIVO_BASE,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4
        )


    return datos


def cargar_linea_base():

    if not os.path.exists(
        ARCHIVO_BASE
    ):

        return None


    with open(
        ARCHIVO_BASE,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(
            archivo
        )