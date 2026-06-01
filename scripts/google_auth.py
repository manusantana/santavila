#!/usr/bin/env python3
"""
Autorización OAuth (desktop) para Google Search Console + GA4.
- NO toca gcloud ni el ADC del sistema. Solo usa el client_secret descargado.
- Guarda el token en token.json (gitignored).
- Tras autorizar, verifica acceso listando sitios de Search Console y cuentas GA4.

Uso:
    python3 scripts/google_auth.py
"""
import glob
import os
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(ROOT, "token.json")

SCOPES = [
    "https://www.googleapis.com/auth/webmasters",        # Search Console (lectura + enviar sitemap)
    "https://www.googleapis.com/auth/analytics.readonly",  # GA4 lectura
    "https://www.googleapis.com/auth/content",            # Merchant Center / Content API for Shopping
]


def find_client_secret():
    matches = glob.glob(os.path.join(ROOT, ".client_secret*.json")) + \
              glob.glob(os.path.join(ROOT, "client_secret*.json"))
    if not matches:
        sys.exit("ERROR: no encuentro el archivo client_secret*.json en la raíz del repo.")
    return matches[0]


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        cs = find_client_secret()
        print(f"Usando client_secret: {os.path.basename(cs)}")
        flow = InstalledAppFlow.from_client_secrets_file(cs, SCOPES)
        # Abre el navegador y espera el callback en localhost
        creds = flow.run_local_server(port=0, prompt="consent")
    with open(TOKEN_PATH, "w") as f:
        f.write(creds.to_json())
    print(f"✅ Token guardado en {TOKEN_PATH}")
    return creds


def verify(creds):
    print("\n===== Verificación de acceso =====")
    # Search Console
    try:
        sc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
        sites = sc.sites().list().execute()
        entries = sites.get("siteEntry", [])
        if entries:
            print("Search Console — propiedades accesibles:")
            for s in entries:
                print(f"  · {s.get('siteUrl')}  [{s.get('permissionLevel')}]")
        else:
            print("Search Console — autenticado, pero esta cuenta no tiene propiedades.")
    except HttpError as e:
        print(f"Search Console — ERROR API: {e}")
    except Exception as e:
        print(f"Search Console — ERROR: {e}")

    # GA4 (Admin API para listar cuentas/propiedades)
    try:
        admin = build("analyticsadmin", "v1beta", credentials=creds, cache_discovery=False)
        accts = admin.accounts().list().execute()
        items = accts.get("accounts", [])
        if items:
            print("\nGA4 — cuentas accesibles:")
            for a in items:
                print(f"  · {a.get('displayName')}  ({a.get('name')})")
        else:
            print("\nGA4 — autenticado, pero sin cuentas accesibles.")
    except HttpError as e:
        print(f"\nGA4 — ERROR API (¿API deshabilitada?): {e}")
    except Exception as e:
        print(f"\nGA4 — ERROR: {e}")


if __name__ == "__main__":
    creds = get_credentials()
    verify(creds)
