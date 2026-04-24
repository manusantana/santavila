#!/usr/bin/env python3
"""
Convierte el CSV de productos al formato de importación de Shopify.
Genera títulos SEO descriptivos (sin nombres de colección) y descripciones enriquecidas.
"""

import csv
import re
import unicodedata

INPUT_FILE = "▶️CSV para clientes  Agrupación - ▶️CSV para clientes  Agrupación.csv"
OUTPUT_FILE = "shopify_products.csv"
VENDOR = "Muebles Exterior"

# Regex que detecta todos los nombres de colección/modelo del proveedor
# Formato: NOMBRE opcionalmente seguido de -XL, -NUM o NUM
_COLLECTION_RE = re.compile(
    r'\b('
    r'BRANDON|DAMASCO|LUNA|YINA|CUPRA|BELLAGIO|CLOE|ODIN|SAIPROS|'
    r'ALBANIA|BOLONIA(?:\s*XL)?|DIVA|LEISA|DOUNVIL|HASTON|ACAPULCO|'
    r'MANHATAN|LOIRA|ADEL|C[ÓO]RCEGA|JANEIRO|MUNDRA|AVALON|BRESCIA|'
    r'VENECIA|VIENA|SAMSON|CARACAS|SIDNEY|YULIEN|GULLIVER|SEVILLA|'
    r'UNIVERSAL|STANDARD|GRANITE'
    r')(?:[-\s](?:XL|\d+))?',
    re.IGNORECASE,
)


def clean_description(text):
    """Elimina nombres de colección del proveedor del texto de descripción."""
    if not text:
        return text
    cleaned = _COLLECTION_RE.sub("", text)
    cleaned = re.sub(r"  +", " ", cleaned)        # espacios dobles
    cleaned = re.sub(r" ([.,;:])", r"\1", cleaned)  # espacio antes de puntuación
    return cleaned.strip()


# ─────────────────────────────────────────────
# Utilidades
# ─────────────────────────────────────────────

def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def parse_price(price_str):
    if not price_str:
        return ""
    cleaned = price_str.replace("€", "").replace(" ", "").replace("Ø", "")
    cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        return f"{float(cleaned):.2f}"
    except ValueError:
        return ""


def clean_dim(val):
    """Extrae solo el número de una dimensión (ej: '300Ø' → '300')."""
    return re.sub(r"[^\d.]", "", val) if val else ""


def dim_str(w, h):
    """Retorna 'W×H cm' si ambos valores existen."""
    cw, ch = clean_dim(w), clean_dim(h)
    if cw and ch:
        return f"{cw}×{ch} cm"
    if cw:
        return f"{cw} cm"
    return ""


def ensure_unique(value, used_set):
    original = value
    counter = 2
    while value in used_set:
        value = f"{original} {counter}"
        counter += 1
    used_set.add(value)
    return value


# ─────────────────────────────────────────────
# Clasificación del producto
# ─────────────────────────────────────────────

def get_product_type(name):
    n = name.upper()
    if "PERGOLA" in n or "PÉRGOLA" in n:
        return "Pérgola"
    if "PARASOL" in n and "BASE" not in n:
        return "Parasol"
    if "BASE DE PARASOL" in n or "LOSAS" in n:
        return "Accesorios"
    if "TUMBONA" in n or "SUNBED" in n:
        return "Tumbona"
    if "BALANCIN" in n or "BALANCÍN" in n:
        return "Balancín"
    if "BANCO" in n and ("MESA" in n or "TABLE" in n):
        return "Banco con mesa"
    if "BANCO" in n or "BENCH" in n:
        return "Banco"
    if "SET" in n and ("RINCONERA" in n or "CORNER" in n):
        return "Conjunto rinconera"
    if "SET" in n:
        return "Conjunto sofá"
    if "MESA COMEDOR" in n or "DINING TABLE" in n:
        return "Mesa comedor"
    if "MESA" in n and ("CENTRO" in n or "COFFEE" in n):
        return "Mesa centro"
    if ("MESA" in n or "TABLE" in n) and "HPL" in n:
        return "Mesa comedor"
    if "REPOSAPIES" in n or "REPOSAPIÉS" in n or "FOOTSTOOL" in n:
        return "Reposapiés"
    if "SILLON" in n or "SILLÓN" in n or "ARMCHAIR" in n:
        return "Sillón"
    if "SOFA" in n or "SOFÁ" in n:
        return "Sofá"
    if "SILLA" in n or "CHAIR" in n:
        return "Silla"
    return "Muebles exterior"


