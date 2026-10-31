# Fase II · Sistema inteligente de control de acceso vehicular

Prototipo académico para la Unidad Habitacional TecMilenio. **No controla dispositivos físicos ni debe utilizarse para autorizar accesos reales.**

## Estado técnico y trazabilidad
- **Fase I / Actividad 5:** clasificación de caracteres individuales con LinearSVC (accuracy 92.09 % sobre 2,566 caracteres), sin lectura integral de matrículas. [Evidencias originales](https://github.com/roquegarciaespinoza-ops/Actividad5-Gestion-Datos-Entrenamiento-MLflow).
- **Fase II / integración:** aplicación web FastAPI, OCR de referencia con Tesseract para imágenes de placas ya recortadas, API REST, verificación simulada contra padrón ficticio y Docker.
- **Importante:** Tesseract **no es** el modelo LinearSVC entrenado en Fase I. No se ha integrado un artefacto serializado de LinearSVC ni validado el OCR de placas completas. No se debe atribuir el 92.09 % a esta aplicación.

## Ejecutar con Docker
```bash
docker build -t vision-fase-ii:local .
docker run --rm -p 8000:8000 vision-fase-ii:local
```
Abrir http://localhost:8000 ; API en http://localhost:8000/docs ; salud en http://localhost:8000/health.

La imagen publicada en Docker Hub puede ejecutarse sustituyendo `vision-fase-ii:local` por el nombre y etiqueta **verificados** de la imagen publicada.

## API
- `GET /health`: estado del servicio.
- `POST /api/reconocer`: multipart `archivo` PNG/JPEG/WebP, máximo 5 MB; devuelve texto OCR, placa normalizada, decisión simulada y latencia.
- `POST /api/verificar?placa=1234ABC`: prueba determinista de reglas de autorización simulada.

Padrón **ficticio**: `1234ABC` y `5678DEF`. Una coincidencia solo produce `SIMULACION_AUTORIZADO`; cualquier otra entrada requiere `REVISION_MANUAL`.

## Pruebas
```bash
docker build -t vision-fase-ii:local .
docker run --rm vision-fase-ii:local pytest -q
```
Las pruebas automatizadas verifican salud, frontend, normalización, autorización simulada y rechazos por tipo, tamaño y corrupción de archivos. **No constituyen una validación de precisión OCR**, que requiere imágenes etiquetadas y evaluación independiente.

## Despliegue en nube (documentado, no ejecutado)
El contenedor expone el puerto 8000 y escucha en 0.0.0.0. En un PaaS compatible con Docker: conectar repositorio o imagen, asignar al menos 1 GB RAM inicialmente sujeto a medición, exponer puerto 8000, definir chequeo de salud `/health`, restringir acceso y revisar logs. No se ha desplegado una instancia pública.

## Seguridad y limitaciones
No cargar placas reales, datos de residentes ni imágenes personales. Sin autenticación, detección de matrículas en fotografías generales, evaluación de OCR sobre conjunto independiente, RFID ni integración física. Uso únicamente educativo. Verificar licencias y privacidad antes de cualquier evolución operativa.

## Evidencias
La construcción, pruebas y publicación se verificarán en GitHub Actions. No considerar un flujo exitoso como prueba de exactitud del modelo. Las métricas históricas permanecen en el repositorio de Actividad 5.
