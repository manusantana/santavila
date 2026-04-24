#!/usr/bin/env python3
"""
Sync Shopify catalog:
- existing non-Balliu products -> vendor/tag Hevea
- Balliu rows from the pre-Shopify CSV -> create/update as active products for review
"""

from __future__ import annotations

import csv
import html
import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


from config import SHOPIFY_ACCESS_TOKEN as TOKEN
SHOP = "mueblesexterior.myshopify.com"
API = f"https://{SHOP}/admin/api/2026-01/graphql.json"
BASE = Path(__file__).resolve().parent
BALLIU_CSV = BASE / "proveedores_raw/CSV-Catalogo-Balliu.csv"
REPORT_CSV = BASE / "shopify_sync_report.csv"


@dataclass
class StoreProduct:
    id: str
    handle: str
    title: str
    vendor: str
    tags: list[str]
    preview_url: str


def gql(query: str, variables: dict | None = None) -> dict:
    payload_bytes = json.dumps({"query": query, "variables": variables or {}}).encode()
    last_error: Exception | None = None

    for attempt in range(1, 6):
        try:
            req = urllib.request.Request(
                API,
                data=payload_bytes,
                headers={
                    "X-Shopify-Access-Token": TOKEN,
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                payload = json.loads(response.read())
            if payload.get("errors"):
                raise RuntimeError(json.dumps(payload["errors"], ensure_ascii=False))
            return payload["data"]
        except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            last_error = exc
            if attempt == 5:
                break
            time.sleep(1.2 * attempt)

    raise RuntimeError(f"Shopify request failed after retries: {last_error}")


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_eur_es(value: str) -> float:
    cleaned = (value or "").replace("€", "").replace("\xa0", " ").strip()
    cleaned = cleaned.replace(".", "").replace(",", ".")
    cleaned = cleaned.strip()
    if not cleaned:
        return 0.0
    return float(cleaned)


def money_to_str(value: str) -> str | None:
    if not value:
        return None
    try:
        return f"{parse_eur_es(value):.2f}"
    except ValueError:
        return None


def csv_delimiter(path: Path) -> str:
    sample = path.read_text(encoding="utf-8")[:4096]
    return csv.Sniffer().sniff(sample, delimiters=",;").delimiter


def read_balliu_rows(path: Path) -> list[dict[str, str]]:
    delimiter = csv_delimiter(path)
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter=delimiter))
    return [row for row in rows if row.get("SKU") and row.get("Producto")]


def description_to_html(value: str) -> str:
    lines = [line.strip() for line in str(value or "").splitlines() if line.strip()]
    if not lines:
        return "<p></p>"
    return "\n".join(f"<p>{html.escape(line)}</p>" for line in lines)


def seo_description(value: str, limit: int = 320) -> str:
    text = " ".join(line.strip() for line in str(value or "").splitlines() if line.strip())
    return text[:limit].rstrip()


def infer_product_type(title: str) -> str:
    value = slugify(title)
    if "cama-balinesa" in value:
        return "Cama balinesa"
    if "parasol" in value:
        return "Parasol"
    if "mini-tumbona" in value:
        return "Mini tumbona"
    if "tumbona" in value:
        return "Tumbona"
    if "silla" in value:
        return "Silla"
    if "mesa" in value:
        return "Mesa"
    if "sofa" in value:
        return "Sofa"
    if "funda" in value:
        return "Funda"
    if any(token in value for token in ["base-de-parasol", "pie-de-parasol", "colchoneta", "cojin", "limpiador"]):
        return "Accesorio"
    return "Mobiliario exterior"


def balliu_handle(sku: str, title: str) -> str:
    sku_suffix = slugify(sku)[-8:] or "item"
    return f"balliu-{slugify(title)}-{sku_suffix}"


def build_balliu_handles(rows: list[dict[str, str]]) -> list[str]:
    base_handles = [balliu_handle(row["SKU"], row["Producto"]) for row in rows]
    totals = Counter(base_handles)
    seen: defaultdict[str, int] = defaultdict(int)
    handles: list[str] = []

    for base_handle in base_handles:
        seen[base_handle] += 1
        occurrence = seen[base_handle]
        if totals[base_handle] == 1 or occurrence == 1:
            handles.append(base_handle)
            continue
        handles.append(f"{base_handle}-{occurrence}")

    return handles


def fetch_all_products() -> list[StoreProduct]:
    query = """
    query productsPage($cursor: String) {
      products(first: 250, after: $cursor, sortKey: ID) {
        edges {
          cursor
          node {
            id
            handle
            title
            vendor
            tags
            onlineStorePreviewUrl
          }
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """
    cursor = None
    products: list[StoreProduct] = []

    while True:
        data = gql(query, {"cursor": cursor})
        page = data["products"]
        for edge in page["edges"]:
            node = edge["node"]
            products.append(
                StoreProduct(
                    id=node["id"],
                    handle=node["handle"],
                    title=node["title"],
                    vendor=node.get("vendor") or "",
                    tags=node.get("tags") or [],
                    preview_url=node.get("onlineStorePreviewUrl") or "",
                )
            )
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    return products


