# Imagen mínima para validar integración GitHub Actions -> Docker Hub.
# No contiene aún el modelo ni la aplicación de Fase II.
FROM alpine:3.20
CMD ["sh", "-c", "echo 'Integracion GitHub Actions y Docker Hub operativa'"]