def detect_material(description, name):
    """Detecta el material principal solo cuando está mencionado explícitamente."""
    d = (description or "").lower()
    n = name.upper()
    if "HPL" in n:
        return "HPL"
    if "BICOLOR" in n:
        return "bicolor"
    if "aluminio" in d:
        return "aluminio"
    return ""


def detect_capacity(name):
    n = name.upper()
    if "2 PLAZAS" in n or "2 SEATER" in n:
        return "2 plazas"
    if "3 PLAZAS" in n or "3 SEATER" in n:
        return "3 plazas"
    return ""


def extract_style(description, name):
    """
    Extrae el adjetivo de diseño más representativo de la descripción.
    Orden de prioridad: de lo más específico a lo más genérico.
    """
    if not description:
        return "contemporáneo"
    d = description.lower()
    n = name.upper()

    if "bicolor" in d or "BICOLOR" in n or "doble tonalidad" in d:
        return "bicolor"
    if "envolvente" in d:
        return "envolvente"
    if "urbano" in d:
        return "urbano"
    if "minimalista" in d:
        return "minimalista"
    if "ligereza" in d or ("estilizad" in d and "sofisticad" not in d):
        return "estilizado"
    if "sofisticad" in d:
        return "sofisticado"
    if "elegant" in d:
        return "elegante"
    if "versátil" in d or "versatil" in d:
        return "versátil"
    if "contemporáneo" in d or "contemporanea" in d:
        return "contemporáneo"
    if "moderno" in d or "moderna" in d:
        return "moderno"
    if "ligero" in d:
        return "ligero"
    return "contemporáneo"


# ─────────────────────────────────────────────
# Generación del título SEO
# ─────────────────────────────────────────────

def build_seo_title(name, product_type, style, material, width, depth, height):
    """
    Genera un título SEO descriptivo sin nombres de colección.
    Formato general: [Tipo] [uso] [material] [capacidad] · [estilo] | [dimensiones]
    """
    n = name.upper()
    capacity = detect_capacity(name)
    mat = f" {material}" if material else ""
    cw, cd, ch = clean_dim(width), clean_dim(depth), clean_dim(height)

    if product_type == "Sillón":
        title = f"Sillón exterior{mat} · estilo {style}"
        d = dim_str(width, height)
        if d:
            title += f" | {d}"

    elif product_type == "Sofá":
        title = f"Sofá terraza{mat}"
        if capacity:
            title += f" {capacity}"
        title += f" · estilo {style}"
        d = dim_str(width, height)
        if d:
            title += f" | {d}"

    elif product_type == "Conjunto sofá":
        title = f"Set jardín{mat}"
        if capacity:
            title += f" {capacity}"
        title += f" · {style}"
        comp = "sofá 3 plazas" if "3 PLAZAS" in n or "3 SEATER" in n else "sofá 2 plazas"
        title += f" | {comp} + 2 sillones + mesa"

    elif product_type == "Conjunto rinconera":
        title = f"Set rinconera exterior{mat} · {style}"
        title += " | sofá de esquina + mesa de centro"

    elif product_type == "Mesa centro":
        title = "Mesa de centro exterior"
        if "HPL" in n:
            title += " HPL"
        if cw:
            title += f" {cw} cm"
        if ch:
            title += f" · altura {ch} cm"

    elif product_type == "Mesa comedor":
        title = "Mesa comedor exterior"
        if "HPL" in n:
            title += " HPL"
        if cw and cd:
            title += f" {cw}×{cd} cm"

    elif product_type == "Reposapiés":
        title = f"Reposapiés exterior{mat}"
        parts = [x for x in [cw, cd, ch] if x]
        if parts:
            title += f" · {'×'.join(parts)} cm"

    elif product_type == "Silla":
        title = f"Silla exterior{mat} · estilo {style}"

    elif product_type == "Tumbona":
        title = "Tumbona de exterior"

    elif product_type == "Balancín":
        title = "Balancín jardín exterior"
        if cw and cd:
            title += f" · {cw}×{cd} cm"

    elif product_type == "Banco con mesa":
        title = "Banco jardín con mesa integrada"
        if cw:
            title += f" · {cw} cm"

    elif product_type == "Banco":
        title = "Banco de exterior"
        if cw:
            title += f" {cw} cm"

    elif product_type == "Pérgola":
        title = "Pérgola aluminio para jardín"
        parts = [x for x in [cw, cd, ch] if x]
        if parts:
            title += f" · {'×'.join(parts)} cm"

    elif product_type == "Parasol":
        title = "Parasol para terraza"
        raw_w = width or ""
        is_diameter = "Ø" in raw_w or (cw and int(cw) >= 200)
        if cw:
            title += f" Ø{cw} cm" if is_diameter else f" {cw} cm"

    elif product_type == "Accesorios":
        if "25KG" in n or "25 KG" in n or "25KG" in name.upper():
            title = "Base de parasol 25 kg"
        elif "LOSAS" in n or "LOSA" in n:
            title = "Set losas cemento para base de parasol"
        else:
            title = "Accesorio para exterior"

    else:
        title = f"Mobiliario exterior · estilo {style}"

    return title


