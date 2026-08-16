import time


class MetricasSOC:
    def __init__(self):
        self.total_analizado = 0
        self.anomalias = 0
        self.normales = 0
        self.alertas = 0
        self.tiempos = []

    def iniciar_medicion(self):
        return time.perf_counter()

    def registrar_resultado(self, es_anomalia, tiempo):
        self.total_analizado += 1
        self.tiempos.append(tiempo)

        if es_anomalia:
            self.anomalias += 1
            self.alertas += 1
        else:
            self.normales += 1

    def porcentaje_anomalias(self):
        if self.total_analizado == 0:
            return 0

        return (self.anomalias / self.total_analizado) * 100

    def porcentaje_normales(self):
        if self.total_analizado == 0:
            return 0

        return (self.normales / self.total_analizado) * 100

    def tiempo_promedio(self):
        if not self.tiempos:
            return 0

        return sum(self.tiempos) / len(self.tiempos)

    def calcular_riesgo(self):
        if self.total_analizado == 0:
            return 0

        return (self.alertas / self.total_analizado) * 100

    def obtener_resumen(self):
        return {
            "total_analizado": self.total_analizado,
            "anomalias": self.anomalias,
            "normales": self.normales,
            "alertas": self.alertas,
            "porcentaje_anomalias": self.porcentaje_anomalias(),
            "porcentaje_normales": self.porcentaje_normales(),
            "tiempo_promedio": self.tiempo_promedio(),
            "riesgo": self.calcular_riesgo()
        }