"""Prototipo académico: OCR de placas y autorización simulada. No controla barreras."""
import io, os, re, time
from pathlib import Path
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, Response
from PIL import Image, ImageOps, UnidentifiedImageError, ImageDraw, ImageFont
import pytesseract

app = FastAPI(title="Control de acceso vehicular - Fase II", version="0.1.0")
BASE = Path(__file__).resolve().parent
PLATES = {"1234ABC", "5678DEF"}  # datos ficticios exclusivamente
MAX_BYTES = 5 * 1024 * 1024

def normalizar(texto: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", texto.upper())

def extraer_matricula(texto: str) -> str:
    """Reconoce formatos ficticios 1234ABC y mexicano AAA999A.

    Corrige confusiones OCR únicamente en posiciones definidas por el formato.
    No debe emplearse para decisiones de acceso real sin validación adicional.
    """
    valor = normalizar(texto)
    if re.fullmatch(r"[0-9]{4}[A-Z]{3}", valor):
        return valor
    if len(valor) == 7:
        letras = {"0": "O", "1": "I", "2": "Z", "5": "S", "7": "Z", "8": "B"}
        digitos = {"O": "0", "I": "1", "L": "1", "S": "5", "B": "8", "Z": "2"}
        candidato = "".join((letras.get(ch, ch) if i in (0, 1, 2, 6) else digitos.get(ch, ch)) for i, ch in enumerate(valor))
        if re.fullmatch(r"[A-Z]{3}[0-9]{3}[A-Z]", candidato):
            return candidato
    return valor


def reconocer_texto(im: Image.Image) -> tuple[str, str]:
    """OCR de referencia: imagen completa y franja central para placas mexicanas.

    No realiza detección de objetos ni garantiza precisión en fotos arbitrarias.
    """
    gris = ImageOps.autocontrast(ImageOps.grayscale(im))
    config = "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    principal = pytesseract.image_to_string(gris, config=f"--psm 7 {config}").strip()
    if re.fullmatch(r"[0-9]{4}[A-Z]{3}", normalizar(principal)):
        return normalizar(principal), principal
    w, h = gris.size
    franja = gris.crop((int(w * .103), int(h * .341), int(w * .849), int(h * .691)))
    alternativo = pytesseract.image_to_string(franja, config=f"--psm 13 {config}").strip()
    candidato = extraer_matricula(alternativo)
    if re.fullmatch(r"[A-Z]{3}[0-9]{3}[A-Z]", candidato):
        return candidato, alternativo
    return extraer_matricula(principal), principal


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

@app.get("/api/demo/placa.png")
def placa_demostracion():
    """Imagen generada artificialmente; no contiene datos de residentes."""
    im = Image.new("RGB", (440, 110), "white")
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 54)
    d.text((32, 16), "1234ABC", font=font, fill="black")
    buffer = io.BytesIO()
    im.save(buffer, format="PNG")
    return Response(content=buffer.getvalue(), media_type="image/png",
                    headers={"Cache-Control": "no-store"})

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
        placa, texto = reconocer_texto(im)
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(422, "Imagen inválida o corrupta")
    except pytesseract.TesseractError:
        raise HTTPException(503, "Motor OCR no disponible")
    resultado = evaluar(placa)
    return {**resultado, "texto_ocr": texto.strip(), "latencia_ms": round((time.perf_counter()-inicio)*1000,2),
            "advertencia": "OCR Tesseract de referencia; no es el modelo LinearSVC de Fase I. Recorte heurístico central, sin detección automática de placa."}

@app.post("/api/verificar")
def verificar(placa: str):
    return evaluar(placa)
