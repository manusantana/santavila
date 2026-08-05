#!/usr/bin/env python3
"""Compone los creativos RRSS de Santavila (GEO-SOCIAL-CONTENT-PACK).

- 6 pins Pinterest 1000x1500 (uno por guia del cluster GEO).
- 6 carruseles de Instagram (6 slides 1080x1350 cada uno).

Uso:
  .venv/bin/python scripts/compose_social_batch1_20260803.py

Salida en content/social/pins/ y content/social/ig/carrusel-0N/.
Tokens de GUIA_DISENO.md: paper #F7F4EC, sage #687060, ink #23251D.
Fuentes: Cormorant (titulares), Hanken Grotesk (cuerpo), JetBrains Mono (eyebrows).
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "content", "social", "fonts")
OUT_PINS = os.path.join(ROOT, "content", "social", "pins")
OUT_IG_BASE = os.path.join(ROOT, "content", "social", "ig")

PAPER = (247, 244, 236)   # #F7F4EC
SAGE = (104, 112, 96)     # #687060
INK = (35, 37, 29)        # #23251D
BONE = (240, 235, 224)

LOGO_DARK = os.path.join(ROOT, "imagen-corporativa", "logo-santavila.png")
LOGO_WHITE = os.path.join(ROOT, "imagen-corporativa", "logo-santavila-blanco.png")


def font(path, size, variation=None):
    f = ImageFont.truetype(os.path.join(FONTS, path), size)
    if variation:
        try:
            f.set_variation_by_name(variation)
        except Exception:
            pass
    return f


def serif(size, weight="SemiBold"):
    return font("Cormorant-SemiBold.ttf", size, weight)


def sans(size, weight="Medium"):
    return font("HankenGrotesk.ttf", size, weight)


def mono(size, weight="Medium"):
    return font("JetBrainsMono.ttf", size, weight)


def text_w(draw, s, f, spacing=0):
    box = draw.textbbox((0, 0), s, font=f)
    return box[2] - box[0] + spacing * max(0, len(s) - 1)


def draw_tracked(draw, xy, s, f, fill, tracking=0):
    """Texto con espaciado entre letras (para eyebrows en mono/uppercase)."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        box = draw.textbbox((0, 0), ch, font=f)
        x += (box[2] - box[0]) + tracking
    return x


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover(img, w, h):
    """Recorta la imagen para llenar w x h (object-fit: cover, centrado)."""
    ratio = max(w / img.width, h / img.height)
    nw, nh = round(img.width * ratio), round(img.height * ratio)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return img.crop((x, y, x + w, y + h))


def paste_logo(canvas, path, height, x, y):
    logo = Image.open(path).convert("RGBA")
    w = round(logo.width * height / logo.height)
    logo = logo.resize((w, height), Image.LANCZOS)
    canvas.paste(logo, (x, y), logo)
    return w


# ---------------------------------------------------------------- Pins

