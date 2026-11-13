"""Genera las páginas estáticas de Pensok (Caamaño y Temporada Pilar).
Uso: python3 build.py  → escribe caamano/index.html, temporada/index.html, index.html
"""
import os, urllib.parse

CSS = """
:root{--navy:#0B3474;--navy2:#082A5E;--cyan:#1FB5E8;--green:#5DBB46;--ink:#14213D;--muted:#55627A;--bg:#F4F8FB;--wa:#25D366}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Montserrat',sans-serif;color:var(--ink);background:#fff;line-height:1.55}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
header{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid #E3EAF2}
.nav{display:flex;align-items:center;justify-content:space-between;height:68px;gap:12px}
.nav img{height:42px;width:auto}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font-weight:800;border-radius:10px;padding:14px 24px;font-size:16px;border:none;cursor:pointer;font-family:inherit;min-height:48px}
.btn-wa{background:var(--wa);color:#fff}.btn-wa:hover{background:#1EBE5A}
.btn-ghost{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.7)}
.nav .btn{padding:10px 16px;font-size:14px;min-height:44px}
.hero{position:relative;color:#fff;background:var(--navy2) center/cover no-repeat}
.hero::before{content:'';position:absolute;inset:0;background:linear-gradient(100deg,rgba(8,42,94,.93) 0%,rgba(8,42,94,.8) 55%,rgba(8,42,94,.45) 100%)}
.hero .wrap{position:relative;padding:64px 20px 72px}
.tag{display:inline-block;background:rgba(93,187,70,.18);border:1px solid rgba(93,187,70,.6);color:#BFF0B0;font-size:13px;font-weight:700;padding:6px 14px;border-radius:100px;margin-bottom:18px}
.hero h1{font-size:clamp(30px,5vw,52px);line-height:1.07;font-weight:900;letter-spacing:-1px;max-width:720px;margin-bottom:16px}
.hero h1 span{color:var(--cyan)}
.hero p{font-size:clamp(16px,2vw,19px);color:#D7E4F2;max-width:580px;margin-bottom:28px}
.hero-btns{display:flex;gap:12px;flex-wrap:wrap}
.facts{display:flex;gap:26px;flex-wrap:wrap;margin-top:36px}
.facts div{border-left:3px solid var(--cyan);padding-left:12px;font-size:14px;color:#D7E4F2}
.facts strong{display:block;color:#fff;font-size:17px}
section{padding:64px 0;scroll-margin-top:68px}
.bg{background:var(--bg)}
.eyebrow{color:var(--cyan);font-weight:800;font-size:13px;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px}
h2{font-size:clamp(25px,3.4vw,36px);line-height:1.15;font-weight:900;color:var(--navy);margin-bottom:12px;letter-spacing:-.5px}
.lead{color:var(--muted);max-width:640px;margin-bottom:36px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.item{background:#fff;border:1px solid #E3EAF2;border-radius:14px;padding:22px;display:flex;flex-direction:column;gap:8px}
.item .ic{font-size:28px}
.item h3{font-size:18px;font-weight:800;color:var(--navy)}
.item p{font-size:14px;color:var(--muted);flex-grow:1}
.item a{font-size:14px;font-weight:800;color:#128C4A}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.gallery img{width:100%;height:260px;object-fit:cover;border-radius:12px}
.why{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}
.why div{background:#fff;border-radius:14px;padding:20px;border-top:4px solid var(--cyan)}
.why h3{font-size:16px;font-weight:800;color:var(--navy);margin-bottom:4px}
.why p{font-size:14px;color:var(--muted)}
.visit{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;align-items:start}
.visit .box{background:#fff;border:1px solid #E3EAF2;border-radius:14px;padding:24px}
.visit dl{display:grid;grid-template-columns:auto 1fr;gap:8px 16px;font-size:15px}
.visit dt{font-weight:800;color:var(--navy)}
.visit dd{color:var(--muted)}
.visit iframe{width:100%;height:300px;border:0;border-radius:14px}
.cta{background:var(--navy);color:#fff;text-align:center}
.cta h2{color:#fff}.cta p{color:#D7E4F2;margin-bottom:24px}
footer{background:#071F45;color:#9FB2CC;font-size:13px;padding:28px 0}
footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
.float{position:fixed;right:18px;bottom:18px;z-index:60;width:60px;height:60px;border-radius:50%;background:var(--wa);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.float svg{width:32px;height:32px;fill:#fff}
@media(max-width:600px){.nav .btn span{display:none}.hero .wrap{padding:44px 20px 52px}.gallery img{height:220px}}
"""

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C9 3 3.3 8.6 3.3 15.6c0 2.2.6 4.4 1.7 6.3L3.2 29l7.3-1.9c1.8 1 3.9 1.5 5.9 1.5 7 0 12.7-5.7 12.7-12.6C29.1 8.6 23.1 3 16 3zm0 23.1c-1.9 0-3.8-.5-5.4-1.5l-.4-.2-4.3 1.1 1.2-4.2-.3-.4c-1.1-1.7-1.6-3.6-1.6-5.6C5.2 9.7 10 5 16 5c5.9 0 10.9 4.8 10.9 10.7 0 5.8-4.9 10.4-10.9 10.4zm6-7.8c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.9 8.9 0 0 1-4.4-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4s-1.2 1.1-1.2 2.7 1.2 3.2 1.4 3.4c.2.2 2.4 3.6 5.8 5 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'


