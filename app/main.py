"""Prototipo académico: OCR de placas y autorización simulada. No controla barreras."""
import io, os, re, time
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from PIL import Image, ImageOps, UnidentifiedImageError
import pytesseract

app = FastAPI(title="Control de acceso vehicular - Fase II", version="0.1.0")
BASE = Path(__file__).resolve().parent
PLATES = {"1234ABC", "5678DEF"}  # datos ficticios exclusivamente
MAX_BYTES = 5 * 1024 * 1024

def normalizar(texto: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", texto.upper())

def evaluar(placa: str) -> dict:
    placa = normalizar(placa)
    return {"placa": placa, "autorizado": placa in PLATES if placa else False,
            "decision": "SIMULACION_AUTORIZADO" if placa in PLATES and placa else "REVISION_MANUAL"}

@app.get("/", response_class=HTMLResponse)
def inicio():
    return (BASE / "index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status": "ok", "modo": "academico", "motor": "tesseract-baseline"}

@app.post("/api/reconocer")
async def reconocer(archivo: UploadFile = File(...)):
    if archivo.content_type not in ("image/png", "image/jpeg", "image/webp"):
        raise HTTPException(415, "Se requiere imagen PNG, JPEG o WebP")
    data = await archivo.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "Imagen mayor de 5 MB")
    inicio = time.perf_counter()
    try:
        im = Image.open(io.BytesIO(data))
        im.verify()
        im = Image.open(io.BytesIO(data))
        if im.width * im.height > 16_000_000:
            raise HTTPException(413, "Imagen demasiado grande")
        im = ImageOps.autocontrast(ImageOps.grayscale(im))
        texto = pytesseract.image_to_string(im, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(422, "Imagen inválida o corrupta")
    except pytesseract.TesseractError:
        raise HTTPException(503, "Motor OCR no disponible")
    resultado = evaluar(texto)
    return {**resultado, "texto_ocr": texto.strip(), "latencia_ms": round((time.perf_counter()-inicio)*1000,2),
            "advertencia": "OCR Tesseract de referencia; no es el modelo LinearSVC de Fase I. Sin detección automática de placa."}

@app.post("/api/verificar")
def verificar(placa: str):
    return evaluar(placa)
