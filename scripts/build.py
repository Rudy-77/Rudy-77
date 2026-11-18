#!/usr/bin/env python3
"""Genera las tarjetas SVG del README del perfil (modo oscuro y claro).

Uso:  python scripts/build.py
Edita los datos de la sección CONTENIDO y vuelve a ejecutarlo.
"""
from __future__ import annotations
import html
import textwrap
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
ASSETS.mkdir(exist_ok=True)

SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code',Consolas,'DejaVu Sans Mono',monospace"

THEMES = {
    "dark": dict(bg="#0d1117", bg2="#111827", border="#30363d", text="#e6edf3",
                 muted="#7d8590", a1="#818cf8", a2="#22d3ee", chip_bg="#161b22",
                 glow=".18", dot="#e6edf3", dotop=".06"),
    "light": dict(bg="#ffffff", bg2="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#656d76", a1="#4f46e5", a2="#0891b2", chip_bg="#f0f3f6",
                  glow=".10", dot="#1f2328", dotop=".07"),
}

# ----------------------------------------------------------------- CONTENIDO
NAME = "Paulo César Pérez Martínez"
KICKER = "FULL STACK DEVELOPER"
SUBTITLE = "Ingeniería en Sistemas Computacionales · México"
TAGLINE = "Interfaces con Next.js, servicios con Spring Boot y Supabase."
BANNER_CHIPS = ["Next.js", "TypeScript", "Spring Boot", "PostgreSQL"]

OVERVIEW = [
    ("FRONT-END", ["Next.js · React", "TypeScript · JavaScript", "Tailwind CSS"]),
    ("BACK-END", ["Java · Spring Boot", "Spring Security · JPA", "REST · JWT"]),
    ("DATOS Y CALIDAD", ["PostgreSQL · Supabase", "RLS y migraciones", "Vitest · Git · Linux"]),
]

PROJECTS = [
    dict(slug="caam", icon="C", title="Adopciones CAAM", note="Equipo · front-end y back-end",
         desc="Plataforma web para gestionar adopciones de mascotas del Centro de Atención Animal de Morelia.",
         mine=["Dashboards de admin y usuario, catálogo y formularios",
               "Flujo de adopción con estados de mascota y citas",
               "Seguimiento post-adopción y cifrado AES-256-GCM"],
         metrics=[("Mis commits", "21"), ("Rol", "Full stack"), ("Cifrado", "AES-256")],
         tags=["Next.js", "TypeScript", "Supabase"]),
    dict(slug="projexus", icon="P", title="ProjeXus", note="Equipo · front-end y back-end",
         desc="Gestión de convocatorias de proyectos: equipos, evaluación por rúbricas y reconocimientos en PDF con QR.",
         mine=["API en Spring Boot: convocatorias, equipos y rúbricas",
               "Registro de jueces y restablecimiento de contraseña",
               "Vistas de proyectos y dashboards en Next.js"],
         metrics=[("Mis commits", "17"), ("Backend", "Java 17"), ("Salida", "PDF + QR")],
         tags=["Java", "Spring Boot", "PostgreSQL", "Next.js"]),
    dict(slug="kuni", icon="K", title="Kuni", note="Innovation Fest 2026 · integrante C (negocio)",
         desc="Monitoreo remoto de pacientes con diabetes e hipertensión: bot de WhatsApp y tablero clínico con reglas explicables.",
         mine=["Reglas de riesgo, adherencia y tendencias (domain-core)",
               "Funciones transaccionales para acciones clínicas",
               "Integración del modelo predictivo y pantallas clínicas"],
         metrics=[("Mis commits", "39"), ("Rol", "Negocio (C)"), ("Pruebas", "Vitest")],
         tags=["Next.js", "TypeScript", "Supabase"]),
    dict(slug="portafolio", icon="W", title="Portafolio", note="Proyecto individual",
         desc="Mi portafolio de trabajo, publicado en Vercel.",
         mine=["Código propio en JavaScript", "Publicado en Vercel"],
         metrics=[], tags=["JavaScript", "Vercel"]),
]
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    return html.escape(s, quote=True)

def chip_w(label: str, size: float = 10.5) -> float:
    return len(label) * size * 0.62 + 18

def chips(labels, x, y, t, size=10.5, h=22):
    out, cx = [], x
    for lb in labels:
        w = chip_w(lb, size)
        out.append(f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" '
                   f'fill="{t["chip_bg"]}" stroke="{t["border"]}"/>'
                   f'<text x="{cx + w/2:.1f}" y="{y + h/2 + 3.6}" text-anchor="middle" '
                   f'style="font:{size}px {MONO};fill:{t["a2"]}">{esc(lb)}</text>')
        cx += w + 8
    return "".join(out)

def defs(t, uid):
    return (f'<defs>'
            f'<linearGradient id="g{uid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{t["a1"]}"/><stop offset="1" stop-color="{t["a2"]}"/></linearGradient>'
            f'<radialGradient id="r{uid}"><stop offset="0" stop-color="{t["a1"]}" stop-opacity="{t["glow"]}"/>'
            f'<stop offset="1" stop-color="{t["a1"]}" stop-opacity="0"/></radialGradient>'
            f'</defs>')

STYLE = ("<style>@keyframes pulse{0%,100%{opacity:.55}50%{opacity:1}}"
         ".pulse{animation:pulse 4s ease-in-out infinite}"
         "@media (prefers-reduced-motion:reduce){.pulse{animation:none}}</style>")

def banner(t, name):
    W, H = 1200, 300
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="{t["dot"]}" opacity="{t["dotop"]}"/>'
                   for x in range(40, W, 40) for y in range(30, H, 40))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(NAME)} — {esc(KICKER)}">
