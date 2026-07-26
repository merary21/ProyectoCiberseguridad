# Arquitectura Actual

## 1. Introducción

El presente documento describe la arquitectura actual del proyecto **Sistema Inteligente de Detección de Anomalías en Aplicaciones Web con Inteligencia Artificial**, mostrando los componentes que conforman la aplicación, la forma en que interactúan entre sí y el flujo de información desde que el usuario realiza una acción hasta que obtiene una respuesta del sistema.

Actualmente el proyecto corresponde a un prototipo funcional ejecutado en un entorno local. La aplicación integra un modelo de Machine Learning para la detección de anomalías y un asistente inteligente basado en Inteligencia Artificial Generativa.

---

# 2. Descripción general de la arquitectura

La arquitectura actual está compuesta por una aplicación web desarrollada en Python, donde el usuario interactúa mediante una interfaz gráfica. La información ingresada es procesada por la lógica del sistema, la cual se comunica con el modelo de detección de anomalías y con el asistente inteligente.

El procesamiento de los datos se realiza completamente de manera local, utilizando un conjunto de datos previamente preparado y un modelo entrenado mediante Machine Learning.

---

# 3. Componentes de la arquitectura

## 3.1 Usuario (Actor principal)

El usuario representa el actor principal del sistema.

Puede ser un administrador de sistemas, un analista de ciberseguridad o cualquier persona autorizada para utilizar la aplicación.

Entre sus funciones se encuentran:

- Consultar el estado del tráfico web.
- Analizar registros.
- Revisar alertas generadas.
- Realizar consultas al asistente inteligente.
- Obtener recomendaciones relacionadas con ciberseguridad.

---

## 3.2 Interfaz de usuario

La aplicación dispone de una interfaz web desarrollada en Python.

Esta interfaz constituye el punto de entrada del sistema y permite al usuario interactuar con todas las funcionalidades disponibles.

Desde la interfaz el usuario puede:

- Analizar registros de tráfico.
- Visualizar alertas.
- Consultar estadísticas.
- Realizar preguntas al asistente de IA.
- Visualizar recomendaciones de seguridad.

---

## 3.3 Backend o lógica principal

El backend contiene la lógica principal del sistema.

Sus responsabilidades incluyen:

- Recibir las solicitudes del usuario.
- Procesar la información.
- Ejecutar el modelo de Machine Learning.
- Comunicarse con el asistente inteligente.
- Mostrar los resultados obtenidos.

Actualmente toda la lógica se ejecuta dentro de la misma aplicación, sin una separación mediante API.

---

## 3.4 Componente de Inteligencia Artificial

La solución incorpora dos componentes principales de Inteligencia Artificial.

### Modelo de Machine Learning

Se utiliza el algoritmo **Isolation Forest**, implementado mediante la biblioteca **Scikit-Learn**.

Su función consiste en analizar el tráfico web para detectar comportamientos que difieran significativamente del comportamiento normal.

Como resultado clasifica cada registro como:

- Tráfico normal.
- Tráfico anómalo.

### Asistente Inteligente

El proyecto incorpora además un asistente conversacional desarrollado mediante **Llama 3.2**, ejecutado utilizando **Ollama**.

Este componente permite responder preguntas relacionadas con ciberseguridad y ofrecer recomendaciones al usuario.

---

## 3.5 Datos utilizados

El sistema trabaja con un conjunto de datos de tráfico web utilizado para entrenar y evaluar el modelo de Machine Learning.

Los datos incluyen información como:

- Dirección IP.
- Método HTTP.
- URL.
- Código de respuesta.
- Fecha y hora.
- User-Agent.
- Variables utilizadas durante el entrenamiento del modelo.

El rendimiento del sistema depende directamente de la calidad del conjunto de datos utilizado.

---

## 3.6 Servicios externos

Actualmente el proyecto utiliza un único servicio externo.

### Ollama

Ollama permite ejecutar localmente el modelo de lenguaje **Llama 3.2**, encargado de responder las consultas realizadas por el usuario.

Este servicio debe encontrarse en ejecución antes de iniciar la aplicación.

---

# 4. Flujo de información

El funcionamiento general del sistema puede resumirse de la siguiente manera:

1. El usuario accede a la interfaz web.

2. El usuario solicita el análisis del tráfico o realiza una consulta al asistente.

3. El backend recibe la solicitud.

4. Dependiendo de la acción realizada:

   - El modelo **Isolation Forest** analiza el tráfico.
   - El asistente **Llama 3.2** procesa la consulta.

5. El sistema obtiene los resultados.

6. La aplicación muestra al usuario:

   - Estado del tráfico.
   - Alertas generadas.
   - Recomendaciones.
   - Respuestas del asistente.

---

# 5. Diagrama de arquitectura actual

```text
                        +----------------------+
                        |       Usuario        |
                        +----------+-----------+
                                   |
                                   |
                                   v
                     +-------------+--------------+
                     |     Interfaz de Usuario    |
                     |      (Aplicación Web)      |
                     +-------------+--------------+
                                   |
                                   |
                                   v
                     +-------------+--------------+
                     | Backend / Lógica Principal |
                     +-------------+--------------+
                                   |
             +---------------------+----------------------+
             |                                            |
             |                                            |
             v                                            v
+-----------------------------+            +-----------------------------+
| Modelo IA                   |            | Asistente Inteligente       |
| Isolation Forest            |            | Ollama - Llama 3.2          |
+--------------+--------------+            +--------------+--------------+
               |                                            |
               |                                            |
               v                                            v
+-----------------------------+            +-----------------------------+
| Dataset de Tráfico Web      |            | Respuestas y                |
| Datos para entrenamiento    |            | recomendaciones             |
+--------------+--------------+            +--------------+--------------+
               \                                            /
                \                                          /
                 +----------------+------------------------+
                                  |
                                  v
                    +-------------+--------------+
                    | Resultados para el usuario |
                    | - Tráfico normal/anómalo   |
                    | - Alertas                  |
                    | - Recomendaciones          |
                    +----------------------------+
```

---

# 6. Dependencias manuales y puntos frágiles

Aunque el sistema funciona correctamente como prototipo, la arquitectura actual presenta algunas limitaciones.

Entre las principales dependencias y puntos frágiles se encuentran:

- Toda la aplicación se ejecuta localmente.
- El funcionamiento del asistente depende de que Ollama esté iniciado.
- No existe una API que separe el backend de la interfaz.
- No existe una base de datos para almacenar el historial.
- El sistema depende de un conjunto de datos previamente preparado.
- No existen pruebas automatizadas.
- No se dispone de monitoreo ni generación de logs.
- El despliegue todavía se realiza de forma manual.

Estas limitaciones serán abordadas en la arquitectura objetivo y en el plan de mejora del proyecto.

---

## Evidencias

Las evidencias de la interfaz y ejecución del proyecto pueden consultarse en el siguiente documento:

[📄 Evidencias.pdf](Evidencias.pdf)
