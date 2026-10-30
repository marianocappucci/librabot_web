#!/usr/bin/env python3
"""Genera public/docs/*.html, sitemap.xml y robots.txt de librabot.com.ar con menú y pie compartidos.
Uso: python3 scripts/generar_docs.py public"""
import sys
from pathlib import Path

PUBLIC = Path(sys.argv[1])
DOCS = PUBLIC / "docs"
DOCS.mkdir(parents=True, exist_ok=True)
SITIO = "https://librabot.com.ar"
PANEL = "https://panel.librabot.com.ar"
WA = "https://wa.me/5491127752983?text=Hola,%20tengo%20una%20consulta%20sobre%20LibraBot"

# (archivo, título del menú, descripción para buscadores)
MENU = [
    ("Inicio", [
        ("index", "Introducción", "Guía para usar LibraBot: cómo entrar al panel, configurar el bot, instalarlo en tu sitio y atender a tus visitantes."),
        ("primeros-pasos", "Primeros pasos", "Qué hacer después de recibir el correo de LibraBot: elegir tu contraseña, entrar al panel y dejar el bot andando en tu sitio."),
    ]),
    ("Configurar tu bot", [
        ("sitio-web", "Sitio web", "Cómo cargar la dirección de tu sitio en LibraBot, volver a leerlo y avisarle cada cambio desde WordPress."),
        ("instalar", "Instalarlo en tu sitio", "Cómo pegar el código de LibraBot en tu sitio web para que aparezca el chat, con o sin WordPress."),
        ("aspecto", "Aspecto del chat", "Cómo cambiar el color y el ícono del botón del chat, el globo y el nombre del asistente de LibraBot."),
        ("mensajes", "Bienvenida y botones de inicio", "Cómo escribir el saludo de tu bot y los botones de inicio que ven tus visitantes al abrir el chat."),
        ("preguntas-fijas", "Preguntas fijas", "Cómo cargar respuestas que LibraBot da siempre igual: horarios, medios de pago, envíos."),
        ("informacion", "Información extra", "Cómo cargar textos y PDF para que LibraBot responda con datos que no están en tu sitio."),
        ("avisos", "Avisos por palabra clave", "Cómo hacer que LibraBot conteste un texto fijo cuando el visitante nombra una palabra clave: urgencias, lo que no hacés, avisos importantes."),
        ("formularios", "Formularios y pedidos", "Cómo armar formularios para que LibraBot pida turnos, presupuestos o reclamos de a un dato por vez, y cómo recibir los pedidos."),
        ("sin-respuesta", "Sin respuesta", "Cómo ver lo que tus visitantes preguntaron y LibraBot no supo contestar, y convertirlo en una respuesta."),
    ]),
    ("Atención", [
        ("atencion", "Hablar con una persona", "Cómo configura LibraBot el pase a una persona: por tu WhatsApp o por el chat del sitio."),
        ("whatsapp", "El bot en tu WhatsApp", "Cómo hacer que LibraBot atienda también los mensajes que llegan al WhatsApp de tu empresa: activarlo, vincular el celular, atender y qué cuidados tener."),
        ("cartel-qr", "Cartel con el QR de WhatsApp", "Cómo armar e imprimir un cartel con un código QR para que tus clientes te escriban por WhatsApp."),
        ("conversaciones", "Conversaciones en Chatwoot", "Cómo entrar a Chatwoot desde el panel de LibraBot para ver y atender las conversaciones."),
    ]),
    ("Seguimiento", [
        ("actividad", "Actividad", "Cómo ver cuántas preguntas recibe tu bot, cuáles se repiten más y cuáles no supo contestar, en los últimos 7, 30 o 90 días."),
        ("historial", "Historial de cambios", "Cómo ver quién cambió qué en el panel de LibraBot y cuándo."),
    ]),
    ("Tu cuenta", [
        ("plan", "Tu plan", "Qué incluye cada plan de LibraBot, cómo ver tus preguntas del mes y cómo pedir un cambio de plan."),
        ("usuarios", "Usuarios y solo lectura", "Cómo sumar a alguien de tu equipo que solo pueda mirar el panel de LibraBot, y cómo quitarlo."),
        ("problemas", "Problemas frecuentes", "Soluciones a lo más habitual en LibraBot: no llega el correo, el enlace venció, el chat no aparece, el cambio no se ve."),
    ]),
]
ORDEN = [p for _, items in MENU for p in items]


def plantilla(archivo, titulo, descripcion, cuerpo, anterior, siguiente):
    url = f"{SITIO}/docs/" + ("" if archivo == "index" else f"{archivo}.html")
    lateral = []
    for seccion, items in MENU:
        lateral.append(f'    <div class="docs-sidebar-section">{seccion}</div>')
        for a, t, _ in items:
            href = "/docs/" if a == "index" else f"/docs/{a}.html"
            activo = ' class="active"' if a == archivo else ""
            lateral.append(f'    <a href="{href}"{activo}>{t}</a>')
    pie = []
    if anterior:
        pie.append(f'<a href="{"/docs/" if anterior[0] == "index" else f"/docs/{anterior[0]}.html"}">← {anterior[1]}</a>')
    else:
        pie.append("<span></span>")
    if siguiente:
        pie.append(f'<a href="/docs/{siguiente[0]}.html">{siguiente[1]} →</a>')
    else:
        pie.append("<span></span>")
    titulo_doc = "Guía de LibraBot" if archivo == "index" else f"{titulo} — Guía de LibraBot"
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titulo_doc}</title>
  <meta name="description" content="{descripcion}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{titulo_doc}">
  <meta property="og:description" content="{descripcion}">
  <meta property="og:url" content="{url}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
  <link rel="icon" type="image/svg+xml" href="/img/favicon.svg">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

<nav class="navbar">
  <a href="/" class="navbar-brand" style="text-decoration:none"><img src="/img/marca.svg" alt="" class="logo-icon" width="32" height="32">LibraBot</a>
  <div class="navbar-links">
    <a href="/#funciones">Qué hace</a>
    <a href="/#planes">Planes</a>
    <a href="/docs/" class="active" style="color:var(--brand)">Guía</a>
    <a href="{PANEL}" target="_blank" rel="noopener" class="btn-nav">Entrar al panel</a>
  </div>
</nav>

<div class="docs-wrapper">
  <nav class="docs-sidebar" aria-label="Guía">
{chr(10).join(lateral)}
  </nav>

  <main class="docs-content">
{cuerpo}
<div class="docs-nav-footer">
{pie[0]}
{pie[1]}
</div>
  </main>
</div>

<footer style="background:var(--dark);color:#94a3b8;text-align:center;padding:1.5rem;font-size:.85rem;">
  © 2026 LibraBot · parte de <a href="https://librasuite.com.ar" style="color:#94a3b8">LibraSuite</a> · <a href="/" style="color:#94a3b8">Inicio</a> · <a href="/legal/terminos.html" style="color:#94a3b8">Términos y condiciones</a>
