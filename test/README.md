# Sistema Inteligente de Detección de Anomalías en Aplicaciones Web con Inteligencia Artificial

## 1. Nombre del proyecto

**Sistema Inteligente de Detección de Anomalías en Aplicaciones Web con Inteligencia Artificial**

Este proyecto consiste en el desarrollo de una aplicación inteligente orientada a fortalecer la seguridad de aplicaciones web mediante el análisis automático del tráfico generado por los usuarios. 
La solución integra técnicas de Inteligencia Artificial para identificar comportamientos anómalos que puedan representar posibles amenazas de ciberseguridad, además de incorporar un asistente inteligente que brinda recomendaciones relacionadas con incidentes de seguridad.

El proyecto forma parte del Módulo 4 de Desarrollo de Aplicaciones con Inteligencia Artificial y tiene como finalidad demostrar la integración de modelos de Machine Learning e Inteligencia Artificial Generativa dentro de una aplicación funcional.

---

## 2. Integrantes del grupo

**Módulo:** Módulo 4 - Desarrollo de Aplicaciones con IA

**Semana:** Semana 1 - Diagnóstico y Arquitectura Inicial

**Grupo:** Grupo #5

**Integrantes**

- Gilmar Adriel González Romero
- Nathaly Sarai Rodríguez Silva
- Merary Julissa Araujo Velásquez

---

## 3. Descripción del problema que se desea resolver

Actualmente las aplicaciones web están expuestas a múltiples amenazas informáticas, entre ellas ataques de fuerza bruta, intentos de acceso no autorizados, escaneo de vulnerabilidades y diferentes tipos de tráfico malicioso. 
En muchas organizaciones la detección de estos incidentes depende de herramientas tradicionales o de procesos manuales que requieren una supervisión constante por parte del personal de seguridad.

Cuando el volumen de tráfico aumenta considerablemente, resulta difícil identificar oportunamente comportamientos sospechosos, incrementando el riesgo de que un ataque afecte la disponibilidad, integridad o confidencialidad de la información.

Como respuesta a esta problemática, el presente proyecto propone una solución basada en Inteligencia Artificial capaz de analizar automáticamente el tráfico web, identificar patrones anómalos y generar alertas tempranas que permitan apoyar la toma de decisiones de los administradores y analistas de ciberseguridad.

---

## 4. Usuarios o beneficiarios principales

Los principales usuarios del sistema son las personas encargadas de administrar y proteger aplicaciones web, así como instituciones interesadas en implementar soluciones inteligentes para fortalecer la seguridad informática.

| Usuario | Beneficio obtenido |
|----------|-------------------|
| Administradores de sistemas | Detectar comportamientos anómalos en el tráfico web de manera automática. |
| Analistas de ciberseguridad | Recibir alertas que faciliten la identificación de posibles amenazas. |
| Empresas y organizaciones | Reducir riesgos asociados a ataques informáticos mediante monitoreo inteligente. |
| Instituciones educativas | Utilizar la aplicación como herramienta de aprendizaje sobre IA aplicada a la ciberseguridad. |

El sistema busca reducir el tiempo requerido para analizar registros de tráfico y facilitar la detección temprana de incidentes de seguridad.

---

## 5. Descripción general de la solución

La solución desarrollada consiste en una aplicación web implementada en Python que analiza registros de tráfico provenientes de aplicaciones web utilizando algoritmos de Inteligencia Artificial.

El sistema procesa automáticamente la información recibida, identifica posibles anomalías mediante un modelo de Machine Learning y presenta los resultados a través de una interfaz amigable para el usuario. 
Cuando se detecta un comportamiento sospechoso, el sistema genera una alerta que puede ser revisada por el administrador.

Como complemento, la aplicación incorpora un asistente inteligente basado en el modelo Llama 3.2 ejecutado mediante Ollama, el cual responde consultas relacionadas con ciberseguridad y proporciona recomendaciones sobre las alertas detectadas.

