#!/usr/bin/env python3
"""Hub GEO de tumbonas de resina + titles/metas striking distance (GEO-DELTA-2026-08-03).

Hace 4 cosas:
1. Crea la coleccion inteligente `tumbonas-de-resina` (tipo Tumbona + titulo contiene
   "resina") con intro citable + FAQ (patron collection-intro/collection-faq del tema)
   y la publica en Online Store.
2. Enlaza el hub desde la intro de la coleccion `tumbonas`.
3. Enlaza el hub desde la guia del blog de tumbonas por material.
4. Aplica SEO titles (y metas donde toca) a las 3 PDP hermanas de resina y a los 4
   productos en striking distance (pergola 300x300x250, sofas 120/130, base parasol).

DRY-RUN por defecto; aplicar con --apply. Backup previo en content/descriptions/.
"""

import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from upload_images import gql  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv

HUB_HANDLE = "tumbonas-de-resina"
GUIA_TUMBONAS = "/blogs/news/tumbona-de-aluminio-resina-o-madera-cual-elegir-para-exterior"
GUIA_MANTENIMIENTO = "/blogs/news/guia-de-mantenimiento-de-muebles-de-exterior-como-prepararlos-para-cada-temporada"

SEP = "<h2>Preguntas frecuentes</h2>"

HUB_TITLE = "Tumbonas de resina"
HUB_SEO_TITLE = "Tumbonas de resina para piscina y jardín | Santavila"
HUB_META = (
    "Tumbonas de resina resistentes al cloro y al sol: línea profesional Balliu Eva Pro "
    "(tablillas o textil) y modelos Noa, Carmen y Lola. Fáciles de limpiar."
)
HUB_BODY = (
    "<p><strong>Las tumbonas de resina son la opción más práctica para piscina y jardín: "
    "resisten el cloro, la humedad y el sol sin oxidarse, pesan poco y se limpian con agua "
    "y jabón.</strong> Aquí reunimos los modelos de resina de Balliu: la línea "
    "<strong>Eva Pro</strong>, pensada para uso intensivo, con superficie de "
    "<strong>tablillas</strong> o <strong>textil</strong>, y modelos como <strong>Noa</strong>, "
    "<strong>Carmen</strong> o <strong>Lola</strong> para uso doméstico. Si dudas entre "
    f"materiales, te lo contamos en la <a href=\"{GUIA_TUMBONAS}\">guía de tumbonas por "
    "material</a>.</p>"
    + SEP
    + "<h3>¿Por qué elegir una tumbona de resina para la piscina?</h3>"
    "<p>La resina no se oxida y aguanta bien el cloro, la humedad y el sol directo. Se limpia "
    "con agua jabonosa y, al ser ligera, es fácil de mover y recolocar alrededor de la piscina.</p>"
    "<h3>¿Qué diferencia hay entre superficie de tablillas y textil?</h3>"
    "<p>Las tablillas forman una superficie rígida de resina, muy fácil de limpiar y pensada "
    "para uso intensivo; la superficie textil aporta una sensación de uso más flexible. Ambas "
    "admiten colchoneta para ganar confort.</p>"
    "<h3>¿Se pueden dejar a la intemperie todo el año?</h3>"
    "<p>La resina soporta bien la intemperie, pero alargarás su vida guardando o cubriendo la "
    "tumbona fuera de temporada, siempre limpia y seca. Tienes el paso a paso en la "
    f"<a href=\"{GUIA_MANTENIMIENTO}\">guía de mantenimiento</a>.</p>"
    "<h3>¿Sirven para hostelería o uso profesional?</h3>"
    "<p>La línea Eva Pro de Balliu está pensada para uso intensivo, como piscinas comunitarias "
    "u hostelería: estructura estable, superficie resistente y limpieza rápida.</p>"
)

# Frase-enlace que se inserta al final de la intro de la coleccion `tumbonas`
TUMBONAS_LINK = (
    " ¿Lo tuyo es la resina? Tienes todos los modelos juntos en la colección de "
    f"<a href=\"/collections/{HUB_HANDLE}\">tumbonas de resina</a>."
)

# Parrafo-enlace para la guia del blog (se inserta antes de la FAQ)
GUIDE_LINK_HTML = (
    "<p>Si ya tienes claro que tu material es la resina, aquí tienes juntas todas las "
    f"<a href=\"/collections/{HUB_HANDLE}\">tumbonas de resina</a> disponibles.</p>"
)