def update_vendor_and_tags(product: StoreProduct, vendor: str, tag: str) -> StoreProduct:
    tags = sorted({*(product.tags or []), tag})
    mutation = """
    mutation productUpdate($product: ProductUpdateInput!) {
      productUpdate(product: $product) {
        product {
          id
          handle
          title
          vendor
          tags
          onlineStorePreviewUrl
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    data = gql(
        mutation,
        {"product": {"id": product.id, "vendor": vendor, "tags": tags}},
    )
    errors = data["productUpdate"]["userErrors"]
    if errors:
        raise RuntimeError(json.dumps(errors, ensure_ascii=False))
    node = data["productUpdate"]["product"]
    return StoreProduct(
        id=node["id"],
        handle=node["handle"],
        title=node["title"],
        vendor=node.get("vendor") or "",
        tags=node.get("tags") or [],
        preview_url=node.get("onlineStorePreviewUrl") or "",
    )


def upsert_balliu_product(row: dict[str, str], handle: str) -> dict[str, str]:
    price = money_to_str(row.get("Precio Venta") or "") or money_to_str(row.get("Precio neto exworks sin iva") or "") or "0.00"
    compare_at = money_to_str(row.get("PVP Recomendado") or "")
    image = (row.get("Imagen") or "").strip()
    tags = ["Balliu"]
    color_match = (row.get("Color Match") or "").strip()
    if color_match:
        tags.append(f"match-{slugify(color_match)}")

    input_payload = {
        "handle": handle,
        "title": row["Producto"].strip(),
        "descriptionHtml": description_to_html(row.get("Descripción") or ""),
        "vendor": "Balliu",
        "productType": infer_product_type(row["Producto"]),
        "tags": tags,
        "status": "ACTIVE",
        "seo": {
            "title": row["Producto"].strip(),
            "description": seo_description(row.get("Descripción") or ""),
        },
        "productOptions": [
            {
                "name": "Title",
                "position": 1,
                "values": [{"name": "Default Title"}],
            }
        ],
        "variants": [
            {
                "sku": row["SKU"].strip(),
                "price": price,
                "compareAtPrice": compare_at,
                "inventoryPolicy": "DENY",
                "taxable": True,
                "optionValues": [{"optionName": "Title", "name": "Default Title"}],
            }
        ],
    }
    if image:
        input_payload["files"] = [
            {
                "originalSource": image,
                "contentType": "IMAGE",
                "alt": row["Producto"].strip(),
            }
        ]

    mutation = """
    mutation productSet($identifier: ProductSetIdentifiers, $input: ProductSetInput!, $synchronous: Boolean!) {
      productSet(identifier: $identifier, input: $input, synchronous: $synchronous) {
        product {
          id
          handle
          title
          vendor
          tags
          status
          onlineStorePreviewUrl
        }
        userErrors {
          code
          field
          message
        }
      }
    }
    """
    data = gql(
        mutation,
        {
            "identifier": {"handle": handle},
            "input": input_payload,
            "synchronous": True,
        },
    )
    errors = data["productSet"]["userErrors"]
    if errors:
        raise RuntimeError(json.dumps(errors, ensure_ascii=False))
    product = data["productSet"]["product"]
    return {
        "handle": product["handle"],
        "title": product["title"],
        "vendor": product["vendor"],
        "preview_url": product.get("onlineStorePreviewUrl") or "",
        "status": product["status"],
    }


def write_report(rows: list[dict[str, str]]) -> None:
    headers = ["action", "handle", "title", "vendor", "preview_url", "status", "notes"]
    with open(REPORT_CSV, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    balliu_rows = read_balliu_rows(BALLIU_CSV)
    balliu_handles = build_balliu_handles(balliu_rows)
    store_products = fetch_all_products()
    store_by_handle = {product.handle: product for product in store_products}
    report_rows: list[dict[str, str]] = []

    # Phase 1: existing current catalog -> Hevea
    hevea_updates = 0
    hevea_total = sum(1 for product in store_products if not product.handle.startswith("balliu-"))
    hevea_seen = 0
    for product in store_products:
        if product.handle.startswith("balliu-"):
            continue
        hevea_seen += 1
        desired_tags = set(product.tags or [])
        desired_tags.add("Hevea")
        if product.vendor == "Hevea" and "Hevea" in desired_tags:
            report_rows.append(
                {
                    "action": "hevea-skip",
                    "handle": product.handle,
                    "title": product.title,
                    "vendor": product.vendor,
                    "preview_url": product.preview_url,
                    "status": "ok",
                    "notes": "Already Hevea-tagged",
                }
            )
            continue
        updated = update_vendor_and_tags(product, "Hevea", "Hevea")
        hevea_updates += 1
        if hevea_seen % 25 == 0 or hevea_seen == hevea_total:
            print(f"Hevea progress: {hevea_seen}/{hevea_total}")
        report_rows.append(
            {
                "action": "hevea-update",
                "handle": updated.handle,
                "title": updated.title,
                "vendor": updated.vendor,
                "preview_url": updated.preview_url,
                "status": "updated",
                "notes": "Vendor=Hevea; tag=Hevea",
            }
        )

    # Phase 2: Balliu upsert
    balliu_created_or_updated = 0
    for index, (row, target_handle) in enumerate(zip(balliu_rows, balliu_handles), start=1):
        existed = target_handle in store_by_handle
        result = upsert_balliu_product(row, target_handle)
        balliu_created_or_updated += 1
        if index % 25 == 0 or index == len(balliu_rows):
            print(f"Balliu progress: {index}/{len(balliu_rows)}")
        report_rows.append(
            {
                "action": "balliu-update" if existed else "balliu-create",
                "handle": result["handle"],
                "title": result["title"],
                "vendor": result["vendor"],
                "preview_url": result["preview_url"],
                "status": result["status"],
                "notes": f"Tag=Balliu; source_color={row.get('Color Match', '')}",
            }
        )

    write_report(report_rows)
    print(f"Hevea updated: {hevea_updates}")
    print(f"Balliu upserted: {balliu_created_or_updated}")
    print(f"Report: {REPORT_CSV}")


if __name__ == "__main__":
    main()