PINS = [
    {
        "slug": "01-lluvia-y-sol",
        "image": "images_generated/leisa/02_ambiente_cantabria.jpg",
        "title": "Muebles de exterior que aguantan lluvia y sol",
        "bullets": [
            "Aluminio lacado: ligero y resistente si el acabado es apto exterior",
            "Resina y polipropileno: prácticos para piscina y limpieza frecuente",
            "Madera: cálida, pero pide mantenimiento y buen secado",
            "Evita cojines húmedos y fundas sobre suciedad",
        ],
    },
    {
        "slug": "02-materiales",
        "image": "images_generated/rinconera/04_asmr_hpl.jpg",
        "title": "Aluminio, resina, HPL o madera: qué material elegir",
        "bullets": [
            "Sol directo: acabados aptos exterior y color estable",
            "Piscina: limpieza fácil y buena resistencia a humedad",
            "Costa: atención a salitre, tornillería y herrajes",
            "Calidez visual: madera, con mantenimiento realista",
        ],
    },
    {
        "slug": "03-mantenimiento",
        "image": "content/images/blog/mantenimiento-tumbona-piscina-cubierta-20260629.png",
        "title": "Checklist de mantenimiento para muebles de exterior",
        "bullets": [
            "Limpieza suave antes de guardar o cubrir",
            "Secar textiles y evitar humedad retenida",
            "Revisar tornillos, ruedas, patas y mecanismos",
            "Sin abrasivos ni presión alta sobre acabados delicados",
        ],
    },
    {
        "slug": "04-terraza-pequena",
        "image": "images_generated/acapulco2p/02_ambiente_exterior_azotea_salamanca.jpg",
        "title": "Cómo amueblar una terraza pequeña sin saturarla",
        "bullets": [
            "Mide el paso libre antes de elegir mesa",
            "Plegables o apilables si el espacio cambia de uso",
            "Bancos y almacenaje vertical liberan suelo",
            "Evita muebles demasiado profundos",
        ],
    },
    {
        "slug": "05-mesas",
        "image": "images_balliu/Atlanta_Silla-Etna_blanco2.jpg",
        "title": "Mesa de exterior: medidas para 2, 4, 6 y 8 personas",
        "bullets": [
            "2 personas: prioriza paso y sillas fáciles de mover",
            "4 personas: cuenta el ancho real de sillas con brazos",
            "6-8 personas: calcula la circulación alrededor",
            "Redonda, rectangular o extensible según el espacio",
        ],
    },
    {
        "slug": "06-tumbonas",
        "image": "images_balliu/Tumbona-Etna_Mesa-auxiliar-Etna_C.jpg",
        "title": "Tumbona de aluminio, resina o madera: cuál elegir",
        "bullets": [
            "Aluminio: ligera y fácil de mover",
            "Resina: práctica para piscina y limpieza frecuente",
            "Madera: más cálida, pero exige más cuidado",
            "Revisa ruedas, respaldo, textiles y tornillería",
        ],
    },
    {
        "slug": "07-chill-out",
        "image": "images_generated/balinesa/02_ambiente_exterior_mallorca.jpg",
        "title": "Cómo montar un chill out en la terraza",
        "bullets": [
            "Elige una pieza protagonista: sofá, set o cama balinesa",
            "Mesa de centro a la altura del asiento (35-45 cm)",
            "Sombra: parasol con buena base, o pérgola",
            "Deja 60-70 cm de paso libre para circular",
        ],
    },
    {
        "slug": "08-base-parasol",
        "image": "images_generated/parasol_roma/02_ambiente_terraza.jpg",
        "title": "Base de parasol: qué peso necesitas",
        "bullets": [
            "Hasta Ø200 cm en terraza protegida: desde 25 kg",
            "Ø250-300 cm: 40 kg o más",
            "Excéntrico: losas de lastre sobre la cruceta",
            "Con viento: sube un escalón y ciérralo si no estás",
        ],
    },
]

PIN_W, PIN_H = 1000, 1500
MARGIN = 84


def compose_pin(spec):
    canvas = Image.new("RGB", (PIN_W, PIN_H), PAPER)
    d = ImageDraw.Draw(canvas)
    maxw = PIN_W - 2 * MARGIN

    # -- cabecera: eyebrow + titulo
    y = 72
    eb_f = mono(23)
    draw_tracked(d, (MARGIN, y), "SANTAVILA · GUÍAS DE EXTERIOR", eb_f, SAGE, tracking=6)
    y += 23 + 30

    t_f = serif(72)
    lines = wrap(d, spec["title"], t_f, maxw)
    for ln in lines:
        d.text((MARGIN, y), ln, font=t_f, fill=INK)
        y += 78
    y += 40

    # -- bloque inferior (bullets + footer), se mide para dar el resto a la foto
    b_f = sans(31)
    bullet_lines = []
    for b in spec["bullets"]:
        bullet_lines.append(wrap(d, b, b_f, maxw - 46))
    bullets_h = sum(len(bl) * 42 + 26 for bl in bullet_lines) - 26
    footer_h = 56 + 34  # divisoria + logo
    bottom_h = 56 + bullets_h + footer_h + 64

    photo_h = PIN_H - y - bottom_h
    photo = cover(Image.open(os.path.join(ROOT, spec["image"])).convert("RGB"), PIN_W, photo_h)
    canvas.paste(photo, (0, y))
    y += photo_h + 56

    # -- bullets
    for bl in bullet_lines:
        d.ellipse((MARGIN + 4, y + 14, MARGIN + 16, y + 26), fill=SAGE)
        for ln in bl:
            d.text((MARGIN + 46, y), ln, font=b_f, fill=INK)
            y += 42
        y += 26
    y -= 26

    # -- footer
    y += 30
    d.line((MARGIN, y, PIN_W - MARGIN, y), fill=(35, 37, 29, 40), width=1)
    y += 26
    paste_logo(canvas, LOGO_DARK, 30, MARGIN, y)
    url_f = mono(22)
    url = "santavila.com"
    d.text((PIN_W - MARGIN - text_w(d, url, url_f), y + 4), url, font=url_f, fill=SAGE)

    out = os.path.join(OUT_PINS, f"pin-{spec['slug']}.png")
    canvas.save(out)
    return out


