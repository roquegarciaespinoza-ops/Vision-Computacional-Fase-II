# Evaluación OCR con muestras sintéticas

Se añadió un benchmark reproducible de seis imágenes **generadas por código**, con caracteres conocidos y condiciones limpia, bajo contraste, desenfoque y rotación leve.

## Ejecución
```bash
docker build -t vision-fase-ii:local .
docker run --rm vision-fase-ii:local python -m scripts.evaluar_ocr_sintetico
```
En GitHub Actions el archivo `results/ocr_sintetico.json` se conserva como artefacto de la ejecución y contiene por muestra: referencia, predicción, coincidencia exacta, CER y latencia en milisegundos, además de agregados.

## Interpretación y límites
- Estas seis imágenes **no son datos reales ni representativos** de placas de vehículos.
- Las métricas son de **Tesseract** (baseline de integración), no de LinearSVC de Fase I.
- No existe garantía de rendimiento en imágenes completas, exteriores o diferentes tipografías.
- El benchmark se ejecuta automáticamente y **no establece umbral mínimo de precisión**, porque no se ha definido uno respaldado por datos reales.
- Para validación final de desempeño real se requieren imágenes autorizadas, etiquetadas y un protocolo independiente.