</footer>
</body>
</html>
"""


P = {}

P["index"] = f"""    <h1>Guía de LibraBot</h1>
<p class="docs-lead">Todo lo que necesitás para dejar tu chatbot andando en tu sitio y mantenerlo al día, paso a paso y sin saber de programación.</p>
<h2>Qué es LibraBot</h2>
<p>LibraBot es un asistente virtual que atiende a los visitantes de tu sitio web. Responde con lo que dice tu propio sitio y con la información que vos le cargues, tanto en el chat de tu sitio como, si querés, en el WhatsApp de tu empresa, y cuando no sabe o alguien pide hablar con una persona, le pasa la conversación a tu equipo o a tu WhatsApp.</p>
<p>Lo manejás desde el <a href="{PANEL}" target="_blank" rel="noopener">panel de LibraBot</a>: ahí cambiás el saludo, cargás respuestas, ves qué no supo contestar y copiás el código que va en tu sitio.</p>
<h2>Por dónde empezar</h2>
<ol class="step-list">
<li><strong>Elegí tu contraseña</strong> con el enlace del correo de bienvenida y entrá al panel.</li>
<li><strong>Revisá la dirección de tu sitio</strong> en «Mi bot»: es de donde el bot aprende.</li>
<li><strong>Pegá el código</strong> en tu sitio para que aparezca el chat.</li>
<li><strong>Personalizalo</strong>: saludo, botones de inicio, color y nombre del asistente.</li>
<li><strong>Cargá lo que no está en tu web</strong>: preguntas fijas, textos y PDF.</li>
<li><strong>Cargá tu WhatsApp</strong> para que el bot sepa a dónde derivar.</li>
</ol>
<p>El detalle de cada paso está en <a href="/docs/primeros-pasos.html">Primeros pasos</a>.</p>
<h2>Las pantallas del panel</h2>
<p>El menú lateral del panel tiene estas entradas:</p>
<table class="docs-table">
<thead><tr><th>Pantalla</th><th>Qué permite hacer</th></tr></thead>
<tbody>
<tr><td><strong>Mi bot</strong></td><td>La pantalla de inicio: sitio, código para pegar, saludo, botones, aspecto del chat, atención de una persona, WhatsApp, cartel con QR, tu plan y las conversaciones. Ver <a href="/docs/sitio-web.html">Sitio web</a>, <a href="/docs/instalar.html">Instalarlo en tu sitio</a>, <a href="/docs/aspecto.html">Aspecto del chat</a>, <a href="/docs/mensajes.html">Bienvenida y botones</a>, <a href="/docs/atencion.html">Hablar con una persona</a>, <a href="/docs/whatsapp.html">WhatsApp</a>, <a href="/docs/cartel-qr.html">Cartel con QR</a> y <a href="/docs/plan.html">Tu plan</a></td></tr>
<tr><td><strong>Actividad</strong></td><td>Cuántas preguntas recibe tu bot y cuáles se repiten. Ver <a href="/docs/actividad.html">Actividad</a></td></tr>
<tr><td><strong>Preguntas fijas</strong></td><td>Respuestas que el bot da siempre igual, con submenús. Ver <a href="/docs/preguntas-fijas.html">Preguntas fijas</a></td></tr>
<tr><td><strong>Avisos</strong></td><td>Un texto fijo cuando el visitante nombra una palabra clave. Ver <a href="/docs/avisos.html">Avisos</a></td></tr>
<tr><td><strong>Formularios</strong> y <strong>Pedidos</strong></td><td>Pedir datos de a uno y recibir lo que dejan. Ver <a href="/docs/formularios.html">Formularios y pedidos</a></td></tr>
<tr><td><strong>Información</strong></td><td>Textos y PDF extra para el bot. Ver <a href="/docs/informacion.html">Información extra</a></td></tr>
<tr><td><strong>Sin respuesta</strong></td><td>Lo que preguntaron y el bot no supo contestar. Ver <a href="/docs/sin-respuesta.html">Sin respuesta</a></td></tr>
<tr><td><strong>Historial</strong></td><td>Quién cambió qué y cuándo. Ver <a href="/docs/historial.html">Historial de cambios</a></td></tr>
<tr><td><strong>Usuarios</strong></td><td>Sumar gente de solo lectura. Ver <a href="/docs/usuarios.html">Usuarios y solo lectura</a></td></tr>
<tr><td><strong>Ayuda</strong></td><td>Un acceso a esta guía desde el panel</td></tr>
</tbody>
</table>
<div class="callout">
<p><strong>¿No encontrás algo?</strong> Probá con <a href="/docs/problemas.html">Problemas frecuentes</a> o escribinos por <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a>.</p>
</div>"""

P["primeros-pasos"] = f"""    <h1>Primeros pasos</h1>
<p class="docs-lead">Del correo de bienvenida a un bot funcionando en tu sitio, en el orden en que conviene hacerlo.</p>
<h2>1. Elegí tu contraseña</h2>
<p>Cuando damos de alta tu bot, te llega un correo a la dirección que nos diste, con un enlace para elegir tu contraseña. Tu usuario es esa misma dirección de correo.</p>
<ol>
<li>Abrí el enlace del correo y escribí la contraseña que quieras usar.</li>
<li>Entrá a <a href="{PANEL}" target="_blank" rel="noopener">panel.librabot.com.ar</a> con tu correo y esa contraseña.</li>
<li>Tildá «No soy un robot» y tocá <strong>Ingresar</strong>.</li>
</ol>
<div class="callout warn">
<p><strong>El enlace del correo dura unas horas.</strong> Si venció o no te llegó, en la pantalla de ingreso tocá «¿Olvidaste tu contraseña?», escribí tu correo y te mandamos otro. Revisá también la carpeta de spam.</p>
</div>
<h2>2. Aceptá los Términos</h2>
<p>La primera vez, el panel te muestra los Términos y condiciones del servicio. Hasta que no los aceptes, el panel no te deja configurar nada. <strong>Tu bot en el sitio sigue funcionando</strong> mientras tanto.</p>
<h2>3. Revisá la dirección de tu sitio</h2>
<p>En «Mi bot», sección <strong>Sitio web</strong>, tiene que estar la dirección de tu sitio. El bot la lee para aprender qué ofrecés. La primera lectura puede tardar unos minutos: el contador «páginas del sitio leídas» te muestra cuánto avanzó. Más en <a href="/docs/sitio-web.html">Sitio web</a>.</p>
<h2>4. Pegá el código en tu sitio</h2>
<p>En «Mi bot», la sección <strong>Código para tu sitio</strong> trae el código que hace aparecer el chat. Copialo y pegalo en tu sitio (o pasáselo a quien lo mantiene). Más en <a href="/docs/instalar.html">Instalarlo en tu sitio</a>.</p>
<h2>5. Personalizalo</h2>
<ul>
<li>El <a href="/docs/mensajes.html">saludo y los botones de inicio</a>.</li>
<li>El <a href="/docs/aspecto.html">color, el ícono, el globo y el nombre del asistente</a>.</li>
<li>Tus <a href="/docs/preguntas-fijas.html">preguntas fijas</a> y la <a href="/docs/informacion.html">información extra</a>.</li>
</ul>
<h2>6. Cargá tu WhatsApp</h2>
<p>En «Atención de una persona», cargá el WhatsApp al que el bot va a derivar cuando alguien pida hablar con una persona o el bot no tenga el dato. Más en <a href="/docs/atencion.html">Hablar con una persona</a>.</p>
<h2>7. Probalo</h2>
<p>Abrí tu sitio, tocá el botón del chat y preguntale cosas como lo haría un cliente. Lo que no sepa contestar queda en <a href="/docs/sin-respuesta.html">Sin respuesta</a>, para que lo corrijas.</p>"""

P["sitio-web"] = f"""    <h1>Sitio web</h1>
<p class="docs-lead">De dónde aprende el bot, cada cuánto se actualiza y cómo avisarle al instante cuando cambiás algo.</p>
<h2>La dirección de tu sitio</h2>
<p>En «Mi bot», sección <strong>Sitio web</strong>, escribí la dirección completa (por ejemplo <code>https://www.tuempresa.com</code>) y tocá <strong>Guardar</strong>. El bot contesta con lo que lee de ese sitio.</p>
<h2>Cuándo se actualiza</h2>
<ul>
<li><strong>Solo, todas las noches.</strong> LibraBot vuelve a leer tu sitio cada noche.</li>
<li><strong>A pedido.</strong> Si cambiaste algo y no querés esperar, tocá <strong>Volver a leer el sitio</strong>. Si cambiaste la dirección, guardala primero: el botón se habilita después.</li>
</ul>
<p>Mientras lee, el panel lo indica y se actualiza solo. Si tu sitio tiene muchas páginas puede tardar varios minutos, y podés seguir usando el panel. Cuando termina, ves la fecha y el resumen de la última lectura; si falló, el panel te dice el motivo.</p>
<h2>Aviso desde WordPress</h2>
<p>Si tu sitio es WordPress, podés instalar un plugin y cada publicación nueva, cambiada o retirada le llega al bot en el momento, sin esperar a la noche. En «Mi bot», sección <strong>Aviso desde WordPress</strong>:</p>
<ol class="step-list">
<li><strong>Descargá el plugin.</strong> Ya viene configurado para tu bot.</li>
<li><strong>Subilo a WordPress:</strong> entrá a <em>Plugins → Añadir nuevo → Subir plugin</em>, elegí el archivo y activalo.</li>
</ol>
<p>Si preferís configurarlo a mano, tocá «Configurarlo a mano»: el panel te muestra la dirección del aviso y la clave, para cargarlas en WordPress, en <em>Ajustes → LibraBot</em>.</p>
<div class="callout warn">
<p><strong>No compartas la clave del aviso.</strong> Con ella se le puede pedir al bot que lea páginas de tu sitio. Si sospechás que se filtró, tocá «Cambiar la clave» y cargá la nueva en WordPress.</p>
</div>
<div class="callout">
<p>Esta sección aparece completa cuando ya cargaste la dirección de tu sitio.</p>
</div>"""

P["instalar"] = f"""    <h1>Instalarlo en tu sitio</h1>
<p class="docs-lead">Cómo hacer que el chat aparezca en tu sitio web.</p>
<h2>Copiá el código</h2>
<p>En «Mi bot», sección <strong>Código para tu sitio</strong>, tocá el botón de copiar. Es un bloque corto de código propio de tu bot.</p>
<h2>Pegalo en tu sitio</h2>
<p>Pegalo justo antes de la etiqueta <code>&lt;/body&gt;</code>, en todas las páginas donde quieras que aparezca el bot. Si tu sitio tiene una plantilla común (un pie o un <em>footer</em> que se repite en todas las páginas), alcanza con ponerlo ahí una sola vez.</p>
<h3>En WordPress</h3>
<p>Lo más simple es un plugin para insertar código en el pie del sitio (de los que se llaman «Insert Headers and Footers» o similares): pegás el código en el campo del pie y guardás. También se puede agregar en el archivo <code>footer.php</code> de tu tema, antes de <code>&lt;/body&gt;</code>.</p>
<h3>En otros sitios</h3>
<p>Si tu sitio lo mantiene otra persona o una agencia, pasale el código con esta indicación: «pegarlo antes del cierre de body en todas las páginas».</p>
<h2>Verificá que anda</h2>
<p>Abrí tu sitio en una ventana nueva. Tiene que aparecer el botón del chat abajo a la derecha. Si lo tocás, se abre el chat con tu saludo y tus botones de inicio.</p>
<div class="callout">
<p><strong>Si no ves el chat</strong>, revisá <a href="/docs/problemas.html">Problemas frecuentes</a>. Las causas más comunes son que el código quedó en una página que no es la que mirás, o que el sitio guarda una copia vieja de la página (caché).</p>
</div>
<div class="callout warn">
<p>Si el panel dice «Este bot todavía no tiene un código para pegar», escribinos: falta terminar de preparar tu cuenta de atención.</p>
</div>"""

P["aspecto"] = """    <h1>Aspecto del chat</h1>
<p class="docs-lead">El color y el ícono del botón, el globo que invita a conversar y el nombre con el que se presenta el asistente.</p>
<h2>Botón del chat</h2>
<p>En «Mi bot», sección <strong>Botón del chat</strong>, elegís el color y el ícono del botón que abre el chat en tu sitio:</p>
<ul>
<li><strong>Clásico:</strong> el ícono de siempre.</li>
<li><strong>Con ojitos que parpadean:</strong> una versión más simpática, con ojos animados.</li>
<li><strong>Imagen propia:</strong> subís tu logo o una imagen. Puede ser PNG, JPG o WebP, de hasta 200 KB. Se ve recortada en círculo, así que conviene una imagen cuadrada.</li>
</ul>
<div class="callout">
<p><strong>Los cambios tardan unos minutos en verse en tu sitio.</strong> Si no los ves enseguida, recargá la página o esperá un rato.</p>
</div>
<h2>Globo del chat</h2>
<p>Es el mensaje que aparece al lado del botón cuando alguien pasa el mouse por encima. En la sección <strong>Globo del chat</strong> escribís el texto (hasta 60 caracteres) y tocás Guardar. Si lo dejás vacío, dice «¿Necesitás ayuda?».</p>
<h2>Nombre del asistente</h2>
<p>Es el nombre que aparece debajo de los mensajes del bot en el chat. En la sección <strong>Nombre del asistente</strong> escribí el que quieras (hasta 60 caracteres). Si no ponés ninguno, dice «Asistente virtual».</p>
<div class="callout success">
<p><strong>Un consejo:</strong> usá un nombre que deje claro que es un asistente virtual, para que nadie crea que habla con una persona.</p>
</div>"""

P["mensajes"] = """    <h1>Bienvenida y botones de inicio</h1>
<p class="docs-lead">Lo primero que ve tu visitante al abrir el chat.</p>
<h2>Mensaje de bienvenida</h2>
<p>Es el saludo que el bot manda apenas alguien abre el chat, junto con los botones de inicio y las preguntas del menú. En «Mi bot», sección <strong>Mensaje de bienvenida</strong>, escribilo (hasta 1000 caracteres) y tocá <strong>Guardar</strong>.</p>
<ul>
<li>Si lo dejás vacío, el bot usa su saludo de siempre, con el nombre de tu empresa.</li>
<li>Si lo cambiás, conviene que siga diciendo que es un asistente virtual.</li>
</ul>
<p>Ejemplo: «¡Hola! Soy el asistente virtual de Los Aromos. Contame qué necesitás o elegí una opción.»</p>
<h2>Botones de inicio</h2>
<p>Son atajos que aparecen con el saludo, al lado de «Hablar con una persona» (o «Hablar por WhatsApp»). Cuando el visitante toca uno, el bot responde como si lo hubiera escrito.</p>
<p>En la sección <strong>Botones de inicio</strong> podés cargar hasta 4, de hasta 60 caracteres cada uno, y tocar <strong>Guardar botones</strong>. Ejemplos: «Ver propiedades en alquiler», «Horarios y ubicación», «Pedir presupuesto».</p>
<div class="callout">
<p>Escribí cada botón como una pregunta o pedido que un cliente haría de verdad. Si el bot no sabe contestarlo, va a quedar en <a href="/docs/sin-respuesta.html">Sin respuesta</a>: cargá la respuesta como <a href="/docs/preguntas-fijas.html">pregunta fija</a>.</p>
</div>"""

P["preguntas-fijas"] = """    <h1>Preguntas fijas</h1>
<p class="docs-lead">Las respuestas que querés que el bot dé siempre igual: horarios, medios de pago, envíos.</p>
<h2>Para qué sirven</h2>
<p>Para todo lo que no se puede improvisar. Lo que cargues acá el bot lo contesta <strong>exactamente como lo escribiste, sin cambiarle una palabra</strong>. Lo que no cargues, lo contesta con lo que lee de tu sitio y de la <a href="/docs/informacion.html">información extra</a>.</p>
<h2>Cargar una pregunta</h2>
<p>En la pantalla <strong>Preguntas fijas</strong>, tocá <strong>Nueva pregunta</strong> y completá:</p>
<table class="docs-table">
<thead><tr><th>Campo</th><th>Qué poner</th></tr></thead>
<tbody>
<tr><td><strong>Pregunta</strong></td><td>La pregunta tal como la haría un cliente. Ejemplo: «¿Cuáles son los horarios de atención?»</td></tr>
<tr><td><strong>Respuesta</strong></td><td>El texto que el bot va a dar, igual cada vez.</td></tr>
<tr><td><strong>Otras formas de preguntarlo</strong></td><td>Variantes, una por línea. Ejemplo: «¿hacen factura A?». Ayudan a que el bot reconozca la pregunta aunque la escriban distinto.</td></tr>
<tr><td><strong>Mostrar en el menú de botones</strong></td><td>Si la tildás, la pregunta aparece como botón en el menú del chat.</td></tr>
<tr><td><strong>Dentro de</strong></td><td>Para armar un submenú: elegí otra pregunta y esta pasa a ser un botón que aparece al tocarla. Se puede anidar hasta tres niveles. Dentro de un submenú el bot ofrece un botón para volver.</td></tr>
<tr><td><strong>Orden</strong></td><td>Un número: define en qué lugar aparece en el menú. Las de número más bajo van primero.</td></tr>
</tbody>
</table>
<p>Para cambiar o borrar una pregunta, usá los botones de su fila en la lista.</p>
<h2>Armar un submenú</h2>
<p>Si tenés muchas respuestas, agrupalas. Por ejemplo, una pregunta fija «Medios de pago» con la respuesta «Estas son las formas de pago», y dentro de ella «¿Aceptan tarjeta?» y «¿Hacen factura A?» con la opción <strong>Dentro de → Medios de pago</strong>. Al tocar «Medios de pago», el bot muestra esas dos como botones.</p>
<p>La pregunta que agrupa las demás se muestra en el menú del chat; las de adentro solo aparecen al entrar a ella.</p>
<div class="callout success">
<p><strong>Un buen hábito:</strong> mirá cada tanto <a href="/docs/sin-respuesta.html">Sin respuesta</a>. Lo que se repite ahí es lo primero que conviene convertir en pregunta fija.</p>
</div>"""

P["informacion"] = """    <h1>Información extra</h1>
<p class="docs-lead">Datos que el bot puede usar además de tu sitio web.</p>
<p>Además de leer tu sitio, el bot puede usar lo que le cargues en la pantalla <strong>Información</strong>: promociones, listas de precios, condiciones, reglamentos. Hay dos formas de cargarla.</p>
<h2>Cargar un texto</h2>
<p>En «Cargar un texto», escribí o pegá la información:</p>
<ul>
<li><strong>Título:</strong> una referencia corta para reconocerla en la lista.</li>
<li><strong>Contenido:</strong> el texto que el bot va a usar.</li>
<li><strong>Vence (opcional):</strong> una fecha. Pasado ese día, el bot deja de usar esa información.</li>
</ul>
<p>Tocá <strong>Guardar información</strong>.</p>
<h2>Subir un PDF</h2>
<p>Sirve para catálogos, listas de precios y reglamentos. En «Subir un PDF» elegí el archivo, poné un título (opcional: si lo dejás vacío se usa el nombre del archivo) y, si corresponde, una fecha de vencimiento.</p>
<div class="callout warn">
<p><strong>El PDF tiene que tener texto.</strong> Un PDF escaneado como imagen no se puede leer. Si no podés seleccionar el texto con el mouse al abrirlo, es una imagen.</p>
</div>
<h2>Qué conviene poner fecha de vencimiento</h2>
<p>Todo lo que cambia: una promoción, una lista de precios, un horario especial de feriados. Así el bot nunca ofrece algo vencido.</p>
<h2>Sacar información</h2>
<p>En «Información cargada» ves todo lo que subiste. Con el ícono de eliminar de cada fila, esa información deja de estar disponible para el bot.</p>"""

P["sin-respuesta"] = """    <h1>Sin respuesta</h1>
<p class="docs-lead">Lo que tus visitantes preguntaron y el bot no supo contestar.</p>
<h2>Para qué sirve</h2>
<p>Es la lista de mejoras de tu bot. Cada fila muestra lo que preguntaron y cuándo. En «Mi bot» también ves cuántas preguntas sin respuesta hay: tocando ese contador llegás a esta pantalla.</p>
<h2>Qué hacer con cada pregunta</h2>
<ul>
<li><strong>Si se repite o es importante,</strong> tocá <strong>Crear pregunta fija</strong>: se abre el formulario con la pregunta ya cargada, solo te falta escribir la respuesta. Ver <a href="/docs/preguntas-fijas.html">Preguntas fijas</a>.</li>
<li><strong>Si es información que falta,</strong> cargala en <a href="/docs/informacion.html">Información</a> o agregala a tu sitio y volvé a leerlo.</li>
</ul>
<p>Si no hay nada en la lista, el bot pudo con todo.</p>"""

P["atencion"] = """    <h1>Hablar con una persona</h1>
<p class="docs-lead">Qué pasa cuando alguien pide hablar con una persona o el bot no tiene el dato.</p>
<h2>Las dos formas de atención</h2>
<table class="docs-table">
<thead><tr><th>Forma</th><th>Cómo funciona</th></tr></thead>
<tbody>
<tr><td><strong>Por tu WhatsApp</strong></td><td>El bot atiende todo el chat y, cuando alguien pide hablar con una persona o el bot no tiene el dato, le pasa el enlace a tu WhatsApp.</td></tr>
<tr><td><strong>En el chat del sitio</strong></td><td>La conversación pasa a tu equipo, que la atiende en vivo desde Chatwoot (ver <a href="/docs/conversaciones.html">Conversaciones</a>). Se activa dejando vacío el campo de WhatsApp.</td></tr>
</tbody>
</table>
<div class="callout">
<p><strong>Depende de tu plan.</strong> En el plan Esencial la atención de una persona es solo por WhatsApp. La atención de tu equipo en el chat está disponible desde el plan Profesional. Ver <a href="/docs/plan.html">Tu plan</a>.</p>
</div>
<h2>Cargar tu WhatsApp</h2>
<p>En «Mi bot», sección <strong>Atención de una persona</strong>, escribí el número en el campo «WhatsApp para derivar» y tocá <strong>Guardar</strong>. Va con el código de país (54) y el 9, sin el 0 ni el 15. Por ejemplo: <code>549 2324 123456</code>.</p>
<p>Al guardarlo, el panel te muestra un enlace para probarlo: tocalo y fijate que abra la conversación con tu número.</p>
<h2>Preguntar el nombre antes de pasar con una persona</h2>
<p>En la misma tarjeta hay un interruptor: <strong>Preguntar el nombre cuando piden hablar con una persona</strong>. Está apagado de entrada. Si lo prendés, antes de pasar la conversación el bot pregunta «¿cómo te llamás?» y recién después deriva, así tu equipo sabe con quién habla.</p>
<ul>
<li>Si el visitante escribe algo que no parece un nombre, el bot se lo vuelve a pedir; con <strong>Cancelar</strong> vuelve al menú.</li>
<li>Con la atención por tu WhatsApp, el nombre viaja en el mensaje («Soy Ana») cuando el visitante toca el enlace.</li>
<li>Con la atención en el chat, tu equipo ve el nombre en Chatwoot, como nota privada y como nombre del contacto.</li>
<li>En WhatsApp, si el contacto ya tiene un nombre en su perfil, el bot no se lo pregunta.</li>
</ul>
<h2>También por WhatsApp</h2>
<p>Si además querés que el bot atienda los mensajes que llegan al WhatsApp de tu empresa, mirá <a href="/docs/whatsapp.html">El bot en tu WhatsApp</a>.</p>"""

P["conversaciones"] = f"""    <h1>Conversaciones en Chatwoot</h1>
<p class="docs-lead">Dónde ver lo que hablaron tus visitantes con el bot y dónde atender cuando hace falta una persona.</p>
<h2>Entrar desde el panel</h2>
<p>Las charlas con tus visitantes, y el pase a una persona cuando el bot no puede resolver, se atienden en <strong>Chatwoot</strong>. No necesitás otra contraseña: al final de «Mi bot», sección <strong>Conversaciones</strong>, tocá <strong>Abrir Chatwoot</strong>. Se abre una pestaña nueva con tu cuenta ya iniciada.</p>
<div class="callout warn">
<p>Si tu navegador bloquea la ventana nueva, el panel te muestra un enlace «Abrir Chatwoot»: tocalo para entrar. El enlace sirve una sola vez.</p>
</div>
<h2>Qué vas a encontrar</h2>
<ul>
<li>Todas las conversaciones de tu chat, con lo que escribió el visitante y lo que respondió el bot.</li>
<li>Las conversaciones que el bot pasó a una persona. Si tu plan incluye atención en el chat, las respondés desde ahí, en vivo.</li>
</ul>
<h2>Sumar a alguien de tu equipo</h2>
<p>Para que otra persona atienda las conversaciones, escribinos por <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a> y vemos cómo hacerlo.</p>"""

P["plan"] = f"""    <h1>Tu plan</h1>
<p class="docs-lead">Qué incluye, cuánto llevás usado y cómo cambiarlo.</p>
<h2>Los planes</h2>
<table class="docs-table">
<thead><tr><th>Plan</th><th>Preguntas por mes</th><th>Atención de una persona</th></tr></thead>
<tbody>
<tr><td><strong>Esencial</strong></td><td>1.000</td><td>Por tu WhatsApp</td></tr>
<tr><td><strong>Profesional</strong></td><td>3.000</td><td>Tu equipo en el chat del sitio, o por WhatsApp</td></tr>
<tr><td><strong>A medida</strong></td><td>Se acuerda con vos</td><td>En el chat o por WhatsApp, con el equipo que necesites</td></tr>
</tbody>
</table>
<p>Los precios están en la sección <a href="/#planes">Planes</a> de la página principal.</p>
<h2>Cuánto llevás usado</h2>
<p>En «Mi bot», la primera tarjeta muestra las <strong>preguntas respondidas este mes</strong> contra las que incluye tu plan, con una barra de avance. El conteo se reinicia el 1.º de cada mes. Si superás lo que incluye tu plan, el panel te lo avisa.</p>
<h2>Pedir un cambio de plan</h2>
<ol class="step-list">
<li>En «Mi bot», sección <strong>Tu plan</strong>, tocá <strong>Pedir cambio de plan</strong>.</li>
<li>Elegí a qué plan querés pasar y, si querés, dejá un comentario (por ejemplo, cuántas personas van a atender).</li>
<li>Tocá <strong>Enviar pedido</strong>. Te avisamos por correo cuando esté resuelto.</li>
</ol>
<p>Mientras el pedido está pendiente, el panel te muestra su estado. Si no se aprueba, vas a ver el motivo.</p>
<div class="callout">
<p>¿Dudas sobre qué plan te conviene? Escribinos por <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a>.</p>
</div>"""

P["problemas"] = f"""    <h1>Problemas frecuentes</h1>
<p class="docs-lead">Lo más habitual y cómo resolverlo.</p>
<h3>No me llegó el correo para elegir mi contraseña</h3>
<p>Revisá la carpeta de spam o correo no deseado. Si no está, en <a href="{PANEL}" target="_blank" rel="noopener">el ingreso al panel</a> tocá «¿Olvidaste tu contraseña?» y pedí uno nuevo con tu correo. Si sigue sin llegar, escribinos y revisamos que la dirección esté bien cargada.</p>
<h3>El enlace del correo dice que venció</h3>
<p>El enlace dura unas horas y sirve una sola vez. Pedí uno nuevo desde «¿Olvidaste tu contraseña?».</p>
<h3>Me dice «usuario o contraseña incorrectos»</h3>
<p>Tu usuario es tu correo completo. Revisá que esté bien escrito y que no tengas activadas las mayúsculas. Si tenés dudas, pedí una contraseña nueva desde «¿Olvidaste tu contraseña?».</p>
<h3>El panel me pide aceptar los Términos y no me deja hacer nada</h3>
<p>Es lo esperado la primera vez: hay que aceptarlos para usar el panel. Tu bot en el sitio sigue funcionando mientras tanto.</p>
<h3>Cambié algo y no lo veo en el chat</h3>
<p>Los cambios de aspecto (color, ícono, globo) tardan unos minutos en verse en tu sitio. Esperá un rato y recargá la página, mejor en una ventana privada o con la memoria caché limpia. Si tu sitio usa un plugin de caché, vaciá la caché.</p>
<h3>El chat no aparece en mi sitio</h3>
<ul>
<li>Verificá que el código esté pegado antes de <code>&lt;/body&gt;</code> y en la página que estás mirando.</li>
<li>Si usás un plugin de caché o un CDN, vaciá la caché.</li>
<li>Probá en una ventana privada, por si una extensión del navegador lo bloquea.</li>
</ul>
<p>Más en <a href="/docs/instalar.html">Instalarlo en tu sitio</a>.</p>
<h3>El bot no sabe algo que está en mi sitio</h3>
<p>Fijate en «Mi bot» que la última lectura haya terminado bien y que la cantidad de páginas leídas sea la esperada. Si publicaste algo hace poco, tocá <strong>Volver a leer el sitio</strong>. Si el dato no está en tu sitio, cargalo como <a href="/docs/preguntas-fijas.html">pregunta fija</a> o <a href="/docs/informacion.html">información extra</a>.</p>
<h3>El bot dice algo que no es correcto</h3>
<p>Cargá la respuesta correcta como <a href="/docs/preguntas-fijas.html">pregunta fija</a>: el bot la da siempre tal cual, sin cambiarle una palabra.</p>
<h3>Se quedó leyendo mi sitio y no termina</h3>
<p>Un sitio con muchas páginas puede tardar varios minutos. Podés seguir usando el panel mientras tanto. Si pasa mucho tiempo y sigue igual, escribinos.</p>
<h3>Me llegó un correo diciendo que la línea de WhatsApp está desconectada</h3>
<p>Entrá a «Mi bot», tarjeta <strong>WhatsApp</strong>, y tocá <strong>Vincular el celular</strong>. Suele pasar si el celular se quedó sin internet o si se cerró la sesión en «Dispositivos vinculados». Más en <a href="/docs/whatsapp.html">El bot en tu WhatsApp</a>.</p>
<h3>El bot no contesta en un chat de WhatsApp</h3>
<p>Si escribiste vos desde el celular de la línea, el bot se calla en ese chat. Vuelve cuando el contacto escribe <em>menu</em> o pasadas 12 horas. Si el estado de la tarjeta no dice <strong>Conectada</strong>, vinculá el celular de nuevo.</p>
<h3>No veo las conversaciones de WhatsApp en Chatwoot</h3>
<p>Mientras el bot atiende, la conversación figura como <em>pendiente</em> y el filtro <em>Abiertas</em> no la muestra. Cambialo a <em>Pendientes</em> o <em>Todas</em>.</p>
<h3>Los pedidos de mis formularios no me llegan por correo</h3>
<p>Entrá a la pantalla <strong>Pedidos</strong>: el pedido está guardado aunque el correo no haya salido. Lo reciben los usuarios con acceso completo (no los de solo lectura); revisá también la carpeta de spam.</p>
<h3>El panel dice «Tu usuario es de solo lectura»</h3>
<p>Tu usuario puede mirar pero no cambiar nada. Si necesitás editar, pedile al responsable de la cuenta que lo haga o que te dé acceso completo escribiéndonos por <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a>.</p>
<div class="callout">
<p><strong>¿Nada de esto lo resuelve?</strong> Escribinos por <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a> contando qué pasó y desde qué pantalla.</p>
</div>"""

P["avisos"] = """    <h1>Avisos por palabra clave</h1>
<p class="docs-lead">Un texto fijo que el bot da apenas el visitante nombra ciertas palabras: lo urgente, lo que no hacés, lo que no puede esperar.</p>
<h2>Para qué sirven</h2>
<p>Hay cosas que no conviene que terminen en un menú ni en una respuesta improvisada. Por ejemplo:</p>
<ul>
<li><strong>Urgencias:</strong> «Ante una emergencia llamá al 107.»</li>
<li><strong>Lo que no hacés:</strong> «No hacemos envíos al exterior.»</li>
<li><strong>Un aviso del momento:</strong> «Esta semana estamos cerrados por vacaciones.»</li>
</ul>
<p>Cuando lo que escribe el visitante nombra alguna de las palabras clave, el bot contesta tu aviso y <strong>nada más</strong>: no sigue con el menú, no consulta tu sitio ni pasa con una persona. Después del aviso queda un botón <em>Ver opciones</em> para volver al menú.</p>
<h2>Cargar un aviso</h2>
<p>En la pantalla <strong>Avisos</strong>, tocá <strong>Nuevo aviso</strong> y completá:</p>
<table class="docs-table">
<thead><tr><th>Campo</th><th>Qué poner</th></tr></thead>
<tbody>
<tr><td><strong>Nombre</strong></td><td>Cómo lo reconocés vos en la lista. Ejemplo: «Urgencias».</td></tr>
<tr><td><strong>Palabras clave</strong></td><td>Una o más, separadas por coma o una por renglón. Cada una con al menos 3 letras. Pueden ser frases: «envío al exterior».</td></tr>
<tr><td><strong>Qué contesta el bot</strong></td><td>El texto del aviso, igual cada vez.</td></tr>
</tbody>
</table>
<p>Podés tener hasta 10 avisos. Para cambiar o borrar uno, usá los botones de su fila.</p>
<h2>Cómo se comparan las palabras</h2>
<ul>
<li>No importan las mayúsculas, los acentos ni los signos: «URGENCIA!!» y «urgencia» son lo mismo.</li>
<li>Se compara <strong>palabra entera</strong>: la clave «urgencia» no se dispara con «urgencias». Si querés cubrir las dos formas, cargá las dos.</li>
<li>Una frase clave tiene que estar completa y en orden: «envío al exterior» no se dispara con solo «envío».</li>
<li>Si dos avisos coinciden, gana el que está primero en la lista.</li>
</ul>
<div class="callout warn">
<p><strong>Un aviso gana sobre todo lo demás</strong>, incluso sobre una pregunta fija o sobre un pedido de hablar con una persona. Usá palabras bien específicas: una palabra muy común haría que el bot conteste el aviso en cualquier conversación.</p>
</div>
<p>Los avisos funcionan igual en el chat de tu sitio y en tu <a href="/docs/whatsapp.html">WhatsApp</a>, y también si tu bot está en modo cerrado.</p>"""

P["formularios"] = """    <h1>Formularios y pedidos</h1>
<p class="docs-lead">Que el bot pida los datos de a uno (nombre, teléfono, qué necesita) y te deje un pedido listo para atender.</p>
<h2>Para qué sirven</h2>
<p>Para tomar un turno, un presupuesto, un reclamo o una consulta sin que el visitante tenga que escribir todo de una vez. Cada formulario aparece como un <strong>botón del menú del chat</strong>: al tocarlo, el bot hace las preguntas una por una y al final te deja un pedido.</p>
<h2>Armar un formulario</h2>
<p>En la pantalla <strong>Formularios</strong>, tocá <strong>Nuevo formulario</strong>:</p>
<table class="docs-table">
<thead><tr><th>Campo</th><th>Qué poner</th></tr></thead>
<tbody>
<tr><td><strong>Nombre</strong></td><td>Es el texto del botón del chat. Ejemplo: «Pedir presupuesto». No puede repetirse entre tus formularios.</td></tr>
<tr><td><strong>Qué dice antes de la primera pregunta</strong></td><td>Opcional. Ejemplo: «Armamos tu presupuesto en un minuto.»</td></tr>
<tr><td><strong>Datos que pide</strong></td><td>De 1 a 12. Cada uno tiene su pregunta, su tipo y si es obligatorio. El orden se cambia con las flechas.</td></tr>
<tr><td><strong>Qué dice al terminar</strong></td><td>Opcional. Si lo dejás vacío, el bot dice que recibió los datos y que le van a responder.</td></tr>
<tr><td><strong>Mostrar un botón en el menú</strong></td><td>Si lo destildás, el formulario no aparece en el menú, pero se puede empezar escribiendo su nombre.</td></tr>
</tbody>
</table>
<h3>Tipos de dato</h3>
<table class="docs-table">
<thead><tr><th>Tipo</th><th>Cómo lo pide el bot</th></tr></thead>
<tbody>
<tr><td><strong>Texto libre</strong></td><td>Acepta cualquier respuesta de hasta 500 letras.</td></tr>
<tr><td><strong>Teléfono</strong></td><td>Revisa que tenga forma de teléfono; si no, lo vuelve a pedir.</td></tr>
<tr><td><strong>Correo</strong></td><td>Revisa que tenga forma de correo; si no, lo vuelve a pedir.</td></tr>
<tr><td><strong>Elegir entre opciones</strong></td><td>Muestra de 2 a 8 botones (una opción por renglón al armarlo). Hay que elegir uno.</td></tr>
</tbody>
</table>
<p>Un dato que no marcás como obligatorio muestra un botón <em>Omitir</em>. En cualquier momento el visitante puede tocar <strong>Cancelar</strong> y volver al menú sin dejar nada.</p>
<div class="callout">
<p>Mientras alguien llena un formulario, <strong>todo lo que escribe es la respuesta a la pregunta en curso</strong>: ni un aviso ni una pregunta fija lo interrumpen. Si editás o borrás el formulario, quien lo estaba llenando empieza de cero.</p>
</div>
<h2>Recibir los pedidos</h2>
<p>Cuando el visitante responde el último dato, el pedido queda guardado y:</p>
<ul>
<li>Te llega un <strong>correo</strong> con todas las respuestas. Lo reciben los usuarios con acceso completo al panel, no los de <a href="/docs/usuarios.html">solo lectura</a>.</li>
<li>Aparece en la pantalla <strong>Pedidos</strong>, lo último primero (se muestran los últimos 200).</li>
</ul>
<p>En <strong>Pedidos</strong> marcás cada uno como <strong>Atendido</strong> (o lo volvés a pendiente) y podés borrarlo. Borrar un formulario <strong>no</strong> borra los pedidos que ya llegaron.</p>
<div class="callout warn">
<p><strong>Son datos personales.</strong> Lo que deja el visitante (nombre, teléfono, correo) usalo solo para responderle, y borrá los pedidos que ya no necesites.</p>
</div>
<h2>Los formularios y tu plan</h2>
<p>Los pasos intermedios no cuentan como preguntas de tu plan: solo cuenta una por cada formulario completado. Funcionan igual en el chat del sitio y en tu <a href="/docs/whatsapp.html">WhatsApp</a>.</p>"""

P["whatsapp"] = """    <h1>El bot en tu WhatsApp</h1>
<p class="docs-lead">Que LibraBot atienda también los mensajes que llegan al WhatsApp de tu empresa, con el mismo menú y las mismas respuestas que en el chat del sitio.</p>
<div class="callout warn">
<p><strong>Leelo antes de activarlo.</strong> WhatsApp no permite oficialmente que un programa atienda un número vinculado con un código QR. Si lo detecta, puede bloquear el número de forma permanente, y LibraBot no puede revertirlo. Por eso conviene usar <strong>un número dedicado a la atención</strong> con <strong>WhatsApp Business</strong>, y no el principal de tu negocio. El bot solo contesta a quien te escribe primero y no manda mensajes masivos.</p>
</div>
<h2>1. Activar WhatsApp</h2>
<p>En «Mi bot», tarjeta <strong>WhatsApp</strong>, tildá «Entiendo el riesgo y quiero activar WhatsApp» y tocá <strong>Activar WhatsApp</strong>. Queda anotado quién aceptó el riesgo y cuándo.</p>
<h2>2. Vincular el celular</h2>
<p>Tocá <strong>Vincular el celular</strong>. Se abre una ventana con los pasos y un código QR:</p>
<ol class="step-list">
<li>Abrí <strong>WhatsApp Business</strong> en el celular que tiene el chip de la línea.</li>
<li>Tocá <strong>Menú</strong> (los tres puntitos) en Android, o <strong>Configuración</strong> en iPhone.</li>
<li>Tocá <strong>Dispositivos vinculados</strong> y después <strong>Vincular un dispositivo</strong>.</li>
<li>Apuntá el celular a la pantalla y escaneá el código.</li>
</ol>
<div class="callout warn">
<p><strong>Escaneá el código solo con el celular de la línea.</strong> Si lo escanea otro celular, el bot atiende con el número equivocado. El código se renueva solo cada unos segundos, y la ventana se cierra sola cuando la línea queda conectada.</p>
</div>
<p>El estado de la línea se ve en la tarjeta: <strong>Conectada</strong>, <strong>Conectando…</strong>, <strong>Sin vincular</strong> o <strong>No se pudo consultar</strong> (se actualiza solo).</p>
<h2>Qué hace el bot por WhatsApp</h2>
<ul>
<li><strong>Contesta lo mismo que en el chat:</strong> el saludo, las preguntas fijas con sus submenús, los <a href="/docs/avisos.html">avisos</a>, los <a href="/docs/formularios.html">formularios</a> y lo que lee de tu sitio y de la <a href="/docs/informacion.html">información extra</a>.</li>
<li><strong>Los botones salen como un menú numerado.</strong> WhatsApp no admite botones en este tipo de línea, así que el bot escribe las opciones con un número y el contacto responde con el número. «Escribí <em>menu</em> para ver las opciones» vuelve al inicio.</li>
<li><strong>Solo lee texto.</strong> Si el contacto manda un audio, una foto o un documento y la atención es desde el celular, el bot le avisa que por ahí solo puede leer texto.</li>
</ul>
<h2>Quién atiende a una persona</h2>
<p>En la misma tarjeta elegís cómo se atiende cuando alguien pide hablar con una persona:</p>
<table class="docs-table">
<thead><tr><th>Modo</th><th>Cómo funciona</th></tr></thead>
<tbody>
<tr><td><strong>Desde el celular de la línea</strong></td><td>Atendés vos, desde el celular. Cuando escribís un mensaje en un chat, <strong>el bot se calla en ese chat</strong>. Vuelve cuando el contacto escribe «menu», o a las 12 horas de que escribiste.</td></tr>
<tr><td><strong>En Chatwoot (varios operadores)</strong></td><td>Tu equipo contesta desde la bandeja «WhatsApp» de Chatwoot y lo que escribe un operador sale por tu WhatsApp. Mientras un operador tiene la conversación abierta, el bot se calla; al resolverla, el bot vuelve a atender. Lo que escribas desde el celular queda como nota privada. Está disponible desde el <a href="/docs/plan.html">plan Profesional</a>.</td></tr>
</tbody>
</table>
<h3>Si atendés por Chatwoot</h3>
<ul>
<li>Mientras el bot atiende, la conversación figura como <strong>pendiente</strong>. En Chatwoot, el filtro <em>Abiertas</em> no muestra las pendientes: cambialo a <em>Pendientes</em> o <em>Todas</em> para verlas. Pasa a <em>abierta</em> cuando el contacto pide una persona o cuando un operador contesta.</li>
<li>Los <strong>audios, fotos y documentos</strong> del contacto llegan como archivos, y los que adjuntes salen por WhatsApp.</li>
<li>Más en <a href="/docs/conversaciones.html">Conversaciones en Chatwoot</a>.</li>
</ul>
<h2>Avisos si se cae la línea</h2>
<p>LibraBot revisa la línea cada pocos minutos. Si una línea que ya estuvo vinculada lleva <strong>más de 10 minutos desconectada</strong>, te mandamos un correo (a los usuarios con acceso completo y a nosotros), y otro cuando vuelve. Una caída corta no avisa, y una línea que todavía no vinculaste tampoco.</p>
<p>Si llegó el correo: entrá a «Mi bot», tarjeta <strong>WhatsApp</strong>, y tocá <strong>Vincular el celular</strong>. Suele pasar si el celular se quedó sin internet o si se cerró la sesión desde «Dispositivos vinculados».</p>
<h2>Quitar la línea</h2>
<p>El botón <strong>Quitar la línea</strong> desvincula el celular y el bot deja de atender por WhatsApp. Podés volver a activarla cuando quieras.</p>
<h2>Cuidados</h2>
<ul>
<li>Usá un número dedicado y WhatsApp Business.</li>
<li>No vincules el mismo número en otro programa a la vez: se pisan las sesiones y la línea se corta una y otra vez.</li>
<li>No mandes mensajes masivos con ese número.</li>
<li>Mantené el celular encendido y con internet.</li>
</ul>"""

P["cartel-qr"] = """    <h1>Cartel con el QR de WhatsApp</h1>
<p class="docs-lead">Un cartel para imprimir y pegar en tu local o en el mostrador: quien escanea el código abre un chat con tu WhatsApp.</p>
<h2>Armar el cartel</h2>
<ol class="step-list">
<li>En «Mi bot», tarjeta <strong>Cartel con el QR de WhatsApp</strong>, escribí el WhatsApp de la empresa <strong>con el código de país</strong>. Por ejemplo: <code>54 9 11 2345 6789</code>. Si ya cargaste un número para la atención por WhatsApp, viene cargado.</li>
<li>Tocá <strong>Armar el cartel</strong>: se abre una vista previa.</li>
<li><strong>Probalo con la cámara de tu celular</strong> antes de imprimir: tiene que abrir WhatsApp con tu número.</li>
<li>Tocá <strong>Imprimir</strong>. El cartel sale solo, a hoja completa, en blanco y negro.</li>
</ol>
<h2>Qué dice</h2>
<p>«Escribinos por WhatsApp», el código QR, «Escaneá el código con la cámara de tu celular», el nombre de tu empresa y tu número. Al escanear, se abre un chat con tu número y un primer mensaje armado: «Hola, los vi por el cartel.»</p>
<div class="callout">
<p><strong>El código lleva a un chat con ese número.</strong> Si querés que lo atienda el bot, el número tiene que ser el de la línea que vinculaste en <a href="/docs/whatsapp.html">El bot en tu WhatsApp</a>. Si es otro número, lo atiende quien lo tenga.</p>
</div>
<div class="callout warn">
<p>Siempre sale en blanco y negro, aunque uses el panel en modo oscuro: es un papel y el código necesita contraste para leerse bien. Imprimilo en un tamaño que se pueda escanear a un par de pasos.</p>
</div>"""

P["actividad"] = """    <h1>Actividad</h1>
<p class="docs-lead">Qué le preguntan a tu bot, cuánto, y qué no supo contestar.</p>
<h2>Elegir el período</h2>
<p>En la pantalla <strong>Actividad</strong>, arriba, elegís <strong>Últimos 7 días</strong>, <strong>30 días</strong> o <strong>90 días</strong> (hoy incluido).</p>
<h2>Qué muestra</h2>
<table class="docs-table">
<thead><tr><th>Qué</th><th>Qué significa</th></tr></thead>
<tbody>
<tr><td><strong>Preguntas</strong></td><td>Cuántas preguntas respondió el bot y en cuántas conversaciones.</td></tr>
<tr><td><strong>Contestadas por el bot</strong></td><td>El porcentaje de esas preguntas que pudo contestar.</td></tr>
<tr><td><strong>Sin respuesta</strong></td><td>Cuántas no supo contestar.</td></tr>
<tr><td><strong>Pasaron a una persona</strong></td><td>Cuántas conversaciones del período terminaron derivadas a tu equipo.</td></tr>
<tr><td><strong>Preguntas por día</strong></td><td>Un gráfico de barras; si pasás el mouse por una barra ves el día y la cantidad.</td></tr>
<tr><td><strong>Lo más preguntado</strong></td><td>Las 10 preguntas que más se repiten, con cuántas veces y la última vez.</td></tr>
<tr><td><strong>Lo que el bot no supo contestar</strong></td><td>Las 15 más repetidas, agrupadas, con el botón <strong>Crear pregunta fija</strong>.</td></tr>
</tbody>
</table>
<h2>Cómo cuenta</h2>
<ul>
<li>Una pregunta es un mensaje del visitante que el bot contestó. <strong>No cuentan</strong> el saludo ni «menú», ni lo que contesta una persona de tu equipo, ni los pasos de un <a href="/docs/formularios.html">formulario</a> (solo el último).</li>
<li>Agrupa las que se escriben casi igual: «¿Cuál es el horario?» y «cual es el horario» cuentan como una. No agrupa por significado: «horario» y «a qué hora abren» quedan separadas.</li>
<li>Los días son de hora argentina; los días sin preguntas figuran en cero.</li>
</ul>
<h2>Qué hacer con esto</h2>
<p>Lo que más se repite en «Lo que el bot no supo contestar» es lo primero que conviene convertir en <a href="/docs/preguntas-fijas.html">pregunta fija</a>. Para ver cada pregunta suelta con su fecha, mirá <a href="/docs/sin-respuesta.html">Sin respuesta</a>.</p>"""

P["historial"] = """    <h1>Historial de cambios</h1>
<p class="docs-lead">Quién cambió qué en el panel, y cuándo.</p>
<h2>Qué registra</h2>
<p>En la pantalla <strong>Historial</strong> ves, lo último primero, los cambios que se hicieron en:</p>
<ul>
<li>Los <strong>ajustes del bot</strong> (bienvenida, sitio, botones, color, nombre del asistente, atención de una persona, etc.).</li>
<li>Las <strong>preguntas fijas</strong>.</li>
<li>Los <strong>avisos</strong> y los <strong>formularios</strong>.</li>
<li>La <strong>información</strong> que cargaste.</li>
</ul>
<p>De cada cambio se ve quién lo hizo, cuándo y qué hizo (creó, cambió, borró). En las ediciones aparece el <strong>antes y el después</strong> de cada campo.</p>
<h2>Qué no muestra</h2>
<ul>
<li><strong>Claves, tokens y textos largos:</strong> el historial dice que cambiaron, pero no copia a qué. Se ve como «cambió».</li>
<li><strong>Lo que hace el sistema solo</strong>, como la lectura nocturna de tu sitio.</li>
<li><strong>Los pedidos de los formularios</strong>, porque llevan datos personales de tus visitantes.</li>
<li>Cambios anteriores a la fecha en que se activó el historial.</li>
</ul>
<div class="callout">
<p>Los cambios que hace el equipo de LibraBot por vos (por ejemplo, un cambio de plan) aparecen a nombre de <strong>Soporte de LibraBot</strong>. Se muestran los últimos 100 cambios.</p>
</div>
<p>Es útil cuando algo cambió y no sabés por qué: acá ves quién fue y qué valor tenía antes.</p>"""

P["usuarios"] = """    <h1>Usuarios y solo lectura</h1>
<p class="docs-lead">Sumar a alguien de tu equipo que pueda mirar el panel sin poder cambiar nada.</p>
<h2>Para qué sirve</h2>
<p>Quien te dio de alta es el responsable de la cuenta y puede hacer todo. Si querés que un socio, un contador o alguien de ventas vea la actividad, las preguntas y el historial sin riesgo de cambiar algo por error, le das un usuario de <strong>solo lectura</strong>.</p>
<h2>Sumar a alguien</h2>
<ol class="step-list">
<li>Entrá a la pantalla <strong>Usuarios</strong>.</li>
<li>En «Sumar a alguien de solo lectura», escribí su nombre y su correo y tocá <strong>Invitar</strong>.</li>
<li>A esa persona le llega un correo para <strong>elegir su contraseña</strong>. Su usuario es su correo.</li>
</ol>
<p>Podés sumar hasta 10. Si el correo no sale, el usuario queda creado igual y la persona puede pedir el enlace desde «¿Olvidaste tu contraseña?» al ingresar.</p>
<h2>Qué puede y qué no</h2>
<table class="docs-table">
<thead><tr><th>Puede</th><th>No puede</th></tr></thead>
<tbody>
<tr><td>Mirar todas las pantallas: Mi bot, Actividad, Preguntas fijas, Avisos, Formularios, Pedidos, Información, Sin respuesta, Historial y Usuarios.<br>Cambiar su propia contraseña.</td><td>Crear, editar ni borrar nada.<br>Marcar pedidos como atendidos.<br>Pedir un cambio de plan.<br>Entrar a Chatwoot.<br>Ver el código QR para vincular el celular.<br>Aceptar los Términos.<br>Sumar a otras personas.</td></tr>
</tbody>
</table>
<p>Quien tiene este usuario ve un aviso arriba, «Tu usuario es de solo lectura», y los botones y campos aparecen apagados. Si intenta cambiar algo igual, el panel se lo rechaza.</p>
<div class="callout">
<p>Los <strong>correos de pedidos</strong> de los formularios los reciben solo los usuarios con acceso completo, no los de solo lectura.</p>
</div>
<h2>Quitar a alguien</h2>
<p>En la lista, tocá el ícono de eliminar de su fila y confirmá. Esa persona deja de poder entrar; se la puede volver a invitar cuando quieras. El responsable de la cuenta no se puede quitar desde acá.</p>"""

# --- escritura -----------------------------------------------------------------------------------------------------
titulos = {a: (t, d) for _, items in MENU for a, t, d in items}
for i, (archivo, titulo, desc) in enumerate(ORDEN):
    cuerpo = P[archivo]
    ant = (ORDEN[i - 1][0], ORDEN[i - 1][1]) if i > 0 else None
    sig = (ORDEN[i + 1][0], ORDEN[i + 1][1]) if i < len(ORDEN) - 1 else None
    nombre = "index.html" if archivo == "index" else f"{archivo}.html"
    (DOCS / nombre).write_text(plantilla(archivo, titulo, desc, cuerpo, ant, sig), encoding="utf-8")

# sitemap y robots
urls = [f"{SITIO}/"] + [f"{SITIO}/docs/" + ("" if a == "index" else f"{a}.html") for a, _, _ in ORDEN]
urls = list(dict.fromkeys(urls))
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f"  <url><loc>{u}</loc></url>" for u in urls]
sm.append("</urlset>")
(PUBLIC / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
(PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITIO}/sitemap.xml\n", encoding="utf-8")
print(len(ORDEN), "páginas,", len(urls), "urls en el sitemap")