# ---------------------------------------------------------- Carruseles IG

IG_W, IG_H = 1080, 1350
IG_M = 96

CAROUSELS = [
    {
        "dirname": "carrusel-01",
        "cover_image": "images_generated/tumbona/02_ambiente_costero.jpg",
        "cover_title": "Qué muebles de exterior aguantan mejor lluvia y sol",
        "slides": [
            ("02", "Aluminio lacado", "Ligero y resistente si el acabado es apto exterior."),
            ("03", "Resina y polipropileno", "Prácticos para piscina y limpieza frecuente."),
            ("04", "Madera", "Cálida, pero pide mantenimiento y buen secado."),
        ],
        "avoid": ("05", "Evita", [
            "Guardar cojines húmedos",
            "Fundas sobre muebles sucios",
            "Tornillería expuesta sin revisar",
        ]),
        "close_image": "images_generated/leisa/02_ambiente_costero_v2.jpg",
        "close_body": "Comparativa de materiales, medidas y mantenimiento para elegir con calma.",
    },
    {
        "dirname": "carrusel-02",
        "cover_image": "images_generated/rinconera/02_ambiente_exterior_costablanca.jpg",
        "cover_title": "Aluminio, resina, HPL o madera: qué elegir",
        "slides": [
            ("02", "Sol directo", "Busca acabados aptos exterior y color estable."),
            ("03", "Piscina", "Prioriza limpieza fácil y buena resistencia a humedad."),
            ("04", "Costa", "Atención a salitre, tornillería y herrajes."),
            ("05", "Calidez visual", "Madera o acabados naturales, con mantenimiento realista."),
        ],
        "close_image": "images_generated/manhattan2p/02_ambiente_exterior_pirineo.jpg",
        "close_body": "Compara aluminio, resina, HPL y madera antes de decidir.",
    },
    {
        "dirname": "carrusel-03",
        "cover_image": "content/images/blog/mantenimiento-tumbona-piscina-cubierta-20260629.png",
        "cover_title": "Checklist de mantenimiento exterior",
        "slides": [
            ("02", "Limpieza suave", "Antes de guardar o cubrir los muebles."),
            ("03", "Secado", "Seca los textiles y evita la humedad retenida."),
            ("04", "Revisión", "Tornillos, ruedas, patas y mecanismos."),
            ("05", "Sin abrasivos", "Ni presión alta sobre acabados delicados."),
        ],
        "close_image": "images_generated/brandon/02_ambiente_exterior_cantabria.jpg",
        "close_body": "Guarda esta checklist para cada cambio de temporada.",
    },
    {
        "dirname": "carrusel-04",
        "cover_image": "images_generated/acapulco2p/02_ambiente_exterior_azotea_salamanca.jpg",
        "cover_title": "Cómo amueblar una terraza pequeña",
        "slides": [
            ("02", "Mide primero", "El paso libre manda antes de elegir mesa."),
            ("03", "Plegables o apilables", "Ayudan si el espacio cambia de uso."),
            ("04", "Piensa en vertical", "Bancos y almacenaje vertical liberan suelo."),
            ("05", "Evita", "Muebles demasiado profundos que se comen la terraza."),
        ],
        "close_image": "images_generated/yina/02_ambiente_exterior_porxada.jpg",
        "close_body": "Medidas, distribución y errores a evitar en balcones y terrazas.",
    },
    {
        "dirname": "carrusel-05",
        "cover_image": "images_balliu/Atlanta_Silla-Etna_blanco2.jpg",
        "cover_title": "Mesa de exterior: cuántas personas caben de verdad",
        "slides": [
            ("02", "2 personas", "Prioriza paso y sillas fáciles de mover."),
            ("03", "4 personas", "Ojo con brazos y ancho real de sillas."),
            ("04", "6-8 personas", "Calcula la circulación alrededor."),
            ("05", "La forma importa", "Redonda, rectangular o extensible: depende del espacio."),
        ],
        "close_image": "images_generated/sidney/02_ambiente_exterior_alpujarra.jpg",
        "close_body": "Medidas por comensales y espacio real necesario.",
    },
    {
        "dirname": "carrusel-06",
        "cover_image": "images_balliu/Tumbona-Etna_Mesa-auxiliar-Etna_C.jpg",
        "cover_title": "Tumbona de aluminio, resina o madera",
        "slides": [
            ("02", "Aluminio", "Ligero y fácil de mover."),
            ("03", "Resina", "Práctica para piscina y limpieza frecuente."),
            ("04", "Madera", "Más cálida, pero exige más cuidado."),
            ("05", "Los detalles", "Revisa ruedas, respaldo, textiles y tornillería."),
        ],
        "close_image": "images_generated/balinesa/02_ambiente_exterior_mallorca.jpg",
        "close_body": "Comparativa por material, peso y mantenimiento.",
    },
    {
        "dirname": "carrusel-07",
        "cover_image": "images_generated/leisa/03_ambiente_madrid_noble.jpg",
        "cover_title": "Cómo montar un chill out en tu terraza",
        "slides": [
            ("02", "Mide primero", "Deja 60-70 cm de paso libre donde circulas."),
            ("03", "La pieza protagonista", "Sofá, set de jardín o cama balinesa: elige una."),
            ("04", "Mesa baja y sombra", "Mesa a la altura del asiento, parasol o pérgola."),
        ],
        "avoid": ("05", "Evita", [
            "Llenar la terraza de piezas",
            "Muebles que bloquean el paso",
            "Cojines fuera todo el invierno",
        ]),
        "close_image": "images_generated/balinesa/02_ambiente_exterior_mallorca.jpg",
        "close_body": "Ideas, medidas y composiciones para montar tu chill out.",
    },
    {
        "dirname": "carrusel-08",
        "cover_image": "images_generated/parasol_roma/02_ambiente_terraza.jpg",
        "cover_title": "Qué base necesita tu parasol",
        "slides": [
            ("02", "Hasta Ø200 cm", "Desde 25 kg en terraza protegida."),
            ("03", "Ø250-300 cm", "40 kg o más: cuanta más tela, más vela."),
            ("04", "Excéntrico", "Losas de lastre sobre la cruceta, no una base central."),
        ],
        "avoid": ("05", "Evita", [
            "Dejarlo abierto sin vigilancia",
            "Mástil que baila en la base",
            "Bases caseras mal repartidas",
        ]),
        "close_image": "images_generated/pergola/03_bajo_la_pergola.jpg",
        "close_body": "Pesos por diámetro, tipos de base y tubo compatible.",
    },
]


