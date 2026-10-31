# Manual de despliegue local y preparación de nube

## Requisitos
Docker Engine o Docker Desktop, puerto 8000 libre, al menos 1 GB de memoria disponible inicialmente (estimación, no medición). Conexión a internet para obtener imagen.

## Alternativa A: imagen publicada
```bash
docker pull roquegarciaespinoza/vision-computacional-fase-ii:fase2-baseline
docker run --rm --name vision-fase2 -p 8000:8000 roquegarciaespinoza/vision-computacional-fase-ii:fase2-baseline
```
Abrir http://localhost:8000 ; documentación API http://localhost:8000/docs ; chequeo http://localhost:8000/health.

## Alternativa B: construir desde GitHub
```bash
git clone https://github.com/roquegarciaespinoza-ops/Vision-Computacional-Fase-II.git
cd Vision-Computacional-Fase-II
docker build -t vision-fase-ii:local .
docker run --rm -p 8000:8000 vision-fase-ii:local
```

## Pruebas locales
En otra terminal:
```bash
curl -fsS http://localhost:8000/health
curl -fsS http://localhost:8000/
curl -X POST 'http://localhost:8000/api/verificar?placa=1234ABC'
curl -X POST -F 'archivo=@placa_recortada.png' http://localhost:8000/api/reconocer
```
El último comando requiere una imagen de prueba propia, preferentemente sintética, y el OCR puede fallar según la calidad de la imagen. La consulta `/api/verificar` es determinista, pero **no demuestra reconocimiento visual**.

## Problemas frecuentes
- Puerto ocupado: cambiar `-p 8000:8000` por `-p 8080:8000` y abrir localhost:8080.
- Imagen ilegible: enviar placa recortada con buena iluminación y caracteres visibles.
- Error 413: reducir imagen a 5 MB o menos.
- Error 415: usar PNG, JPEG o WebP.
- Error 422: comprobar integridad de imagen.
- Error de Docker Hub: construir localmente desde GitHub.

## Estrategia de nube (sin ejecución)
1. Elegir PaaS que acepte imagen Docker y soporte los recursos medidos.
2. Configurar puerto 8000 y healthcheck GET /health.
3. Restringir acceso, habilitar HTTPS y autenticación antes de utilizar datos reales.
4. Ejecutar pruebas de humo y observar latencia, errores y consumo.
5. Mantener despliegue privado y rollback por etiqueta de imagen.
**No se proporciona URL pública porque no existe despliegue real.**