# handle -> {seo title, seo description (None = conservar la actual)}
PRODUCT_SEO = {
    "balliu-tumbona-de-exterior-resina-28ff014d": {
        "title": "Tumbona de resina Noa · piscina y jardín | Santavila",
        "description": (
            "Tumbona de resina Noa: ligera, fácil de limpiar y resistente al cloro, la humedad "
            "y el sol. Pensada para piscina, jardín y terraza de uso frecuente."
        ),
    },
    "balliu-tumbona-de-exterior-resina-923110d9": {
        "title": "Tumbona de resina profesional Eva Pro T · tablillas Ø73 cm",
        "description": (
            "Tumbona de resina Balliu Eva Pro T con superficie de tablillas Ø73 cm. Línea "
            "profesional para piscina y hostelería: resistente al uso intensivo y de limpieza rápida."
        ),
    },
    "balliu-tumbona-de-exterior-resina-b19af1ea": {
        "title": "Tumbona de resina profesional Eva Pro · textil Ø73 cm",
        "description": (
            "Tumbona de resina Balliu Eva Pro con superficie textil Ø73 cm, de sensación más "
            "flexible. Línea profesional para piscina, solárium y uso intensivo."
        ),
    },
    "pergola-aluminio-para-jardin-300300250-cm": {
        "title": "Pérgola de aluminio 300×300 cm · altura 250 cm | Santavila",
        "description": None,
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-12078-cm": {
        "title": "Sofá terraza 120 cm · 2 plazas exterior | Santavila",
        "description": None,
    },
    "sofa-terraza-2-plazas-estilo-contemporaneo-13090-cm": {
        "title": "Sofá exterior 130 cm · 2 plazas terraza | Santavila",
        "description": None,
    },
    "base-de-parasol-25-kg": {
        "title": "Base de parasol 25 kg para sombrilla | Santavila",
        "description": None,
    },
}

Q_COLLECTION = """query($h:String!){ collectionByHandle(handle:$h){ id title descriptionHtml seo{title description} } }"""
M_COLLECTION_CREATE = """
mutation($input: CollectionInput!) {
  collectionCreate(input: $input) { collection { id handle } userErrors { field message } }
}"""
M_COLLECTION_UPDATE = """
mutation($input: CollectionInput!) {
  collectionUpdate(input: $input) { collection { id handle } userErrors { field message } }
}"""
Q_PUBLICATIONS = """query { publications(first: 10) { nodes { id name } } }"""
M_PUBLISH = """
mutation($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) { userErrors { field message } }
}"""
Q_PRODUCT = """query($h:String!){ productByHandle(handle:$h){ id title seo{title description} } }"""
M_PRODUCT = """
mutation($input: ProductInput!) {
  productUpdate(input: $input) { product { id } userErrors { field message } }
}"""
Q_ARTICLES = """
query { articles(first: 50) { nodes { id handle title body } } }"""
M_ARTICLE = """
mutation($article: ArticleUpdateInput!, $id: ID!) {
  articleUpdate(article: $article, id: $id) { article { id } userErrors { field message } }
}"""


def check(res, label):
    errs = res.get("userErrors")
    if errs:
        raise SystemExit(f"{label}: {errs}")


