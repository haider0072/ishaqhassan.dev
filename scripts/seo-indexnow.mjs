#!/usr/bin/env node
/**
 * IndexNow ping for ishaqhassan.dev.
 *
 * Behavior:
 *   - Reads URLs from sitemap.xml.
 *   - Submits batch to IndexNow API (Bing/Yandex/Naver respect this).
 *   - Smart dedup: optional state file at .seo-state/indexnow-last.json prevents
 *     re-pinging the same URL within 24h (per IndexNow rate guidance).
 *
 * Usage:
 *   node scripts/seo-indexnow.mjs                 # ping all sitemap URLs (24h dedup)
 *   node scripts/seo-indexnow.mjs --force         # bypass dedup
 *   node scripts/seo-indexnow.mjs --urls=u1,u2    # ping specific URLs
 *
 * Exit non-zero on API failure so CI surfaces it.
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname);
const HOST = 'ishaqhassan.dev';
const KEY = '7a68b5bf55888c4f985708dec83a2a53';
const KEY_LOC = `https://${HOST}/indexnow-${KEY}.txt`;
const STATE_DIR = path.join(ROOT, '.seo-state');
const STATE_FILE = path.join(STATE_DIR, 'indexnow-last.json');
const DEDUP_MS = 24 * 60 * 60 * 1000;

const args = new Set(process.argv.slice(2));
const force = args.has('--force');
const urlsArg = [...args].find(a => a.startsWith('--urls='));

function readSitemapUrls() {
  const xml = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].trim());
}

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); }
  catch { return {}; }
}

function saveState(state) {
  fs.mkdirSync(STATE_DIR, { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

async function pingIndexNow(urls) {
  const res = await fetch('https://api.indexnow.org/IndexNow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ host: HOST, key: KEY, keyLocation: KEY_LOC, urlList: urls })
  });
  return { status: res.status, body: await res.text() };
}

async function main() {
  let urls;
  if (urlsArg) {
    urls = urlsArg.replace('--urls=', '').split(',').map(s => s.trim()).filter(Boolean);
  } else {
    urls = readSitemapUrls();
  }

  if (!urls.length) {
    console.error('No URLs to ping.');
    process.exit(1);
  }

  const state = loadState();
  const now = Date.now();
  const toPing = force ? urls : urls.filter(u => !state[u] || (now - state[u]) > DEDUP_MS);

  if (!toPing.length) {
    console.log(`All ${urls.length} URLs pinged within last 24h. Skipping (use --force to override).`);
    process.exit(0);
  }

  // IndexNow allows up to 10000 URLs per request. We're well under that.
  console.log(`Pinging IndexNow with ${toPing.length} URLs (of ${urls.length} total in sitemap)...`);
  const r = await pingIndexNow(toPing);
  console.log(`IndexNow response: ${r.status} ${r.body || '(empty)'}`);

  if (r.status >= 200 && r.status < 300) {
    toPing.forEach(u => { state[u] = now; });
    saveState(state);
    console.log(`State saved: ${toPing.length} URLs marked as pinged.`);
    process.exit(0);
  } else {
    console.error(`IndexNow ping failed: HTTP ${r.status}`);
    process.exit(1);
  }
}

main().catch(err => { console.error(err); process.exit(1); });
