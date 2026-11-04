# Genera una página por zona a partir del diseño de public/index.html
import re, json, os, sys, html
from urllib.parse import quote
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=R+'/public'
D='https://oscarposadamecanico.netlify.app'
home=open(P+'/index.html',encoding='utf-8').read()

css=re.search(r'<style>\n(.*?)</style>\n</head>',home,re.S).group(1)
css=css.replace('url(assets/','url(/assets/')
sprite=re.search(r'<svg width="0" height="0".*?</svg>',home,re.S).group(0)
fav=re.search(r'<link rel="icon"[^>]*>',home).group(0)
fonts='<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">'

# (nombre, slug, barrios/zonas, frase propia)
Z=[
('Málaga','malaga','Teatinos, Churriana, El Palo, Pedregalejo, Cruz de Humilladero y Ciudad Jardín','Si vives en Málaga capital y aparcas en la calle, en un garaje comunitario o en el parking del trabajo, voy yo hasta allí con las herramientas.'),
('Torremolinos','torremolinos','La Carihuela, Montemar, El Bajondillo y Playamar','En Torremolinos reparo tu coche donde lo tengas aparcado, sea en tu urbanización, en un garaje o en la calle.'),
('Benalmádena','benalmadena','Arroyo de la Miel, Benalmádena Costa y Benalmádena Pueblo','Desde Arroyo de la Miel hasta Benalmádena Costa, me acerco a tu casa o a tu trabajo para arreglar tu coche sin que pierdas el día.'),
('Fuengirola','fuengirola','Los Boliches, Carvajal, Las Lagunas y el centro','En Fuengirola me desplazo a tu domicilio y te doy el presupuesto por WhatsApp antes de empezar, sin sorpresas.'),
('Mijas','mijas','Las Lagunas, La Cala de Mijas y Mijas Pueblo','Si vives en Mijas, en Las Lagunas o en La Cala, no tienes que mover el coche: voy yo a tu puerta.'),
('Marbella','marbella','Nueva Andalucía, San Pedro de Alcántara, Puerto Banús y el centro','En Marbella y sus urbanizaciones reparo tu coche en tu garaje o donde lo tengas aparcado.'),
('Estepona','estepona','el centro, El Paraíso, Cancelada y Seghers','En Estepona te arreglo el coche en tu casa, en tu garaje o en el sitio que te venga mejor.'),
('Vélez-Málaga','velez-malaga','Torre del Mar, Caleta de Vélez y el centro','En Vélez-Málaga y Torre del Mar atiendo a domicilio, para que no tengas que llevar el coche a ningún taller.'),
('Rincón de la Victoria','rincon-de-la-victoria','La Cala del Moral, Torre de Benagalbón y el centro','En el Rincón de la Victoria y La Cala del Moral voy a tu domicilio y reparo tu coche allí mismo.'),
('Alhaurín de la Torre','alhaurin-de-la-torre','el centro, Los Manantiales y Las Lagunas','En Alhaurín de la Torre me desplazo a tu domicilio y repararo tu coche sin que pierdas la mañana en un taller.'),
]
Z[-1]=Z[-1][:3]+('En Alhaurín de la Torre me desplazo a tu domicilio y reparo tu coche sin que pierdas la mañana en un taller.',)

SERV=['Revisión general','Cambio de aceite y filtros','Distribución','Embrague y caja de cambios','Frenos','Suspensión y dirección','Diagnosis','Aire acondicionado','Sistema eléctrico','Escapes','Inyección','Pre-ITV']
def wa(t): return 'https://wa.me/34674623880?text='+quote(t,safe='')
def e(s): return html.escape(s,quote=True)
def url(slug): return f'{D}/mecanico-a-domicilio-{slug}/'

