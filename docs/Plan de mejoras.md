# 16. Plan de Mejoras

## Objetivo

El presente plan de mejoras tiene como finalidad fortalecer la arquitectura del sistema, reducir la deuda técnica identificada durante el desarrollo del prototipo y aumentar la precisión del modelo de inteligencia artificial. Las actividades propuestas permitirán que el sistema evolucione hacia una solución más escalable, mantenible y preparada para una futura implementación en un entorno de producción.

---

## Plan de trabajo

| **Mejora** | **Problema identificado** | **Actividades a realizar** | **Resultado esperado** | **Prioridad** |
|-------------|---------------------------|----------------------------|------------------------|:-------------:|
| **Separación de la arquitectura mediante una API REST** | La interfaz y la lógica de negocio presentan un alto acoplamiento. | - Diseñar los contratos de la API.<br>- Implementar los endpoints REST.<br>- Desacoplar el frontend del backend.<br>- Validar la comunicación entre módulos. | Arquitectura modular, mayor mantenibilidad y facilidad para futuras integraciones. | 🔴 Alta |
| **Optimización del modelo de Inteligencia Artificial** | La precisión del modelo puede verse afectada por la cantidad y calidad de los datos utilizados durante el entrenamiento. | - Incorporar nuevos conjuntos de datos.<br>- Limpiar la información.<br>- Ajustar hiperparámetros.<br>- Comparar distintos algoritmos de aprendizaje automático. | Mayor precisión en la detección de amenazas y reducción de falsos positivos. | 🔴 Alta |
| **Implementación de pruebas automatizadas** | La cobertura de pruebas es limitada y algunos errores podrían detectarse tardíamente. | - Crear pruebas unitarias.<br>- Implementar pruebas de integración.<br>- Automatizar las validaciones antes del despliegue. | Mayor estabilidad del sistema y reducción de errores durante el desarrollo. | 🔴 Alta |
| **Optimización del rendimiento** | El sistema aún no ha sido evaluado bajo escenarios de alta carga. | - Medir tiempos de respuesta.<br>- Optimizar consultas y procesamiento.<br>- Reducir consumo de memoria y CPU. | Mejor desempeño y capacidad para atender múltiples solicitudes simultáneamente. | 🟡 Media |
| **Automatización del despliegue** | La instalación del sistema requiere varios pasos manuales. | - Crear archivos Docker.<br>- Automatizar la configuración del entorno.<br>- Documentar el proceso de despliegue. | Instalación rápida, consistente y con menor probabilidad de errores. | 🟡 Media |
| **Fortalecimiento del monitoreo** | El sistema únicamente genera alertas básicas. | - Incorporar registros detallados (logs).<br>- Agregar métricas de rendimiento.<br>- Implementar paneles de monitoreo. | Mayor capacidad para supervisar el funcionamiento del sistema y detectar incidentes. | 🟡 Media |
| **Actualización de la documentación técnica** | La documentación requiere mantenerse sincronizada con el desarrollo del proyecto. | - Actualizar diagramas.<br>- Documentar cambios de arquitectura.<br>- Registrar nuevas funcionalidades y dependencias. | Facilitar el mantenimiento y la incorporación de nuevos desarrolladores. | 🟢 Baja |

---

## Cronograma de implementación

| **Fase** | **Mejora principal** | **Tiempo estimado** |
|-----------|----------------------|---------------------|
| Fase 1 | Separación mediante API REST | 1 semana |
| Fase 2 | Optimización del modelo de IA | 2 semanas |
| Fase 3 | Implementación de pruebas automatizadas | 1 semana |
| Fase 4 | Optimización del rendimiento | 1 semana |
| Fase 5 | Automatización del despliegue | 1 semana |
| Fase 6 | Implementación de monitoreo | 1 semana |
| Fase 7 | Actualización de la documentación | Durante todo el proyecto |

---

## Indicadores de éxito

| **Indicador** | **Meta esperada** |
|---------------|-------------------|
| Precisión del modelo de IA | Mayor al 90 % |
| Reducción de falsos positivos | Disminuir al menos un 20 % |
| Cobertura de pruebas | Igual o superior al 80 % |
| Tiempo promedio de respuesta | Menor a 2 segundos |
| Automatización del despliegue | Instalación completa mediante Docker |
| Actualización de documentación | 100 % de las funcionalidades documentadas |

---

## Beneficios esperados

- Incrementar la precisión en la detección de amenazas.
- Reducir la deuda técnica acumulada durante el desarrollo del prototipo.
- Facilitar el mantenimiento y la evolución del sistema.
- Mejorar el rendimiento y la escalabilidad de la aplicación.
- Contar con un proceso de despliegue más eficiente y reproducible.
- Disponer de una documentación técnica completa y actualizada.