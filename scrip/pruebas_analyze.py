# ============================================================
# scrip/pruebas_analyze.py
# Pruebas funcionales y de rendimiento del endpoint /api/analyze
# de SOC-AI. Ejecuta 20 casos de prueba (tráfico normal y
# sospechoso), mide tiempos de respuesta y genera un reporte en
# docs/reporte_pruebas_analyze.md
# ============================================================

import http.cookiejar
import json
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:5000"
LOGIN_URL = f"{BASE_URL}/login"
REGISTRO_URL = f"{BASE_URL}/registro"
ANALYZE_URL = f"{BASE_URL}/api/analyze"

# Usuario de prueba. Si no existe, el script lo registra automáticamente
# antes de ejecutar las pruebas.
TEST_EMAIL = "pruebas.automatizadas@soc-ai.local"
TEST_PASSWORD = "PruebasSOC123"
TEST_EMPRESA = {
    "nombre_empresa": "SOC-AI QA",
    "nit": "QA-000000001",
    "sector": "Tecnología",
    "nombre_completo": "Cuenta de Pruebas Automatizadas",
}

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
REPORTE_PATH = DOCS_DIR / "reporte_pruebas_analyze.md"

# 20 casos de prueba: alternan tráfico normal y tráfico sospechoso
# para ejercitar ambas ramas de clasificación del modelo Isolation Forest.
CASOS_DE_PRUEBA = [
    {"nombre": "Tráfico normal - Dashboard", "ip": "192.168.1.10", "metodo": "GET", "url": "/dashboard", "estado": 200, "tamano": 1200, "hora": 10},
    {"nombre": "Tráfico normal - Consulta de métricas", "ip": "192.168.1.11", "metodo": "GET", "url": "/api/metrics", "estado": 200, "tamano": 900, "hora": 11},
    {"nombre": "Tráfico normal - Página de inicio", "ip": "192.168.1.12", "metodo": "GET", "url": "/", "estado": 200, "tamano": 1500, "hora": 9},
    {"nombre": "Tráfico normal - Reporte mensual", "ip": "192.168.1.13", "metodo": "GET", "url": "/reportes/mensual", "estado": 200, "tamano": 2000, "hora": 14},
    {"nombre": "Tráfico normal - Login exitoso", "ip": "192.168.1.14", "metodo": "POST", "url": "/login", "estado": 200, "tamano": 400, "hora": 8},
    {"nombre": "Tráfico normal - Consulta de alertas", "ip": "192.168.1.15", "metodo": "GET", "url": "/api/alerts", "estado": 200, "tamano": 700, "hora": 16},
    {"nombre": "Tráfico sospechoso - Acceso admin no autorizado", "ip": "45.33.10.20", "metodo": "GET", "url": "/admin/login", "estado": 401, "tamano": 500, "hora": 3},
    {"nombre": "Tráfico sospechoso - Fuerza bruta wp-admin", "ip": "45.33.10.21", "metodo": "POST", "url": "/wp-admin/", "estado": 403, "tamano": 8000, "hora": 2},
    {"nombre": "Tráfico sospechoso - Escaneo de rutas", "ip": "185.220.101.5", "metodo": "GET", "url": "/admin/config.php", "estado": 404, "tamano": 300, "hora": 1},
    {"nombre": "Tráfico sospechoso - Intento de auth inválido", "ip": "185.220.101.6", "metodo": "POST", "url": "/auth/login", "estado": 401, "tamano": 6000, "hora": 4},
    {"nombre": "Tráfico sospechoso - Posible inyección en API", "ip": "91.219.237.10", "metodo": "POST", "url": "/api/users?id=1", "estado": 500, "tamano": 15000, "hora": 23},
    {"nombre": "Tráfico sospechoso - Posible exfiltración de datos", "ip": "91.219.237.11", "metodo": "GET", "url": "/api/export/all", "estado": 200, "tamano": 500000, "hora": 2},
    {"nombre": "Tráfico normal - Actualización de perfil", "ip": "192.168.1.16", "metodo": "POST", "url": "/perfil/actualizar", "estado": 200, "tamano": 1800, "hora": 13},
    {"nombre": "Tráfico normal - Health check", "ip": "192.168.1.17", "metodo": "GET", "url": "/api/health", "estado": 200, "tamano": 300, "hora": 12},
    {"nombre": "Tráfico sospechoso - Redirección sospechosa", "ip": "172.16.5.9", "metodo": "GET", "url": "/login?redirect=evil.com", "estado": 302, "tamano": 700, "hora": 5},
    {"nombre": "Tráfico sospechoso - Acceso repetido a admin", "ip": "172.16.5.10", "metodo": "GET", "url": "/admin/dashboard", "estado": 403, "tamano": 900, "hora": 3},
    {"nombre": "Tráfico normal - Recurso estático", "ip": "192.168.1.18", "metodo": "GET", "url": "/static/css/styles.css", "estado": 200, "tamano": 4000, "hora": 15},
    {"nombre": "Tráfico normal - Consulta al asistente IA", "ip": "192.168.1.19", "metodo": "POST", "url": "/api/ai-analysis", "estado": 200, "tamano": 600, "hora": 17},
    {"nombre": "Tráfico sospechoso - Método no habitual en API", "ip": "203.0.113.5", "metodo": "PUT", "url": "/api/config", "estado": 500, "tamano": 12000, "hora": 0},
    {"nombre": "Tráfico sospechoso - Intentos fallidos repetidos", "ip": "203.0.113.6", "metodo": "POST", "url": "/admin/login", "estado": 401, "tamano": 5500, "hora": 4},
]

