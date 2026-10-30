# LibraBot — Sitio web / Landing

Landing de [LibraBot](https://librabot.com.ar), el chatbot con IA de la suite. HTML estático
servido por nginx en Docker, como `librasuite_web` (con una guía pública en `/docs/`, sin login).

- **El propio LibraBot atiende la landing**: el widget de `chat.librabot.com.ar` (bandeja
  «Web librabot.com.ar») y el bot responde leyendo esta página.
- **Marca**: `public/img/marca.svg` y `favicon.svg`, copiados del tag `v0.175.0` de libra-ui
  (ADR-088). No se redibujan acá.
- **CSS**: `public/css/style.css` sale del generador de libra-web-kit con los tokens de LibraBot
  (`scripts/generar_css.py`, con el kit clonado al lado). No se edita a mano.
- **Guía para clientes** (`/docs/`, pública): `public/docs/`, `sitemap.xml` y `robots.txt` salen de
  `scripts/generar_docs.py` (`python3 scripts/generar_docs.py public`); se edita el script y se regenera,
  no los HTML. Describe las pantallas de `panel.librabot.com.ar` y el canal de WhatsApp: si cambia el panel, se actualiza acá (y la lista de temas de `frontend/src/pages/Ayuda.tsx` de `librabot`).
- **Pie**: «parte de LibraSuite», sin listar los otros productos (decisión del 2026-10-10).
- **Deploy**: push a `main` → workflow reusable de libra-web-kit → `/root/librabot_web/` en el VPS,
  contenedor `librabot-web` en `127.0.0.1:8105`, red `stack_stack-net`.
