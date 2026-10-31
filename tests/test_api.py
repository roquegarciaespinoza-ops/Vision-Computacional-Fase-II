from fastapi.testclient import TestClient
from app.main import app, evaluar, normalizar

client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "ok"

def test_frontend():
    assert client.get("/").status_code == 200

def test_normalizar():
    assert normalizar(" 1234-abc ") == "1234ABC"

def test_autorizado_simulado():
    assert evaluar("1234-abc")["decision"] == "SIMULACION_AUTORIZADO"

def test_denegado_a_revision():
    assert evaluar("9999ZZZ")["decision"] == "REVISION_MANUAL"

def test_imagen_no_permitida():
    assert client.post("/api/reconocer", files={"archivo": ("x.txt", b"texto", "text/plain")}).status_code == 415

def test_imagen_corrupta():
    assert client.post("/api/reconocer", files={"archivo": ("x.png", b"corrupta", "image/png")}).status_code == 422

def test_imagen_grande():
    assert client.post("/api/reconocer", files={"archivo": ("x.png", b"x"*(5*1024*1024+1), "image/png")}).status_code == 413

def test_ocr_imagen_sintetica_integracion():
    """Prueba ruta completa HTTP -> imagen -> Tesseract -> JSON, sin imponer exactitud."""
    import io
    from scripts.evaluar_ocr_sintetico import imagen
    im = imagen("1234ABC", "limpia")
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    response = client.post("/api/reconocer", files={"archivo": ("sintetica.png", buf.getvalue(), "image/png")})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["placa"], str)
    assert data["decision"] in ("SIMULACION_AUTORIZADO", "REVISION_MANUAL")
    assert data["latencia_ms"] >= 0
    assert "advertencia" in data
