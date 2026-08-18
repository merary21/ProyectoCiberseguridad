import os
import joblib


class DetectorSOC:

    def __init__(self):

        modelo_path = os.path.join(
            "modelo_guardado",
            "isolation_forest_model.pkl"
        )

        scaler_path = os.path.join(
            "modelo_guardado",
            "scaler.pkl"
        )

        metodo_path = os.path.join(
            "modelo_guardado",
            "label_encoder_metodo.pkl"
        )

        metadata_path = os.path.join(
            "modelo_guardado",
            "metadata.pkl"
        )

        self.modelo = joblib.load(modelo_path)
        self.scaler = joblib.load(scaler_path)
        self.le_metodo = joblib.load(metodo_path)
        self.metadata = joblib.load(metadata_path)


    def analizar(
        self,
        ip,
        metodo,
        url,
        estado,
        tamano,
        hora
    ):

        # Feature engineering

        url_length = len(url)

        request_rate = 5.0

        base = (
            1.5
            if metodo == "POST"
            else 0.5
        )

        duration = (
            base
            if 200 <= estado < 300
            else base * 2.0
        )

        src_bytes = (
            tamano * 0.1
            if metodo == "POST"
            else tamano * 0.01
        )

        dst_bytes = tamano

        num_packets = int(
            (src_bytes + dst_bytes) / 1500
        ) + 1


        # Método

        if metodo in self.le_metodo.classes_:

            metodo_enc = self.le_metodo.transform(
                [metodo]
            )[0]

        else:

            metodo_enc = 0


        # Servicio

        url_lower = url.lower()

        if (
            "admin" in url_lower
            or "wp-admin" in url_lower
        ):

            service_enc = 0

        elif (
            "login" in url_lower
            or "auth" in url_lower
        ):

            service_enc = 1

        elif "api" in url_lower:

            service_enc = 2

        else:

            service_enc = 4


        # Estado HTTP

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

        input_data = [[

            duration,
            src_bytes,
            dst_bytes,
            num_packets,
            url_length,
            request_rate,
            estado,
            metodo_enc,
            service_enc,
            flag_enc,
            hora

        ]]


        # Escalamiento

        input_scaled = self.scaler.transform(
            input_data
        )


        # Predicción

        pred = self.modelo.predict(
            input_scaled
        )[0]


        score = self.modelo.decision_function(
            input_scaled
        )[0]


        es_anomalo = pred == -1


        return {

            "ip": ip,

            "metodo": metodo,

            "url": url,

            "estado": estado,

            "resultado": (
                "ALERTA"
                if es_anomalo
                else "OK"
            ),

            "score": float(score),

            "anomalo": bool(es_anomalo)

        }