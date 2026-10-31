# Cierre de Fase II — revisión documental y pruebas manuales (31 octubre 2026)

## Decisión de alcance
Se congela el desarrollo funcional. Este registro documenta el comportamiento actual, incluidos errores, sin modificar OCR, API, interfaz, contenedor ni modelo.

## Doble verificación técnica
- Repositorio principal: https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II
- Imagen Docker Hub: `roquegarciaespinoza/vision-computacional-fase-ii:fase2-baseline`.
- CI más reciente verificada: [run 41253589161](https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II/actions/runs/41253589161), resultado **success**. Incluye construcción, pytest, benchmark sintético, publicación de artefacto, comprobación HTTP y push a Docker Hub.
- Evidencia del benchmark sintético: [06_resultados_verificados.md](06_resultados_verificados.md): 6/6 exactas, CER 0 %, latencia media 92.71 ms **solo en imágenes generadas de manera controlada**.
- Entregables presentes en `entregables/`: `Manual_despliegue_nube.pdf`, `Manual_despliegue_nube.docx`, `Informe_pruebas_validacion.pdf`, `Informe_pruebas_validacion.docx`.
- Se comprobó manualmente `GET /health` con respuesta `status: ok` y `GET /` con HTTP 200 en Codespaces, además de la visualización de la interfaz en navegador.
- La demostración sintética 1234ABC devolvió placa 1234ABC, `SIMULACION_AUTORIZADO`, latencia 1294.3 ms, según captura del usuario. No equivale a autorización real.

## Pruebas manuales con fotografías de placas mexicanas
| Caso | Matrícula visible | OCR devuelto | Decisión | Latencia | Interpretación |
|---|---|---|---|---:|---|
| Fotografía de placa Jalisco | JCZ-263-A | JCZ-263-A; normalizada `JCZ263A` | `REVISION_MANUAL` | 373.52 ms | Reconocimiento correcto del texto; no está en padrón ficticio |
| Fotografía de placa Estado de México | PCH-96-04 | Vacío | `REVISION_MANUAL` | 586.86 ms | Falla de reconocimiento; no se autoriza por defecto |

**Resultado descriptivo:** 1 de 2 fotografías de prueba fue reconocida exactamente. No constituye un estudio estadístico ni un estimador generalizable de precisión. Las fotografías y capturas fueron mostradas por el usuario en conversación; **no se publican imágenes de matrículas reales en el repositorio** para evitar divulgación innecesaria. Los tiempos son los mostrados por la aplicación, no un benchmark reproducible bajo hardware controlado.

## Incidencias de despliegue observadas y resueltas
1. `curl -I /` devolvió HTTP 405 porque solicita HEAD y la ruta admite GET; no demuestra caída del servicio.
2. El puerto 8000 estuvo ocupado por otro contenedor; `docker ps` permitió identificarlo.
3. Codespaces devolvió HTTP 401 en URL reenviada privada en un momento de la sesión; corresponde al acceso del proxy de Codespaces, no al motor OCR. Posteriormente la aplicación se visualizó en navegador.
4. En un momento `curl` devolvió `connection refused` porque no había servidor escuchando; se volvió a iniciar el contenedor y `/health` respondió correctamente.
5. Se observó temporalmente un error HTTP interno/no JSON al analizar una imagen; otra prueba posterior devolvió respuesta JSON. No hay diagnóstico definitivo del error transitorio.

## Límites explícitos
- OCR Tesseract de referencia; **no** es el clasificador LinearSVC de Fase I.
- No hay detector robusto de placas en fotografías generales; se esperan imágenes centradas/recortadas.
- El 92.09 % histórico de Fase I mide clasificación de caracteres, no exactitud OCR integral.
- No hay despliegue PaaS público; sí existe imagen Docker publicada y reproducible localmente.
- Sin autenticación ni conexión a torniquetes/barreras; autorización únicamente simulada con matrículas ficticias.
- No atribuir 100 % de precisión a fotografías reales por el resultado 6/6 sintético.

## Cierre y rúbrica
La infraestructura, integración, pruebas automatizadas, documentación y artefactos están presentes y cuentan con enlaces de evidencia. Los resultados reales y las limitaciones quedan explícitos. Esta revisión **no garantiza una calificación de 100/100**; corresponde al docente evaluar el alcance de cada criterio. No se requieren cambios funcionales para este cierre documental.