# ─────────────────────────────────────────────
# Descripción enriquecida
# ─────────────────────────────────────────────

def build_rich_description(description, name, product_type, width, depth, height, material):
    """
    Construye una descripción HTML con:
    1. Párrafo principal (texto original)
    2. Lista de características clave (auto-generada)
    3. Bloque de dimensiones
    """
    parts = []
    n = name.upper()
    d = (description or "").lower()
    capacity = detect_capacity(name)
    cw, cd, ch = clean_dim(width), clean_dim(depth), clean_dim(height)

    # ── 1. Párrafo principal ──────────────────
    if description:
        parts.append(f"<p>{description}</p>")

    # ── 2. Características ────────────────────
    features = []

    # Estructura / material
    if material == "aluminio" or "aluminio" in d:
        features.append(
            "Estructura en <strong>aluminio termo-lacado</strong>: ligera, resistente a la "
            "corrosión y duradera sin mantenimiento especial"
        )
    if material == "HPL" or "HPL" in n:
        features.append(
            "Tablero en <strong>HPL de alta presión</strong>: resiste humedad, rayos UV y "
            "uso intensivo — fácil de limpiar con agua y jabón"
        )
    if material == "bicolor" or "bicolor" in d or "doble tonalidad" in d:
        features.append(
            "Acabado <strong>bicolor</strong>: combinación cromática que aporta personalidad "
            "y un toque de sofisticación al espacio exterior"
        )

    # Cojines
    if "cojines" in d or "cojin" in d:
        if "alta densidad" in d:
            features.append(
                "Cojines de <strong>espuma de alta densidad</strong> con tapizado técnico "
                "resistente a la intemperie y de fácil mantenimiento"
            )
        else:
            features.append(
                "Cojines con <strong>tapizado técnico para exterior</strong>, "
                "resistentes a la intemperie"
            )

    # Resistencia exterior
    if product_type not in ["Accesorios"]:
        features.append(
            "Resistente a <strong>rayos UV, lluvia y humedad</strong> — "
            "preparado para exterior durante todo el año"
        )

    # Mantenimiento
    if product_type not in ["Accesorios", "Parasol", "Pérgola"]:
        features.append(
            "Mantenimiento mínimo: no requiere tratamientos ni almacenamiento en invierno"
        )

    # Composición set
    if product_type == "Conjunto sofá":
        comp = "sofá 3 plazas" if "3 PLAZAS" in n or "3 SEATER" in n else "sofá 2 plazas"
        features.append(
            f"Composición completa: <strong>{comp} + 2 sillones + mesa de centro</strong> "
            "(todo incluido en el precio, listo para montar)"
        )
    if product_type == "Conjunto rinconera":
        features.append(
            "Composición: <strong>módulos de rinconera + mesa de centro</strong> — "
            "aprovecha al máximo esquinas y terrazas grandes"
        )

    # Set de mesas
    if "SET MESAS" in n:
        features.append(
            "Set de <strong>dos mesas de centro</strong> de distintas alturas — "
            "superponibles o usables de forma independiente"
        )

    # Hostelería y contract
    if product_type in ["Conjunto sofá", "Conjunto rinconera", "Sillón", "Sofá"]:
        features.append(
            "Apto para uso residencial y proyectos de "
            "<strong>hostelería y contract</strong> "
            "(hoteles, restaurantes, terrazas de establecimientos)"
        )

    # Transporte y montaje
    if product_type not in ["Pérgola", "Accesorios"]:
        features.append(
            "Transporte sencillo y <strong>montaje sin herramientas especiales</strong>"
        )

    if features:
        items = "\n".join(f"  <li>{f}</li>" for f in features)
        parts.append(f"<ul>\n{items}\n</ul>")

    # ── 3. Dimensiones ────────────────────────
    dims = []
    raw_w = width or ""
    if cw:
        label = "Diámetro" if ("Ø" in raw_w or (cw and cw.isdigit() and int(cw) >= 200)) else "Ancho"
        dims.append(f"{label}: {cw} cm")
    if cd:
        dims.append(f"Fondo: {cd} cm")
    if ch:
        dims.append(f"Alto: {ch} cm")

    if dims:
        dims_html = " &nbsp;|&nbsp; ".join(dims)
        parts.append(f'<p><strong>Dimensiones:</strong> {dims_html}</p>')

    return "\n".join(parts)