def ig_canvas():
    return Image.new("RGB", (IG_W, IG_H), PAPER)


def slide_cover(c):
    canvas = ig_canvas()
    photo = cover(Image.open(os.path.join(ROOT, c["cover_image"])).convert("RGB"), IG_W, IG_H)
    canvas.paste(photo, (0, 0))
    # gradiente inferior para legibilidad
    grad = Image.new("L", (1, IG_H), 0)
    for i in range(IG_H):
        grad.putpixel((0, i), min(200, max(0, int((i - IG_H * 0.45) / (IG_H * 0.55) * 210))))
    overlay = Image.new("RGB", (IG_W, IG_H), (18, 20, 15))
    canvas.paste(overlay, (0, 0), grad.resize((IG_W, IG_H)))

    d = ImageDraw.Draw(canvas)
    paste_logo(canvas, LOGO_WHITE, 34, IG_M, 84)
    y = IG_H - 96
    hint_f = mono(24)
    d.text((IG_M, y), "Desliza →", font=hint_f, fill=(237, 230, 222))
    t_f = serif(84)
    lines = wrap(d, c["cover_title"], t_f, IG_W - 2 * IG_M)
    ty = y - 40 - len(lines) * 90
    eb_f = mono(24)
    draw_tracked(d, (IG_M, ty - 46), "GUÍA DE EXTERIOR", eb_f, (237, 230, 222), tracking=8)
    for ln in lines:
        d.text((IG_M, ty), ln, font=t_f, fill=(255, 255, 255))
        ty += 90
    return canvas