TOTAL_PRUEBAS = len(CASOS_DE_PRUEBA)


def crear_sesion():
    """Crea un opener de urllib con manejo de cookies para mantener la sesión."""
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    return opener


def enviar_formulario(opener, url, campos):
    body = urllib.parse.urlencode(campos).encode("utf-8")
    solicitud = urllib.request.Request(url, data=body, method="POST")
    with opener.open(solicitud, timeout=30) as respuesta:
        return respuesta.geturl(), respuesta.read().decode("utf-8", errors="replace")


def iniciar_sesion(opener):
    """Inicia sesión con el usuario de prueba; si no existe, lo registra."""
    url_final, _ = enviar_formulario(
        opener, LOGIN_URL, {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )

    if "/login" not in url_final:
        print(f"Sesión iniciada correctamente como {TEST_EMAIL}")
        return True

    print("El usuario de pruebas no existe o las credenciales cambiaron. Registrando...")

    campos_registro = {
        **TEST_EMPRESA,
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "confirmar_password": TEST_PASSWORD,
    }
    url_final, _ = enviar_formulario(opener, REGISTRO_URL, campos_registro)

    if "/registro" not in url_final:
        print(f"Cuenta de pruebas registrada e inicio de sesión completado ({TEST_EMAIL}).")
        return True

    print("No fue posible autenticar al usuario de pruebas. Revisa TEST_EMAIL/TEST_PASSWORD.")
    return False


def ejecutar_caso(opener, indice, caso):
    payload = {
        "ip": caso["ip"],
        "metodo": caso["metodo"],
        "url": caso["url"],
        "estado": caso["estado"],
        "tamano": caso["tamano"],
        "hora": caso["hora"],
    }
    cuerpo = json.dumps(payload).encode("utf-8")
    solicitud = urllib.request.Request(
        ANALYZE_URL,
        data=cuerpo,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    inicio = time.perf_counter()
    try:
        with opener.open(solicitud, timeout=60) as respuesta:
            cuerpo_respuesta = respuesta.read().decode("utf-8")
            status = respuesta.status
            datos = json.loads(cuerpo_respuesta)
    except urllib.error.HTTPError as error:
        status = error.code
        datos = {"error": error.read().decode("utf-8", errors="replace")}
    except Exception as error:
        status = 0
        datos = {"error": type(error).__name__}

    duracion_ms = (time.perf_counter() - inicio) * 1000
    ok = 200 <= status < 300 and isinstance(datos, dict) and datos.get("ok") is True

    resultado = {
        "prueba": indice + 1,
        "nombre": caso["nombre"],
        "ip": caso["ip"],
        "metodo": caso["metodo"],
        "url": caso["url"],
        "estado_enviado": caso["estado"],
        "status_http": status,
        "duracion_ms": round(duracion_ms, 2),
        "ok": ok,
        "alerta": datos.get("alerta") if isinstance(datos, dict) else None,
        "score": datos.get("score") if isinstance(datos, dict) else None,
        "mensaje": datos.get("mensaje") or datos.get("error") if isinstance(datos, dict) else None,
    }

    print(
        f"[{indice + 1}/{TOTAL_PRUEBAS}] {caso['nombre']} -> "
        f"status={status} alerta={resultado['alerta']} duracion_ms={resultado['duracion_ms']}"
    )

    return resultado


def calcular_resumen(resultados):
    duraciones_ok = [r["duracion_ms"] for r in resultados if r["ok"]]
    todas_duraciones = [r["duracion_ms"] for r in resultados]
    errores = sum(1 for r in resultados if not r["ok"])
    alertas_detectadas = sum(1 for r in resultados if r.get("alerta") is True)

    if duraciones_ok:
        ordenadas = sorted(duraciones_ok)
        p50 = statistics.median(ordenadas)
        indice_p95 = min(len(ordenadas) - 1, max(0, int(len(ordenadas) * 0.95) - 1))
        p95 = ordenadas[indice_p95]
    else:
        p50 = None
        p95 = None

    return {
        "endpoint": ANALYZE_URL,
        "total_pruebas": TOTAL_PRUEBAS,
        "pruebas_exitosas": TOTAL_PRUEBAS - errores,
        "errores": errores,
        "tasa_error_porcentaje": round(errores / TOTAL_PRUEBAS * 100, 2),
        "alertas_detectadas": alertas_detectadas,
        "trafico_normal_detectado": (TOTAL_PRUEBAS - errores) - alertas_detectadas,
        "p50_ms": round(p50, 2) if p50 is not None else None,
        "p95_ms": round(p95, 2) if p95 is not None else None,
        "max_ms": round(max(todas_duraciones), 2) if todas_duraciones else None,
    }


def generar_reporte_markdown(resultados, resumen):
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    lineas = [
        "# Reporte de pruebas - Endpoint /api/analyze (SOC-AI)",
        "",
        f"Generado automáticamente el {ahora} por `scrip/pruebas_analyze.py`.",
        "",
        "## Resumen",
        "",
        f"- Endpoint probado: `{resumen['endpoint']}`",
        f"- Total de pruebas ejecutadas: {resumen['total_pruebas']}",
        f"- Pruebas exitosas: {resumen['pruebas_exitosas']}",
        f"- Errores: {resumen['errores']} ({resumen['tasa_error_porcentaje']}%)",
        f"- Tráfico clasificado como anómalo: {resumen['alertas_detectadas']}",
        f"- Tráfico clasificado como normal: {resumen['trafico_normal_detectado']}",
        f"- Latencia p50: {resumen['p50_ms']} ms",
        f"- Latencia p95: {resumen['p95_ms']} ms",
        f"- Latencia máxima: {resumen['max_ms']} ms",
        "",
        "## Detalle de las 20 pruebas",
        "",
        "| # | Caso de prueba | IP | Método | URL | HTTP | Resultado | Score | Duración (ms) |",
        "|---|-----------------|----|--------|-----|------|-----------|-------|----------------|",
    ]

    for r in resultados:
        if not r["ok"]:
            resultado_txt = "ERROR"
        elif r["alerta"] is True:
            resultado_txt = "Anómalo"
        elif r["alerta"] is False:
            resultado_txt = "Normal"
        else:
            resultado_txt = "N/D"

        lineas.append(
            f"| {r['prueba']} | {r['nombre']} | {r['ip']} | {r['metodo']} | "
            f"`{r['url']}` | {r['status_http']} | {resultado_txt} | "
            f"{r['score']} | {r['duracion_ms']} |"
        )

    lineas.extend(
        [
            "",
            "## Datos crudos (JSON)",
            "",
            "```json",
            json.dumps({"resumen": resumen, "resultados": resultados}, indent=2, ensure_ascii=False),
            "```",
            "",
        ]
    )

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTE_PATH.write_text("\n".join(lineas), encoding="utf-8")


def main():
    print(f"Iniciando {TOTAL_PRUEBAS} pruebas contra {ANALYZE_URL}")

    opener = crear_sesion()

    if not iniciar_sesion(opener):
        print("Abortando: no se pudo iniciar sesión para ejecutar las pruebas.")
        return

    resultados = [
        ejecutar_caso(opener, indice, caso)
        for indice, caso in enumerate(CASOS_DE_PRUEBA)
    ]

    resumen = calcular_resumen(resultados)
    generar_reporte_markdown(resultados, resumen)

    print("\n=== RESUMEN ===")
    print(json.dumps(resumen, indent=2, ensure_ascii=False))
    print(f"\nReporte generado en: {REPORTE_PATH}")


if __name__ == "__main__":
    main()