# ─────────────────────────────────────────────
# Tags
# ─────────────────────────────────────────────

def get_tags(name, product_type, material):
    tags = ["exterior", "terraza", "jardín"]
    n = name.upper()
    if product_type:
        tags.append(product_type.lower())
    if material:
        tags.append(material)
    if "HPL" in n:
        tags.append("HPL")
    if "BICOLOR" in n:
        tags.append("bicolor")
    if "2 PLAZAS" in n or "2 SEATER" in n:
        tags.append("2 plazas")
    elif "3 PLAZAS" in n or "3 SEATER" in n:
        tags.append("3 plazas")
    if product_type in ["Conjunto sofá", "Conjunto rinconera", "Sillón", "Sofá"]:
        tags.append("hostelería")
    return ", ".join(dict.fromkeys(tags))


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

SHOPIFY_HEADERS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags",
    "Published", "Option1 Name", "Option1 Value", "Variant SKU", "Variant Grams",
    "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
    "Variant Requires Shipping", "Variant Taxable", "Image Src", "Image Position",
    "Image Alt Text", "Gift Card", "SEO Title", "SEO Description", "Status", "Cost per item",
]


def main():
    used_handles = set()
    used_titles = set()
    output_rows = []

    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # saltar cabecera

        for row in reader:
            if len(row) < 2 or not row[0].strip():
                continue

            sku         = row[0].strip()
            name_raw    = row[1].strip() if len(row) > 1 else ""
            precio_neto = row[2].strip() if len(row) > 2 else ""
            precio_venta= row[3].strip() if len(row) > 3 else ""
            pvp         = row[8].strip() if len(row) > 8 else ""
            descripcion = clean_description(row[9].strip() if len(row) > 9 else "")
            ancho       = row[10].strip() if len(row) > 10 else ""
            fondo       = row[11].strip() if len(row) > 11 else ""
            alto        = row[12].strip() if len(row) > 12 else ""
            imagen      = row[13].strip() if len(row) > 13 else ""

            if not name_raw:
                continue

            product_type = get_product_type(name_raw)
            material     = detect_material(descripcion, name_raw)
            style        = extract_style(descripcion, name_raw)

            title = build_seo_title(name_raw, product_type, style, material, ancho, fondo, alto)
            title = ensure_unique(title, used_titles)

            handle = slugify(title)
            handle = ensure_unique(handle, used_handles)

            body_html = build_rich_description(
                descripcion, name_raw, product_type, ancho, fondo, alto, material
            )
            tags = get_tags(name_raw, product_type, material)

            shopify_row = {
                "Handle":                    handle,
                "Title":                     title,
                "Body (HTML)":               body_html,
                "Vendor":                    VENDOR,
                "Product Category":          "",
                "Type":                      product_type,
                "Tags":                      tags,
                "Published":                 "TRUE",
                "Option1 Name":              "Title",
                "Option1 Value":             "Default Title",
                "Variant SKU":               sku,
                "Variant Grams":             "0",
                "Variant Inventory Tracker": "shopify",
                "Variant Inventory Qty":     "10",
                "Variant Inventory Policy":  "deny",
                "Variant Fulfillment Service": "manual",
                "Variant Price":             parse_price(precio_venta),
                "Variant Compare At Price":  parse_price(pvp),
                "Variant Requires Shipping": "TRUE",
                "Variant Taxable":           "TRUE",
                "Image Src":                 imagen,
                "Image Position":            "1",
                "Image Alt Text":            title,
                "Gift Card":                 "FALSE",
                "SEO Title":                 title[:70],
                "SEO Description":           descripcion[:320] if descripcion else "",
                "Status":                    "active",
                "Cost per item":             parse_price(precio_neto),
            }

            output_rows.append(shopify_row)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SHOPIFY_HEADERS)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"✓ {len(output_rows)} productos exportados → {OUTPUT_FILE}\n")
    print(f"{'SKU':<16} {'Tipo':<22} {'Título'}")
    print("─" * 90)
    for row in output_rows:
        print(f"{row['Variant SKU']:<16} {row['Type']:<22} {row['Title']}")


if __name__ == "__main__":
    main()