La combinación de ambas tecnologías permite ofrecer una herramienta capaz de automatizar parte del proceso de monitoreo y análisis de eventos de seguridad.

---

## 6. Explicación clara de dónde se encuentra la Inteligencia Artificial dentro del proyecto

La Inteligencia Artificial representa el componente principal de la aplicación y se encuentra integrada en dos módulos diferentes.

El primero corresponde al sistema de detección de anomalías, donde se utiliza el algoritmo **Isolation Forest** para analizar automáticamente el tráfico web e identificar registros cuyo comportamiento difiere significativamente del resto de los datos analizados. 
Este proceso permite detectar posibles amenazas sin necesidad de definir reglas manuales para cada tipo de ataque.

El segundo módulo corresponde al asistente inteligente implementado mediante **Llama 3.2**, ejecutado utilizando **Ollama**. 
Este asistente utiliza Inteligencia Artificial Generativa para responder preguntas del usuario relacionadas con conceptos de ciberseguridad, interpretación de alertas y recomendaciones generales de seguridad.

Gracias a la integración de ambos componentes, la aplicación combina técnicas de Machine Learning con modelos de lenguaje para ofrecer una solución más completa y de mayor utilidad para el usuario.

---

## 7. Tipo de IA, modelo, servicio, algoritmo o técnica utilizada

| Elemento | Tecnología utilizada |
|-----------|----------------------|
| Tipo de Inteligencia Artificial | Machine Learning e Inteligencia Artificial Generativa |
| Técnica utilizada | Aprendizaje No Supervisado |
| Algoritmo | Isolation Forest |
| Modelo de lenguaje | Llama 3.2 |
| Servicio utilizado | Ollama |
| Biblioteca de Machine Learning | Scikit-Learn |
| Lenguaje de programación | Python |

El algoritmo **Isolation Forest** permite detectar anomalías dentro del conjunto de datos analizados, mientras que **Llama 3.2** proporciona capacidades conversacionales que permiten responder consultas relacionadas con ciberseguridad.

---

## 8. Datos de entrada y salida esperados

### Datos de entrada

El sistema recibe información correspondiente al tráfico generado por una aplicación web, entre la que se encuentran:

- Dirección IP.
- Método HTTP utilizado.
- URL solicitada.
- Código de respuesta HTTP.
- Hora de la solicitud.
- User-Agent del navegador.
- Registros del tráfico web.
- Consultas realizadas por el usuario al asistente inteligente.

### Datos de salida

Después del procesamiento, el sistema genera los siguientes resultados:

- Clasificación del tráfico como **Normal** o **Anómalo**.
- Alertas sobre posibles amenazas.
- Recomendaciones de seguridad generadas por el asistente inteligente.
- Historial de eventos analizados.
- Métricas generales del monitoreo realizado.

---

## 9. Instrucciones básicas de instalación o ejecución

### Requisitos

- Python 3.11 o superior.
- Pip.
- Ollama instalado.
- Modelo Llama 3.2 descargado.

### Levantar el entorno virtual

```bash
.venv\Scripts\Activate.ps1
```

### Instalación de dependencias


```bash
pip install -r test/requirements.txt
```

### Descargar el modelo de lenguaje

```bash
ollama pull llama3.2
```

### Ejecutar Ollama

```bash
ollama serve
```

### Ejecutar la aplicación

```bash
python app.py
```

Una vez iniciada la aplicación, el usuario podrá acceder a la interfaz web para monitorear el tráfico, visualizar las alertas generadas por el modelo de Inteligencia Artificial y realizar consultas al asistente inteligente.

---

## 10. Variables de entorno requeridas
Las principales variables utilizadas son:

| Variable | Descripción |
|----------|-------------|
| OLLAMA_MODEL | Modelo utilizado por Ollama para responder consultas. |

