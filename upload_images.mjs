/**
 * Sube las imágenes optimizadas a Shopify CDN y actualiza los productos.
 * Uso: node upload_images.mjs
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

import fs from "fs";
let TOKEN = "";
try {
  const envFile = fs.readFileSync(".env", "utf8");
  const match = envFile.match(/SHOPIFY_ACCESS_TOKEN=(.*)/);
  if (match) TOKEN = match[1].trim();
} catch (e) {}
const SHOP  = "mueblesexterior.myshopify.com";
const API   = `https://${SHOP}/admin/api/2026-01/graphql.json`;
const BASE  = path.dirname(fileURLToPath(import.meta.url));

// ── GraphQL helper ────────────────────────────────────────────────────────────

async function gql(query, variables = {}) {
  const res = await fetch(API, {
    method:  "POST",
    headers: { "X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json" },
    body:    JSON.stringify({ query, variables }),
  });
  const json = await res.json();
  if (json.errors) throw new Error(JSON.stringify(json.errors));
  return json.data;
}

// ── Staged upload ─────────────────────────────────────────────────────────────

async function stagedUpload(filename, mimeType, fileSize) {
  const data = await gql(`
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets {
          url
          resourceUrl
          parameters { name value }
        }
        userErrors { field message }
      }
    }
  `, {
    input: [{
      filename,
      mimeType,
      fileSize: String(fileSize),
      resource: "IMAGE",
      httpMethod: "POST",
    }],
  });
  const errs = data.stagedUploadsCreate.userErrors;
  if (errs.length) throw new Error(errs.map(e => e.message).join(", "));
  return data.stagedUploadsCreate.stagedTargets[0];
}

async function uploadToS3(target, filePath, mimeType) {
  const fileBuffer = fs.readFileSync(filePath);
  const boundary   = "----FormBoundary" + Math.random().toString(36).slice(2);

  let headerStr = "";
  for (const { name, value } of target.parameters) {
    headerStr += `--${boundary}\r\nContent-Disposition: form-data; name="${name}"\r\n\r\n${value}\r\n`;
  }
  headerStr += `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${path.basename(filePath)}"\r\nContent-Type: ${mimeType}\r\n\r\n`;

  const body = Buffer.concat([
    Buffer.from(headerStr),
    fileBuffer,
    Buffer.from(`\r\n--${boundary}--\r\n`),
  ]);

  const uploadRes = await fetch(target.url, {
    method:  "POST",
    headers: { "Content-Type": `multipart/form-data; boundary=${boundary}` },
    body,
  });

  if (!uploadRes.ok) {
    const txt = await uploadRes.text();
    throw new Error(`S3 upload failed ${uploadRes.status}: ${txt.slice(0, 300)}`);
  }
  return target.resourceUrl;
}

// ── Shopify product helpers ───────────────────────────────────────────────────

async function getProductByHandle(handle) {
  const data = await gql(`
    query($handle: String!) {
      productByHandle(handle: $handle) {
        id
        images(first: 20) {
          edges { node { id src } }
        }
      }
    }
  `, { handle });
  return data.productByHandle;
}

async function appendProductImage(productId, src) {
  const data = await gql(`
    mutation productAppendImages($input: ProductAppendImagesInput!) {
      productAppendImages(input: $input) {
        newImages { id src }
        userErrors { field message }
      }
    }
  `, { input: { id: productId, images: [{ src }] } });
  const errs = data.productAppendImages.userErrors;
  if (errs.length) throw new Error(errs.map(e => e.message).join(", "));
  return data.productAppendImages.newImages[0];
}

// ── CSV parser ────────────────────────────────────────────────────────────────

function parseCSV(filePath) {
  const lines = fs.readFileSync(filePath, "utf-8").split("\n");
  const headers = parseCSVLine(lines[0]);
  return lines.slice(1).filter(l => l.trim()).map(l => {
    const vals = parseCSVLine(l);
    return Object.fromEntries(headers.map((h, i) => [h, vals[i] ?? ""]));
  });
}

function parseCSVLine(line) {
  const result = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') {
      if (inQuotes && line[i + 1] === '"') { current += '"'; i++; }
      else inQuotes = !inQuotes;
    } else if (ch === "," && !inQuotes) {
      result.push(current); current = "";
    } else {
      current += ch;
    }
  }
  result.push(current);
  return result;
}

// ── main ──────────────────────────────────────────────────────────────────────

async function main() {
  const rows = parseCSV(path.join(BASE, "shopify_products_optimized.csv"));

  // Collect unique localPath → [handles]
  const imageMap = new Map();
  for (const row of rows) {
    const img = (row["Image Src"] || "").trim();
    if (!img.startsWith("images_optimized/")) continue;
    const localPath = path.join(BASE, img);
    if (!fs.existsSync(localPath)) {
      console.warn(`⚠ No existe: ${img}`);
      continue;
    }
    if (!imageMap.has(img)) imageMap.set(img, []);
    const handle = row["Handle"];
    if (handle && !imageMap.get(img).includes(handle)) imageMap.get(img).push(handle);
  }

  console.log(`\nImágenes a subir: ${imageMap.size}\n`);

  const cdnMap = new Map();
  let i = 0;

  // Step 1: Upload all images
  for (const [imgPath] of imageMap) {
    i++;
    const localPath = path.join(BASE, imgPath);
    const filename  = path.basename(localPath);
    const fileSize  = fs.statSync(localPath).size;

    process.stdout.write(`[${i}/${imageMap.size}] ${filename.padEnd(50)} `);
    try {
      const target = await stagedUpload(filename, "image/jpeg", fileSize);
      const cdnUrl = await uploadToS3(target, localPath, "image/jpeg");
      cdnMap.set(imgPath, cdnUrl);
      console.log("✓");
    } catch (err) {
      console.log(`✗ ${err.message.slice(0, 80)}`);
    }
  }

  console.log(`\n── Actualizando productos (${cdnMap.size} imágenes subidas) ────────────\n`);

  // Step 2: Update products
  const done = new Set();
  for (const [imgPath, handles] of imageMap) {
    const cdnUrl = cdnMap.get(imgPath);
    if (!cdnUrl) continue;

    for (const handle of handles) {
      const key = handle + "|" + imgPath;
      if (done.has(key)) continue;
      done.add(key);

      try {
        const product = await getProductByHandle(handle);
        if (!product) { console.log(`  ⚠ No encontrado: ${handle}`); continue; }

        const filename = path.basename(imgPath);
        const alreadyHas = product.images.edges.some(e => e.node.src.includes(filename));
        if (alreadyHas) { console.log(`  ✓ ${handle} (ya tiene imagen)`); continue; }

        await appendProductImage(product.id, cdnUrl);
        console.log(`  ✓ ${handle}`);
      } catch (err) {
        console.log(`  ✗ ${handle}: ${err.message.slice(0, 100)}`);
      }
    }
  }

  console.log("\n✅ Completado.\n");
}

main().catch(err => { console.error("Fatal:", err); process.exit(1); });