def main():
    backup = {}
    print("APLICAR" if APPLY else "DRY-RUN")

    # 1) coleccion hub
    existing = gql(Q_COLLECTION, {"h": HUB_HANDLE})["collectionByHandle"]
    if existing:
        print(f"• hub ya existe ({existing['id']}) -> update")
        backup["hub"] = existing
        if APPLY:
            res = gql(M_COLLECTION_UPDATE, {"input": {
                "id": existing["id"], "descriptionHtml": HUB_BODY,
                "seo": {"title": HUB_SEO_TITLE, "description": HUB_META},
            }})["collectionUpdate"]
            check(res, "hub update")
    else:
        print("• crear coleccion inteligente tumbonas-de-resina (Tumbona + resina)")
        if APPLY:
            res = gql(M_COLLECTION_CREATE, {"input": {
                "title": HUB_TITLE,
                "handle": HUB_HANDLE,
                "descriptionHtml": HUB_BODY,
                "seo": {"title": HUB_SEO_TITLE, "description": HUB_META},
                "ruleSet": {"appliedDisjunctively": False, "rules": [
                    {"column": "TYPE", "relation": "EQUALS", "condition": "Tumbona"},
                    {"column": "TITLE", "relation": "CONTAINS", "condition": "resina"},
                ]},
            }})["collectionCreate"]
            check(res, "hub create")
            hub_id = res["collection"]["id"]
            pubs = gql(Q_PUBLICATIONS)["publications"]["nodes"]
            online = [p for p in pubs if p["name"] == "Online Store"]
            if online:
                pres = gql(M_PUBLISH, {"id": hub_id, "input": [{"publicationId": online[0]["id"]}]})["publishablePublish"]
                check(pres, "hub publish")
                print(f"  publicado en Online Store ({hub_id})")
            else:
                print("  ⚠️ no se encontro publication 'Online Store' — publicar a mano")

    # 2) enlace desde coleccion tumbonas
    tumb = gql(Q_COLLECTION, {"h": "tumbonas"})["collectionByHandle"]
    backup["tumbonas"] = tumb
    if f"/collections/{HUB_HANDLE}" in (tumb["descriptionHtml"] or ""):
        print("• coleccion tumbonas: enlace ya presente, no se toca")
    else:
        parts = tumb["descriptionHtml"].split(SEP, 1)
        intro = parts[0]
        if intro.rstrip().endswith("</p>"):
            idx = intro.rstrip().rfind("</p>")
            new_intro = intro.rstrip()[:idx] + TUMBONAS_LINK + "</p>"
        else:
            new_intro = intro + f"<p>{TUMBONAS_LINK.strip()}</p>"
        new_body = new_intro + (SEP + parts[1] if len(parts) > 1 else "")
        print("• coleccion tumbonas: se añade frase-enlace al hub en la intro")
        if APPLY:
            res = gql(M_COLLECTION_UPDATE, {"input": {"id": tumb["id"], "descriptionHtml": new_body}})["collectionUpdate"]
            check(res, "tumbonas update")

    # 3) enlace desde la guia del blog
    arts = gql(Q_ARTICLES)["articles"]["nodes"]
    guide = next((a for a in arts if a["handle"] == GUIA_TUMBONAS.split("/")[-1]), None)
    if not guide:
        raise SystemExit("guia de tumbonas no encontrada")
    backup["guia"] = {"id": guide["id"], "handle": guide["handle"], "body": guide["body"]}
    if f"/collections/{HUB_HANDLE}" in guide["body"]:
        print("• guia tumbonas: enlace ya presente, no se toca")
    else:
        body = guide["body"]
        if SEP in body:
            body = body.replace(SEP, GUIDE_LINK_HTML + SEP, 1)
        elif "<h2>Preguntas frecuentes" in body:
            i = body.index("<h2>Preguntas frecuentes")
            body = body[:i] + GUIDE_LINK_HTML + body[i:]
        else:
            body = body + GUIDE_LINK_HTML
        print("• guia tumbonas: se inserta parrafo-enlace al hub antes de la FAQ")
        if APPLY:
            res = gql(M_ARTICLE, {"id": guide["id"], "article": {"body": body}})["articleUpdate"]
            check(res, "guia update")

    # 4) SEO titles/metas de productos
    for handle, seo in PRODUCT_SEO.items():
        p = gql(Q_PRODUCT, {"h": handle})["productByHandle"]
        if not p:
            print(f"✗ {handle}: no encontrado")
            continue
        backup[handle] = p
        new_seo = {"title": seo["title"]}
        if seo["description"]:
            new_seo["description"] = seo["description"]
        print(f"• {handle}\n    seo.title: {p['seo']['title']!r} -> {seo['title']!r}")
        if seo["description"]:
            print(f"    seo.desc actualizada ({len(seo['description'])} chars)")
        if APPLY:
            res = gql(M_PRODUCT, {"input": {"id": p["id"], "seo": new_seo}})["productUpdate"]
            check(res, handle)

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = os.path.join(ROOT, "content", "descriptions", f"backup_geo_hub_{ts}.json")
    json.dump(backup, open(bpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n💾 Backup -> {bpath}")
    print("✅ Aplicado" if APPLY else "ℹ️ Dry-run (nada tocado)")


if __name__ == "__main__":
    main()
