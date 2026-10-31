"""Benchmark reproducible sobre imágenes sintéticas; NO equivale a evaluación real."""
import json, time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import pytesseract
from app.main import normalizar

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SAMPLES = [("1234ABC","limpia"),("5678DEF","limpia"),("2345BCD","contraste_bajo"),
           ("3456CDE","borrosa"),("4567DEF","rotada"),("6789FGH","limpia")]

def imagen(placa, condicion):
    im=Image.new("RGB",(440,110),"white")
    d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,54)
    d.text((32,16),placa,font=f,fill="black")
    if condicion=="contraste_bajo":
        im=ImageEnhance.Contrast(im).enhance(0.25)
    if condicion=="borrosa":
        im=im.filter(ImageFilter.GaussianBlur(1.8))
    if condicion=="rotada":
        im=im.rotate(5,expand=False,fillcolor="white")
    return im

def cer(ref, pred):
    prev=list(range(len(pred)+1))
    for i,a in enumerate(ref,1):
        cur=[i]+[0]*len(pred)
        for j,b in enumerate(pred,1):
            cur[j]=min(prev[j]+1,cur[j-1]+1,prev[j-1]+(a!=b))
        prev=cur
    return prev[-1]/max(1,len(ref))

def evaluar():
    registros=[]
    for placa,condicion in SAMPLES:
        im=imagen(placa,condicion)
        inicio=time.perf_counter()
        raw=pytesseract.image_to_string(im,config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        ms=round((time.perf_counter()-inicio)*1000,2)
        pred=normalizar(raw)
        registros.append({"referencia":placa,"prediccion":pred,"condicion":condicion,
                          "exact_match":pred==placa,"cer":round(cer(placa,pred),4),"latencia_ms":ms})
    return {"tipo":"benchmark_sintetico_no_representativo","motor":"Tesseract",
            "n":len(registros),"exact_match":sum(r["exact_match"] for r in registros)/len(registros),
            "cer_medio":sum(r["cer"] for r in registros)/len(registros),
            "latencia_media_ms":round(sum(r["latencia_ms"] for r in registros)/len(registros),2),
            "casos":registros,
            "limitacion":"Imágenes artificiales; no validan reconocimiento de matrículas reales ni modelo LinearSVC."}

if __name__=="__main__":
    out=Path("results/ocr_sintetico.json")
    out.parent.mkdir(exist_ok=True)
    report=evaluar()
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
