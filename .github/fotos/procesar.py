"""Descarga los originales elegidos de Wikimedia Commons y genera versiones optimizadas en img/."""
import io, json, os, time, urllib.parse, urllib.request
from PIL import Image, ImageOps

UA = "AltamiranoNosigliaSite/1.0 (https://github.com/ramiroperichon/AltamiranoNosiglia)"
API = "https://commons.wikimedia.org/w/api.php"
SEL = json.load(open(".github/fotos/seleccion.json", encoding="utf-8"))
os.makedirs("img", exist_ok=True)
creditos = json.load(open("img/creditos.json", encoding="utf-8")) if os.path.exists("img/creditos.json") else {}

def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for intento in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = r.read()
                return d if binary else json.loads(d)
        except Exception as e:
            print("reintento", intento, e); time.sleep(3 + 4 * intento)
    raise RuntimeError(url)

for s in SEL:
    if os.path.exists(f"img/{s['id']}-{s['anchos'][0]}.jpg") and s["id"] in creditos:
        continue
    q = {"action": "query", "format": "json", "titles": s["titulo"], "prop": "imageinfo",
         "iiprop": "url|size|extmetadata", "iiurlwidth": 4000}
    pag = list(get(API + "?" + urllib.parse.urlencode(q))["query"]["pages"].values())[0]
    ii = pag["imageinfo"][0]
    # Para originales enormes se usa una miniatura de 4000 px como fuente.
    fuente = ii["url"] if ii["width"] <= 6000 else ii["thumburl"]
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(get(fuente, binary=True)))).convert("RGB")
    W, H = im.size
    r = s.get("ratio")
    if r:
        fx, fy = s.get("focoX", 0.5), s.get("focoY", 0.5)
        if W / H > r:
            nw = int(H * r); x = int(min(max(fx * W - nw / 2, 0), W - nw)); im = im.crop((x, 0, x + nw, H))
        else:
            nh = int(W / r); y = int(min(max(fy * H - nh / 2, 0), H - nh)); im = im.crop((0, y, W, y + nh))
    for w in s["anchos"]:
        out = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        out.save(f"img/{s['id']}-{w}.jpg", "JPEG", quality=s.get("calidad", 80), optimize=True, progressive=True)
    m = ii.get("extmetadata", {})
    import re
    limpiar = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h or "")).strip()
    creditos[s["id"]] = {
        "titulo": s["titulo"], "autor": limpiar(m.get("Artist", {}).get("value", "")),
        "licencia": m.get("LicenseShortName", {}).get("value", ""), "licenciaUrl": m.get("LicenseUrl", {}).get("value", ""),
        "fuente": ii.get("descriptionurl"), "original": f"{W}x{H}", "final": f"{im.width}x{im.height}",
    }
    print("ok", s["id"], W, H, "->", im.size)
    time.sleep(1)

json.dump(creditos, open("img/creditos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
