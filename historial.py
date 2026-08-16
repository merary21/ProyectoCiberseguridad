import json
import os
from datetime import datetime


ARCHIVO_HISTORIAL = "historial_metricas.json"


def guardar_resultado(metricas):
    historial = []

    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            historial = json.load(archivo)

    registro = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        **metricas
    }

    historial.append(registro)

    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4)

    return registro


def cargar_historial():
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return []

    with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
        return json.load(archivo)