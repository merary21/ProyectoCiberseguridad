# Reporte de pruebas - Endpoint /api/analyze (SOC-AI)

Generado automáticamente el 22/08/2026 10:28:48 por `scrip/pruebas_analyze.py`.

## Resumen

- Endpoint probado: `http://localhost:5000/api/analyze`
- Total de pruebas ejecutadas: 20
- Pruebas exitosas: 20
- Errores: 0 (0.0%)
- Tráfico clasificado como anómalo: 13
- Tráfico clasificado como normal: 7
- Latencia p50: 2069.81 ms
- Latencia p95: 2087.66 ms
- Latencia máxima: 2093.41 ms

## Detalle de las 20 pruebas

| # | Caso de prueba | IP | Método | URL | HTTP | Resultado | Score | Duración (ms) |
|---|-----------------|----|--------|-----|------|-----------|-------|----------------|
| 1 | Tráfico normal - Dashboard | 192.168.1.10 | GET | `/dashboard` | 200 | Normal | 0.0306 | 2084.4 |
| 2 | Tráfico normal - Consulta de métricas | 192.168.1.11 | GET | `/api/metrics` | 200 | Normal | 0.0036 | 2056.94 |
| 3 | Tráfico normal - Página de inicio | 192.168.1.12 | GET | `/` | 200 | Normal | 0.0114 | 2070.34 |
| 4 | Tráfico normal - Reporte mensual | 192.168.1.13 | GET | `/reportes/mensual` | 200 | Normal | 0.0126 | 2064.3 |
| 5 | Tráfico normal - Login exitoso | 192.168.1.14 | POST | `/login` | 200 | Anómalo | -0.0575 | 2063.08 |
| 6 | Tráfico normal - Consulta de alertas | 192.168.1.15 | GET | `/api/alerts` | 200 | Normal | 0.0077 | 2054.9 |
| 7 | Tráfico sospechoso - Acceso admin no autorizado | 45.33.10.20 | GET | `/admin/login` | 200 | Anómalo | -0.0116 | 2069.27 |
| 8 | Tráfico sospechoso - Fuerza bruta wp-admin | 45.33.10.21 | POST | `/wp-admin/` | 200 | Anómalo | -0.1043 | 2050.25 |
| 9 | Tráfico sospechoso - Escaneo de rutas | 185.220.101.5 | GET | `/admin/config.php` | 200 | Anómalo | -0.0467 | 2041.37 |
| 10 | Tráfico sospechoso - Intento de auth inválido | 185.220.101.6 | POST | `/auth/login` | 200 | Anómalo | -0.0986 | 2066.08 |
| 11 | Tráfico sospechoso - Posible inyección en API | 91.219.237.10 | POST | `/api/users?id=1` | 200 | Anómalo | -0.1391 | 2072.74 |
| 12 | Tráfico sospechoso - Posible exfiltración de datos | 91.219.237.11 | GET | `/api/export/all` | 200 | Anómalo | -0.1112 | 2068.44 |
| 13 | Tráfico normal - Actualización de perfil | 192.168.1.16 | POST | `/perfil/actualizar` | 200 | Anómalo | -0.0482 | 2087.66 |
| 14 | Tráfico normal - Health check | 192.168.1.17 | GET | `/api/health` | 200 | Normal | 0.0091 | 2093.41 |
| 15 | Tráfico sospechoso - Redirección sospechosa | 172.16.5.9 | GET | `/login?redirect=evil.com` | 200 | Anómalo | -0.0179 | 2085.52 |
| 16 | Tráfico sospechoso - Acceso repetido a admin | 172.16.5.10 | GET | `/admin/dashboard` | 200 | Anómalo | -0.0376 | 2086.14 |
| 17 | Tráfico normal - Recurso estático | 192.168.1.18 | GET | `/static/css/styles.css` | 200 | Normal | 0.0051 | 2082.36 |
| 18 | Tráfico normal - Consulta al asistente IA | 192.168.1.19 | POST | `/api/ai-analysis` | 200 | Anómalo | -0.0607 | 2072.69 |
| 19 | Tráfico sospechoso - Método no habitual en API | 203.0.113.5 | PUT | `/api/config` | 200 | Anómalo | -0.0682 | 2075.34 |
| 20 | Tráfico sospechoso - Intentos fallidos repetidos | 203.0.113.6 | POST | `/admin/login` | 200 | Anómalo | -0.1046 | 2051.32 |

## Datos crudos (JSON)

