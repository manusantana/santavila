#!/usr/bin/env python3
"""
Baseline de Google Search Console para santavila.com.
- Lista sitemaps registrados (y su estado).
- Envía el sitemap si no está registrado (--submit).
- Pulla Search Analytics de los últimos 28 días: totales, top queries, top páginas.
- Guarda un informe en SEO-BASELINE.md.

Uso:
    .venv/bin/python scripts/gsc_baseline.py            # solo lee y reporta
    .venv/bin/python scripts/gsc_baseline.py --submit   # además envía el sitemap
"""
import os
import sys
from datetime import date, timedelta

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(ROOT, "token.json")
SITE = "sc-domain:santavila.com"
SITEMAP_URL = "https://santavila.com/sitemap.xml"
SCOPES = [
    "https://www.googleapis.com/auth/webmasters",
    "https://www.googleapis.com/auth/analytics.readonly",
]
SUBMIT = "--submit" in sys.argv


def creds():
    c = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if c.expired and c.refresh_token:
        c.refresh(Request())
        with open(TOKEN_PATH, "w") as f:
            f.write(c.to_json())
    return c


def fmt_row(cells, widths):
    return " | ".join(str(c)[:w].ljust(w) for c, w in zip(cells, widths))


def main():
    sc = build("searchconsole", "v1", credentials=creds(), cache_discovery=False)
    out = []
    def log(s=""):
        print(s)
        out.append(s)

    log(f"# Baseline SEO — Search Console")
    log(f"\n**Propiedad:** {SITE}  ·  **Fecha:** {date.today().isoformat()}\n")

    # ---- Sitemaps ----
    log("## Sitemaps registrados\n")
    try:
        sm = sc.sitemaps().list(siteUrl=SITE).execute()
        paths = [s.get("path") for s in sm.get("sitemap", [])]
        if paths:
            for s in sm.get("sitemap", []):
                log(f"- `{s.get('path')}` — última descarga: {s.get('lastDownloaded','n/a')} · "
                    f"errores: {s.get('errors','0')} · warnings: {s.get('warnings','0')}")
        else:
            log("- (ninguno registrado)")
        if SITEMAP_URL not in paths:
            if SUBMIT:
                sc.sitemaps().submit(siteUrl=SITE, feedpath=SITEMAP_URL).execute()
                log(f"\n✅ Sitemap enviado: {SITEMAP_URL}")
            else:
                log(f"\n⚠️ {SITEMAP_URL} NO está registrado. Relanza con --submit para enviarlo.")
        else:
            log(f"\n✅ {SITEMAP_URL} ya está registrado.")
    except HttpError as e:
        log(f"ERROR sitemaps: {e}")

    # ---- Search Analytics (28d) ----
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=27)
    log(f"\n## Rendimiento (28 días: {start} → {end})\n")

    def query(dimensions, limit=25):
        body = {
            "startDate": start.isoformat(),
            "endDate": end.isoformat(),
            "dimensions": dimensions,
            "rowLimit": limit,
        }
        return sc.searchanalytics().query(siteUrl=SITE, body=body).execute().get("rows", [])

    try:
        totals = query([], limit=1)
        if totals:
            t = totals[0]
            log(f"- **Clics:** {t.get('clicks',0):.0f}")
            log(f"- **Impresiones:** {t.get('impressions',0):.0f}")
            log(f"- **CTR:** {t.get('ctr',0)*100:.2f}%")
            log(f"- **Posición media:** {t.get('position',0):.1f}")
        else:
            log("- Sin datos de rendimiento todavía (propiedad nueva o sin impresiones).")
    except HttpError as e:
        log(f"ERROR totales: {e}")

    for dim, title in [("query", "Top consultas"), ("page", "Top páginas")]:
        try:
            rows = query([dim], limit=25)
            log(f"\n### {title}\n")
            if not rows:
                log("(sin datos)")
                continue
            w = [50, 7, 7, 7, 6]
            log("```")
            log(fmt_row([dim, "clicks", "impr", "ctr%", "pos"], w))
            log("-" * (sum(w) + 12))
            for r in rows:
                k = r["keys"][0]
                log(fmt_row([k, f"{r['clicks']:.0f}", f"{r['impressions']:.0f}",
                             f"{r['ctr']*100:.1f}", f"{r['position']:.1f}"], w))
            log("```")
        except HttpError as e:
            log(f"ERROR {dim}: {e}")

    # Guardar informe
    report = os.path.join(ROOT, "SEO-BASELINE.md")
    with open(report, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"\n💾 Informe guardado en {report}")


if __name__ == "__main__":
    main()
