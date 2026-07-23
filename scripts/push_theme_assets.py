#!/usr/bin/env python3
"""
Sube assets concretos del theme por Shopify Admin Asset API y verifica el remoto.

Flujo oficial (ver docs/santavila/WORKFLOW_STAGING_PRODUCCION.md):
  1) se prueba en STAGING, 2) se valida, 3) se promociona a PRODUCCIÓN con confirmación.

Uso:
    # a staging (sin fricción)
    python3 scripts/push_theme_assets.py --theme staging \
      snippets/meta-tags.liquid sections/santavila-collection-hero.liquid

    # a producción (REQUIERE confirmación explícita — guardia fail-closed)
    python3 scripts/push_theme_assets.py --theme prod \
      --prod-confirm "validado en staging + ok de Sergio" sections/santavila-hero.liquid

Aliases de --theme: prod/production/live, staging/stage, dev/development, o el ID numérico.
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

# IDs reales verificados 2026-06-30 (ver WORKFLOW_STAGING_PRODUCCION.md)
PROD_THEME = "189222715716"      # main / publicado — NO cambia nunca
STAGING_THEME = "189491151172"   # unpublished — banco de pruebas
DEV_THEME = "189114876228"       # legacy, divergido — NO usar como gate

THEME_ALIASES = {
    "prod": PROD_THEME, "production": PROD_THEME, "live": PROD_THEME,
    "staging": STAGING_THEME, "stage": STAGING_THEME,
    "dev": DEV_THEME, "development": DEV_THEME,
}


def resolve_theme(value):
    """Traduce un alias a su ID; deja pasar un ID numérico tal cual."""
    if value is None:
        return None
    key = value.strip().lower()
    if key in THEME_ALIASES:
        return THEME_ALIASES[key]
    if value.strip().isdigit():
        return value.strip()
    sys.exit(f"--theme '{value}' no reconocido. Usa: prod, staging, dev o un ID numérico.")


def load_token():
    """Lee SHOPIFY_ACCESS_TOKEN de .envlocal (o .env.local como respaldo)."""
    for fn in (".envlocal", ".env.local"):
        env_path = os.path.join(ROOT, fn)
        if not os.path.isfile(env_path):
            continue
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("SHOPIFY_ACCESS_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("No encuentro SHOPIFY_ACCESS_TOKEN en .envlocal ni en .env.local")


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
    parser.add_argument("--theme", help="Destino: prod, staging, dev o ID numérico")
    parser.add_argument(
        "--prod-confirm", metavar="MOTIVO",
        help="OBLIGATORIO para subir a PRODUCCIÓN. Texto con el motivo/confirmación.",
    )
    parser.add_argument("keys", nargs="*", help="Asset keys, por ejemplo snippets/meta-tags.liquid")
    args = parser.parse_args()

    if args.list_themes:
        list_themes()
        return
    if not args.theme or not args.keys:
        parser.error("--theme y al menos un asset son obligatorios salvo con --list-themes")

    theme_id = resolve_theme(args.theme)

    # Guardia fail-closed: no se sube a PRODUCCIÓN sin confirmación explícita.
    if theme_id == PROD_THEME:
        if not args.prod_confirm or not args.prod_confirm.strip():
            sys.exit(
                "\n⛔ BLOQUEADO: destino = PRODUCCIÓN (tema publicado).\n"
                "   El flujo exige validar en STAGING y confirmación explícita del dueño.\n"
                "   Si de verdad está validado y con 'ok', repite con:\n"
                "     --prod-confirm \"validado en staging + ok de Sergio\"\n"
                "   (ver docs/santavila/WORKFLOW_STAGING_PRODUCCION.md)\n"
            )
        print(f"⚠️  Subiendo a PRODUCCIÓN {theme_id} · confirmación: {args.prod_confirm!r}\n")

    failures = []
    for key in args.keys:
        value = local_value(key)
        api(theme_id, "PUT", key=key, value=value)
        # La Asset API puede devolver aún la versión anterior justo tras el PUT
        # (propagación). Reintentamos la verificación antes de darla por fallida,
        # y NO abortamos el resto de archivos si uno no cuadra.
        ok = False
        for intento in range(4):
            remote = api(theme_id, "GET", key=key)["asset"]["value"]
            if remote == value:
                ok = True
                break
            time.sleep(1.5 * (intento + 1))
        if ok:
            print(f"✓ {key} subido y verificado en theme {theme_id}")
        else:
            print(f"⚠️  {key}: subido, pero la verificación no cuadró tras varios reintentos (revisar manualmente)")
            failures.append(key)

    if failures:
        sys.exit(f"\nVerificación no confirmada para: {', '.join(failures)}")


if __name__ == "__main__":
    main()
