# Resultados verificados del benchmark OCR sintético

**Origen:** [GitHub Actions 41246847647](https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II/actions/runs/41246847647), artefacto `benchmark-ocr-sintetico` (ID 13058499923), commit `a57529d3d8e2ef3269d58024b8c278932da43d2b`.

## Resultados observados
- Motor: Tesseract (baseline de integración).
- Tamaño de muestra: **6 imágenes sintéticas** de matrículas recortadas.
- Coincidencia exacta: **6/6 (100 %)**.
- CER promedio: **0.0 (0 %)**.
- Latencia media: **92.71 ms** en el entorno GitHub Actions.

| Referencia | Condición | Predicción | Exacta | Latencia (ms) |
|---|---|---|---|---:|
| 1234ABC | Limpia | 1234ABC | Sí | 94.29 |
| 5678DEF | Limpia | 5678DEF | Sí | 94.11 |
| 2345BCD | Bajo contraste | 2345BCD | Sí | 93.89 |
| 3456CDE | Borrosa | 3456CDE | Sí | 92.86 |
| 4567DEF | Rotada | 4567DEF | Sí | 90.33 |
| 6789FGH | Limpia | 6789FGH | Sí | 90.80 |

## Interpretación responsable
Las imágenes fueron generadas por código y usan tipografía controlada. Este resultado solo demuestra que la ruta de OCR reconoce las seis condiciones ensayadas en el entorno de CI. No es un intervalo de confianza ni una medición representativa de fotografías reales. No valida detección automática de placas, control de acceso físico ni el clasificador LinearSVC histórico.

La aplicación sigue siendo una demostración con padrón ficticio. Antes de cualquier aplicación real deben obtenerse datos autorizados, etiquetas independientes, pruebas de errores y supervisión humana.
