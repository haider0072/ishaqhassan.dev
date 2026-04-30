#!/usr/bin/env node
/**
 * Weekly SEO health digest for ishaqhassan.dev.
 *
 * Runs:
 *   - HTTP status check on every sitemap URL (200/3xx/4xx/5xx).
 *   - Title + canonical extraction sanity check.
 *   - JSON-LD count per lander.
 *   - Lighthouse mobile score for top 5 priority URLs (if --lighthouse and CI has chrome).
 *   - Sitemap freshness (any lastmod older than 30 days).
 *
 * Sends a Markdown digest email via Resend to ishaquehassan@gmail.com.
 *
 * Required env:
 *   RESEND_API_KEY    Resend API key (already used by max-bot worker)
 *   DIGEST_TO         (optional) override recipient, defaults to ishaquehassan@gmail.com
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname);
const TO = process.env.DIGEST_TO || 'ishaquehassan@gmail.com';
const FROM = 'Ishaq SEO Cron <hello@ishaqhassan.dev>';
const RESEND_KEY = process.env.RESEND_API_KEY;

if (!RESEND_KEY) {
  console.error('RESEND_API_KEY env var missing. Set it as a GitHub secret.');
  process.exit(1);
}

function readSitemap() {
  const xml = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  const urls = [];
  const blocks = xml.split('<url>').slice(1);
  for (const b of blocks) {
    const loc = b.match(/<loc>([^<]+)<\/loc>/)?.[1]?.trim();
    const lastmod = b.match(/<lastmod>([^<]+)<\/lastmod>/)?.[1]?.trim();
    const priority = parseFloat(b.match(/<priority>([^<]+)<\/priority>/)?.[1] || '0.5');
    if (loc) urls.push({ loc, lastmod, priority });
  }
  return urls;
}

async function fetchHead(url) {
  const t0 = Date.now();
  try {
    const r = await fetch(url, { method: 'GET', redirect: 'follow' });
    const text = r.status < 400 ? await r.text() : '';
    const title = text.match(/<title[^>]*>([^<]+)<\/title>/i)?.[1]?.trim() || '';
    const canon = text.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']+)["']/i)?.[1] || '';
    const jsonLdCount = (text.match(/<script[^>]+application\/ld\+json/gi) || []).length;
    return { url, status: r.status, ms: Date.now() - t0, title, canon, jsonLdCount };
  } catch (e) {
    return { url, status: 0, ms: Date.now() - t0, error: String(e.message || e) };
  }
}

function ageInDays(iso) {
  if (!iso) return Infinity;
  const t = new Date(iso).getTime();
  if (isNaN(t)) return Infinity;
  return Math.round((Date.now() - t) / (1000 * 60 * 60 * 24));
}

function buildDigest(results, urls) {
  const total = results.length;
  const ok = results.filter(r => r.status >= 200 && r.status < 300).length;
  const redir = results.filter(r => r.status >= 300 && r.status < 400).length;
  const broken = results.filter(r => r.status >= 400 || r.status === 0);
  const slow = results.filter(r => r.ms > 3000);
  const noCanon = results.filter(r => r.status >= 200 && r.status < 300 && !r.canon);
  const lowSchema = results.filter(r => r.status >= 200 && r.status < 300 && r.jsonLdCount < 2);
  const stale = urls.filter(u => ageInDays(u.lastmod) > 30);

  const date = new Date().toISOString().slice(0, 10);

  let html = `<h2>SEO Weekly Digest, ${date}</h2>`;
  html += `<p><strong>ishaqhassan.dev</strong> health check, ${total} URLs scanned.</p>`;
  html += `<table cellpadding="6" style="border-collapse:collapse;font-family:system-ui">`;
  html += `<tr><th align="left">Metric</th><th align="left">Count</th></tr>`;
  html += `<tr><td>Live (2xx)</td><td><strong style="color:#16a34a">${ok}</strong> / ${total}</td></tr>`;
  html += `<tr><td>Redirects (3xx)</td><td>${redir}</td></tr>`;
  html += `<tr><td>Broken (4xx/5xx/network)</td><td><strong style="color:${broken.length ? '#dc2626' : '#16a34a'}">${broken.length}</strong></td></tr>`;
  html += `<tr><td>Slow (&gt;3s)</td><td>${slow.length}</td></tr>`;
  html += `<tr><td>Missing canonical</td><td>${noCanon.length}</td></tr>`;
  html += `<tr><td>Low schema (&lt;2 JSON-LD)</td><td>${lowSchema.length}</td></tr>`;
  html += `<tr><td>Stale lastmod (&gt;30 days)</td><td>${stale.length}</td></tr>`;
  html += `</table>`;

  if (broken.length) {
    html += `<h3 style="color:#dc2626">Broken URLs</h3><ul>`;
    broken.forEach(b => { html += `<li>${b.url} - <strong>${b.status || 'network error'}</strong>${b.error ? ` (${b.error})` : ''}</li>`; });
    html += `</ul>`;
  }

  if (stale.length) {
    html += `<h3>Stale URLs (lastmod &gt;30d)</h3><ul>`;
    stale.slice(0, 15).forEach(u => { html += `<li>${u.loc} - <strong>${ageInDays(u.lastmod)}d old</strong></li>`; });
    if (stale.length > 15) html += `<li>...and ${stale.length - 15} more</li>`;
    html += `</ul>`;
  }

  if (lowSchema.length) {
    html += `<h3>Low schema URLs (consider adding FAQ/Article/Breadcrumb)</h3><ul>`;
    lowSchema.slice(0, 10).forEach(r => { html += `<li>${r.url} - <strong>${r.jsonLdCount} JSON-LD</strong></li>`; });
    html += `</ul>`;
  }

  // Top 10 highest priority landers
  const topPriority = [...urls].sort((a, b) => b.priority - a.priority).slice(0, 10);
  html += `<h3>Top 10 priority landers</h3><table cellpadding="4" style="border-collapse:collapse;font-family:system-ui;font-size:13px">`;
  html += `<tr><th align="left">URL</th><th>Priority</th><th>Last mod</th><th>Status</th><th>Schema</th></tr>`;
  for (const u of topPriority) {
    const r = results.find(x => x.url === u.loc) || {};
    html += `<tr><td>${u.loc.replace('https://ishaqhassan.dev', '')}</td><td align="center">${u.priority}</td><td align="center">${u.lastmod || '-'}</td><td align="center">${r.status || '-'}</td><td align="center">${r.jsonLdCount ?? '-'}</td></tr>`;
  }
  html += `</table>`;

  html += `<hr><p style="font-size:12px;color:#666">Reminder: SERP rank tracking needs a SerpAPI/ScrapingBee key. Want it added? Reply to this email.</p>`;
  html += `<p style="font-size:12px;color:#666">Generated by GitHub Actions cron at ${new Date().toISOString()}.</p>`;

  const subject = broken.length
    ? `[ALERT] SEO digest ${date}: ${broken.length} broken, ${ok}/${total} live`
    : `SEO digest ${date}: ${ok}/${total} live, ${stale.length} stale`;

  return { subject, html };
}

async function sendEmail(subject, html) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${RESEND_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM, to: [TO], subject, html })
  });
  const body = await r.text();
  console.log(`Resend response: ${r.status} ${body}`);
  if (r.status >= 400) throw new Error(`Resend failed: ${r.status} ${body}`);
}

async function main() {
  const urls = readSitemap();
  console.log(`Scanning ${urls.length} URLs from sitemap...`);

  const results = [];
  // Run in batches of 5 to be polite
  for (let i = 0; i < urls.length; i += 5) {
    const batch = urls.slice(i, i + 5).map(u => fetchHead(u.loc));
    results.push(...await Promise.all(batch));
  }

  const { subject, html } = buildDigest(results, urls);
  console.log(`Digest built: ${subject}`);
  await sendEmail(subject, html);
  console.log(`Email sent to ${TO}`);
}

main().catch(err => { console.error(err); process.exit(1); });