```json
{
  "resumen": {
    "endpoint": "http://localhost:5000/api/analyze",
    "total_pruebas": 20,
    "pruebas_exitosas": 20,
    "errores": 0,
    "tasa_error_porcentaje": 0.0,
    "alertas_detectadas": 13,
    "trafico_normal_detectado": 7,
    "p50_ms": 2069.81,
    "p95_ms": 2087.66,
    "max_ms": 2093.41
  },
  "resultados": [
    {
      "prueba": 1,
      "nombre": "Tráfico normal - Dashboard",
      "ip": "192.168.1.10",
      "metodo": "GET",
      "url": "/dashboard",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2084.4,
      "ok": true,
      "alerta": false,
      "score": 0.0306,
      "mensaje": "El tráfico se encuentra dentro de los parámetros normales."
    },
    {
      "prueba": 2,
      "nombre": "Tráfico normal - Consulta de métricas",
      "ip": "192.168.1.11",
      "metodo": "GET",
      "url": "/api/metrics",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2056.94,
      "ok": true,
      "alerta": false,
      "score": 0.0036,
      "mensaje": "El tráfico se encuentra dentro de los parámetros normales."
    },
    {
      "prueba": 3,
      "nombre": "Tráfico normal - Página de inicio",
      "ip": "192.168.1.12",
      "metodo": "GET",
      "url": "/",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2070.34,
      "ok": true,
      "alerta": false,
      "score": 0.0114,
      "mensaje": "El tráfico se encuentra dentro de los parámetros normales."
    },
    {
      "prueba": 4,
      "nombre": "Tráfico normal - Reporte mensual",
      "ip": "192.168.1.13",
      "metodo": "GET",
      "url": "/reportes/mensual",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2064.3,
      "ok": true,
      "alerta": false,
      "score": 0.0126,
      "mensaje": "El tráfico se encuentra dentro de los parámetros normales."
    },
    {
      "prueba": 5,
      "nombre": "Tráfico normal - Login exitoso",
      "ip": "192.168.1.14",
      "metodo": "POST",
      "url": "/login",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2063.08,
      "ok": true,
      "alerta": true,
      "score": -0.0575,
      "mensaje": "Tráfico anómalo detectado. La IP 192.168.1.14 presenta comportamiento sospechoso accediendo a /login."
    },
    {
      "prueba": 6,
      "nombre": "Tráfico normal - Consulta de alertas",
      "ip": "192.168.1.15",
      "metodo": "GET",
      "url": "/api/alerts",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2054.9,
      "ok": true,
      "alerta": false,
      "score": 0.0077,
      "mensaje": "El tráfico se encuentra dentro de los parámetros normales."
    },
    {
      "prueba": 7,
      "nombre": "Tráfico sospechoso - Acceso admin no autorizado",
      "ip": "45.33.10.20",
      "metodo": "GET",
      "url": "/admin/login",
      "estado_enviado": 401,
      "status_http": 200,
      "duracion_ms": 2069.27,
      "ok": true,
      "alerta": true,
      "score": -0.0116,
      "mensaje": "Tráfico anómalo detectado. La IP 45.33.10.20 presenta comportamiento sospechoso accediendo a /admin/login."
    },
    {
      "prueba": 8,
      "nombre": "Tráfico sospechoso - Fuerza bruta wp-admin",
      "ip": "45.33.10.21",
      "metodo": "POST",
      "url": "/wp-admin/",
      "estado_enviado": 403,
      "status_http": 200,
      "duracion_ms": 2050.25,
      "ok": true,
      "alerta": true,
      "score": -0.1043,
      "mensaje": "Tráfico anómalo detectado. La IP 45.33.10.21 presenta comportamiento sospechoso accediendo a /wp-admin/."
    },
    {
      "prueba": 9,
      "nombre": "Tráfico sospechoso - Escaneo de rutas",
      "ip": "185.220.101.5",
      "metodo": "GET",
      "url": "/admin/config.php",
      "estado_enviado": 404,
      "status_http": 200,
      "duracion_ms": 2041.37,
      "ok": true,
      "alerta": true,
      "score": -0.0467,
      "mensaje": "Tráfico anómalo detectado. La IP 185.220.101.5 presenta comportamiento sospechoso accediendo a /admin/config.php."
    },
    {
      "prueba": 10,
      "nombre": "Tráfico sospechoso - Intento de auth inválido",
      "ip": "185.220.101.6",
      "metodo": "POST",
      "url": "/auth/login",
      "estado_enviado": 401,
      "status_http": 200,
      "duracion_ms": 2066.08,
      "ok": true,
      "alerta": true,
      "score": -0.0986,
      "mensaje": "Tráfico anómalo detectado. La IP 185.220.101.6 presenta comportamiento sospechoso accediendo a /auth/login."
    },
    {
      "prueba": 11,
      "nombre": "Tráfico sospechoso - Posible inyección en API",
      "ip": "91.219.237.10",
      "metodo": "POST",
      "url": "/api/users?id=1",
      "estado_enviado": 500,
      "status_http": 200,
      "duracion_ms": 2072.74,
      "ok": true,
      "alerta": true,
      "score": -0.1391,
      "mensaje": "Tráfico anómalo detectado. La IP 91.219.237.10 presenta comportamiento sospechoso accediendo a /api/users?id=1."
    },
    {
      "prueba": 12,
      "nombre": "Tráfico sospechoso - Posible exfiltración de datos",
      "ip": "91.219.237.11",
      "metodo": "GET",
      "url": "/api/export/all",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2068.44,
      "ok": true,
      "alerta": true,
      "score": -0.1112,
      "mensaje": "Tráfico anómalo detectado. La IP 91.219.237.11 presenta comportamiento sospechoso accediendo a /api/export/all."
    },
    {
      "prueba": 13,
      "nombre": "Tráfico normal - Actualización de perfil",
      "ip": "192.168.1.16",
      "metodo": "POST",
      "url": "/perfil/actualizar",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2087.66,
      "ok": true,
      "alerta": true,
      "score": -0.0482,
      "mensaje": "Tráfico anómalo detectado. La IP 192.168.1.16 presenta comportamiento sospechoso accediendo a /perfil/actualizar."
    },
    {
      "prueba": 14,
      "nombre": "Tráfico normal - Health check",
      "ip": "192.168.1.17",
      "metodo": "GET",
      "url": "/api/health",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2093.41,
      "ok": true,
      "alerta": false,
      "score": 0.0091,
      "mensaje": "El tráfico se encuentra dentro de los parámetros normales."
    },
    {
      "prueba": 15,
      "nombre": "Tráfico sospechoso - Redirección sospechosa",
      "ip": "172.16.5.9",
      "metodo": "GET",
      "url": "/login?redirect=evil.com",
      "estado_enviado": 302,
      "status_http": 200,
      "duracion_ms": 2085.52,
      "ok": true,
      "alerta": true,
      "score": -0.0179,
      "mensaje": "Tráfico anómalo detectado. La IP 172.16.5.9 presenta comportamiento sospechoso accediendo a /login?redirect=evil.com."
    },
    {
      "prueba": 16,
      "nombre": "Tráfico sospechoso - Acceso repetido a admin",
      "ip": "172.16.5.10",
      "metodo": "GET",
      "url": "/admin/dashboard",
      "estado_enviado": 403,
      "status_http": 200,
      "duracion_ms": 2086.14,
      "ok": true,
      "alerta": true,
      "score": -0.0376,
      "mensaje": "Tráfico anómalo detectado. La IP 172.16.5.10 presenta comportamiento sospechoso accediendo a /admin/dashboard."
    },
    {
      "prueba": 17,
      "nombre": "Tráfico normal - Recurso estático",
      "ip": "192.168.1.18",
      "metodo": "GET",
      "url": "/static/css/styles.css",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2082.36,
      "ok": true,
      "alerta": false,
      "score": 0.0051,
      "mensaje": "El tráfico se encuentra dentro de los parámetros normales."
    },
    {
      "prueba": 18,
      "nombre": "Tráfico normal - Consulta al asistente IA",
      "ip": "192.168.1.19",
      "metodo": "POST",
      "url": "/api/ai-analysis",
      "estado_enviado": 200,
      "status_http": 200,
      "duracion_ms": 2072.69,
      "ok": true,
      "alerta": true,
      "score": -0.0607,
      "mensaje": "Tráfico anómalo detectado. La IP 192.168.1.19 presenta comportamiento sospechoso accediendo a /api/ai-analysis."
    },
    {
      "prueba": 19,
      "nombre": "Tráfico sospechoso - Método no habitual en API",
      "ip": "203.0.113.5",
      "metodo": "PUT",
      "url": "/api/config",
      "estado_enviado": 500,
      "status_http": 200,
      "duracion_ms": 2075.34,
      "ok": true,
      "alerta": true,
      "score": -0.0682,
      "mensaje": "Tráfico anómalo detectado. La IP 203.0.113.5 presenta comportamiento sospechoso accediendo a /api/config."
    },
    {
      "prueba": 20,
      "nombre": "Tráfico sospechoso - Intentos fallidos repetidos",
      "ip": "203.0.113.6",
      "metodo": "POST",
      "url": "/admin/login",
      "estado_enviado": 401,
      "status_http": 200,
      "duracion_ms": 2051.32,
      "ok": true,
      "alerta": true,
      "score": -0.1046,
      "mensaje": "Tráfico anómalo detectado. La IP 203.0.113.6 presenta comportamiento sospechoso accediendo a /admin/login."
    }
  ]
}
```
