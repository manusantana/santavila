#!/usr/bin/env python3
"""
Oportunidades GSC para santavila.com (ventana 90 días):
- Pares (página, query) para ver qué busca cada URL.
- "Striking distance": queries en posición 4-20 con impresiones (a tiro de top 3).
Uso: .venv/bin/python scripts/gsc_opportunities.py
"""
import os
from datetime import date, timedelta
from collections import defaultdict

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(ROOT, "token.json")
SITE = "sc-domain:santavila.com"
SCOPES = ["https://www.googleapis.com/auth/webmasters",
          "https://www.googleapis.com/auth/analytics.readonly"]


def creds():
    c = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if c.expired and c.refresh_token:
        c.refresh(Request())
        open(TOKEN_PATH, "w").write(c.to_json())
    return c


sc = build("searchconsole", "v1", credentials=creds(), cache_discovery=False)
end = date.today() - timedelta(days=1)
start = end - timedelta(days=89)


def query(dims, limit=1000):
    body = {"startDate": start.isoformat(), "endDate": end.isoformat(),
            "dimensions": dims, "rowLimit": limit}
    return sc.searchanalytics().query(siteUrl=SITE, body=body).execute().get("rows", [])


print(f"Ventana: {start} → {end}\n")

rows = query(["page", "query"], 1000)

# Agrupar por página
by_page = defaultdict(list)
for r in rows:
    page, q = r["keys"]
    by_page[page].append((q, r["clicks"], r["impressions"], r["ctr"], r["position"]))

# Striking distance: pos 4-20, impresiones >= 1
striking = [(r["keys"][1], r["keys"][0], r["impressions"], r["position"], r["clicks"])
            for r in rows if 4 <= r["position"] <= 20 and r["impressions"] >= 1]
striking.sort(key=lambda x: (-x[2], x[3]))

print("=" * 90)
print("STRIKING DISTANCE — queries en pos 4-20 (ordenadas por impresiones)")
print("=" * 90)
print(f"{'query':<38}{'impr':>5}{'pos':>6}  página")
print("-" * 90)
for q, page, impr, pos, clicks in striking[:30]:
    short = page.replace("https://santavila.com", "").replace("http://santavila.com", "")
    print(f"{q[:37]:<38}{impr:>5.0f}{pos:>6.1f}  {short[:34]}")

print("\n" + "=" * 90)
print("DESGLOSE POR PÁGINA (solo páginas ES, con sus queries)")
print("=" * 90)
for page in sorted(by_page, key=lambda p: -sum(x[2] for x in by_page[p])):
    if "/en/" in page:
        continue
    short = page.replace("https://santavila.com", "").replace("http://santavila.com", "") or "/"
    tot_impr = sum(x[2] for x in by_page[page])
    tot_clicks = sum(x[1] for x in by_page[page])
    print(f"\n▸ {short}   (impr={tot_impr:.0f}, clicks={tot_clicks:.0f})")
    for q, c, impr, ctr, pos in sorted(by_page[page], key=lambda x: -x[2])[:8]:
        print(f"    {q[:42]:<44} impr={impr:>3.0f} pos={pos:>4.1f} clicks={c:.0f}")
