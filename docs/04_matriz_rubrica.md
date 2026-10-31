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

## Doble check final — 31 octubre 2026
- **Contenerización (25 pts):** Dockerfile, imagen versionada, ejecución local documentada y [CI 41253589161 exitosa](https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II/actions/runs/41253589161).
- **Integración (25 pts):** frontend/API/backend, salud HTTP, demo sintética y pruebas manuales de navegador documentadas en [cierre](07_cierre_y_pruebas_manuales.md).
- **Pruebas (25 pts):** pytest y benchmark sintético verificables; **también se registran los dos ensayos reales, incluido el fallo de OCR**, sin extrapolar 6/6 a campo.
- **Documentación (25 pts):** README, manual, informe, arquitectura, matriz, evidencia cuantitativa y cierre; PDF y DOCX en `entregables/`.

**Precisión de la documentación:** los PDF/DOCX existentes se generaron antes de esta adenda. La evidencia manual más reciente y el doble check están en `docs/07_cierre_y_pruebas_manuales.md`; no se afirma que los binarios incorporen esas observaciones. El profesor determina la puntuación final; no se garantiza 100/100.
