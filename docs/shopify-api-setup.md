# Shopify Admin API — Proceso de conexión (desde 2026)

> Las "Custom Apps" desde el Admin y las "Private Apps" ya no están disponibles.
> El único método válido es crear una app en el Partner Dashboard.

---

## Requisitos previos

- Cuenta en [partners.shopify.com](https://partners.shopify.com) (gratuita)
- Shopify CLI instalado: `npm install -g @shopify/cli`
- Node.js instalado

---

## Paso 1 — Crear la app en Partner Dashboard

1. Ir a **partners.shopify.com → Apps → Crear app**
2. Elegir **"Crear app manualmente"**
3. Ponerle nombre (ej. `API-Products`)
4. En la configuración de la app:
   - **URL de la app:** `http://localhost:3000`
   - **URLs de redireccionamiento:** `http://localhost:3000/callback`
   - Marcar ✅ **"Usar flujo de instalación heredado"**
5. En **Scopes / Alcances de API**, añadir los necesarios:
   - `read_products`, `write_products`
   - `read_files`, `write_files`
   - (añadir los que necesite el proyecto)
6. Guardar y anotar el **Client ID** y **Client Secret**

---

## Paso 2 — Vincular con Shopify CLI

En la carpeta del proyecto (debe tener `package.json`):

```bash
# Si no hay package.json:
echo '{"name":"api-products","version":"1.0.0"}' > package.json

# Vincular la app
shopify auth login
shopify app config link --client-id TU_CLIENT_ID

# Desplegar versión
shopify app deploy --client-id TU_CLIENT_ID --allow-updates
```

---

## Paso 3 — Configurar distribución personalizada

1. En Partner Dashboard → **API-Products → Distribución**
2. Seleccionar **"Distribución personalizada"**
3. Introducir el dominio de la tienda: `nombretienda.myshopify.com`
4. Clic en **"Generar enlace"**
5. Copiar el enlace generado (formato: `https://admin.shopify.com/oauth/install_custom_app?...`)

---

## Paso 4 — Obtener el token de acceso

### Opción A — Servidor OAuth local (recomendado)

Crear `get_shopify_token.mjs`:

```javascript
import http from "http";
import { randomBytes } from "crypto";
import { URL } from "url";

const CLIENT_ID     = "TU_CLIENT_ID";
const CLIENT_SECRET = "TU_CLIENT_SECRET";
const SHOP          = "nombretienda.myshopify.com";
const REDIRECT_URI  = "http://localhost:3000/callback";
const SCOPES        = "read_products,write_products,read_files,write_files";
const state         = randomBytes(16).toString("hex");

const authUrl = `https://${SHOP}/admin/oauth/authorize?client_id=${CLIENT_ID}&scope=${SCOPES}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&state=${state}`;

console.log("\nAbre esta URL en el navegador con sesión de Shopify activa:");
console.log(authUrl + "\n");

const server = http.createServer(async (req, res) => {
  const url    = new URL(req.url, "http://localhost:3000");
  const code   = url.searchParams.get("code");
  const rState = url.searchParams.get("state");

  if (!code || rState !== state) {
    res.end("Error: state inválido");
    return;
  }

  const tokenRes = await fetch(`https://${SHOP}/admin/oauth/access_token`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ client_id: CLIENT_ID, client_secret: CLIENT_SECRET, code }),
  });
  const { access_token } = await tokenRes.json();
  console.log("\n✅ TOKEN OBTENIDO:\n\n  ", access_token, "\n");
  res.end("Token obtenido. Puedes cerrar esta ventana.");
  server.close();
});

server.listen(3000, () => console.log("Esperando callback en http://localhost:3000..."));
```

Ejecutar:
```bash
node get_shopify_token.mjs
```

Abrir la URL que imprime → Instalar la app → El token aparece en terminal.

### Opción B — Instalar directo con el enlace del Paso 3

Abrir el enlace generado en el navegador → **Instalar** → El token llega al servidor OAuth.

---

## Paso 5 — Guardar el token

```bash
echo "SHOPIFY_TOKEN=shpat_xxxx" >> .env.local
```

> ⚠️ **Rotar el CLIENT_SECRET** si se compartió en algún chat o correo.
> Partner Dashboard → App → Credenciales → Rotar secreto.

---

## Uso del token en scripts Python

```python
TOKEN = "shpat_xxxx"
SHOP  = "nombretienda.myshopify.com"
API   = f"https://{SHOP}/admin/api/2026-01/graphql.json"

import urllib.request, json

def gql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=payload,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(str(data["errors"]))
    return data["data"]
```

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Esta app no se puede instalar todavía" | Sin método de distribución | Paso 3: configurar distribución personalizada |
| "redirect_uri mismatch" | URL no coincide | App URL y redirect URI deben ser exactamente `http://localhost:3000` y `http://localhost:3000/callback` |
| OAuth lleva al panel de Shopify sin token | `no_redirect=true` en el enlace | Usar el servidor OAuth del Paso 4 antes de abrir el enlace |
| Token `shpca_` en lugar de `shpat_` | App de Partner, no custom app | Es válido igualmente para Admin API |

---

## Scopes más usados

```
read_products, write_products
read_files, write_files
read_orders, write_orders
read_customers, write_customers
read_inventory, write_inventory
read_price_rules, write_price_rules
```

---

*Documentado en el proyecto Muebles Exterior — Marzo 2026*
