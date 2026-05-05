/**
 * Obtiene el access token de Shopify via OAuth.
 * Uso: node get_shopify_token.mjs
 */

import http from "http";
import { createHash, randomBytes } from "crypto";
import { exec } from "child_process";
import fs from "fs";

let CLIENT_SECRET = "";
try {
  const envFile = fs.readFileSync(".env", "utf8");
  const match = envFile.match(/SHOPIFY_CLIENT_SECRET=(.*)/);
  if (match) {
    CLIENT_SECRET = match[1].trim();
  }
} catch (e) {
  console.warn("No se pudo leer .env. Asegúrate de crearlo con SHOPIFY_CLIENT_SECRET=...");
}

// ── Configuración ─────────────────────────────────────────
const CLIENT_ID     = "b29216aed8d9ba73423c54a8828cf65d";
const SHOP          = "mueblesexterior.myshopify.com";
const SCOPES        = "read_products,write_products,read_files,write_files,read_content,write_content";
const REDIRECT_URI  = "http://localhost:3000/callback";
const PORT          = 3000;
// ──────────────────────────────────────────────────────────

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
    res.end("Esperando callback...");
    return;
  }

  const returnedState = url.searchParams.get("state");
  const code          = url.searchParams.get("code");

  if (returnedState !== state) {
    res.end("Error: state no coincide. Inténtalo de nuevo.");
    server.close();
    return;
  }

  // Intercambiar código por access token
  const tokenRes = await fetch(
    `https://${SHOP}/admin/oauth/access_token`,
    {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ client_id: CLIENT_ID, client_secret: CLIENT_SECRET, code }),
    }
  );

  const data = await tokenRes.json();

  if (data.access_token) {
    console.log("\n✅ TOKEN OBTENIDO:");
    console.log(`\n   ${data.access_token}\n`);
    console.log("Guárdalo en un lugar seguro. No lo compartas.");
    res.end(`<h1>✅ Token obtenido</h1><p>Revisa la terminal.</p>`);
  } else {
    console.error("Error:", data);
    res.end(`<h1>Error</h1><pre>${JSON.stringify(data, null, 2)}</pre>`);
  }

  server.close();
});

server.listen(PORT, () => {
  console.log(`\nAbriendo navegador para autorizar la app...`);
  console.log(`Si no se abre automáticamente, ve a:\n\n  ${authUrl}\n`);
  exec(`open "${authUrl}"`); // macOS
});
