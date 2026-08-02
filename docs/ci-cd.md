# Integración Continua (CI)

## Descripción

Se implementó un pipeline de Integración Continua utilizando GitHub Actions. El objetivo es automatizar la validación del código cada vez que se realizan cambios en las ramas principales del repositorio.

El pipeline permite verificar automáticamente que las dependencias se instalen correctamente y que las pruebas automatizadas de la API sean ejecutadas exitosamente.

---

## Ubicación del pipeline

El archivo de configuración se encuentra en:

`.github/workflows/ci.yml`

---

## Funcionamiento del pipeline

El pipeline se ejecuta automáticamente cuando:

- Se realiza un `push` a la rama `main`.
- Se crea o actualiza un `pull request` hacia la rama `main`.

---

## Etapas del pipeline

### 1. Descarga del código

Se utiliza la acción:

```yaml
actions/checkout@v4