EXTRA='''
.zh{padding:44px 0 36px;color:#fff;text-shadow:0 2px 22px rgba(0,0,0,.6)}
.zh h1{max-width:20ch}
.zh .lead{max-width:56ch}
.zh .r{display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center;margin-top:20px}
.zh .tel{font:700 1.7rem var(--head);text-decoration:none;color:var(--or2)}
.zh .btn{text-shadow:none}
.zs{padding:34px 0}
.zs h2{font-size:clamp(1.7rem,3.6vw,2.3rem);margin-bottom:14px;text-shadow:0 2px 18px rgba(0,0,0,.6)}
.zs p{color:#dfe5ea;max-width:70ch;margin-bottom:12px;text-shadow:0 1px 12px rgba(0,0,0,.7)}
.zc{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin-top:18px}
.zc article{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px}
.zc b{display:block;font:700 1.4rem var(--head);color:var(--or);margin-bottom:4px}
.zc h3{font-size:1.3rem;margin-bottom:4px}.zc p{margin:0;color:var(--muted);text-shadow:none}
.zl{display:flex;flex-wrap:wrap;gap:10px;list-style:none;padding:0;margin-top:14px}
.zl a{display:inline-block;padding:9px 16px;border-radius:999px;border:1px solid var(--line);background:rgba(20,25,31,.8);color:#fff;text-decoration:none;font-weight:500}
.zl a:hover{border-color:var(--or);color:var(--or2)}
.crumb{font-size:.92rem;color:#cfd6dd;margin-bottom:14px;text-shadow:0 1px 10px rgba(0,0,0,.8)}.crumb a{color:inherit}
.zs .ch{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin-top:14px}
.zs .ch a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:10px 18px;border-radius:999px;border:1px solid var(--line);background:rgba(20,25,31,.85);color:#fff;text-decoration:none;font-weight:600;text-shadow:none;-webkit-tap-highlight-color:rgba(255,122,0,.3)}.zs .ch a::after{content:'→';color:var(--or)}.zs .ch a:hover,.zs .ch a:active{border-color:var(--or);color:var(--or2)}
'''

def page(z):
    n,slug,bar,frase=z
    u=url(slug)
    title=f'Mecánico a domicilio en {n} · Oscar Posada'
    desc=f'Mecánico a domicilio en {n}: frenos, aceite, distribución, embrague, diagnosis y pre-ITV. Presupuesto por WhatsApp: 674 623 880.'
    faq=[(f'¿Haces reparaciones a domicilio en {n}?',f'Sí. Voy a tu domicilio, a tu garaje o a tu trabajo en {n} ({bar}) y reparo tu coche allí mismo, sin que tengas que llevarlo al taller.'),
         ('¿Cómo pido presupuesto?',f'Escríbeme por WhatsApp al 674 623 880 y cuéntame qué le pasa al coche y dónde está en {n}. Te doy el precio antes de empezar, sin sorpresas.'),
         ('¿Qué servicios haces?','Revisión general, cambio de aceite y filtros, distribución, embrague, frenos, suspensión, diagnosis, aire acondicionado, sistema eléctrico, escapes, inyección y revisión pre-ITV. Si tu avería no está en la lista, escríbeme y te digo si puedo encargarme.')]
    ld_biz={"@context":"https://schema.org","@type":"AutoRepair","name":"Oscar Posada · Mecánico a domicilio","url":u,"image":D+"/assets/og-image.jpg","telephone":"+34674623880","priceRange":"€€","areaServed":{"@type":"City","name":n}}
    ld_faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    ld_bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Inicio","item":D+"/"},{"@type":"ListItem","position":2,"name":f"Mecánico a domicilio en {n}","item":u}]}
    others=''.join(f'<li><a href="/mecanico-a-domicilio-{s}/">{e(m)}</a></li>' for m,s,_,_ in Z if s!=slug)
    serv=''.join(f'<li><a href="{wa(f"Hola Oscar, necesito {s} en {n}. Quiero pedir presupuesto.")}" target="_blank" rel="noopener">{e(s)}</a></li>' for s in SERV)
    msg=wa(f'Hola Oscar, quiero pedir presupuesto en {n}.')
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#111418">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:url" content="{u}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{D}/assets/og-image.jpg">
<meta name="twitter:card" content="summary">
<meta name="color-scheme" content="dark">
{fav}
{fonts}
<script type="application/ld+json">{json.dumps(ld_biz,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_faq,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_bc,ensure_ascii=False)}</script>
<style>
{css}{EXTRA}</style>
</head>
<body>
<a class="skip" href="#top">Saltar al contenido</a>
<div class="bg" aria-hidden="true"><div class="stage"><span class="k ka"></span><span class="k kc"></span><span class="k kb"></span></div></div>
{sprite}
<header class="nav"><div class="w">
  <a class="logo" href="/"><span class="mk" role="img" aria-label="Logo de Oscar Posada, mecánico a domicilio"></span><span><b>Oscar Posada</b><small>Mecánico a domicilio</small></span></a>
  <a class="btn wa" href="{msg}" target="_blank" rel="noopener"><svg class="i" style="width:20px;height:20px"><use href="#ct"/></svg><span>WhatsApp </span>674 623 880</a>