En futuras versiones se incorporarán variables adicionales relacionadas con la conexión a bases de datos, configuraciones de despliegue y servicios externos.

---

## 11. Referencia a la arquitectura actual y arquitectura objetivo

La documentación técnica del proyecto se encuentra organizada dentro de la carpeta **docs/**.

Los documentos disponibles son:

- [Diagnóstico técnico](docs/diagnostico-semana-1.md)
- [Arquitectura actual](docs/arquitectura-actual.md)
- [Arquitectura objetivo](docs/arquitectura-objetivo.md)
- [Riesgos técnicos y deuda técnica](docs/riesgos-tecnicos.md)
- [Plan de mejora](docs/plan-mejora.md)

En estos documentos se describe el estado actual del proyecto, la arquitectura implementada, la arquitectura objetivo propuesta, los riesgos técnicos identificados y el plan de mejora que se desarrollará durante las siguientes semanas del módulo.

---

## 12. Limitaciones conocidas del prototipo

Actualmente el proyecto corresponde a un prototipo funcional desarrollado con fines académicos, por lo que aún presenta algunas limitaciones técnicas que serán abordadas durante el desarrollo del módulo.

Las principales limitaciones identificadas son las siguientes:

- El modelo de detección depende de la calidad y cantidad del conjunto de datos utilizado para el entrenamiento.
- El asistente inteligente requiere que Ollama esté instalado y ejecutándose localmente.
- La aplicación únicamente detecta anomalías y genera alertas, pero no ejecuta acciones automáticas para bloquear ataques.
- La arquitectura actual aún no cuenta con una API que permita separar la lógica del backend de la interfaz.
- No se dispone de pruebas automatizadas que permitan validar el correcto funcionamiento del sistema.
- La aplicación todavía no se encuentra preparada para un despliegue mediante contenedores.
- No existen mecanismos de monitoreo, métricas o registros (logs) que permitan supervisar el comportamiento de la aplicación.
- La aplicación no cuenta con autenticación de usuarios ni otras medidas de seguridad para un entorno de producción.
- La documentación técnica aún debe ampliarse y actualizarse conforme avance el desarrollo del proyecto.

Estas limitaciones representan oportunidades de mejora que serán abordadas progresivamente durante las semanas 2 a 6 del módulo.

---

## 13. Plan de mejora para las semanas 2 a 6

Con el propósito de superar las limitaciones identificadas en el prototipo actual, se ha definido el siguiente plan de trabajo:

| Semana | Objetivo | Relación con las limitaciones |
|---------|----------|-------------------------------|
| **Semana 2** | Implementar una API inteligente que separe la interfaz del backend y definir los contratos de entrada y salida del sistema. | Soluciona la falta de una arquitectura organizada y mejora la escalabilidad del proyecto. |
| **Semana 3** | Implementar pruebas unitarias, automatización e integración continua (CI/CD). Además, mejorar el conjunto de datos para fortalecer el rendimiento del modelo de IA. | Reduce errores del sistema y mejora la calidad del modelo de detección. |
| **Semana 4** | Contenerizar la aplicación utilizando Docker y preparar el entorno de despliegue. | Elimina la dependencia de configuraciones manuales y facilita la instalación del sistema. |
| **Semana 5** | Incorporar registros (logs), métricas, monitoreo del sistema y optimizar el rendimiento general de la aplicación. | Permite supervisar el funcionamiento del sistema y detectar fallos de forma temprana. |
| **Semana 6** | Implementar autenticación de usuarios, fortalecer la seguridad, actualizar la documentación técnica y preparar la defensa final del proyecto. | Atiende las limitaciones relacionadas con la seguridad, documentación y presentación del proyecto. |

Al finalizar estas mejoras, se espera contar con una aplicación más robusta, organizada y preparada para un posible despliegue, manteniendo la capacidad de detectar anomalías mediante Inteligencia Artificial y proporcionando una solución más completa para el monitoreo de aplicaciones web.
