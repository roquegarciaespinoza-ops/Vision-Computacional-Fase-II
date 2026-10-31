# Validación, casos extremos y evidencias

## Evidencia automatizada comprobada
[GitHub Actions — ejecución 41246280587](https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II/actions/runs/41246280587): construcción Docker, pruebas Python, comprobación HTTP del servicio y publicación de imagen completadas exitosamente.

## Casos cubiertos por tests/test_api.py
| Caso | Resultado esperado |
|---|---|
| GET /health | 200 y status=ok |
| GET / | 200 |
| Normalizar ' 1234-abc ' | 1234ABC |
| Matrícula ficticia 1234ABC | SIMULACION_AUTORIZADO |
| Matrícula no registrada 9999ZZZ | REVISION_MANUAL |
| Archivo text/plain | 415 |
| Archivo PNG corrupto | 422 |
| Archivo >5 MB | 413 |

Estos son **resultados esperados definidos por las aserciones**; el workflow reporta que la batería terminó exitosamente. No se atribuye precisión OCR a estos casos.

## Pruebas pendientes de calidad del modelo
1. Preparar muestras sintéticas de matrículas recortadas con etiquetas conocidas.
2. Ejecutar inferencia OCR en muestras claras, borrosas, inclinadas y de bajo contraste.
3. Medir exact match, CER y latencia por muestra, con número de observaciones y hardware.
4. Analizar errores y establecer límites de uso.

## Interpretación
El pipeline de infraestructura y API está validado en CI. La evaluación estadística del reconocimiento de matrículas completas **no está realizada**. La cifra histórica 92.09 % pertenece a clasificación de caracteres de Fase I.

## Adenda de pruebas reales y cierre
Se documentaron dos fotografías de placas mexicanas: Jalisco `JCZ-263-A` reconocida correctamente (373.52 ms) y Estado de México `PCH-96-04` con OCR vacío (586.86 ms). Ambas resultaron en `REVISION_MANUAL`, dado que el padrón es ficticio. Ver [registro completo, incidencias y evidencia de CI](07_cierre_y_pruebas_manuales.md). La tasa descriptiva 1/2 no es una medición estadísticamente representativa.
