# Arquitectura Objetivo

## 1. Introducción

El presente documento describe la arquitectura objetivo propuesta para el proyecto **Sistema Inteligente de Detección de Anomalías en Aplicaciones Web con Inteligencia Artificial**.

Esta arquitectura representa la evolución del prototipo actual hacia una solución más organizada, modular, escalable y preparada para un posible despliegue.

La arquitectura actual funciona como un prototipo local donde la interfaz, la lógica principal, el modelo de Machine Learning y el asistente inteligente se encuentran integrados dentro de una misma aplicación. 

Por esta razón, la arquitectura objetivo plantea una separación de componentes, incorporando una API de comunicación, almacenamiento persistente, mecanismos de monitoreo, automatización del desarrollo y mejoras de seguridad.

---

# 2. Objetivo de la arquitectura

La arquitectura objetivo tiene como finalidad transformar el prototipo actual en una solución más robusta para el monitoreo y detección de anomalías en aplicaciones web mediante Inteligencia Artificial.

Esta arquitectura permitirá:

- Separar la interfaz de usuario del backend mediante una API.
- Mejorar la organización y mantenimiento del sistema.
- Facilitar la escalabilidad del proyecto.
- Incorporar almacenamiento histórico de eventos y alertas.
- Mejorar la calidad del modelo de detección mediante mejores datos.
- Facilitar el despliegue mediante contenedores.
- Implementar mecanismos de monitoreo y registro.
- Fortalecer la seguridad mediante autenticación y control de acceso.

---

# 3. Relación con el plan de mejora

La arquitectura objetivo está directamente relacionada con el plan de mejora establecido para las semanas 2 a 6 del proyecto.

| Semana | Mejora planificada | Impacto en la arquitectura |
|--------|--------------------|----------------------------|
| Semana 2 | Implementación de una API inteligente para separar interfaz y backend. | Creación de una capa de servicios independiente y mejora de la comunicación entre componentes. |
| Semana 3 | Implementación de pruebas unitarias, CI/CD y mejora del conjunto de datos. | Mayor calidad del software y mejor rendimiento del modelo de Inteligencia Artificial. |
| Semana 4 | Contenerización con Docker y preparación del entorno de despliegue. | Facilita la instalación, configuración y ejecución del sistema. |
| Semana 5 | Implementación de logs, métricas y monitoreo. | Permite supervisar el estado del sistema y detectar errores tempranamente. |
| Semana 6 | Implementación de autenticación, seguridad y documentación técnica. | Mejora la protección del sistema y facilita su administración. |

Estas mejoras permiten evolucionar desde un prototipo local hacia una arquitectura preparada para futuras implementaciones.

---

# 4. Descripción general de la arquitectura

La arquitectura objetivo estará basada en una estructura modular compuesta por diferentes capas:

1. Capa de presentación.
2. Capa de servicios mediante API.
3. Capa de procesamiento y análisis inteligente.
4. Capa de almacenamiento.
5. Capa de monitoreo y seguridad.
6. Capa de infraestructura y despliegue.

Cada componente tendrá responsabilidades específicas, permitiendo mejorar la mantenibilidad y escalabilidad del sistema.

---

# 5. Componentes de la arquitectura

## 5.1 Usuario

El usuario continúa siendo el actor principal del sistema.

Puede representar:

- Administrador de sistemas.
- Analista de ciberseguridad.
- Personal encargado del monitoreo.

Sus funciones serán:

- Consultar el estado del tráfico web.
- Revisar alertas generadas.
- Analizar eventos detectados.
- Consultar recomendaciones del asistente inteligente.
- Gestionar usuarios autorizados.

---

# 5.2 Interfaz de usuario (Dashboard)

La interfaz será responsable de la interacción entre el usuario y el sistema.

A diferencia de la arquitectura actual, la interfaz no contendrá la lógica principal del sistema, sino que realizará solicitudes al backend mediante una API.

Funciones:

- Mostrar tráfico analizado.
- Visualizar alertas.
- Consultar historial de eventos.
- Mostrar estadísticas y métricas.
- Interactuar con el asistente inteligente.

Tecnologías propuestas:

- Streamlit.
- Framework web equivalente.

---

# 5.3 API Backend / Lógica del sistema

El backend será el componente encargado de coordinar la comunicación entre los diferentes módulos.

Esta capa reemplazará la estructura actual donde toda la lógica se encuentra dentro de una única aplicación.

Funciones:

- Recibir solicitudes desde la interfaz.
- Procesar peticiones.
- Gestionar comunicación con el modelo IA.
- Consultar y almacenar información.
- Administrar usuarios y permisos.
- Entregar resultados al dashboard.

Tecnologías propuestas:

- Python.
- Flask o FastAPI.

---

# 5.4 Módulo de captura de tráfico web

Este componente permitirá obtener información de las solicitudes realizadas hacia las aplicaciones web monitoreadas.

Su objetivo es reducir la dependencia del dataset preparado manualmente utilizado actualmente.

Información recopilada:

