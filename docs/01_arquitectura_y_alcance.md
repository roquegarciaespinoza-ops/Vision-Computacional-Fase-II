# Arquitectura, alcance y trazabilidad — Fase II

## Problema
Demostrar un prototipo de lectura de caracteres de placas y consulta de un padrón **ficticio**, sin conexión a barreras físicas.

## Arquitectura
Navegador HTML/JS → POST multipart a FastAPI → validación de archivo → preprocesamiento PIL → OCR Tesseract → normalización alfanumérica → comparación con padrón ficticio → JSON con decisión simulada.

## Relación con Fase I
La [Actividad 5](https://github.com/roquegarciaespinoza-ops/Actividad5-Gestion-Datos-Entrenamiento-MLflow) seleccionó LinearSVC (92.09 % accuracy sobre caracteres recortados). El modelo serializado no está publicado por razones de privacidad/reproducibilidad. **El servicio actual emplea Tesseract como baseline de integración**, no el modelo de Fase I. La métrica histórica no es transferible al OCR de placas completas.

## Riesgos y límites
- No existe detector automático de placas en fotografías generales.
- No hay medición de exactitud OCR con conjunto etiquetado independiente.
- Sin autenticación ni protección para información real: uso local con datos sintéticos.
- No activar dispositivos físicos ni usar para decisiones reales.
- Evitar publicar fotografías de matrículas reales o datos personales.

## Nube
Arquitectura preparada para PaaS compatible con contenedores, pero **no desplegada**. Para producción requeriría autenticación, protección de datos, observabilidad, almacenamiento seguro y validación en campo.
