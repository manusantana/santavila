#!/usr/bin/env python3
"""
Sube assets concretos del theme por Shopify Admin Asset API y verifica el remoto.

Uso:
    .venv/bin/python scripts/push_theme_assets.py --theme 189114876228 \
      snippets/meta-tags.liquid sections/santavila-collection-hero.liquid
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOP = "mueblesexterior.myshopify.com"
API_VERSION = "2026-01"


def load_token():
    env_path = os.path.join(ROOT, ".env.local")
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("SHOPIFY_ACCESS_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("No encuentro SHOPIFY_ACCESS_TOKEN en .env.local")


def api(theme_id, method, key=None, value=None, attempts=3):
    url = f"https://{SHOP}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    body = None
    if method == "GET":
        url += "?asset%5Bkey%5D=" + urllib.parse.quote(key)
    elif method == "PUT":
        body = json.dumps({"asset": {"key": key, "value": value}}).encode()

    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": load_token(),
        },
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            print(f"HTTP {e.code} al {method} {key}: {e.read().decode()[:600]}")
            raise
        except Exception:
            if attempt == attempts:
                raise
            time.sleep(attempt * 2)


def list_themes():
    url = f"https://{SHOP}/admin/api/{API_VERSION}/themes.json"
    req = urllib.request.Request(url, headers={"X-Shopify-Access-Token": load_token()})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    for theme in data.get("themes", []):
        print(f"{theme.get('id')}\t{theme.get('role')}\t{theme.get('name')}")


def local_value(key):
    path = os.path.join(ROOT, "theme", key)
    if not os.path.isfile(path):
        sys.exit(f"No existe theme/{key}")
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-themes", action="store_true", help="Lista themes y sale")
    parser.add_argument("--theme", help="Theme ID destino")
    parser.add_argument("keys", nargs="*", help="Asset keys, por ejemplo snippets/meta-tags.liquid")
    args = parser.parse_args()

    if args.list_themes:
        list_themes()
        return
    if not args.theme or not args.keys:
        parser.error("--theme y al menos un asset son obligatorios salvo con --list-themes")

    for key in args.keys:
        value = local_value(key)
        api(args.theme, "PUT", key=key, value=value)
        remote = api(args.theme, "GET", key=key)["asset"]["value"]
        if remote != value:
            sys.exit(f"Verificacion fallida para {key}: remoto != local")
        print(f"✓ {key} subido y verificado en theme {args.theme}")


if __name__ == "__main__":
    main()