- Dirección IP.
- Método HTTP.
- URL solicitada.
- Código de respuesta.
- Fecha y hora.
- User-Agent.
- Frecuencia de solicitudes.

Los datos obtenidos serán enviados al módulo de procesamiento.

---

# 5.5 Módulo de procesamiento de datos

Este módulo será responsable de preparar la información antes de ser analizada por los modelos inteligentes.

Funciones:

- Limpieza de datos.
- Eliminación de información innecesaria.
- Transformación de variables.
- Normalización de información.
- Generación de características.

Tecnologías propuestas:

- Python.
- Pandas.
- NumPy.
- Scikit-Learn.

---

# 5.6 Servicio de Inteligencia Artificial

El componente de Inteligencia Artificial será independiente del backend principal.

Estará compuesto por dos servicios principales:

---

## Modelo de Machine Learning

Se mantendrá el algoritmo:

**Isolation Forest**

Este modelo será utilizado para identificar comportamientos anómalos dentro del tráfico web.

Funciones:

- Analizar patrones de comportamiento.
- Detectar desviaciones respecto al tráfico normal.
- Clasificar eventos sospechosos.

Resultados posibles:

- Tráfico normal.
- Tráfico anómalo.

Como mejoras futuras se podrán evaluar modelos como:

- Random Forest.
- XGBoost.
- Autoencoders.
- Redes neuronales.

---

## Asistente Inteligente

Se mantendrá la integración con modelos generativos mediante:

- Ollama.
- Llama 3.2.

Funciones:

- Resolver consultas relacionadas con ciberseguridad.
- Explicar alertas detectadas.
- Proporcionar recomendaciones.

En la arquitectura objetivo este componente funcionará como un servicio independiente.

---

# 5.7 Base de datos

La arquitectura objetivo incorporará almacenamiento persistente para evitar la pérdida de información generada durante la ejecución.

Permitirá almacenar:

- Registros de tráfico.
- Alertas generadas.
- Resultados del modelo.
- Historial de análisis.
- Usuarios registrados.

Beneficios:

- Consulta de eventos anteriores.
- Generación de reportes.
- Análisis histórico.
- Mayor trazabilidad.

Tecnologías propuestas:

- PostgreSQL.
- MySQL.
- MongoDB.

---

# 5.8 Módulo de alertas

Este componente administrará los eventos detectados por el modelo de Inteligencia Artificial.

Funciones:

- Recibir resultados del análisis.
- Clasificar eventos.
- Generar alertas.
- Registrar información en la base de datos.

Tipos de resultados:

- Actividad normal.
- Actividad sospechosa.
- Posible amenaza.

El sistema continuará funcionando como herramienta de monitoreo, sin realizar bloqueo automático.

---

# 5.9 Sistema de monitoreo y registros

Este componente permitirá supervisar el funcionamiento interno del sistema.

Funciones:

- Registrar eventos importantes.
- Detectar errores.
- Generar métricas.
- Evaluar rendimiento.

Información registrada:

- Solicitudes procesadas.
- Alertas generadas.
- Errores del sistema.
- Estado de los servicios.
- Tiempo de respuesta.

Esto permitirá detectar fallos de manera temprana y facilitar el mantenimiento.

---

# 5.10 Seguridad y autenticación

La arquitectura objetivo incorporará mecanismos básicos de seguridad.

Funciones:

- Autenticación de usuarios.
- Control de acceso.
- Protección de información.
- Gestión de permisos.

Esta mejora permitirá restringir el acceso únicamente a usuarios autorizados.

---

# 5.11 Infraestructura y despliegue

Para mejorar la instalación y ejecución del sistema se incorporará una estrategia de despliegue basada en contenedores.

Tecnologías propuestas:

- Docker.
- Docker Compose.
- Kubernetes como mejora futura.

Beneficios:

- Configuración uniforme.
- Facilidad de instalación.
- Menor dependencia del entorno local.
- Preparación para ambientes productivos.

---

# 6. Diagrama de arquitectura objetivo

```text
                         +----------------+
                         |     Usuario    |
                         +-------+--------+
                                 |
                                 v
                    +------------+-------------+
                    | Dashboard / Interfaz Web |
                    +------------+-------------+
                                 |
                                 |
                                 v
                    +------------+-------------+
                    |        API Backend       |
                    |      Flask / FastAPI     |
                    +------------+-------------+
                                 |
        +------------------------+-------------------------+
        |                        |                         |
        v                        v                         v

+---------------+       +----------------+       +----------------+
| Captura de    |       | Servicio IA    |       | Base de Datos |
| tráfico web   |       | ML + LLM       |       | Historial     |
+-------+-------+       +--------+-------+       +-------+--------+
        |                        |                       |
        v                        v                       v

+---------------+       +----------------+       +----------------+
| Procesamiento |       | Isolation      |       | Alertas y      |
| de datos      |       | Forest/Llama   |       | registros      |
+---------------+       +----------------+       +----------------+

                                 |
                                 v

                     +----------------------+
                     | Monitoreo y métricas |
                     +----------------------+
