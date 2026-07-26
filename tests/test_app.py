from pathlib import Path
import joblib


def test_app_existe():

    ruta_app = Path("app.py")

    assert ruta_app.exists()


def test_modelos_existen():

    modelo_dir = Path("modelo_guardado")

    assert modelo_dir.exists()

    assert (
        modelo_dir / "isolation_forest_model.pkl"
    ).exists()

    assert (
        modelo_dir / "scaler.pkl"
    ).exists()

    assert (
        modelo_dir / "label_encoder_metodo.pkl"
    ).exists()


def test_modelo_puede_cargarse():

    modelo = joblib.load(
        "modelo_guardado/isolation_forest_model.pkl"
    )

    scaler = joblib.load(
        "modelo_guardado/scaler.pkl"
    )

    le_metodo = joblib.load(
        "modelo_guardado/label_encoder_metodo.pkl"
    )

    assert modelo is not None
    assert scaler is not None
    assert le_metodo is not None