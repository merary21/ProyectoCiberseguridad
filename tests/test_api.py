from fastapi.testclient import TestClient

from API.main import app


client = TestClient(app)


def test_health_responde_correctamente():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "SOC-AI API"
    }


def test_metadata_responde_correctamente():
    response = client.get("/metadata")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "SOC-AI"
    assert data["version"] == "2.0.0"
    assert data["model"] == "Isolation Forest"


def test_analyze_recibe_solicitud_web():
    response = client.post(
        "/analyze",
        json={
            "method": "GET",
            "url": "/login",
            "status_code": 200,
            "response_size": 500,
            "user_agent": "Mozilla/5.0",
            "ip": "192.168.1.10"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ip"] == "192.168.1.10"
    assert data["url"] == "/login"
    assert data["resultado"] in ["NORMAL", "ALERTA"]
    assert "nivel_riesgo" in data
    assert "anomalia" in data