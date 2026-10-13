"""Busca fotos con licencia libre en Wikimedia Commons y guarda vistas previas + metadatos.
Uso temporal para elegir imágenes del sitio. Se elimina al terminar."""
import json, os, re, time, urllib.parse, urllib.request

UA = "AltamiranoNosigliaSite/1.0 (https://github.com/ramiroperichon/AltamiranoNosiglia)"
API = "https://commons.wikimedia.org/w/api.php"
import sys
OUT = sys.argv[2] if len(sys.argv) > 2 else "fotos-candidatas"
TEMAS = json.load(open(sys.argv[1] if len(sys.argv) > 1 else ".github/fotos/temas.json", encoding="utf-8"))
LIC_OK = re.compile(r"^(cc0|public domain|pd|cc[ -]by(-sa)?[ -]\d)", re.I)

def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
                return data if binary else json.loads(data)
        except Exception as e:
            print("  reintento", intento, url[:120], e)
            time.sleep(2 + intento * 3)
    return None

def limpiar(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()

os.makedirs(OUT, exist_ok=True)
resumen = {}
for tema, consultas in TEMAS.items():
    vistos, elegidos = set(), []
    for q in consultas:
        params = {
            "action": "query", "format": "json", "generator": "search",
            "gsrsearch": f"{q} filetype:bitmap filew:>2800", "gsrnamespace": 6, "gsrlimit": 30,
            "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 500,
        }
        data = get(API + "?" + urllib.parse.urlencode(params))
        paginas = sorted((data or {}).get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        for p in paginas:
            ii = (p.get("imageinfo") or [{}])[0]
            meta = ii.get("extmetadata", {})
            lic = meta.get("LicenseShortName", {}).get("value", "")
            if p["title"] in vistos or ii.get("mime") != "image/jpeg": continue
            if not LIC_OK.match(lic.strip()): continue
            if ii.get("width", 0) < ii.get("height", 1) * 1.2: continue  # solo apaisadas
            vistos.add(p["title"])
            elegidos.append({
                "titulo": p["title"], "ancho": ii.get("width"), "alto": ii.get("height"),
                "licencia": lic, "licencia_url": meta.get("LicenseUrl", {}).get("value", ""),
                "autor": limpiar(meta.get("Artist", {}).get("value", "")),
                "descripcion": limpiar(meta.get("ImageDescription", {}).get("value", ""))[:200],
                "pagina": ii.get("descriptionurl"), "original": ii.get("url"), "preview": ii.get("thumburl"),
            })
            if len(elegidos) >= 8: break
        if len(elegidos) >= 8: break
        time.sleep(1)
    for i, c in enumerate(elegidos):
        nombre = f"{tema}-{i}.jpg"
        datos = get(c["preview"], binary=True)
        if datos:
            open(os.path.join(OUT, nombre), "wb").write(datos)
            c["archivo"] = nombre
        time.sleep(0.5)
    resumen[tema] = elegidos
    print(tema, len(elegidos))

json.dump(resumen, open(os.path.join(OUT, "candidatas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

