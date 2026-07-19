# Documentación de la API

## 1. Descripción

La aplicación proporciona una interfaz para analizar solicitudes web y detectar comportamientos potencialmente sospechosos utilizando un modelo de Inteligencia Artificial.

El sistema recibe información de una solicitud web, procesa los datos y genera un resultado indicando si la solicitud es normal o representa una posible anomalía.

---

## 2. Endpoint principal

### Analizar solicitud

**Método:** `POST`

**Ruta:**

```text
/api/analizar
```

Este endpoint recibe los datos de una solicitud web y ejecuta el análisis mediante el modelo de Inteligencia Artificial.

---

## 3. Flujo de procesamiento

1. El cliente envía los datos de la solicitud.
2. La API valida la información recibida.
3. Los datos son procesados.
4. El modelo de Inteligencia Artificial analiza la solicitud.
5. El sistema genera una respuesta.
6. La respuesta indica el resultado del análisis.

---

## 4. Posibles respuestas

### Solicitud normal

```json
{
  "estado": "exitoso",
  "resultado": "NORMAL",
  "nivel_riesgo": "BAJO"
}
```

### Solicitud sospechosa

```json
{
  "estado": "exitoso",
  "resultado": "ALERTA",
  "nivel_riesgo": "ALTO"
}
```

### Error

```json
{
  "estado": "error",
  "tipo": "Error de validación",
  "mensaje": "Los datos de entrada son incorrectos"
}
```

---

## 5. Manejo de errores

La API utiliza códigos y mensajes para informar los errores ocurridos durante el procesamiento.

Los errores pueden producirse cuando:

* Faltan datos obligatorios.
* Los datos tienen un formato incorrecto.
* Ocurre un error durante el procesamiento.
* El modelo de Inteligencia Artificial no está disponible.

---

## 6. Seguridad

La API no bloquea automáticamente las solicitudes.

Su función principal es analizar el tráfico y generar alertas para que el personal encargado de la seguridad pueda tomar decisiones.
