#!/usr/bin/env python3
"""
Actualiza solo el titulo de una coleccion Shopify por GraphQL.

Uso:
    .venv/bin/python scripts/update_shopify_collection_title.py 659834831172 "Sofás de exterior"
"""
import json
import os
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOP = "mueblesexterior.myshopify.com"
API_VERSION = "2026-01"


def load_token():
    with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
        for line in f:
            if line.startswith("SHOPIFY_ACCESS_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("No encuentro SHOPIFY_ACCESS_TOKEN en .env")


def graphql(query, variables):
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/{API_VERSION}/graphql.json",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": load_token(),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:600]}")
        raise


def main():
    if len(sys.argv) != 3:
        sys.exit('Uso: update_shopify_collection_title.py <collection_id_num> "Nuevo titulo"')
    collection_id, title = sys.argv[1], sys.argv[2]
    gid = f"gid://shopify/Collection/{collection_id}"
    mutation = """
    mutation UpdateCollectionTitle($input: CollectionInput!) {
      collectionUpdate(input: $input) {
        collection {
          id
          handle
          title
        }
        userErrors {
          field
          message
        }
      }
    }
    """
    data = graphql(mutation, {"input": {"id": gid, "title": title}})
    if data.get("errors"):
        sys.exit(json.dumps(data["errors"], ensure_ascii=False))
    result = data["data"]["collectionUpdate"]
    if result["userErrors"]:
        sys.exit(json.dumps(result["userErrors"], ensure_ascii=False))
    col = result["collection"]
    print(f"✓ Coleccion actualizada: {col['handle']} -> {col['title']}")


if __name__ == "__main__":
    main()
