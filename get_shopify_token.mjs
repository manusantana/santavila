/**
 * Obtiene el access token de Shopify vía OAuth.
 *
 * Lee la configuración desde .env / .env.local (prioridad: .env.local > .env):
 *   SHOPIFY_CLIENT_ID       = client id de la app en Partner Dashboard
 *   SHOPIFY_CLIENT_SECRET   = client secret de la app
 *   SHOPIFY_SHOP            = mueblesexterior.myshopify.com (opcional, default este)
 *   SHOPIFY_APP_SCOPES      = lista separada por comas (opcional, default amplio)
 *
 * Uso:
 *   node get_shopify_token.mjs
 *
 * Salida: imprime el access token en consola. Cópialo a .env.local como
 *   SHOPIFY_ACCESS_TOKEN=shpat_xxxx  (o shpca_xxxx según el tipo de app)
 */

import http from "http";
import { randomBytes } from "crypto";
import { exec } from "child_process";
import fs from "fs";

// ── Cargar variables de entorno ───────────────────────────────────────────────

function loadEnv() {
  const env = {};
  for (const fname of [".env", ".env.local"]) {  // .env.local pisa a .env
    if (!fs.existsSync(fname)) continue;
    const content = fs.readFileSync(fname, "utf8");
    for (const line of content.split("\n")) {
      const m = line.match(/^([A-Z_][A-Z0-9_]*)=(.*)$/);
      if (!m) continue;
      env[m[1]] = m[2].trim().replace(/^["']|["']$/g, "");
    }
  }
  return env;
}

const env = loadEnv();

const CLIENT_ID     = env.SHOPIFY_CLIENT_ID;
const CLIENT_SECRET = env.SHOPIFY_CLIENT_SECRET;
const SHOP          = env.SHOPIFY_SHOP || "mueblesexterior.myshopify.com";
const REDIRECT_URI  = "http://localhost:3000/callback";
const PORT          = 3000;

// Scopes por defecto: cubre Sprint 1-2 completo (productos, archivos, contenido,
// idiomas, envíos, themes, traducciones, pedidos, inventario, publicaciones).
const DEFAULT_SCOPES = [
  "read_products", "write_products",
  "read_files", "write_files",
  "read_content", "write_content",
  "read_shipping", "write_shipping",
  "read_themes", "write_themes",
  "read_locales",
  "read_translations", "write_translations",
  "read_orders", "write_orders",
  "read_inventory", "write_inventory",
  "read_publications", "write_publications",
].join(",");
const SCOPES = env.SHOPIFY_APP_SCOPES || DEFAULT_SCOPES;

// ── Validación ────────────────────────────────────────────────────────────────

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error("\n✗ Faltan variables en .env / .env.local:");
  if (!CLIENT_ID)     console.error("   - SHOPIFY_CLIENT_ID");
  if (!CLIENT_SECRET) console.error("   - SHOPIFY_CLIENT_SECRET");
  console.error("\nObtén ambos desde Partner Dashboard → tu app → Client credentials.\n");
  process.exit(1);
}

console.log("\n── Config para OAuth ──");
console.log(`   Shop:      ${SHOP}`);
console.log(`   Client ID: ${CLIENT_ID.slice(0, 8)}…`);
console.log(`   Scopes:    ${SCOPES.split(",").length} scopes`);
console.log(`              ${SCOPES.split(",").join("\n              ")}`);
console.log("");

// ── OAuth flow ────────────────────────────────────────────────────────────────

const state = randomBytes(16).toString("hex");

const authUrl =
  `https://${SHOP}/admin/oauth/authorize` +
  `?client_id=${CLIENT_ID}` +
  `&scope=${SCOPES}` +
  `&redirect_uri=${encodeURIComponent(REDIRECT_URI)}` +
  `&state=${state}`;

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (url.pathname !== "/callback") {
    res.end("Esperando callback de Shopify...");
    return;
  }

  const returnedState = url.searchParams.get("state");
  const code          = url.searchParams.get("code");

  if (returnedState !== state) {
    res.end("Error: state no coincide. Inténtalo de nuevo.");
    server.close();
    return;
  }

  let tokenRes, body, data;
  try {
    tokenRes = await fetch(
      `https://${SHOP}/admin/oauth/access_token`,
      {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ client_id: CLIENT_ID, client_secret: CLIENT_SECRET, code }),
      }
    );
    body = await tokenRes.text();   // leer como texto primero, parsear después
  } catch (e) {
    console.error("\n✗ Error de red al canjear el código:", e.message);
    res.end(`<h1>Error de red</h1><pre>${e.message}</pre>`);
    server.close();
    return;
  }

  const ct = tokenRes.headers.get("content-type") || "";
  if (!ct.includes("application/json")) {
    console.error(`\n✗ Shopify respondió con ${tokenRes.status} y Content-Type "${ct}".`);
    console.error("   Causa probable: CLIENT_SECRET incorrecto, app no instalada, o scopes mal guardados.");
    console.error("\n── Respuesta cruda (primeros 400 chars) ──");
    console.error(body.slice(0, 400));
    console.error("\nQué hacer:");
    console.error("  1. Verifica en Partner Dashboard → tu app → Client credentials");
    console.error("     que el SHOPIFY_CLIENT_SECRET de .env.local coincide.");
    console.error("  2. Verifica que la app está instalada en la tienda (Distribution → Custom).");
    console.error("  3. Relanza: node get_shopify_token.mjs\n");
    res.end(`<h1>Error: respuesta no-JSON de Shopify</h1><pre>HTTP ${tokenRes.status}\n\n${body.slice(0, 800).replace(/[<>&]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]))}</pre>`);
    server.close();
    return;
  }

  try {
    data = JSON.parse(body);
  } catch (e) {
    console.error("\n✗ JSON inválido pese a content-type JSON:", e.message);
    console.error(body.slice(0, 400));
    res.end("<h1>Error parseando respuesta</h1>");
    server.close();
    return;
  }

  if (data.access_token) {
    console.log("\n✅ TOKEN OBTENIDO:\n");
    console.log(`   ${data.access_token}\n`);
    console.log(`   Scope asignado: ${data.scope || "(no devuelto)"}\n`);
    console.log("Siguiente paso:");
    console.log("  1. Copiar el token de arriba.");
    console.log("  2. Editar .env.local y reemplazar SHOPIFY_ACCESS_TOKEN=<token-anterior>");
    console.log("     por SHOPIFY_ACCESS_TOKEN=<token-nuevo>.");
    console.log("  3. Validar: python3 assign_products_to_shipping_profiles.py --list\n");
    res.end(`<h1>✅ Token obtenido</h1><p>Revisa la terminal y pégalo en .env.local.</p>`);
  } else {
    console.error("\n✗ Error obteniendo token:", data);
    res.end(`<h1>Error</h1><pre>${JSON.stringify(data, null, 2)}</pre>`);
  }

  server.close();
});

server.listen(PORT, () => {
  console.log(`Abriendo navegador para autorizar la app...`);
  console.log(`Si no se abre automáticamente, abre esta URL en un navegador con sesión de ${SHOP}:\n`);
  console.log(`  ${authUrl}\n`);
  exec(`open "${authUrl}"`);  // macOS
});
