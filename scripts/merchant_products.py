#!/usr/bin/env python3
"""Lista los productos del feed de Merchant (cuenta Santavila) y los agrega por
idioma declarado (contentLanguage), país y feedLabel. Muestra un título de ejemplo
por grupo para ver en qué idioma está realmente el contenido.
Uso: .venv/bin/python scripts/merchant_products.py [merchantId]
"""
import os, sys
from collections import Counter

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.path.join(ROOT, "token.json")
MID = sys.argv[1] if len(sys.argv) > 1 else "5781655181"
SCOPES = ["https://www.googleapis.com/auth/content"]

c = Credentials.from_authorized_user_file(TOKEN, SCOPES)
if c.expired and c.refresh_token:
    c.refresh(Request()); open(TOKEN, "w", encoding="utf-8").write(c.to_json())
svc = build("content", "v2.1", credentials=c, cache_discovery=False)

groups = Counter()
sample = {}
total = 0
req = svc.products().list(merchantId=MID, maxResults=250)
while req is not None:
    resp = req.execute()
    for p in resp.get("resources", []):
        total += 1
        key = (p.get("contentLanguage"), p.get("targetCountry"), p.get("feedLabel"), p.get("channel"))
        groups[key] += 1
        if key not in sample:
            sample[key] = p.get("title", "")
    req = svc.products().list_next(req, resp) if resp.get("nextPageToken") else None

print(f"Cuenta {MID} — {total} entradas en el feed\n")
print(f"{'idioma':<8}{'país':<6}{'feedLabel':<12}{'canal':<10}{'nº':>6}  ejemplo de título")
print("-" * 100)
for key, n in groups.most_common():
    lang, country, fl, ch = key
    print(f"{str(lang):<8}{str(country):<6}{str(fl):<12}{str(ch):<10}{n:>6}  {sample[key][:48]}")
