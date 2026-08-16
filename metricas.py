import numpy as np


class MetricasSOC:

    def __init__(self):

        self.total_analizado = 0
        self.anomalias = 0
        self.normales = 0
        self.alertas = 0
        self.errores = 0
        self.tiempos = []


    def iniciar_medicion(self):

        import time

        return time.perf_counter()


    def registrar_resultado(
        self,
        es_anomalia,
        tiempo
    ):

        self.total_analizado += 1

        self.tiempos.append(tiempo)

        if es_anomalia:

            self.anomalias += 1
            self.alertas += 1

        else:

            self.normales += 1


    def registrar_error(self):

        self.errores += 1


    def porcentaje_anomalias(self):

        if self.total_analizado == 0:
            return 0

        return (
            self.anomalias
            / self.total_analizado
        ) * 100


    def porcentaje_normales(self):

        if self.total_analizado == 0:
            return 0

        return (
            self.normales
            / self.total_analizado
        ) * 100


    def tiempo_promedio(self):

        if not self.tiempos:
            return 0

        return sum(
            self.tiempos
        ) / len(self.tiempos)


    def p50(self):

        if not self.tiempos:
            return 0

        return np.percentile(
            self.tiempos,
            50
        )


    def p95(self):

        if not self.tiempos:
            return 0

        return np.percentile(
            self.tiempos,
            95
        )


    def tiempo_maximo(self):

        if not self.tiempos:
            return 0

        return max(
            self.tiempos
        )


    def tasa_error(self):

        total = (
            self.total_analizado
            + self.errores
        )

        if total == 0:
            return 0

        return (
            self.errores
            / total
        ) * 100


    def calcular_riesgo(self):

        if self.total_analizado == 0:
            return 0

        return (
            self.alertas
            / self.total_analizado
        ) * 100


    def obtener_resumen(self):

        return {

            "total_analizado":
                self.total_analizado,

            "anomalias":
                self.anomalias,

            "normales":
                self.normales,

            "alertas":
                self.alertas,

            "errores":
                self.errores,

            "porcentaje_anomalias":
                self.porcentaje_anomalias(),

            "porcentaje_normales":
                self.porcentaje_normales(),

            "tiempo_promedio":
                self.tiempo_promedio(),

            "p50":
                self.p50(),

            "p95":
                self.p95(),

            "tiempo_maximo":
                self.tiempo_maximo(),

            "tasa_error":
                self.tasa_error(),

            "riesgo":
                self.calcular_riesgo()
        }