def wa(num, text):
    return f"https://wa.me/{num}?text=" + urllib.parse.quote(text)


def page(cfg):
    num = cfg["wa"]
    def link(text):
        return f'href="{wa(num, text)}" target="_blank" rel="noopener" onclick="convertir()"'
    main_link = link(cfg["wa_text"])
    items = "".join(
        f'<div class="item"><div class="ic">{ic}</div><h3>{t}</h3><p>{d}</p>'
        f'<a {link(cfg["wa_item"].format(t.lower()))}>Consultar por WhatsApp →</a></div>'
        for ic, t, d in cfg["products"])
    why = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in cfg["why"])
    gallery = "".join(f'<img src="/img/{f}" alt="{cfg["alt"]}" loading="lazy">' for f in cfg["gallery"])
    facts = "".join(f"<div><strong>{a}</strong>{b}</div>" for a, b in cfg["facts"])
    dl = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in cfg["visit"])
    tag = cfg.get("gtag", "")
    gscript = ""
    if tag:
        gscript = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={tag}"></script>'
                   "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
                   f"gtag('js',new Date());gtag('config','{tag}');"
                   f"window.CONV='{cfg.get('conv','')}';</script>")
    conv_fn = ("<script>function convertir(){try{if(window.CONV&&window.gtag)gtag('event','conversion',{send_to:window.CONV});"
               "if(window.gtag)gtag('event','click_whatsapp',{local:'" + cfg["slug"] + "'})}catch(e){}}</script>")
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cfg['title']}</title>
<meta name="description" content="{cfg['desc']}">
<link rel="icon" href="/img/logo-pensok.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800;900&display=swap" rel="stylesheet">
{gscript}{conv_fn}
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap nav">
<img src="/img/logo-pensok.png" alt="Pensok">
<a class="btn btn-wa" {main_link}>{WA_SVG.replace('<svg','<svg style="width:20px;height:20px;fill:#fff"')}<span>{cfg['wa_display']}</span></a>
</div></header>

<section class="hero" style="background-image:url('/img/{cfg['hero']}')"><div class="wrap">
<div class="tag">{cfg['tag']}</div>
<h1>{cfg['h1']}</h1>
<p>{cfg['sub']}</p>
<div class="hero-btns">
<a class="btn btn-wa" {main_link}>{WA_SVG.replace('<svg','<svg style="width:22px;height:22px;fill:#fff"')} Escribinos por WhatsApp</a>
<a class="btn btn-ghost" href="#visitanos">Cómo llegar</a>
</div>
<div class="facts">{facts}</div>
</div></section>

<section><div class="wrap">
<div class="eyebrow">Productos</div>
<h2>{cfg['prod_h2']}</h2>
<p class="lead">{cfg['prod_lead']}</p>
<div class="grid">{items}</div>
</div></section>

<section class="bg"><div class="wrap">
<div class="eyebrow">Por qué Pensok</div>
<h2>Te decimos qué usar y cuánto</h2>
<p class="lead">No vendemos productos sueltos: te ayudamos a que el agua quede cristalina con lo justo.</p>
<div class="why">{why}</div>
</div></section>

<section><div class="wrap">
<div class="eyebrow">El local</div>
<h2>{cfg['gal_h2']}</h2>
<p class="lead">{cfg['gal_lead']}</p>
<div class="gallery">{gallery}</div>
</div></section>

<section id="visitanos" class="bg"><div class="wrap">
<div class="eyebrow">Visitanos</div>
<h2>{cfg['visit_h2']}</h2>
<p class="lead">{cfg['visit_lead']}</p>
<div class="visit">
<div class="box"><dl>{dl}</dl>
<p style="margin-top:20px"><a class="btn btn-wa" {main_link}>Escribinos por WhatsApp</a></p>
<p style="margin-top:12px"><a href="{cfg['maps']}" target="_blank" rel="noopener" style="font-weight:800;color:var(--navy)">Abrir en Google Maps →</a></p></div>
<iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={urllib.parse.quote(cfg['map_q'])}&output=embed" title="Mapa"></iframe>
</div>
</div></section>

