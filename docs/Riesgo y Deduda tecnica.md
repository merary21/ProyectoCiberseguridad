| Riesgo técnico                                   | Descripción                                                                                                      | Probabilidad | Impacto | Estrategia de mitigación                                                                               |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ------------ | ------- | ------------------------------------------------------------------------------------------------------ |
| Datos insuficientes para entrenar el modelo      | El conjunto de datos puede no contener suficientes ejemplos de tráfico malicioso para obtener un modelo preciso. | Alta         | Alta    | Utilizar conjuntos de datos adicionales, realizar limpieza de datos y validar continuamente el modelo. |
| Alta tasa de falsos positivos                    | El modelo puede generar alertas sobre tráfico legítimo, disminuyendo la confianza en el sistema.                 | Media        | Alta    | Ajustar los hiperparámetros del modelo y evaluar diferentes algoritmos de aprendizaje automático.      |
| Baja capacidad de detección de nuevas amenazas   | El modelo puede no identificar ataques que no estuvieron presentes durante el entrenamiento.                     | Media        | Alta    | Actualizar periódicamente el modelo con nuevos datos y realizar reentrenamientos.                      |
| Problemas de integración entre módulos           | Pueden surgir incompatibilidades entre la interfaz web, la API y el módulo de inteligencia artificial.           | Media        | Media   | Definir contratos claros mediante una API REST y realizar pruebas de integración.                      |
| Bajo rendimiento en tiempo real                  | El procesamiento de grandes volúmenes de solicitudes puede aumentar el tiempo de respuesta del sistema.          | Media        | Alta    | Optimizar el código, reducir operaciones innecesarias y monitorear el consumo de recursos.             |
| Errores en la captura de tráfico                 | El sistema podría no registrar correctamente todas las solicitudes HTTP analizadas.                              | Baja         | Alta    | Implementar validaciones, manejo de excepciones y pruebas funcionales continuas.                       |
| Dependencia de librerías externas                | Cambios o incompatibilidades en bibliotecas utilizadas podrían afectar el funcionamiento del sistema.            | Baja         | Media   | Utilizar versiones estables y documentar las dependencias del proyecto.                                |
| Cambios en la arquitectura durante el desarrollo | La incorporación de nuevas funcionalidades puede requerir modificaciones importantes en la arquitectura inicial. | Media        | Media   | Diseñar una arquitectura modular y documentar los cambios realizados.                                  |


## Deuda Técnica

**Proyecto:** Sistema de Monitoreo Inteligente para Ciberseguridad Web
*Probabilidad e Impacto calificados como: **Baja / Media / Alta***

| # | Categoría | Elemento de Deuda | Probabilidad | Impacto | Plan de reducción |
| :-: | :--- | :--- | :-: | :-: | :--- |
| 1 | Arquitectura | **Arquitectura inicial monolítica:** Durante el primer prototipo algunos componentes permanecen acoplados, dificultando su mantenimiento. | Alta | Alta | Separar la lógica mediante una API y una arquitectura por capas. |
| 2 | Calidad / QA | **Cobertura limitada de pruebas:** No todos los módulos cuentan con pruebas unitarias e integración automatizadas. | Media | Alta | Incorporar pruebas automatizadas conforme avance el desarrollo. |
| 3 | Código | **Código pendiente de refactorización:** Algunas funciones fueron implementadas rápidamente para validar el prototipo y requieren optimización. | Alta | Media | Refactorizar el código siguiendo buenas prácticas y principios SOLID. |
| 4 | Documentación | **Documentación técnica incompleta:** Parte de la documentación del código y de la arquitectura aún no está completamente actualizada. | Media | Media | Mantener la documentación sincronizada con cada iteración del proyecto. |
| 5 | DevOps | **Configuración manual del entorno:** Algunas dependencias requieren configuración manual para ejecutar el sistema. | Media | Media | Automatizar la instalación mediante scripts o contenedores Docker. |
| 6 | Escalabilidad | **Escalabilidad limitada:** El sistema está diseñado como un prototipo académico y no para un entorno de producción. | Alta | Alta | Implementar una arquitectura basada en servicios y preparada para escalar. |
| 7 | Monitoreo | **Ausencia de monitoreo avanzado:** El sistema genera alertas, pero aún no incorpora métricas avanzadas ni paneles de monitoreo. | Media | Media | Integrar herramientas de monitoreo y generación de métricas en futuras versiones. |
| 8 | Modelo (IA) | **Optimización pendiente del modelo de IA:** El modelo puede mejorar su precisión mediante ajuste de parámetros y nuevos datos de entrenamiento. | Alta | Alta | Realizar reentrenamientos periódicos y comparar el desempeño con otros algoritmos. |
