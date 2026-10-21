#!/usr/bin/env python3
"""Genera `public/css/style.css` con el generador de CSS de libra-web-kit.

LibraBot no es una de las ocho apps de `IDENTIDAD` del kit (es un complemento, como
LibraEdge: ADR-088 de libra-ui), y el kit exige que `IDENTIDAD`, `SITES` y `SIDEBARS`
sean el mismo conjunto. Por eso sus tokens viven acá y se le pasan al generador del kit
en el momento: la landing recibe el mismo template y el mismo `pulido.css` (ADR-010 del
kit) que las ocho, sin agregar una novena app al kit.

Uso, con el kit clonado al lado (`~/proyectos/libra-web-kit`):

    python3 scripts/generar_css.py           # escribe public/css/style.css
    python3 scripts/generar_css.py --check   # exit 1 si el archivo quedó distinto
"""
import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
KIT = RAIZ.parent / "libra-web-kit"
sys.path.insert(0, str(KIT))

from libra_web_kit import css_gen  # noqa: E402
from libra_web_kit.site_css_tokens import PULIDO_VARS, SITES  # noqa: E402

# Rojo frambuesa (#e11d48), el color de la marca. Lo que no es de marca, igual que VentaLibra.
TOKENS = {
    **SITES["ventalibra"],
    "tokens": """  --brand:       #e11d48;
  --brand-dark:  #be123c;
  --brand-light: #fff1f2;
  --accent:      #10b981;
  --dark:        #0f172a;
  --dark-2:      #1e293b;
  --muted:       #64748b;
  --border:      #e2e8f0;
  --bg:          #f8fafc;
""",
    # Sin foto: un degradé oscuro del color de la marca.
    "hero_bg": """    linear-gradient(135deg, #1a0710 0%, #3b0a1c 55%, #1a0710 100%),
    #1a0710;
""",
    "hero_before": """.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 60% 40%, rgba(225,29,72,.28) 0%, transparent 65%);
}
""",
    "hero_badge": """  display: inline-block; background: rgba(225,29,72,.25);
  border: 1px solid rgba(225,29,72,.5);
  color: #fda4af; font-size: .82rem; font-weight: 600;
""",
    "hero_span_p": """.hero h1 span { color: #fb7185; }
.hero p { font-size: 1.15rem; color: #e4d8dc; margin: 0 auto 2.5rem;
""",
    "plan_featured_shadow": "  box-shadow: 0 8px 32px rgba(225,29,72,.15);\n",
    "cta_p": ".cta-section p  { color: #fecdd3; margin: 0 auto 2rem; max-width: 500px; }\n",
}

PULIDO = {
    "hero-accent": "#fda4af",
    "on-dark-accent": "#fb7185",
    "brand-rgb": "225,29,72",
    "deep-rgb": "26,7,16",
    "hover-rgb": "136,19,55",
    "card-border": "#e7e5e4",
    "step-end": "#fecdd3",
    "dark-1": "#1a0710",
    "dark-2": "#2a0c18",
    "footer-bg": "#14050c",
    "footer-line": "#2a1820",
    "on-dark-text": "#e4d8dc",
    "on-dark-muted": "#b4a3a9",
    "on-dark-faint": "#94868b",
    "on-dark-accent-rgb": "251,113,133",
}


def render() -> str:
    # Se registran sólo en memoria, para esta corrida: el kit no cambia.
    SITES["librabot"] = TOKENS
    PULIDO_VARS["librabot"] = PULIDO
    try:
        return css_gen.render("librabot")
    finally:
        del SITES["librabot"], PULIDO_VARS["librabot"]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    destino = RAIZ / "public" / "css" / "style.css"
    css = render()
    if args.check:
        if not destino.exists() or destino.read_text(encoding="utf-8") != css:
            print("public/css/style.css no coincide con lo que genera el kit", file=sys.stderr)
            return 1
        return 0
    destino.write_text(css, encoding="utf-8")
    print(f"escrito {destino.relative_to(RAIZ)} ({len(css):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