def slide_statement(num, head, body):
    canvas = ig_canvas()
    d = ImageDraw.Draw(canvas)
    paste_logo(canvas, LOGO_DARK, 30, IG_M, 84)
    num_f = mono(26)
    d.text((IG_W - IG_M - text_w(d, f"{num} / 06", num_f), 86), f"{num} / 06", font=num_f, fill=SAGE)

    # barra de acento
    d.rectangle((IG_M, 470, IG_M + 8, 470 + 96), fill=SAGE)
    h_f = serif(92)
    y = 440
    for ln in wrap(d, head, h_f, IG_W - 2 * IG_M - 40):
        d.text((IG_M + 44, y), ln, font=h_f, fill=INK)
        y += 100
    y += 28
    b_f = sans(38, "Regular")
    for ln in wrap(d, body, b_f, IG_W - 2 * IG_M - 44):
        d.text((IG_M + 44, y), ln, font=b_f, fill=(90, 93, 80))
        y += 52

    d.text((IG_M, IG_H - 110), "santavila.com", font=mono(24), fill=SAGE)
    return canvas


def slide_avoid(c):
    num, head, items = c["avoid"]
    canvas = ig_canvas()
    d = ImageDraw.Draw(canvas)
    paste_logo(canvas, LOGO_DARK, 30, IG_M, 84)
    num_f = mono(26)
    d.text((IG_W - IG_M - text_w(d, f"{num} / 06", num_f), 86), f"{num} / 06", font=num_f, fill=SAGE)

    d.rectangle((IG_M, 388, IG_M + 8, 388 + 96), fill=SAGE)
    d.text((IG_M + 44, 360), head, font=serif(92), fill=INK)
    y = 530
    b_f = sans(40, "Regular")
    for it in items:
        # aspa dibujada (Hanken no tiene el glifo ✕)
        cx, cy, r = IG_M + 58, y + 26, 12
        d.line((cx - r, cy - r, cx + r, cy + r), fill=SAGE, width=5)
        d.line((cx - r, cy + r, cx + r, cy - r), fill=SAGE, width=5)
        for ln in wrap(d, it, b_f, IG_W - 2 * IG_M - 120):
            d.text((IG_M + 110, y), ln, font=b_f, fill=INK)
            y += 54
        y += 40
    d.text((IG_M, IG_H - 110), "santavila.com", font=mono(24), fill=SAGE)
    return canvas


def slide_close(c):
    canvas = ig_canvas()
    photo_h = 700
    photo = cover(Image.open(os.path.join(ROOT, c["close_image"])).convert("RGB"), IG_W, photo_h)
    canvas.paste(photo, (0, 0))
    d = ImageDraw.Draw(canvas)
    y = photo_h + 90
    eb_f = mono(24)
    draw_tracked(d, (IG_M, y), "GUÍA COMPLETA EN", eb_f, SAGE, tracking=8)
    y += 24 + 26
    t_f = serif(88)
    d.text((IG_M, y), "santavila.com", font=t_f, fill=INK)
    y += 130
    b_f = sans(34, "Regular")
    for ln in wrap(d, c["close_body"], b_f, IG_W - 2 * IG_M):
        d.text((IG_M, y), ln, font=b_f, fill=(90, 93, 80))
        y += 48
    paste_logo(canvas, LOGO_DARK, 34, IG_M, IG_H - 120)
    return canvas


def main():
    os.makedirs(OUT_PINS, exist_ok=True)

    for spec in PINS:
        print("pin ->", compose_pin(spec))

    for c in CAROUSELS:
        out_dir = os.path.join(OUT_IG_BASE, c["dirname"])
        os.makedirs(out_dir, exist_ok=True)
        slides = [slide_cover(c)]
        for num, head, body in c["slides"]:
            slides.append(slide_statement(num, head, body))
        if "avoid" in c:
            slides.append(slide_avoid(c))
        slides.append(slide_close(c))
        for i, s in enumerate(slides, 1):
            out = os.path.join(out_dir, f"slide-{i:02d}.png")
            s.save(out)
            print("slide ->", out)


if __name__ == "__main__":
    main()