<section class="cta"><div class="wrap">
<h2>{cfg['cta_h2']}</h2>
<p>{cfg['cta_p']}</p>
<a class="btn btn-wa" {main_link}>{WA_SVG.replace('<svg','<svg style="width:22px;height:22px;fill:#fff"')} {cfg['wa_display']}</a>
</div></section>

<footer><div class="wrap"><span>Pensok · {cfg['footer']}</span><span>Instagram @pensok.piletas</span></div></footer>
<a class="float" aria-label="WhatsApp" {main_link}>{WA_SVG}</a>
</body>
</html>
"""


COMMON_WHY = [
    ("Asesoramiento real", "Contanos el tamaño de tu pileta y cómo está el agua: te armamos la lista exacta."),
    ("Envíos a domicilio", "Te llevamos el pedido a tu casa en la zona."),
    ("Todo en un lugar", "Químicos, equipos, repuestos y accesorios, de marcas reconocidas."),
    ("Mayorista y minorista", "Para tu pileta, para consorcios, countries y profesionales."),
]

caamano = dict(
    slug="caamano",
    title="Pensok Villa Rosa | Cloro, pastillas y productos para piletas en Caamaño",
    desc="Tienda de productos para piletas en Villa Rosa (Caamaño 914): cloro, pastillas, bombas, filtros y accesorios. Envíos a domicilio y asesoramiento por WhatsApp.",
    wa="5491123932702", wa_display="11 2393-2702",
    wa_text="Hola Pensok Caamaño, quiero consultar por productos para mi pileta",
    wa_item="Hola Pensok Caamaño, quiero consultar por {}",
    hero="caamano_hero.jpg",
    tag="Villa Rosa · Pilar · Del Viso · Manzanares",
    h1="Todo para tu pileta en <span>Villa Rosa</span>",
    sub="Cloro, pastillas, bombas, filtros y accesorios para dejar tu pileta lista. Te asesoramos y te lo llevamos a tu casa.",
    facts=[("Caamaño 914", "Local 4, Villa Rosa"), ("Envíos", "a domicilio"), ("Lun a Vie", "9 a 18:30 · Sáb 9 a 13:30")],
    prod_h2="Lo que necesitás para la temporada",
    prod_lead="Consultá stock y precio por WhatsApp.",
    products=[
        ("🧪", "Cloro líquido y granulado", "Cloro para el mantenimiento diario y el shock de inicio de temporada."),
        ("⚪", "Pastillas de cloro", "Pastillas triple acción y de disolución lenta, en distintos tamaños."),
        ("💧", "Alguicidas y clarificadores", "Para recuperar el agua verde o turbia y mantenerla cristalina."),
        ("⚙️", "Bombas y filtros", "Bombas, filtros, arena y repuestos. Te ayudamos a elegir el equipo justo."),
        ("🧹", "Accesorios y limpieza", "Barrefondos, saca hojas, cepillos, mangueras, boyas y kits de análisis."),
        ("🏠", "Limpieza y hogar", "Productos de limpieza para el hogar, consorcios y comercios."),
    ],
    why=COMMON_WHY,
    gal_h2="Pasá por el local de Caamaño",
    gal_lead="Atención personalizada y todo el stock a la vista.",
    gallery=["caamano_1.jpg", "caamano_2.jpg", "caamano_4.jpg", "caamano_5.jpg"],
    alt="Local de Pensok en Villa Rosa",
    visit_h2="Caamaño 914, Villa Rosa",
    visit_lead="Vení al local o pedí por WhatsApp y te lo llevamos.",
    visit=[("Dirección", "Caamaño 914, Local 4, Villa Rosa, Pilar"),
           ("Horario", "Lunes a viernes 9 a 18:30 · Sábados 9 a 13:30"),
           ("WhatsApp", "11 2393-2702"), ("Envíos", "A domicilio en la zona")],
    maps="https://maps.google.com/maps?cid=9466607380143316014",
    map_q="Pensok, Caamaño 914, Villa Rosa, Buenos Aires",
    cta_h2="¿Tu pileta necesita algo?",
    cta_p="Mandanos un WhatsApp con lo que necesitás y te pasamos precio y envío.",
    footer="Caamaño 914, Local 4, Villa Rosa",
)

temporada = dict(
    slug="temporada",
    title="Pensok Pilar | Productos para piletas: cloro, cloradores salinos, robots Dolphin y bombas",
    desc="Todo para tu pileta en Pilar: cloro, pastillas, cloradores salinos, robots Dolphin, bombas y filtros. Envíos a domicilio y asesoramiento por WhatsApp.",
    wa="5491170645115", wa_display="11 7064-5115",
    wa_text="Hola Pensok, quiero consultar por productos para mi pileta",
    wa_item="Hola Pensok, quiero consultar por {}",
    gtag="AW-16866458233",
    conv="AW-16866458233/y4yVCO_q_bcdEPn0xuo-",
    hero="pilar_int1.jpg",
    tag="Temporada 2026-27 · Pilar y zona norte",
    h1="Todo para tu pileta <span>en Pilar</span>",
    sub="Cloro, cloradores salinos, robots Dolphin, bombas y filtros. Te asesoramos y te lo llevamos a tu casa.",
    facts=[("Mateo Gelves 1126", "Pilar"), ("Lun a Vie", "9 a 18 · Sáb 9 a 13"), ("Envíos", "a domicilio"), ],
    prod_h2="Prepará tu pileta para el verano",
    prod_lead="Consultá stock y precio por WhatsApp.",
    products=[
        ("🧪", "Cloro y pastillas", "Cloro líquido y granulado, pastillas triple acción y de disolución lenta."),
        ("🧂", "Cloradores salinos", "Olvidate de comprar cloro: el equipo lo produce a partir de sal. Te asesoramos con el modelo."),
        ("🤖", "Robots Dolphin", "Limpiafondos automáticos: fondo, paredes y línea de agua sin esfuerzo."),
        ("⚙️", "Bombas y filtros", "Bombas, filtros, arena y repuestos de primeras marcas."),
        ("💧", "Alguicidas y clarificadores", "Para recuperar el agua verde o turbia y mantenerla cristalina."),
        ("🧹", "Accesorios", "Barrefondos, saca hojas, cepillos, mangueras, boyas y kits de análisis."),
    ],
    why=COMMON_WHY,
    gal_h2="Pasá por el local de Pilar",
    gal_lead="Equipos y químicos a la vista, con quien te explica cómo usarlos.",
    gallery=["pilar_frente.jpg", "pilar_int2.jpg", "pilar_int3.jpg"],
    alt="Local de Pensok en Pilar",
    visit_h2="Mateo Gelves 1126, Pilar",
    visit_lead="Vení al local o pedí por WhatsApp y te lo llevamos.",
    visit=[("Dirección", "Granadero Juan Mateo Gelves 1126, Pilar"),
           ("Horario", "Lunes a viernes 9 a 18 · Sábados 9 a 13"), ("WhatsApp", "11 7064-5115"), ("Envíos", "A domicilio en Pilar y zona")],
    maps="https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote("Pensok Granadero Juan Mateo Gelves 1126 Pilar"),
    map_q="Granadero Juan Mateo Gelves 1126, Pilar, Buenos Aires",
    cta_h2="¿Arrancás la temporada?",
    cta_p="Mandanos un WhatsApp con lo que necesitás y te pasamos precio y envío.",
    footer="Granadero Juan Mateo Gelves 1126, Pilar",
)

INDEX = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pensok | Productos para piletas en Pilar y Villa Rosa</title>
<meta name="description" content="Pensok: productos para piletas en Pilar y Villa Rosa. Cloro, pastillas, bombas, filtros, cloradores salinos y robots Dolphin.">
<link rel="icon" href="/img/logo-pensok.png">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800;900&display=swap" rel="stylesheet">
<style>body{font-family:Montserrat,sans-serif;margin:0;background:#F4F8FB;color:#14213D}main{max-width:760px;margin:0 auto;padding:48px 20px;text-align:center}
img{height:56px}h1{color:#0B3474;font-size:30px}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:28px}
a{display:block;background:#fff;border:1px solid #E3EAF2;border-radius:14px;padding:24px;text-decoration:none;color:#0B3474;font-weight:800}a span{display:block;font-weight:600;color:#55627A;font-size:14px;margin-top:6px}</style></head>
<body><main><img src="/img/logo-pensok.png" alt="Pensok"><h1>Todo para tu pileta</h1><p>Elegí tu local más cercano</p>
<div class="g"><a href="/temporada">Pensok Pilar<span>Granadero Juan Mateo Gelves 1126</span></a><a href="/caamano">Pensok Villa Rosa<span>Caamaño 914, Local 4</span></a></div></main></body></html>"""

for name, cfg in [("caamano", caamano), ("temporada", temporada)]:
    os.makedirs(name, exist_ok=True)
    open(f"{name}/index.html", "w").write(page(cfg))
open("index.html", "w").write(INDEX)
print("ok")
