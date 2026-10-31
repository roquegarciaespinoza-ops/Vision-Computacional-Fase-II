# Matriz de cumplimiento Fase II

| Criterio (25 puntos cada uno) | Evidencia | Estado |
|---|---|---|
| Contenerización y despliegue local | Dockerfile, Docker Hub, [CI exitosa](https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II/actions/runs/41246280587), healthcheck | Verificado en CI; ejecución por evaluador reproducible |
| Integración frontend/backend/API | app/index.html, app/main.py, /docs y prueba HTTP en CI | Integración base verificada |
| Pruebas y validación | tests/test_api.py y docs/03_validacion_y_evidencias.md | Casos funcionales verificados; evaluación OCR cuantitativa pendiente |
| Documentación y repositorio | README.md, docs/01 a 04, historial GitHub | Documentación técnica publicada |

**Nota:** esta matriz no implica 100/100 garantizado. La aplicación Tesseract de referencia no es el modelo LinearSVC seleccionado previamente; se requiere cerrar esa brecha para sostener continuidad plena.