<title>{esc(NAME)} — {esc(KICKER)}</title>{STYLE}{defs(t, "b")}
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="20" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>
{dots}
<circle cx="1010" cy="70" r="260" fill="url(#rb)" class="pulse"/>
<circle cx="150" cy="300" r="200" fill="url(#rb)" opacity=".6"/>
<text x="72" y="92" style="font:700 13px {MONO};letter-spacing:4px;fill:{t["a2"]}">&#9679; {esc(KICKER)}</text>
<text x="72" y="160" style="font:800 50px {SANS};fill:{t["text"]}">{esc(NAME)}</text>
<rect x="72" y="178" width="96" height="4" rx="2" fill="url(#gb)"/>
<text x="72" y="216" style="font:400 19px {SANS};fill:{t["text"]}">{esc(TAGLINE)}</text>
<text x="72" y="238" style="font:400 14px {MONO};fill:{t["muted"]}">{esc(SUBTITLE)}</text>
{chips(BANNER_CHIPS, 72, 256, t, size=12, h=26)}
<text x="1010" y="190" text-anchor="middle" style="font:800 150px {MONO};fill:url(#gb);opacity:.9">&lt;/&gt;</text>
</svg>'''

def overview(t, name):
    W, H = 1200, 190
    colw = (W - 80) / len(OVERVIEW)
    cols = []
    for i, (head, items) in enumerate(OVERVIEW):
        x = 40 + i * colw
        cols.append(f'<text x="{x+24:.0f}" y="52" style="font:700 12px {MONO};letter-spacing:3px;fill:{t["a2"]}">{esc(head)}</text>')
        for j, it in enumerate(items):
            cols.append(f'<text x="{x+24:.0f}" y="{88 + j*28}" style="font:400 17px {SANS};fill:{t["text"]}">'
                        f'<tspan fill="{t["a1"]}">&#9656;</tspan><tspan dx="7">{esc(it)}</tspan></text>')
        if i:
            cols.append(f'<line x1="{x:.0f}" y1="34" x2="{x:.0f}" y2="{H-34}" stroke="{t["border"]}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Resumen de tecnologías">
<title>Resumen de tecnologías</title>{defs(t, "o")}
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="16" fill="{t["bg2"]}" stroke="{t["border"]}" stroke-width="1.5"/>
{"".join(cols)}
</svg>'''

def card(t, p, fixed_h=None):
    W = 480
    desc = textwrap.wrap(p["desc"], 64)[:3]
    y = 94
    parts = [f'<text x="24" y="{y + i*17}" style="font:400 12.5px {SANS};fill:{t["text"]}">{esc(l)}</text>'
             for i, l in enumerate(desc)]
    y = 94 + len(desc) * 17 + 18
    parts.append(f'<text x="24" y="{y}" style="font:700 9.5px {MONO};letter-spacing:2px;fill:{t["muted"]}">MI PARTE</text>')
    for i, m in enumerate(p["mine"]):
        parts.append(f'<text x="24" y="{y + 20 + i*19}" style="font:400 12px {SANS};fill:{t["text"]}">'
                     f'<tspan fill="{t["a1"]}">&#9656;</tspan><tspan dx="6">{esc(m)}</tspan></text>')
    y = y + 20 + len(p["mine"]) * 19 + 8
    if p["metrics"]:
        parts.append(f'<line x1="24" y1="{y}" x2="{W-24}" y2="{y}" stroke="{t["border"]}"/>')
        cw = (W - 48) / len(p["metrics"])
        for i, (lab, val) in enumerate(p["metrics"]):
            x = 24 + i * cw
            parts.append(f'<text x="{x:.0f}" y="{y+28}" style="font:700 16px {MONO};fill:{t["a1"]}">{esc(val)}</text>'
                         f'<text x="{x:.0f}" y="{y+44}" style="font:400 10px {MONO};fill:{t["muted"]}">{esc(lab)}</text>')
        y += 58
    else:
        y += 8
    if fixed_h:
        y = fixed_h - 44
    parts.append(chips(p["tags"], 24, y, t))
    H = y + 22 + 22
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(p["title"])}">
<title>{esc(p["title"])}</title>{defs(t, "c")}
<rect x=".75" y=".75" width="{W-1.5}" height="{H-1.5}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}" stroke-width="1.5"/>
<circle cx="{W-50}" cy="50" r="110" fill="url(#rc)"/>
<rect x="24" y="22" width="40" height="40" rx="10" fill="url(#gc)"/>
<text x="44" y="49" text-anchor="middle" style="font:800 20px {SANS};fill:#fff">{esc(p["icon"])}</text>
<text x="76" y="40" style="font:700 18px {SANS};fill:{t["text"]}">{esc(p["title"])}</text>
<text x="76" y="57" style="font:400 11px {MONO};fill:{t["muted"]}">{esc(p["note"])}</text>
{"".join(parts)}
</svg>'''

def main():
    for name, t in THEMES.items():
        (ASSETS / f"banner-{name}.svg").write_text(banner(t, name), encoding="utf-8")
        (ASSETS / f"overview-{name}.svg").write_text(overview(t, name), encoding="utf-8")
        # todas las tarjetas con la misma altura para que la cuadrícula quede pareja
        import re
        H = max(int(re.search(r'height="(\d+)"', card(t, p)).group(1)) for p in PROJECTS)
        for p in PROJECTS:
            (ASSETS / f"project-{p['slug']}-{name}.svg").write_text(card(t, p, H), encoding="utf-8")
    print("SVG generados en", ASSETS)

if __name__ == "__main__":
    main()
