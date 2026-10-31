# Matriz de cumplimiento Fase II (evidencia actualizada)

| Criterio (25 puntos cada uno) | Evidencia verificable | Estado y alcance |
|---|---|---|
| Contenerización y ejecución local | `Dockerfile`, Docker Hub, [CI exitosa con publicación](https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II/actions/runs/41247540361), `GET /health` | Construcción, tests y publicación verificados en CI; ejecución por evaluador disponible |
| Integración frontend/backend/API | `app/index.html`, `app/main.py`, `POST /api/reconocer`, botón de demostración sintética y test integral | Verificado en contenedor y pruebas HTTP |
| Pruebas y validación | `tests/test_api.py`, `tests/test_benchmark.py`, [benchmark medido](06_resultados_verificados.md), [artefacto de CI](https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II/actions/runs/41246847647) | 6/6 imágenes sintéticas; CER 0 %; latencia media 92.71 ms. **Sin validación de fotografías reales** |
| Documentación y repositorio | `README.md`, `docs/`, `entregables/` PDF/DOCX y [generación exitosa](https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II/actions/runs/41247296970) | Cuatro documentos formales publicados y trazables |

## Aspectos pendientes y límites explícitos
- **Continuidad de Fase I:** LinearSVC entrenado sobre caracteres individuales no se ha integrado; el OCR actual usa Tesseract.
- **Alcance visual:** entrada de matrícula recortada, sin detección de placas en fotografías generales.
- **Despliegue:** aplicación reproducible en Docker local; **no hay despliegue público en nube**.
- **Precisión:** el 100 % de coincidencia de seis imágenes sintéticas no estima rendimiento real.
- **Seguridad:** padrón ficticio y decisión simulada; sin autorización física, autenticación ni tratamiento de datos reales.

Esta matriz muestra evidencias de cumplimiento, **no constituye una calificación garantizada de 100/100**.
