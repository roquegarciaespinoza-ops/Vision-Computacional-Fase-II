from scripts.evaluar_ocr_sintetico import cer, imagen, evaluar

def test_cer_identico():
    assert cer("1234ABC","1234ABC")==0

def test_cer_una_sustitucion():
    assert round(cer("1234ABC","1234ABD"),4)==round(1/7,4)

def test_imagen_sintetica():
    assert imagen("1234ABC","limpia").size==(440,110)

def test_benchmark_devuelve_seis_casos():
    reporte=evaluar()
    assert reporte["n"]==6
    assert len(reporte["casos"])==6
    assert 0<=reporte["exact_match"]<=1
    assert reporte["cer_medio"]>=0
