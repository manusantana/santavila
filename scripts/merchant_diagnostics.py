#!/usr/bin/env python3
"""
Diagnóstico de Google Merchant Center (Content API for Shopping v2.1).
Descubre la cuenta, lista el estado de los productos y agrega los problemas
por gravedad (desaprobado / degradado / aviso) y por tipo de problema.

Uso: .venv/bin/python scripts/merchant_diagnostics.py
"""
import os, sys
from collections import Counter, defaultdict

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(ROOT, "token.json")
SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/content",
]


def creds():
    c = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if c.expired and c.refresh_token:
        c.refresh(Request())
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            f.write(c.to_json())
    return c


def main():
    svc = build("content", "v2.1", credentials=creds(), cache_discovery=False)

    # 1) Descubrir cuenta(s) de Merchant
    try:
        info = svc.accounts().authinfo().execute()
    except HttpError as e:
        sys.exit(f"ERROR Content API (¿API 'shoppingcontent' deshabilitada?): {e}")
    ids = info.get("accountIdentifiers", [])
    if not ids:
        sys.exit("La cuenta autenticada no tiene acceso a ninguna cuenta de Merchant Center.")
    # Elegir la cuenta cuya web sea santavila.com (o por arg)
    target = sys.argv[1] if len(sys.argv) > 1 else None
    mid = None
    print("Cuentas Merchant accesibles:")
    for a in ids:
        m = a.get("merchantId"); agg = a.get("aggregatorId")
        web = name = "?"
        try:
            acc = svc.accounts().get(merchantId=(agg or m), accountId=m).execute()
            web, name = acc.get("websiteUrl", "?"), acc.get("name", "?")
        except HttpError:
            pass
        print(f"  id={m} agg={agg} | {name} | {web}")
        if target and str(m) == target:
            mid = m
        elif not target and isinstance(web, str) and "santavila.com" in web:
            mid = m
    if not mid:
        mid = target or (ids[0].get("merchantId") or ids[0].get("aggregatorId"))
    print(f"\nUsando merchantId = {mid} (Santavila)\n" + "="*70)

    # 2) Listar estado de productos (paginado)
    by_serv = Counter()              # disapproved / demoted / unaffected
    issue_serv = defaultdict(Counter)  # descripción -> Counter(servability)
    issue_examples = {}
    total = 0
    req = svc.productstatuses().list(merchantId=mid, maxResults=250)
    while req is not None:
        resp = req.execute()
        for p in resp.get("resources", []):
            total += 1
            worst = "unaffected"
            for it in p.get("itemLevelIssues", []):
                serv = it.get("servability", "unaffected")
                desc = it.get("description", it.get("code", "?"))
                issue_serv[desc][serv] += 1
                issue_examples.setdefault(desc, {
                    "code": it.get("code"), "attribute": it.get("attributeName"),
                    "resolution": it.get("resolution"), "doc": it.get("documentation"),
                })
                if serv == "disapproved":
                    worst = "disapproved"
                elif serv == "demoted" and worst != "disapproved":
                    worst = "demoted"
            by_serv[worst] += 1
        token = resp.get("nextPageToken")
        req = svc.productstatuses().list_next(req, resp) if token else None

    print(f"PRODUCTOS EN EL FEED: {total}")
    print(f"  ✅ Sin problemas (unaffected):   {by_serv['unaffected']}")
    print(f"  🟡 Degradados/aviso (demoted):   {by_serv['demoted']}")
    print(f"  🔴 Desaprobados (disapproved):   {by_serv['disapproved']}")

    print("\n" + "="*70 + "\nPROBLEMAS POR TIPO (ordenados por nº de productos afectados)")
    print("="*70)
    ranked = sorted(issue_serv.items(), key=lambda kv: -sum(kv[1].values()))
    for desc, servs in ranked:
        ex = issue_examples[desc]
        flag = "🔴" if servs.get("disapproved") else ("🟡" if servs.get("demoted") else "ℹ️")
        tot = sum(servs.values())
        det = " · ".join(f"{k}:{v}" for k, v in servs.items())
        print(f"\n{flag} {desc}  (afecta a {tot} productos · {det})")
        print(f"     code={ex['code']} · atributo={ex['attribute']}")
        if ex.get("resolution"):
            print(f"     resolución sugerida por Google: {ex['resolution']}")


if __name__ == "__main__":
    main()
