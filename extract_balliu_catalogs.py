#!/usr/bin/env python3
"""
Extract Balliu catalog data from PDFs and web pages into a Shopify-ready CSV.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import fitz
import pandas as pd
import requests
from bs4 import BeautifulSoup


SHOPIFY_HEADERS = [
    "Handle",
    "Title",
    "Body (HTML)",
    "Vendor",
    "Product Category",
    "Type",
    "Tags",
    "Published",
    "Option1 Name",
    "Option1 Value",
    "Variant SKU",
    "Variant Grams",
    "Variant Inventory Tracker",
    "Variant Inventory Qty",
    "Variant Inventory Policy",
    "Variant Fulfillment Service",
    "Variant Price",
    "Variant Compare At Price",
    "Variant Requires Shipping",
    "Variant Taxable",
    "Image Src",
    "Image Position",
    "Image Alt Text",
    "Gift Card",
    "SEO Title",
    "SEO Description",
    "Status",
    "Cost per item",
]

SUMMARY_HEADERS = [
    "SKU",
    "Producto",
    "Precio neto exworks sin iva",
    "Precio Venta",
    "Margen €",
    "Margen%",
    "Coste de Envio",
    "",
    "PVP Recomendado",
    "Descripción",
    "Ancho (cm)",
    "Fondo (cm)",
    "Alto (cm)",
    "Imagen",
    "Proveedor",
    "Match %",
    "Color Match",
    "Detalle Match",
]

SPANISH_HINTS = {
    "de",
    "la",
    "el",
    "los",
    "las",
    "para",
    "con",
    "una",
    "un",
    "su",
    "sus",
    "que",
    "ofrece",
    "ideal",
    "disenada",
    "disenado",
    "fabricada",
    "fabricado",
}

GENERIC_MATCH_TOKENS = {
    "balliu",
    "producto",
    "productos",
    "muebles",
    "exterior",
    "para",
    "con",
    "sin",
    "de",
    "del",
    "la",
    "el",
    "los",
    "las",
    "apilable",
    "alta",
    "mini",
    "pack",
    "cm",
    "kg",
    "tela",
    "color",
}

TYPE_STOPWORDS = {
    "tumbona",
    "mini",
    "silla",
    "mesa",
    "sofa",
    "parasol",
    "cama",
    "balinesa",
    "auxiliar",
    "funda",
    "base",
    "hormigon",
    "cojin",
    "colchoneta",
    "pasarela",
    "limpiador",
    "central",
    "lateral",
}

VARIANT_STARTERS = (
    "chasis",
    "sin ",
    "con ",
    "tela",
    "taburete",
    "blanca",
    "blanco",
    "negra",
    "negro",
    "color",
    "tablero",
    "diam",
    "diametro",
    "individual",
    "doble",
    "triple",
    "central",
    "esquinera",
    "parasol",
    "sofa",
    "12 unidades",
    "24 unidades",
)

VARIANT_MARKER_PREFIXES = (
    "chasis",
    "sin ruedas",
    "con ruedas",
    "tela",
    "taburete",
    "blanca",
    "blanco",
    "negra",
    "negro",
    "color",
    "tablero",
    "diam",
    "diametro",
    "individual",
    "doble",
    "triple",
    "central",
    "esquinera",
    "acrilico",
    "acrílico",
    "sofa individual",
    "sofa doble",
    "sofa triple",
    "12 unidades",
    "24 unidades",
)

PRODUCT_BOUNDARY_PATTERNS = [
    "cama balinesa",
    "mini tumbona",
    "tumbona apilable",
    "tumbona alta",
    "mesa auxiliar",
    "auxiliar mesa",
    "silla con brazos",
    "silla",
    "mesa",
    "tumbona",
    "sofa",
    "parasol",
    "funda tumbona",
    "funda parasol",
    "funda sofa",
    "funda silla",
    "base hormigon",
    "pie parasol",
    "caja seguridad",
    "colchoneta",
    "cojin",
    "pasarela",
    "limpiador",
]

EXTRA_KNOWN_TITLES = [
    "Pamela Parasol",
    "Ocean Parasol",
    "Agora Parasol",
    "Parasol Brisa",
    "Parasol Garbí Central",
    "Parasol Roma Lateral",
    "Colchoneta Tumbona",
    "Caja Seguridad Weguard",
    "Pie Parasol 40 kg",
    "Pie Parasol 40 kg Recubrimiento Plastico",
    "Base Hormigón 25 Kg",
    "Base Hormigón 30 Kg",
    "Funda Tumbona",
    "Funda Parasol",
    "Funda sofá",
    "Funda Silla",
    "Cojin 40X40",
    "Producto Limpiador",
    "Pasarela Resina Reciclada 100 %",
    "Pasarela Resina",
]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)

PRICE_RE = re.compile(r"^(?P<body>.+?)\s+(?P<group>G\d)\s+(?P<price>\d[\d.,]*)\s*€$")
WHITESPACE_RE = re.compile(r"\s+")


@dataclass
class CatalogEntry:
    title: str
    page: int
    description_paragraphs: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    normalized_title: str = ""
    tokens: set[str] = field(default_factory=set)
    key_tokens: set[str] = field(default_factory=set)


@dataclass
class TariffRow:
    product_name: str
    variant_name: str
    group: str
    price: float
    page: int
    order_index: int
    source_text: str


@dataclass
class WebCandidate:
    url: str
    slug_text: str
    tokens: set[str]
    key_tokens: set[str]


def ascii_fold(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    return value.encode("ascii", "ignore").decode("ascii")


def normalize_text(value: str) -> str:
    value = ascii_fold(value).lower()
    value = re.sub(r"[^a-z0-9/]+", " ", value)
    return WHITESPACE_RE.sub(" ", value).strip()


def slugify(value: str) -> str:
    value = normalize_text(value).replace("/", "-")
    value = re.sub(r"[^a-z0-9 -]", "", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def clean_text(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value or "").strip()


def tokenize(value: str) -> set[str]:
    return {token for token in normalize_text(value).split() if token}


def key_tokens(value: str) -> set[str]:
    tokens = tokenize(value)
    return {
        token
        for token in tokens
        if token not in GENERIC_MATCH_TOKENS
        and token not in TYPE_STOPWORDS
        and not token.isdigit()
    }


def looks_spanish(value: str) -> bool:
    tokens = tokenize(value)
    return sum(1 for token in tokens if token in SPANISH_HINTS) >= 2


def strip_bilingual_segment(value: str) -> str:
    value = clean_text(value)
    if "•" in value:
        value = value.split("•", 1)[0]
    if "·" in value:
        value = value.split("·", 1)[0]
    value = value.replace("(", " ").replace(")", " ")
    return clean_text(value)


def parse_price(value: str) -> float:
    cleaned = value.replace(".", "").replace(",", ".")
    return float(cleaned)


def format_price(value: float) -> str:
    return f"{value:.2f}"


def format_eur_es(value: float | None) -> str:
    if value is None:
        return ""
    amount = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{amount} €"


def stable_sku(product_name: str, variant_name: str) -> str:
    raw = f"{product_name}::{variant_name}".strip()
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:8].upper()
    base = slugify(product_name).upper().replace("-", "_")[:20]
    variant = slugify(variant_name).upper().replace("-", "_")[:16]
    if variant and variant != "DEFAULT_TITLE":
        return f"BALLIU_{base}_{variant}_{digest}"
    return f"BALLIU_{base}_{digest}"


def score_candidate(name: str, candidate_text: str, candidate_tokens: set[str], candidate_key_tokens: set[str]) -> float:
    name_tokens = tokenize(name)
    name_key_tokens = key_tokens(name)
    if not name_tokens or not candidate_tokens:
        return 0.0

    all_intersection = len(name_tokens & candidate_tokens)
    all_union = len(name_tokens | candidate_tokens)
    key_intersection = len(name_key_tokens & candidate_key_tokens)
    key_union = len(name_key_tokens | candidate_key_tokens) or 1

    score = 30 * (all_intersection / all_union)
    if name_key_tokens or candidate_key_tokens:
        score += 60 * (key_intersection / key_union)
    normalized_name = normalize_text(name)
    normalized_candidate = normalize_text(candidate_text)
    if normalized_name == normalized_candidate:
        score += 50
    if name_key_tokens and name_key_tokens.issubset(candidate_key_tokens):
        score += 10
    if candidate_key_tokens and candidate_key_tokens.issubset(name_key_tokens):
        score += 10
    if name_tokens & {"tumbona", "silla", "mesa", "parasol", "sofa"} and candidate_tokens & name_tokens:
        score += 5
    return score


def choose_best_match(name: str, candidates: list[dict[str, Any]], threshold: float = 35.0) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    best_score = 0.0
    for candidate in candidates:
        score = score_candidate(
            name,
            candidate["title"],
            candidate["tokens"],
            candidate["key_tokens"],
        )
        if score > best_score:
            best_score = score
            best = candidate
    if best_score < threshold:
        return None
    return {**best, "_score": round(best_score, 2)}


def build_requests_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def parse_catalog_pdf(path: Path) -> list[CatalogEntry]:
    pdf = fitz.open(path)
    entries: list[CatalogEntry] = []

    for page_number, page in enumerate(pdf, start=1):
        blocks = []
        for block in page.get_text("blocks", sort=True):
            x0, y0, x1, y1, text, *_ = block
            text = clean_text(text)
            if not text:
                continue
            blocks.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1, "text": text})

        title_parts: list[str] = []
        for block in blocks:
            if block["x0"] >= 130 or block["y0"] >= 110:
                continue
            text = strip_bilingual_segment(block["text"])
            if not text or text.isdigit():
                continue
            if re.fullmatch(r"\d+[,.]?\d*\s*kg", normalize_text(text)):
                continue
            if "dimensiones" in normalize_text(text):
                continue
            title_parts.append(text)
            if len(title_parts) >= 2:
                break

        if not title_parts:
            continue

        title = clean_text(" ".join(title_parts))
        if len(tokenize(title)) < 1:
            continue

        description_paragraphs: list[str] = []
        for block in blocks:
            if block["x0"] <= 240 or block["y0"] >= 360:
                continue
            text = clean_text(block["text"])
            if len(text) < 70:
                continue
            if looks_spanish(text):
                description_paragraphs.append(text)
            if len(description_paragraphs) >= 2:
                break

        if not description_paragraphs:
            continue

        features: list[str] = []
        for block in blocks:
            if block["y0"] < 470 or block["y0"] > 575:
                continue
            text = block["text"]
            if "•" not in text:
                continue
            left_text = strip_bilingual_segment(text)
            normalized_left = normalize_text(left_text)
            if not left_text or normalized_left in {"estructura", "tejido", "frame", "fabric"}:
                continue
            if len(tokenize(left_text)) <= 4:
                features.append(left_text)

        entry = CatalogEntry(
            title=title,
            page=page_number,
            description_paragraphs=description_paragraphs,
            features=list(dict.fromkeys(features)),
        )
        entry.normalized_title = normalize_text(entry.title)
        entry.tokens = tokenize(entry.title)
        entry.key_tokens = key_tokens(entry.title)
        entries.append(entry)

    deduped: dict[str, CatalogEntry] = {}
    for entry in entries:
        existing = deduped.get(entry.normalized_title)
        if existing is None or len(" ".join(entry.description_paragraphs)) > len(" ".join(existing.description_paragraphs)):
            deduped[entry.normalized_title] = entry
    return list(deduped.values())


def load_product_sitemap(session: requests.Session, cache_path: Path) -> list[WebCandidate]:
    if cache_path.exists():
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        return [
            WebCandidate(
                url=item["url"],
                slug_text=item["slug_text"],
                tokens=set(item["tokens"]),
                key_tokens=set(item["key_tokens"]),
            )
            for item in data
        ]

    response = session.get("https://www.balliuexport.com/product-sitemap.xml", timeout=30)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for node in root.findall(".//sm:loc", ns):
        if not node.text:
            continue
        url = node.text.strip()
        path = urlparse(url).path
        if not path.startswith("/producto/"):
            continue
        urls.append(url)

    candidates = []
    for url in urls:
        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        slug_text = clean_text(slug.replace("-", " ").replace("_", " "))
        candidates.append(
            WebCandidate(
                url=url,
                slug_text=slug_text,
                tokens=tokenize(slug_text),
                key_tokens=key_tokens(slug_text),
            )
        )

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(
            [
                {
                    "url": candidate.url,
                    "slug_text": candidate.slug_text,
                    "tokens": sorted(candidate.tokens),
                    "key_tokens": sorted(candidate.key_tokens),
                }
                for candidate in candidates
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return candidates


def fetch_web_product(session: requests.Session, url: str) -> dict[str, Any]:
    response = session.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    title = ""
    title_node = soup.select_one("h1.product_title, h1")
    if title_node:
        title = clean_text(title_node.get_text(" ", strip=True))

    image = ""
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        image = og_image["content"].strip()

    attributes: dict[str, str] = {}
    for row in soup.select(".woocommerce-product-attributes tr"):
        key_node = row.find("th")
        value_node = row.find("td")
        if not key_node or not value_node:
            continue
        key = clean_text(key_node.get_text(" ", strip=True))
        value = clean_text(value_node.get_text(" ", strip=True))
        if key and value:
            attributes[key] = value

    content_parts: list[str] = []
    for node in soup.select("main h2, main p"):
        text = clean_text(node.get_text(" ", strip=True))
        if len(text) < 50:
            continue
        if "precio con iva incluido" in normalize_text(text):
            continue
        content_parts.append(text)
        if len(content_parts) >= 3:
            break

    return {
        "url": url,
        "title": title,
        "image": image,
        "attributes": attributes,
        "content_parts": content_parts,
        "tokens": list(tokenize(title or "")),
        "key_tokens": list(key_tokens(title or "")),
    }


def get_cached_web_product(session: requests.Session, url: str, cache_dir: Path) -> dict[str, Any]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{hashlib.sha1(url.encode('utf-8')).hexdigest()}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    data = fetch_web_product(session, url)
    cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.05)
    return data


def find_best_web_candidate(product_name: str, candidates: list[WebCandidate]) -> WebCandidate | None:
    best = None
    best_score = 0.0
    for candidate in candidates:
        score = score_candidate(product_name, candidate.slug_text, candidate.tokens, candidate.key_tokens)
        if score > best_score:
            best_score = score
            best = candidate
    if best_score < 28:
        return None
    return best


def product_kind_tokens(value: str) -> set[str]:
    normalized = normalize_text(value)
    kinds = set()
    for token in [
        "tumbona",
        "silla",
        "mesa",
        "parasol",
        "sofa",
        "cama",
        "funda",
        "pasarela",
        "limpiador",
        "colchoneta",
        "cojin",
    ]:
        if token in normalized:
            kinds.add(token)
    return kinds


def is_valid_web_match(product_name: str, web_entry: dict[str, Any] | None) -> bool:
    if not web_entry or not web_entry.get("title"):
        return False
    score = score_candidate(
        product_name,
        web_entry["title"],
        set(web_entry.get("tokens", [])),
        set(web_entry.get("key_tokens", [])),
    )
    if score < 32:
        return False
    product_kinds = product_kind_tokens(product_name)
    web_kinds = product_kind_tokens(web_entry["title"])
    if product_kinds and not web_kinds:
        return False
    if product_kinds and web_kinds and not (product_kinds & web_kinds):
        return False
    return True


def calculate_web_match_score(product_name: str, web_entry: dict[str, Any] | None) -> float:
    if not web_entry or not web_entry.get("title"):
        return 0.0
    return round(
        score_candidate(
            product_name,
            web_entry["title"],
            set(web_entry.get("tokens", [])),
            set(web_entry.get("key_tokens", [])),
        ),
        2,
    )


def clamp_match_score(value: float | None) -> int:
    if value is None:
        return 0
    return max(0, min(100, int(round(value))))


def summarize_match_quality(catalog_score: float | None, web_score: float | None, web_valid: bool) -> tuple[int, str, str]:
    catalog_pct = clamp_match_score(catalog_score)
    web_pct = clamp_match_score(web_score if web_valid else 0)

    if catalog_pct and web_pct:
        overall = int(round((catalog_pct + web_pct) / 2))
        detail = "Catalogo + web"
    elif catalog_pct:
        overall = min(79, catalog_pct)
        detail = "Solo catalogo"
    elif web_pct:
        overall = min(79, web_pct)
        detail = "Solo web"
    else:
        overall = 0
        detail = "Sin match fiable"

    if overall >= 80:
        color = "Verde"
    elif overall >= 50:
        color = "Amarillo"
    else:
        color = "Rojo"
    return overall, color, detail


def startswith_normalized(body: str, title: str) -> bool:
    body_tokens = normalize_text(body).split()
    title_tokens = normalize_text(title).split()
    if len(body_tokens) < len(title_tokens):
        return False
    return body_tokens[: len(title_tokens)] == title_tokens


def split_body_with_boundary(body: str) -> tuple[str, str]:
    normalized = normalize_text(body)
    for pattern in PRODUCT_BOUNDARY_PATTERNS:
        match = re.match(rf"^(.+?\b{re.escape(pattern)}\b)(?:\s+(.*))?$", normalized)
        if not match:
            continue
        prefix_normalized = match.group(1).strip()
        suffix_normalized = (match.group(2) or "").strip()
        prefix_text = []
        suffix_text = []
        words = clean_text(body).split()
        prefix_len = len(prefix_normalized.split())
        prefix_text = words[:prefix_len]
        suffix_text = words[prefix_len:]
        return clean_text(" ".join(prefix_text)), clean_text(" ".join(suffix_text))
    return clean_text(body), ""


def split_body_by_variant_markers(body: str) -> tuple[str, str]:
    words = clean_text(body).split()
    if len(words) < 3:
        return clean_text(body), ""

    for index in range(1, len(words)):
        tail = normalize_text(" ".join(words[index:]))
        head = clean_text(" ".join(words[:index]))
        if not head:
            continue
        if not product_kind_tokens(head):
            continue
        if any(tail.startswith(prefix) for prefix in VARIANT_MARKER_PREFIXES):
            return head, clean_text(" ".join(words[index:]))
    return clean_text(body), ""


def assign_marker(markers: list[tuple[float, str]], y: float) -> str | None:
    if not markers:
        return None
    if len(markers) == 1:
        return markers[0][1]
    for index, (marker_y, marker_name) in enumerate(markers):
        prev_y = markers[index - 1][0] if index > 0 else None
        next_y = markers[index + 1][0] if index + 1 < len(markers) else None
        upper = float("-inf") if prev_y is None else (prev_y + marker_y) / 2
        lower = float("inf") if next_y is None else (marker_y + next_y) / 2
        if upper <= y < lower:
            return marker_name
    return markers[-1][1]


def parse_tariff_pdf(path: Path, known_titles: list[str]) -> list[TariffRow]:
    pdf = fitz.open(path)
    known_titles = sorted(set(known_titles), key=lambda value: len(normalize_text(value)), reverse=True)
    rows: list[TariffRow] = []
    order_index = 0

    for page_number, page in enumerate(pdf, start=1):
        blocks = []
        for block in page.get_text("blocks", sort=True):
            x0, y0, x1, y1, text, *_ = block
            text = clean_text(text)
            if not text:
                continue
            if "tarifa 2026" in normalize_text(text):
                continue
            if "producto grupo" in normalize_text(text):
                continue
            if "client" == normalize_text(text):
                continue
            if re.fullmatch(r"2026\s+\d+", normalize_text(text)):
                continue
            blocks.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1, "text": text})

        markers: list[tuple[float, str]] = []
        priced_blocks: list[dict[str, Any]] = []

        for block in blocks:
            match = PRICE_RE.match(block["text"])
            if match:
                priced_blocks.append({**block, **match.groupdict()})
                continue
            if block["x0"] < 180 and block["x1"] < 240:
                markers.append((block["y0"], clean_text(block["text"])))

        markers.sort(key=lambda item: item[0])

        for block in priced_blocks:
            body = clean_text(block["body"])
            marker_product = assign_marker(markers, block["y0"])
            product_name = ""
            variant_name = ""

            for title in known_titles:
                if startswith_normalized(body, title):
                    product_name = title
                    title_len = len(normalize_text(title).split())
                    words = body.split()
                    variant_name = clean_text(" ".join(words[title_len:]))
                    break

            if not product_name and marker_product and startswith_normalized(body, marker_product):
                product_name = marker_product
                marker_len = len(normalize_text(marker_product).split())
                words = body.split()
                variant_name = clean_text(" ".join(words[marker_len:]))

            if not product_name:
                split_product, split_variant = split_body_by_variant_markers(body)
                if split_variant:
                    product_name = split_product
                    variant_name = split_variant

            if not product_name and block["x0"] >= 240 and marker_product:
                product_name = marker_product
                variant_name = body

            if not product_name and marker_product and normalize_text(body).startswith(tuple(VARIANT_STARTERS)):
                product_name = marker_product
                variant_name = body

            if not product_name:
                product_name, variant_name = split_body_with_boundary(body)

            if not product_name:
                product_name = body

            variant_name = variant_name or "Default Title"

            rows.append(
                TariffRow(
                    product_name=product_name,
                    variant_name=variant_name,
                    group=block["group"],
                    price=parse_price(block["price"]),
                    page=page_number,
                    order_index=order_index,
                    source_text=block["text"],
                )
            )
            order_index += 1

    deduped: dict[tuple[str, str, str, str], TariffRow] = {}
    for row in rows:
        key = (
            normalize_text(row.product_name),
            normalize_text(row.variant_name),
            row.group,
            format_price(row.price),
        )
        deduped[key] = row
    return list(deduped.values())


def classify_product_type(name: str) -> str:
    normalized = normalize_text(name)
    if "funda" in normalized:
        return "Funda"
    if any(token in normalized for token in ["colchoneta", "cojin", "limpiador", "pie parasol", "base hormigon", "caja seguridad", "pasarela"]):
        return "Accesorio"
    if "cama balinesa" in normalized:
        return "Cama balinesa"
    if "mini tumbona" in normalized:
        return "Mini tumbona"
    if "parasol" in normalized:
        return "Parasol"
    if "tumbona" in normalized:
        return "Tumbona"
    if "silla" in normalized:
        return "Silla"
    if "mesa" in normalized:
        return "Mesa"
    if "sofa" in normalized:
        return "Sofa"
    return "Mobiliario exterior"


def clean_numeric_dimension(value: Any) -> str:
    value = "" if value is None else str(value)
    value = value.replace(",", ".")
    match = re.search(r"\d+(?:\.\d+)?", value)
    return match.group(0) if match else ""


def compact_dimension(value: str) -> str:
    if not value:
        return ""
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return value.replace(".", ",")


def detect_capacity_balliu(product_name: str, variant_name: str, description: str) -> str:
    combined = normalize_text(f"{product_name} {variant_name} {description}")
    if "3 plazas" in combined or "triple" in combined:
        return "3 plazas"
    if "2 plazas" in combined or "doble" in combined:
        return "2 plazas"
    if "individual" in combined:
        return "individual"
    return ""


def detect_material_balliu(product_name: str, variant_name: str, description: str) -> str:
    combined = normalize_text(f"{product_name} {variant_name} {description}")
    if "aluminio" in combined:
        return "aluminio"
    if "hpl" in combined:
        return "HPL"
    if "madera" in combined:
        return "madera"
    if "resina" in combined:
        return "resina"
    if "acrilico" in combined or "acrilica" in combined:
        return "acrílico"
    if "tejido nautico" in combined:
        return "tejido náutico"
    return ""


def detect_style_balliu(description: str) -> str:
    text = normalize_text(description)
    if "minimalista" in text:
        return "minimalista"
    if "elegante" in text:
        return "elegante"
    if "sofistic" in text:
        return "sofisticado"
    if "clasico" in text:
        return "clásico"
    if "moderno" in text:
        return "moderno"
    if "contempor" in text:
        return "contemporáneo"
    if "funcional" in text:
        return "funcional"
    return "contemporáneo"


def infer_variant_size_text(variant_name: str) -> str:
    variant = clean_text(variant_name)
    dim_match = re.search(r"(\d+(?:/\d+)?)\s*[xX]\s*(\d+)", variant)
    if dim_match:
        return f"{dim_match.group(1)}×{dim_match.group(2)} cm"
    diam_match = re.search(r"(?:diam(?:etro)?\.?\s*)(\d+)", normalize_text(variant))
    if diam_match:
        return f"Ø{diam_match.group(1)} cm"
    return ""


def build_seo_like_title(
    product_name: str,
    variant_name: str,
    description: str,
    width: str,
    depth: str,
    height: str,
) -> str:
    product_type = classify_product_type(product_name)
    material = detect_material_balliu(product_name, variant_name, description)
    style = detect_style_balliu(description)
    capacity = detect_capacity_balliu(product_name, variant_name, description)
    width_num = clean_numeric_dimension(width)
    depth_num = clean_numeric_dimension(depth)
    height_num = clean_numeric_dimension(height)
    variant_norm = normalize_text(variant_name)

    size_text = ""
    if width_num and depth_num:
        size_text = f"{compact_dimension(width_num)}×{compact_dimension(depth_num)} cm"
    elif width_num:
        size_text = f"{compact_dimension(width_num)} cm"
    else:
        size_text = infer_variant_size_text(variant_name)

    if product_type == "Mini tumbona":
        title = "Mini tumbona de exterior"
    elif product_type == "Tumbona":
        title = "Tumbona de exterior"
        if "mini" in normalize_text(product_name):
            title = "Mini tumbona de exterior"
        if "apilable" in normalize_text(product_name):
            title += " apilable"
        if "con ruedas" in variant_norm:
            title += " con ruedas"
        elif "sin ruedas" in variant_norm:
            title += " sin ruedas"
    elif product_type == "Silla":
        title = "Silla exterior"
        if "con brazos" in variant_norm or "con brazos" in normalize_text(product_name):
            title += " con brazos"
        elif "sin brazos" in variant_norm:
            title += " sin brazos"
        elif "taburete" in variant_norm:
            title = "Taburete exterior"
    elif product_type == "Mesa":
        normalized_product = normalize_text(product_name)
        if "auxiliar" in normalized_product:
            title = "Mesa auxiliar exterior"
        elif "central" in normalized_product or "centro" in normalized_product:
            title = "Mesa de centro exterior"
        elif "alta" in normalized_product or "mesa alta" in variant_norm:
            title = "Mesa alta exterior"
        else:
            title = "Mesa exterior"
    elif product_type == "Parasol":
        title = "Parasol para terraza"
    elif product_type == "Cama balinesa":
        title = "Cama balinesa exterior"
    elif product_type == "Sofa":
        title = "Sofá exterior"
        if capacity:
            title += f" {capacity}"
    elif product_type == "Funda":
        title = "Funda protectora exterior"
    elif product_type == "Accesorio":
        normalized_product = normalize_text(product_name)
        if "base hormigon" in normalized_product:
            title = "Base de parasol"
        elif "pie parasol" in normalized_product:
            title = "Pie de parasol"
        elif "colchoneta" in normalized_product:
            title = "Colchoneta para tumbona"
        elif "cojin" in normalized_product:
            title = "Cojín exterior"
        elif "limpiador" in normalized_product:
            title = "Limpiador para mobiliario exterior"
        else:
            title = "Accesorio exterior"
    else:
        title = "Mobiliario exterior"

    if material and material not in normalize_text(title):
        title += f" {material}"
    if product_type in {"Silla", "Sofa", "Cama balinesa"}:
        title += f" · estilo {style}"
    if size_text:
        title += f" | {size_text}"
    return clean_text(title)


def extract_dimensions(attributes: dict[str, str]) -> list[str]:
    labels = ["Largo", "Ancho", "Alto", "Fondo", "Diametro", "Diámetro", "Peso"]
    dimensions = []
    for label in labels:
        if label in attributes:
            value = attributes[label]
            suffix = "" if normalize_text(value).endswith(("cm", "kg")) else (" kg" if label == "Peso" else " cm")
            dimensions.append(f"{label}: {value}{suffix}")
    return dimensions


def extract_dimension_value(attributes: dict[str, str], *keys: str) -> str:
    for key in keys:
        if key in attributes:
            value = clean_text(str(attributes[key]))
            if value and value.upper() != "N/D":
                return value
    return ""


def build_html_description(
    product_name: str,
    catalog_entry: dict[str, Any] | None,
    web_entry: dict[str, Any] | None,
) -> str:
    paragraphs = []
    if catalog_entry:
        paragraphs.extend(catalog_entry["description_paragraphs"])
    elif web_entry:
        paragraphs.extend(web_entry.get("content_parts", []))

    features = []
    if catalog_entry:
        features.extend(catalog_entry["features"])

    dimensions = extract_dimensions(web_entry.get("attributes", {}) if web_entry else {})

    html_parts = []
    for paragraph in paragraphs[:2]:
        html_parts.append(f"<p>{html.escape(paragraph)}</p>")
    if features:
        html_parts.append("<ul>")
        for feature in dict.fromkeys(features):
            html_parts.append(f"  <li>{html.escape(feature)}</li>")
        html_parts.append("</ul>")
    if dimensions:
        html_parts.append(f"<p><strong>Dimensiones:</strong> {html.escape(' | '.join(dimensions))}</p>")
    if not html_parts:
        html_parts.append(f"<p>{html.escape(product_name)}</p>")
    return "\n".join(html_parts)


def seo_excerpt(html_body: str, limit: int = 320) -> str:
    text = clean_text(re.sub(r"<[^>]+>", " ", html_body))
    return text[:limit].rstrip()


def build_tags(product_type: str, product_name: str) -> str:
    tags = ["balliu", "exterior", product_type.lower()]
    for token in sorted(key_tokens(product_name)):
        if len(token) > 2:
            tags.append(token)
    return ", ".join(dict.fromkeys(tags))


def enrich_products(
    tariff_rows: list[TariffRow],
    catalog_entries: list[CatalogEntry],
    web_candidates: list[WebCandidate],
    session: requests.Session,
    cache_dir: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    catalog_candidates = [
        {
            "title": entry.title,
            "description_paragraphs": entry.description_paragraphs,
            "features": entry.features,
            "page": entry.page,
            "tokens": entry.tokens,
            "key_tokens": entry.key_tokens,
        }
        for entry in catalog_entries
    ]

    grouped_rows: dict[str, list[TariffRow]] = defaultdict(list)
    display_names: dict[str, str] = {}
    for row in tariff_rows:
        handle = slugify(row.product_name)
        grouped_rows[handle].append(row)
        display_names.setdefault(handle, row.product_name)

    product_matches: dict[str, dict[str, Any]] = {}
    pending_web_urls: dict[str, str] = {}
    report = {
        "catalog_matched": 0,
        "catalog_unmatched": [],
        "web_matched": 0,
        "web_unmatched": [],
        "web_rejected_after_validation": [],
    }

    for handle, rows in grouped_rows.items():
        product_name = display_names[handle]
        catalog_match = choose_best_match(product_name, catalog_candidates, threshold=33.0)
        if catalog_match:
            report["catalog_matched"] += 1
        else:
            report["catalog_unmatched"].append(product_name)

        web_candidate = find_best_web_candidate(product_name, web_candidates)
        if web_candidate:
            pending_web_urls[handle] = web_candidate.url

        product_matches[handle] = {
            "product_name": catalog_match["title"] if catalog_match else product_name,
            "catalog": catalog_match,
            "web_url": pending_web_urls.get(handle),
            "rows": rows,
        }

    fetched_web_data: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(get_cached_web_product, session, url, cache_dir): handle
            for handle, url in pending_web_urls.items()
        }
        for future in as_completed(futures):
            handle = futures[future]
            try:
                fetched_web_data[handle] = future.result()
            except Exception as exc:  # pragma: no cover - diagnostic only
                fetched_web_data[handle] = {"error": str(exc), "url": pending_web_urls[handle]}

    enriched_products: list[dict[str, Any]] = []
    for handle, match in product_matches.items():
        web_entry = fetched_web_data.get(handle)
        web_score = None
        web_valid = False
        if isinstance(web_entry, dict) and "error" not in web_entry:
            web_score = calculate_web_match_score(match["product_name"], web_entry)
            web_valid = is_valid_web_match(match["product_name"], web_entry)
        if isinstance(web_entry, dict) and "error" not in web_entry and web_valid:
            match["web"] = web_entry
            report["web_matched"] += 1
        else:
            match["web"] = None
            if match.get("web_url"):
                report["web_rejected_after_validation"].append(match["product_name"])
            else:
                report["web_unmatched"].append(match["product_name"])
        match["catalog_score"] = match["catalog"]["_score"] if match.get("catalog") else None
        match["web_score"] = web_score
        match["match_percent"], match["match_color"], match["match_detail"] = summarize_match_quality(
            match["catalog_score"],
            web_score,
            web_valid,
        )
        enriched_products.append(match)

    return enriched_products, report


def build_shopify_rows(products: list[dict[str, Any]], copy_price_to_cost: bool) -> list[dict[str, Any]]:
    csv_rows: list[dict[str, Any]] = []

    for product in products:
        handle = slugify(product["product_name"])
        rows = product["rows"]
        unique_variants = {row.variant_name for row in rows}
        option_name = "Configuracion" if len(unique_variants) > 1 or "Default Title" not in unique_variants else "Title"
        body_html = build_html_description(product["product_name"], product["catalog"], product["web"])
        product_type = classify_product_type(product["product_name"])
        image_src = product["web"]["image"] if product.get("web") else ""
        attributes = product.get("web", {}).get("attributes", {}) if product.get("web") else {}
        seo_title = build_seo_like_title(
            product["product_name"],
            "",
            html_to_plain_text(body_html),
            extract_dimension_value(attributes, "Ancho"),
            extract_dimension_value(attributes, "Fondo"),
            extract_dimension_value(attributes, "Alto"),
        )
        image_alt = seo_title
        seo_description = seo_excerpt(body_html)
        tags = build_tags(product_type, product["product_name"])

        for index, row in enumerate(rows, start=1):
            csv_rows.append(
                {
                    "Handle": handle,
                    "Title": seo_title if index == 1 else "",
                    "Body (HTML)": body_html if index == 1 else "",
                    "Vendor": "Balliu" if index == 1 else "",
                    "Product Category": "",
                    "Type": product_type if index == 1 else "",
                    "Tags": tags if index == 1 else "",
                    "Published": "TRUE" if index == 1 else "",
                    "Option1 Name": option_name,
                    "Option1 Value": row.variant_name if option_name != "Title" else "Default Title",
                    "Variant SKU": stable_sku(product["product_name"], row.variant_name),
                    "Variant Grams": "0",
                    "Variant Inventory Tracker": "shopify",
                    "Variant Inventory Qty": "0",
                    "Variant Inventory Policy": "deny",
                    "Variant Fulfillment Service": "manual",
                    "Variant Price": format_price(row.price),
                    "Variant Compare At Price": "",
                    "Variant Requires Shipping": "TRUE",
                    "Variant Taxable": "TRUE",
                    "Image Src": image_src if index == 1 else "",
                    "Image Position": "1" if index == 1 and image_src else "",
                    "Image Alt Text": image_alt if index == 1 and image_src else "",
                    "Gift Card": "FALSE",
                    "SEO Title": seo_title if index == 1 else "",
                    "SEO Description": seo_description if index == 1 else "",
                    "Status": "active",
                    "Cost per item": format_price(row.price) if copy_price_to_cost else "",
                }
            )

    return csv_rows


def html_to_plain_text(value: str) -> str:
    text = re.sub(r"</p>|</li>|<br\s*/?>", "\n", value)
    text = re.sub(r"<[^>]+>", " ", text)
    lines = [clean_text(line) for line in text.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def build_summary_rows(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for product in products:
        body_html = build_html_description(product["product_name"], product["catalog"], product["web"])
        description = html_to_plain_text(body_html)
        attributes = product.get("web", {}).get("attributes", {}) if product.get("web") else {}
        ancho = extract_dimension_value(attributes, "Ancho")
        fondo = extract_dimension_value(attributes, "Fondo")
        alto = extract_dimension_value(attributes, "Alto")
        image_src = product.get("web", {}).get("image", "") if product.get("web") else ""

        for row in product["rows"]:
            producto = build_seo_like_title(
                product["product_name"],
                row.variant_name,
                description,
                ancho,
                fondo,
                alto,
            )

            rows.append(
                {
                    "SKU": stable_sku(product["product_name"], row.variant_name),
                    "Producto": producto,
                    "Precio neto exworks sin iva": format_eur_es(row.price),
                    "Precio Venta": "",
                    "Margen €": "",
                    "Margen%": "",
                    "Coste de Envio": "",
                    "": "",
                    "PVP Recomendado": "",
                    "Descripción": description,
                    "Ancho (cm)": ancho,
                    "Fondo (cm)": fondo,
                    "Alto (cm)": alto,
                    "Imagen": image_src,
                    "Proveedor": "Balliu",
                    "Match %": product.get("match_percent", 0),
                    "Color Match": product.get("match_color", "Rojo"),
                    "Detalle Match": product.get("match_detail", "Sin match fiable"),
                }
            )

    return rows


def write_csv(output_path: Path, rows: list[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(rows, columns=SHOPIFY_HEADERS)
    dataframe.to_csv(output_path, index=False, quoting=csv.QUOTE_MINIMAL)


def write_summary_csv(output_path: Path, rows: list[dict[str, Any]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(rows, columns=SUMMARY_HEADERS)
    dataframe.to_csv(output_path, index=False, quoting=csv.QUOTE_MINIMAL)


def write_report(report_path: Path, tariff_rows: list[TariffRow], catalog_entries: list[CatalogEntry], report: dict[str, Any]) -> None:
    normalized_report = {}
    for key, value in report.items():
        if isinstance(value, list):
            normalized_report[key] = sorted(dict.fromkeys(value))
        else:
            normalized_report[key] = value
    payload = {
        "tariff_variants": len(tariff_rows),
        "catalog_entries": len(catalog_entries),
        **normalized_report,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    base_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tariff-pdf",
        type=Path,
        default=base_dir / "proveedores_raw/balliu/TARIFA 2026 UBICUO LIBRES PENSADORES SL.pdf",
    )
    parser.add_argument(
        "--catalog-pdf",
        type=Path,
        default=base_dir / "proveedores_raw/balliu/2025 CATALOGO GENERAL - Baja resolución.pdf",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=base_dir / "balliu_shopify_products.csv",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=base_dir / "balliu_extraction_report.json",
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=base_dir / "proveedores_raw/CSV-Catalogo-Balliu.csv",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=base_dir / ".cache/balliu",
    )
    parser.add_argument(
        "--copy-price-to-cost",
        action="store_true",
        help="Copy the tariff price into Shopify's Cost per item column.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.tariff_pdf.exists():
        raise FileNotFoundError(f"Missing tariff PDF: {args.tariff_pdf}")
    if not args.catalog_pdf.exists():
        raise FileNotFoundError(f"Missing catalog PDF: {args.catalog_pdf}")

    session = build_requests_session()
    sitemap_cache = args.cache_dir / "product_sitemap.json"
    product_cache_dir = args.cache_dir / "products"

    catalog_entries = parse_catalog_pdf(args.catalog_pdf)
    known_titles = [entry.title for entry in catalog_entries] + EXTRA_KNOWN_TITLES
    tariff_rows = parse_tariff_pdf(args.tariff_pdf, known_titles)
    web_candidates = load_product_sitemap(session, sitemap_cache)
    enriched_products, report = enrich_products(
        tariff_rows=tariff_rows,
        catalog_entries=catalog_entries,
        web_candidates=web_candidates,
        session=session,
        cache_dir=product_cache_dir,
    )
    shopify_rows = build_shopify_rows(enriched_products, copy_price_to_cost=args.copy_price_to_cost)
    summary_rows = build_summary_rows(enriched_products)

    write_csv(args.output_csv, shopify_rows)
    write_summary_csv(args.summary_csv, summary_rows)
    write_report(args.report_json, tariff_rows, catalog_entries, report)

    print(f"Tariff variants: {len(tariff_rows)}")
    print(f"Catalog entries: {len(catalog_entries)}")
    print(f"Shopify rows: {len(shopify_rows)}")
    print(f"CSV written to: {args.output_csv}")
    print(f"Summary CSV written to: {args.summary_csv}")
    print(f"Report written to: {args.report_json}")


if __name__ == "__main__":
    main()
