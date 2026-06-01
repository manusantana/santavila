#!/usr/bin/env python3
"""Lista los productos de la cuenta Santavila (5781655181) afectados por cada
problema concreto de Merchant, deduplicados por handle de tienda.
Uso: .venv/bin/python scripts/merchant_issue_products.py
"""
import os, re, sys
from collections import defaultdict

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.path.join(ROOT, "token.json")
MID = "5781655181"
SCOPES = ["https://www.googleapis.com/auth/content"]

# Problemas que nos interesan (por descripción)
TARGETS = ["Low image quality", "Missing unit pricing measure"]

c = Credentials.from_authorized_user_file(TOKEN, SCOPES)
if c.expired and c.refresh_token:
    c.refresh(Request()); open(TOKEN, "w", encoding="utf-8").write(c.to_json())
svc = build("content", "v2.1", credentials=c, cache_discovery=False)

def handle_from_link(link):
    m = re.search(r"/products/([^?/#]+)", link or "")
    return m.group(1) if m else (link or "?")

# desc -> {handle -> (title, link, langs set)}
hits = defaultdict(dict)
req = svc.productstatuses().list(merchantId=MID, maxResults=250)
while req is not None:
    resp = req.execute()
    for p in resp.get("resources", []):
        link = p.get("link", "")
        h = handle_from_link(link)
        for it in p.get("itemLevelIssues", []):
            desc = it.get("description", "")
            for t in TARGETS:
                if desc.startswith(t):
                    rec = hits[t].setdefault(h, {"title": p.get("title", ""), "link": link})
    req = svc.productstatuses().list_next(req, resp) if resp.get("nextPageToken") else None

for t in TARGETS:
    items = hits[t]
    print("\n" + "=" * 80)
    print(f"{t}  —  {len(items)} productos distintos (por handle)")
    print("=" * 80)
    for h, d in sorted(items.items()):
        print(f"  • {h}")
        print(f"      {d['title'][:70]}")