</div></header>
<main id="top">
<section class="zh"><div class="w">
  <p class="crumb"><a href="/">Inicio</a> › Mecánico a domicilio en {e(n)}</p>
  <h1>Mecánico a domicilio en <em>{e(n)}</em></h1>
  <p class="lead">{e(frase)} Te doy el presupuesto por WhatsApp antes de empezar.</p>
  <div class="r"><a class="btn wa" href="{msg}" target="_blank" rel="noopener"><svg class="i" style="width:22px;height:22px"><use href="#ct"/></svg>Pedir presupuesto por WhatsApp</a><a class="tel" href="tel:+34674623880">674 623 880</a></div>
</div></section>

<section class="zs"><div class="w">
  <h2>Reparo tu coche en {e(n)} sin que lo muevas</h2>
  <p>Trabajo en {e(n)} y alrededores, incluidas zonas como {e(bar)}. Vas a tu vida y yo me encargo de la avería: sin colas, sin dejar el coche tirado todo el día y con el precio claro desde el principio.</p>
  <div class="zc">
    <article><b>1</b><h3>Escríbeme por WhatsApp</h3><p>Cuéntame qué le pasa a tu coche y dónde está en {e(n)}. Puedes mandar una foto o un audio.</p></article>
    <article><b>2</b><h3>Recibe tu presupuesto</h3><p>Sabrás el precio antes de empezar, sin sorpresas.</p></article>
    <article><b>3</b><h3>Voy a tu puerta</h3><p>Quedamos el día y la hora que te vaya bien y lo reparo allí mismo.</p></article>
  </div>
</div></section>

<section class="zs"><div class="w">
  <h2>Servicios a domicilio en {e(n)}</h2>
  <p>Se hace todo tipo de reparaciones, desde un cambio de aceite hasta una avería de motor. <b>Pulsa el servicio que necesitas</b> y te abro WhatsApp con el mensaje listo para pedir presupuesto.</p>
  <ul class="ch">{serv}</ul>
</div></section>

<section class="zs"><div class="w faq">
  <h2>Dudas frecuentes en {e(n)}</h2>
  {''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in faq)}
</div></section>

<section class="zs"><div class="w">
  <h2>También trabajo en otras zonas</h2>
  <ul class="zl"><li><a href="/">Málaga y toda su zona</a></li>{others}</ul>
</div></section>

<section class="cta"><div class="w">
  <span class="lg" role="img" aria-label="Logo Oscar Posada"></span>
  <h2 class="tx">¿Necesitas un mecánico en {e(n)}?</h2>
  <div class="r">
    <a class="tel" href="tel:+34674623880">674 623 880</a>
    <a class="btn" href="{msg}" target="_blank" rel="noopener"><svg class="i" style="width:22px;height:22px"><use href="#ct"/></svg>Escríbeme por WhatsApp</a>
  </div>
</div></section>
</main>
<footer><div class="w"><span>© 2026 Oscar Posada · Mecánico a domicilio</span><span>Rápido, económico y de confianza</span><a href="tel:+34674623880" style="color:inherit">674 623 880</a></div></footer>
<div class="bar"><a class="btn wa" href="{msg}" target="_blank" rel="noopener"><svg class="i" style="width:22px;height:22px"><use href="#ct"/></svg>Pedir presupuesto por WhatsApp</a></div>
</body>
</html>
'''

for z in Z:
    d=f'{P}/mecanico-a-domicilio-{z[1]}'
    os.makedirs(d,exist_ok=True)
    open(d+'/index.html','w',encoding='utf-8').write(page(z))
# sitemap
urls=[(D+'/','1.0')]+[(url(z[1]),'0.8') for z in Z]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{p}</priority></url>\n' for u,p in urls)+'</urlset>\n'
open(P+'/sitemap.xml','w',encoding='utf-8').write(sm)
print(len(Z),'páginas generadas')
json.dump([(z[0],z[1]) for z in Z],open(R+'/tools/zonas.json','w'),ensure_ascii=False)
