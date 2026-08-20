#!/usr/bin/env python3
"""
Anade UNA imagen al final de la galeria de una ficha, SIN borrar ni reordenar nada.

Se separa de publicar_galeria_producto.py a proposito: aquel reemplaza la galeria entera
(sube -> espera READY -> reordena -> borra la vieja). Este solo suma, para casos como
"a esta ficha ya aprobada le falta la imagen de medidas".

  python3 scripts/anadir_imagen_ficha.py <handle> <fichero.jpg> "<texto alternativo>" [--apply]
"""
import sys, os, importlib.util

aqui = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(aqui, "publicar_galeria_producto.py"))
pub = importlib.util.module_from_spec(spec)
sys.argv_backup = sys.argv; sys.argv = [sys.argv[0]]
try: spec.loader.exec_module(pub)
except SystemExit: pass
sys.argv = sys.argv_backup

def main():
    args = [a for a in sys.argv[1:] if a != "--apply"]
    apply_ = "--apply" in sys.argv
    if len(args) < 3:
        print(__doc__); sys.exit(1)
    handle, fichero, alt = args[0], args[1], args[2]
    if not os.path.exists(fichero):
        print(f"  ✗ no existe {fichero}"); sys.exit(1)
    if not alt.strip():
        print("  ✗ sin texto alternativo -- no se sube"); sys.exit(1)

    nodes = pub.gql(pub.Q_PROD, {"h": f"handle:{handle}"})["products"]["nodes"]
    p = nodes[0] if nodes else None
    if not p:
        print(f"  ✗ handle no encontrado: {handle}"); sys.exit(1)
    n = len(p["media"]["nodes"])
    kb = os.path.getsize(fichero)//1024
    print(f"== {p['title']}")
    print(f"   media actuales: {n}   ->   se anade 1 al final")
    print(f"   + {os.path.basename(fichero)}  ({kb} KB)  alt: {alt[:70]}")
    if not apply_:
        print("\n(dry-run: repite con --apply)"); return

    nombre = os.path.basename(fichero)
    tgt = pub.gql(pub.M_STAGED, {"input": [{
        "filename": nombre, "mimeType": "image/jpeg",
        "httpMethod": "POST", "resource": "IMAGE"}]})["stagedUploadsCreate"]["stagedTargets"][0]
    pub.post_multipart(tgt["url"], tgt["parameters"], fichero)
    r = pub.gql(pub.M_CREATE, {"pid": p["id"], "media": [{
        "originalSource": tgt["resourceUrl"], "alt": alt, "mediaContentType": "IMAGE"}]})["productCreateMedia"]
    if r["mediaUserErrors"]:
        print("  ✗", r["mediaUserErrors"]); sys.exit(1)
    nuevos = [m["id"] for m in r["media"]]
    import time
    for _ in range(40):
        time.sleep(4)
        st = pub.gql(pub.Q_STATUS, {"id": p["id"]})["product"]
        estados = {m["id"]: m["status"] for m in st["media"]["nodes"]}
        if all(estados.get(i) == "READY" for i in nuevos):
            print(f"   OK: READY. La ficha pasa a {st['mediaCount']['count']} media"); return
        print("   esperando READY...")
    print("   ✗ no llego a READY")

if __name__ == "__main__":
    main()
