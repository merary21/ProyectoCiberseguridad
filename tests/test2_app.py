def test_modelo_realiza_prediccion():

    modelo = joblib.load(
        "modelo_guardado/isolation_forest_model.pkl"
    )

    scaler = joblib.load(
        "modelo_guardado/scaler.pkl"
    )

    le_metodo = joblib.load(
        "modelo_guardado/label_encoder_metodo.pkl"
    )

    metodo = "GET"
    url = "/admin/login"
    estado = 403
    tamano = 1500
    hora = 12

    url_length = len(url)

    request_rate = 5.0

    base = 1.5 if metodo == "POST" else 0.5

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

    metodo_enc = (
        le_metodo.transform([metodo])[0]
        if metodo in le_metodo.classes_
        else 0
    )

    service_enc = 0
    flag_enc = 2

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

    input_scaled = scaler.transform(input_data)

    pred = modelo.predict(input_scaled)[0]

    score = modelo.decision_function(input_scaled)[0]

    assert pred in [-1, 1]

    assert isinstance(
        float(score),
        float
    )