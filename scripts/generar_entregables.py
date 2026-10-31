"""Genera los dos entregables oficiales DOCX y PDF desde Markdown del repositorio."""
from pathlib import Path
import re
from docx import Document
from docx.shared import Pt, Inches
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"entregables"
OUT.mkdir(exist_ok=True)
FILES=[
 ("Manual_despliegue_nube",["docs/01_arquitectura_y_alcance.md","docs/02_manual_despliegue.md"]),
 ("Informe_pruebas_validacion",["docs/03_validacion_y_evidencias.md","docs/05_evaluacion_ocr_sintetica.md","docs/06_resultados_verificados.md"])
]

def lines(paths):
    for path in paths:
        yield ("h1",Path(path).stem.replace("_"," ").title())
        for line in (ROOT/path).read_text(encoding="utf8").splitlines():
            if not line.strip():
                continue
            if line.startswith("#"):
                n=len(line)-len(line.lstrip("#"))
                yield ("h1" if n<=1 else "h2",line[n:].strip())
            elif line.startswith("|"):
                yield ("text",line.replace("|"," · ").strip(" ·"))
            elif line.startswith("```"):
                continue
            elif line.startswith("- "):
                yield ("bullet",line[2:])
            else:
                yield ("text",line)

def clean(s):
    return re.sub(r"\[([^\]]+)\]\([^)]*\)",r"\1",s).replace("`","").replace("**","")

for name,paths in FILES:
    items=list(lines(paths))
    doc=Document()
    sec=doc.sections[0];sec.top_margin=Inches(.8);sec.bottom_margin=Inches(.8)
    normal=doc.styles["Normal"];normal.font.name="Calibri";normal.font.size=Pt(10)
    doc.add_heading(name.replace("_"," "),0)
    for kind,s in items:
        s=clean(s)
        if kind=="h1":doc.add_heading(s,level=1)
        elif kind=="h2":doc.add_heading(s,level=2)
        elif kind=="bullet":doc.add_paragraph(s,style="List Bullet")
        else:doc.add_paragraph(s)
    doc.save(OUT/(name+".docx"))
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BodyCustom",parent=styles["BodyText"],fontName="Helvetica",fontSize=9.5,leading=13,spaceAfter=7,wordWrap="CJK"))
    styles.add(ParagraphStyle(name="TitleCustom",parent=styles["Heading1"],textColor=colors.HexColor("#146b76"),spaceBefore=14,spaceAfter=8))
    story=[Paragraph(escape(name.replace("_"," ")),styles["Title"])]
    for kind,s in items:
        s=clean(s)
        style=styles["TitleCustom"] if kind=="h1" else styles["Heading2"] if kind=="h2" else styles["BodyCustom"]
        if kind=="bullet":s="• "+s
        story.append(Paragraph(escape(s),style))
    SimpleDocTemplate(str(OUT/(name+".pdf")),pagesize=(595.28,841.89),rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=45).build(story)
print("Entregables generados:",*[str(p) for p in OUT.iterdir()])
