import json
import os
from datetime import datetime


ARCHIVO_BASE = "linea_base.json"


def guardar_linea_base(metricas):
    datos = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_analizado": metricas["total_analizado"],
        "anomalias": metricas["anomalias"],
        "normales": metricas["normales"],
        "alertas": metricas["alertas"],
        "porcentaje_anomalias": metricas["porcentaje_anomalias"],
        "porcentaje_normales": metricas["porcentaje_normales"],
        "tiempo_promedio": metricas["tiempo_promedio"],
        "riesgo": metricas["riesgo"]
    }

    with open(ARCHIVO_BASE, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)

    return datos


def cargar_linea_base():
    if not os.path.exists(ARCHIVO_BASE):
        return None

    with open(ARCHIVO_BASE, "r", encoding="utf-8") as archivo:
        return json.load(archivo)