#!/usr/bin/env node
/**
 * Weekly SEO Dashboard email for ishaqhassan.dev.
 *
 * Sends a beautiful dashboard-style email to ishaquehassan@gmail.com via Resend with:
 *   - Hero stats: clicks, impressions, avg position (last 7d vs prev 7d)
 *   - Top ranking keywords (with WoW position change)
 *   - Top landing pages by clicks
 *   - Rising stars: queries showing strong WoW growth
 *   - Falling: queries that lost positions
 *   - Health snapshot: HTTP status / schema / freshness
 *
 * Required env:
 *   RESEND_API_KEY   Resend API key (existing)
 *   GSC_SA_KEY       (optional) Google service account JSON, gives ranking data
 *   DIGEST_TO        (optional) override recipient
 *
 * Without GSC_SA_KEY, falls back to health-only mode and includes setup CTA.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname);
const TO = process.env.DIGEST_TO || 'ishaquehassan@gmail.com';
const FROM = 'Ishaq SEO <hello@ishaqhassan.dev>';
const SITE = 'sc-domain:ishaqhassan.dev'; // GSC property (domain property). Use https://ishaqhassan.dev/ if URL property.
const SITE_URL = 'https://ishaqhassan.dev';
const RESEND_KEY = process.env.RESEND_API_KEY;
const GSC_SA_KEY = process.env.GSC_SA_KEY;

if (!RESEND_KEY) { console.error('RESEND_API_KEY missing'); process.exit(1); }

// ─── helpers ──────────────────────────────────────────────────────────────

function readSitemap() {
  const xml = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  const out = [];
  for (const b of xml.split('<url>').slice(1)) {
    const loc = b.match(/<loc>([^<]+)<\/loc>/)?.[1]?.trim();
    const lastmod = b.match(/<lastmod>([^<]+)<\/lastmod>/)?.[1]?.trim();
    const priority = parseFloat(b.match(/<priority>([^<]+)<\/priority>/)?.[1] || '0.5');
    if (loc) out.push({ loc, lastmod, priority });
  }
  return out;
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

function ageDays(iso) {
  if (!iso) return Infinity;
  const t = new Date(iso).getTime();
  return isNaN(t) ? Infinity : Math.round((Date.now() - t) / 86400000);
}

function fmtNum(n) {
  if (n == null) return '-';
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
  return Math.round(n).toString();
}

function fmtPos(p) {
  return p == null ? '-' : p.toFixed(1);
}

function fmtPct(p) {
  if (p == null || !isFinite(p)) return '-';
  const sign = p > 0 ? '+' : '';
  return sign + (p * 100).toFixed(0) + '%';
}

function deltaArrow(curr, prev, lowerIsBetter = false) {
  if (curr == null || prev == null) return { html: '<span style="color:#64748b">·</span>', val: 0 };
  const diff = curr - prev;
  if (Math.abs(diff) < 0.05) return { html: '<span style="color:#64748b">→</span>', val: 0 };
  const positive = lowerIsBetter ? diff < 0 : diff > 0;
  const color = positive ? '#10b981' : '#ef4444';
  const arrow = diff > 0 ? '▲' : '▼';
  const display = lowerIsBetter ? Math.abs(diff).toFixed(1) : (diff > 0 ? '+' : '') + diff.toFixed(0);
  return { html: `<span style="color:${color};font-weight:600">${arrow} ${display}</span>`, val: diff };
}

// ─── Google Search Console API (service account JWT) ──────────────────────

async function gscJwt(saKey) {
  const sa = typeof saKey === 'string' ? JSON.parse(saKey) : saKey;
  const now = Math.floor(Date.now() / 1000);
  const header = { alg: 'RS256', typ: 'JWT' };
  const claim = {
    iss: sa.client_email,
    scope: 'https://www.googleapis.com/auth/webmasters.readonly',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600
  };
  const b64 = obj => Buffer.from(JSON.stringify(obj)).toString('base64url');
  const signInput = `${b64(header)}.${b64(claim)}`;
  const signer = crypto.createSign('RSA-SHA256');
  signer.update(signInput);
  const signature = signer.sign(sa.private_key, 'base64url');
  const jwt = `${signInput}.${signature}`;

  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `grant_type=${encodeURIComponent('urn:ietf:params:oauth:grant-type:jwt-bearer')}&assertion=${jwt}`
  });
  if (!r.ok) throw new Error(`OAuth failed: ${r.status} ${await r.text()}`);
  const j = await r.json();
  return j.access_token;
}

async function gscQuery(token, body) {
  const r = await fetch(`https://searchconsole.googleapis.com/webmasters/v3/sites/${encodeURIComponent(SITE)}/searchAnalytics/query`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (!r.ok) throw new Error(`GSC API: ${r.status} ${await r.text()}`);
  const j = await r.json();
  return j.rows || [];
}

function dateNDaysAgo(n) {
  const d = new Date(Date.now() - n * 86400000);
  return d.toISOString().slice(0, 10);
}

async function fetchGscData() {
  if (!GSC_SA_KEY) return null;
  try {
    const token = await gscJwt(GSC_SA_KEY);
    const ENDED = dateNDaysAgo(3);    // GSC has 2-3 day lag
    const RECENT_START = dateNDaysAgo(9);
    const PREV_END = dateNDaysAgo(10);
    const PREV_START = dateNDaysAgo(16);

    const totals = (rows) => rows.reduce((a, r) => {
      a.clicks += r.clicks; a.impressions += r.impressions;
      a.posSum += r.position * r.impressions; a.imps += r.impressions;
      return a;
    }, { clicks: 0, impressions: 0, posSum: 0, imps: 0 });

    const recent = await gscQuery(token, { startDate: RECENT_START, endDate: ENDED, dimensions: ['query'], rowLimit: 250 });
    const prev = await gscQuery(token, { startDate: PREV_START, endDate: PREV_END, dimensions: ['query'], rowLimit: 250 });
    const recentPages = await gscQuery(token, { startDate: RECENT_START, endDate: ENDED, dimensions: ['page'], rowLimit: 50 });
    const totalsRecent = await gscQuery(token, { startDate: RECENT_START, endDate: ENDED, dimensions: [], rowLimit: 1 });
    const totalsPrev = await gscQuery(token, { startDate: PREV_START, endDate: PREV_END, dimensions: [], rowLimit: 1 });

    const sumRecent = totalsRecent[0] ? { clicks: totalsRecent[0].clicks, impressions: totalsRecent[0].impressions, position: totalsRecent[0].position } : { clicks: 0, impressions: 0, position: null };
    const sumPrev = totalsPrev[0] ? { clicks: totalsPrev[0].clicks, impressions: totalsPrev[0].impressions, position: totalsPrev[0].position } : { clicks: 0, impressions: 0, position: null };

    // Build merged keyword diff
    const prevByKey = new Map(prev.map(r => [r.keys[0], r]));
    const merged = recent.map(r => {
      const k = r.keys[0];
      const p = prevByKey.get(k);
      return {
        query: k,
        clicks: r.clicks, impressions: r.impressions, ctr: r.ctr, position: r.position,
        prevPosition: p?.position ?? null, prevClicks: p?.clicks ?? 0, prevImpressions: p?.impressions ?? 0
      };
    });

    return {
      window: { start: RECENT_START, end: ENDED },
      prevWindow: { start: PREV_START, end: PREV_END },
      sumRecent, sumPrev,
      queries: merged,
      pages: recentPages.map(r => ({ page: r.keys[0], clicks: r.clicks, impressions: r.impressions, ctr: r.ctr, position: r.position }))
    };
  } catch (e) {
    console.error('GSC fetch failed:', e.message);
    return { error: e.message };
  }
}

// ─── HTML email builder ───────────────────────────────────────────────────

function emailShell(inner, subject) {
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${subject}</title></head><body style="margin:0;padding:0;background:#0b0e14;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#e2e8f0">
<div style="max-width:680px;margin:0 auto;padding:24px 16px">${inner}</div></body></html>`;
}

function heroCard(gsc, healthLive, healthTotal) {
  if (!gsc || gsc.error) {
    return `
<div style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border:1px solid rgba(125,211,252,0.18);border-radius:16px;padding:28px 24px;margin-bottom:18px">
  <div style="font-size:11px;font-weight:700;letter-spacing:1.2px;color:#7dd3fc;text-transform:uppercase;margin-bottom:6px">SEO Dashboard</div>
  <div style="font-size:26px;font-weight:800;color:#fff;line-height:1.2;margin-bottom:14px">ishaqhassan.dev</div>
  <div style="background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.25);border-radius:10px;padding:14px 16px;color:#fde68a;font-size:14px;line-height:1.5">
    <strong>Ranking data not connected yet.</strong><br>
    Connect Google Search Console (5 min one-time setup) to see exact keyword positions, click trends, and rising queries here.
    ${gsc?.error ? `<br><span style="color:#fca5a5;font-size:12px">Error: ${gsc.error}</span>` : ''}
  </div>
  <div style="margin-top:16px;display:flex;gap:12px;flex-wrap:wrap">
    <div style="flex:1;min-width:140px;background:rgba(125,211,252,0.05);border:1px solid rgba(125,211,252,0.15);border-radius:10px;padding:14px"><div style="font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.6px">Live URLs</div><div style="font-size:24px;font-weight:800;color:#10b981;margin-top:4px">${healthLive}/${healthTotal}</div></div>
  </div>
</div>`;
  }

  const dClicks = deltaArrow(gsc.sumRecent.clicks, gsc.sumPrev.clicks);
  const dImps = deltaArrow(gsc.sumRecent.impressions, gsc.sumPrev.impressions);
  const dPos = deltaArrow(gsc.sumRecent.position, gsc.sumPrev.position, true);
  const pctClicks = gsc.sumPrev.clicks ? (gsc.sumRecent.clicks - gsc.sumPrev.clicks) / gsc.sumPrev.clicks : null;

  return `
<div style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border:1px solid rgba(125,211,252,0.18);border-radius:16px;padding:28px 24px;margin-bottom:18px">
  <div style="font-size:11px;font-weight:700;letter-spacing:1.2px;color:#7dd3fc;text-transform:uppercase;margin-bottom:6px">SEO Dashboard, last 7 days</div>
  <div style="font-size:26px;font-weight:800;color:#fff;line-height:1.2;margin-bottom:6px">ishaqhassan.dev</div>
  <div style="font-size:13px;color:#94a3b8;margin-bottom:22px">${gsc.window.start} → ${gsc.window.end} · vs ${gsc.prevWindow.start} → ${gsc.prevWindow.end}</div>

  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:separate;border-spacing:8px 0">
    <tr>
      <td width="33%" style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:12px;padding:16px;vertical-align:top">
        <div style="font-size:11px;color:#a7f3d0;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Clicks</div>
        <div style="font-size:30px;font-weight:800;color:#fff;margin:6px 0 4px">${fmtNum(gsc.sumRecent.clicks)}</div>
        <div style="font-size:13px">${dClicks.html} ${pctClicks != null ? `<span style="color:#94a3b8">(${fmtPct(pctClicks)})</span>` : ''}</div>
      </td>
      <td width="33%" style="background:rgba(125,211,252,0.08);border:1px solid rgba(125,211,252,0.25);border-radius:12px;padding:16px;vertical-align:top">
        <div style="font-size:11px;color:#bae6fd;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Impressions</div>
        <div style="font-size:30px;font-weight:800;color:#fff;margin:6px 0 4px">${fmtNum(gsc.sumRecent.impressions)}</div>
        <div style="font-size:13px">${dImps.html}</div>
      </td>
      <td width="33%" style="background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.25);border-radius:12px;padding:16px;vertical-align:top">
        <div style="font-size:11px;color:#e9d5ff;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Avg Position</div>
        <div style="font-size:30px;font-weight:800;color:#fff;margin:6px 0 4px">${fmtPos(gsc.sumRecent.position)}</div>
        <div style="font-size:13px">${dPos.html}</div>
      </td>
    </tr>
  </table>

  <div style="margin-top:16px;font-size:13px;color:#cbd5e1;background:rgba(255,255,255,0.03);border-radius:10px;padding:12px 14px">
    Health: <strong style="color:#10b981">${healthLive}/${healthTotal} URLs live</strong> · ${gsc.queries.length} queries ranked · ${gsc.pages.length} pages received traffic
  </div>
</div>`;
}

function topQueriesCard(gsc) {
  if (!gsc || gsc.error) return '';
  const top = [...gsc.queries].sort((a, b) => b.clicks - a.clicks || b.impressions - a.impressions).slice(0, 12);
  if (!top.length) return '';

  let rows = '';
  top.forEach((q, i) => {
    const posDelta = q.prevPosition != null ? deltaArrow(q.position, q.prevPosition, true) : { html: '<span style="color:#fde68a;font-weight:600">NEW</span>' };
    const posColor = q.position <= 3 ? '#10b981' : q.position <= 10 ? '#7dd3fc' : q.position <= 20 ? '#fbbf24' : '#94a3b8';
    rows += `<tr style="border-bottom:1px solid rgba(255,255,255,0.06)">
      <td style="padding:10px 8px;font-size:13px;color:#cbd5e1">${i + 1}</td>
      <td style="padding:10px 8px;font-size:13.5px;color:#fff;font-weight:500">${q.query}</td>
      <td style="padding:10px 8px;font-size:13px;color:${posColor};font-weight:700;text-align:center">#${fmtPos(q.position)}</td>
      <td style="padding:10px 8px;font-size:12px;text-align:center">${posDelta.html}</td>
      <td style="padding:10px 8px;font-size:13px;color:#10b981;text-align:right;font-weight:600">${fmtNum(q.clicks)}</td>
      <td style="padding:10px 8px;font-size:12px;color:#94a3b8;text-align:right">${fmtNum(q.impressions)}</td>
    </tr>`;
  });

  return `
<div style="background:#0f172a;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:20px 4px 8px;margin-bottom:18px">
  <div style="padding:0 16px 14px"><div style="font-size:11px;color:#7dd3fc;letter-spacing:1.2px;text-transform:uppercase;font-weight:700">Top Ranking Keywords</div><div style="font-size:13px;color:#94a3b8;margin-top:2px">By clicks, last 7 days. Position color: <span style="color:#10b981">top 3</span> · <span style="color:#7dd3fc">top 10</span> · <span style="color:#fbbf24">top 20</span></div></div>
  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse">
    <thead><tr style="border-top:1px solid rgba(255,255,255,0.08);border-bottom:1px solid rgba(255,255,255,0.12)">
      <th style="padding:8px;font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.6px;text-align:left;font-weight:700">#</th>
      <th style="padding:8px;font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.6px;text-align:left;font-weight:700">Query</th>
      <th style="padding:8px;font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.6px;text-align:center;font-weight:700">Pos</th>
      <th style="padding:8px;font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.6px;text-align:center;font-weight:700">WoW</th>
      <th style="padding:8px;font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.6px;text-align:right;font-weight:700">Clicks</th>
      <th style="padding:8px;font-size:10.5px;color:#94a3b8;text-transform:uppercase;letter-spacing:0.6px;text-align:right;font-weight:700">Imps</th>
    </tr></thead>
    <tbody>${rows}</tbody>
  </table>
</div>`;
}

function risingFallingCard(gsc) {
  if (!gsc || gsc.error) return '';
  const withPrev = gsc.queries.filter(q => q.prevPosition != null && q.impressions >= 5);

  // Rising: position improved by ≥3 OR new entries with ≥10 impressions
  const newQueries = gsc.queries.filter(q => q.prevPosition == null && q.impressions >= 10).sort((a, b) => b.impressions - a.impressions).slice(0, 5);
  const moved = withPrev.filter(q => (q.prevPosition - q.position) >= 3).sort((a, b) => (b.prevPosition - b.position) - (a.prevPosition - a.position)).slice(0, 5);
  const fell = withPrev.filter(q => (q.position - q.prevPosition) >= 3).sort((a, b) => (b.position - b.prevPosition) - (a.position - a.prevPosition)).slice(0, 5);

  if (!newQueries.length && !moved.length && !fell.length) return '';

  const buildRows = (arr, mode) => arr.map(q => {
    if (mode === 'new') return `<div style="padding:8px 12px;background:rgba(251,191,36,0.06);border-left:3px solid #fbbf24;border-radius:0 8px 8px 0;margin-bottom:6px"><div style="color:#fff;font-size:13px;font-weight:500">${q.query}</div><div style="font-size:11.5px;color:#fde68a">NEW · pos #${fmtPos(q.position)} · ${fmtNum(q.impressions)} imps</div></div>`;
    if (mode === 'up') return `<div style="padding:8px 12px;background:rgba(16,185,129,0.06);border-left:3px solid #10b981;border-radius:0 8px 8px 0;margin-bottom:6px"><div style="color:#fff;font-size:13px;font-weight:500">${q.query}</div><div style="font-size:11.5px;color:#a7f3d0">▲ #${fmtPos(q.prevPosition)} → #${fmtPos(q.position)} · ${fmtNum(q.clicks)} clicks</div></div>`;
    return `<div style="padding:8px 12px;background:rgba(239,68,68,0.06);border-left:3px solid #ef4444;border-radius:0 8px 8px 0;margin-bottom:6px"><div style="color:#fff;font-size:13px;font-weight:500">${q.query}</div><div style="font-size:11.5px;color:#fecaca">▼ #${fmtPos(q.prevPosition)} → #${fmtPos(q.position)} · was ${fmtNum(q.prevImpressions)} imps</div></div>`;
  }).join('');

  let html = `<div style="background:#0f172a;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:20px;margin-bottom:18px">
    <div style="font-size:11px;color:#7dd3fc;letter-spacing:1.2px;text-transform:uppercase;font-weight:700;margin-bottom:14px">Movement This Week</div>`;

  if (newQueries.length) html += `<div style="font-size:13px;color:#fde68a;font-weight:700;margin-bottom:6px;letter-spacing:0.4px">★ Rising stars (new keywords)</div>${buildRows(newQueries, 'new')}<div style="height:14px"></div>`;
  if (moved.length) html += `<div style="font-size:13px;color:#a7f3d0;font-weight:700;margin-bottom:6px;letter-spacing:0.4px">▲ Climbing positions</div>${buildRows(moved, 'up')}<div style="height:14px"></div>`;
  if (fell.length) html += `<div style="font-size:13px;color:#fecaca;font-weight:700;margin-bottom:6px;letter-spacing:0.4px">▼ Lost positions, attention needed</div>${buildRows(fell, 'down')}`;

  html += `</div>`;
  return html;
}

function topPagesCard(gsc) {
  if (!gsc || gsc.error || !gsc.pages.length) return '';
  const top = [...gsc.pages].sort((a, b) => b.clicks - a.clicks).slice(0, 8);
  let rows = '';
  top.forEach((p, i) => {
    const display = p.page.replace('https://ishaqhassan.dev', '') || '/';
    const posColor = p.position <= 3 ? '#10b981' : p.position <= 10 ? '#7dd3fc' : '#94a3b8';
    rows += `<tr style="border-bottom:1px solid rgba(255,255,255,0.06)">
      <td style="padding:9px 8px;font-size:12.5px;color:#cbd5e1">${i + 1}</td>
      <td style="padding:9px 8px;font-size:12.5px;color:#fff"><a href="${p.page}" style="color:#7dd3fc;text-decoration:none">${display}</a></td>
      <td style="padding:9px 8px;font-size:12.5px;color:#10b981;font-weight:700;text-align:right">${fmtNum(p.clicks)}</td>
      <td style="padding:9px 8px;font-size:12px;color:#94a3b8;text-align:right">${fmtNum(p.impressions)}</td>
      <td style="padding:9px 8px;font-size:12.5px;color:${posColor};font-weight:600;text-align:right">#${fmtPos(p.position)}</td>
    </tr>`;
  });
  return `<div style="background:#0f172a;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:20px 4px 8px;margin-bottom:18px">
  <div style="padding:0 16px 12px"><div style="font-size:11px;color:#7dd3fc;letter-spacing:1.2px;text-transform:uppercase;font-weight:700">Top Pages</div><div style="font-size:12.5px;color:#94a3b8;margin-top:2px">Pages getting clicks last 7 days</div></div>
  <table cellpadding="0" cellspacing="0" border="0" width="100%"><thead><tr style="border-top:1px solid rgba(255,255,255,0.08);border-bottom:1px solid rgba(255,255,255,0.12)"><th style="padding:8px;font-size:10.5px;color:#94a3b8;text-align:left;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">#</th><th style="padding:8px;font-size:10.5px;color:#94a3b8;text-align:left;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Page</th><th style="padding:8px;font-size:10.5px;color:#94a3b8;text-align:right;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Clicks</th><th style="padding:8px;font-size:10.5px;color:#94a3b8;text-align:right;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Imps</th><th style="padding:8px;font-size:10.5px;color:#94a3b8;text-align:right;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Pos</th></tr></thead><tbody>${rows}</tbody></table>
</div>`;
}

function healthCard(results, urls) {
  const total = results.length;
  const ok = results.filter(r => r.status >= 200 && r.status < 300).length;
  const broken = results.filter(r => r.status >= 400 || r.status === 0);
  const noCanon = results.filter(r => r.status >= 200 && r.status < 300 && !r.canon);
  const lowSchema = results.filter(r => r.status >= 200 && r.status < 300 && r.jsonLdCount < 2);
  const stale = urls.filter(u => ageDays(u.lastmod) > 30);

  const issueCount = broken.length + noCanon.length + lowSchema.length + stale.length;
  const allGood = issueCount === 0;

  let issues = '';
  if (broken.length) issues += `<div style="padding:10px 12px;background:rgba(239,68,68,0.08);border-left:3px solid #ef4444;border-radius:0 8px 8px 0;margin-bottom:6px;font-size:12.5px"><strong style="color:#fecaca">${broken.length} broken URL${broken.length > 1 ? 's' : ''}</strong>${broken.slice(0, 5).map(b => `<br><span style="color:#cbd5e1">${b.url.replace('https://ishaqhassan.dev', '')} → ${b.status || 'network err'}</span>`).join('')}</div>`;
  if (stale.length) issues += `<div style="padding:10px 12px;background:rgba(251,191,36,0.06);border-left:3px solid #fbbf24;border-radius:0 8px 8px 0;margin-bottom:6px;font-size:12.5px"><strong style="color:#fde68a">${stale.length} stale URL${stale.length > 1 ? 's' : ''}</strong> (lastmod &gt;30d)</div>`;
  if (lowSchema.length) issues += `<div style="padding:10px 12px;background:rgba(125,211,252,0.06);border-left:3px solid #7dd3fc;border-radius:0 8px 8px 0;margin-bottom:6px;font-size:12.5px"><strong style="color:#bae6fd">${lowSchema.length} low schema</strong> (consider adding FAQ/Article/Breadcrumb)</div>`;
  if (noCanon.length) issues += `<div style="padding:10px 12px;background:rgba(168,85,247,0.06);border-left:3px solid #a855f7;border-radius:0 8px 8px 0;margin-bottom:6px;font-size:12.5px"><strong style="color:#e9d5ff">${noCanon.length} missing canonical</strong></div>`;

  return `<div style="background:#0f172a;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:20px;margin-bottom:18px">
    <div style="font-size:11px;color:#7dd3fc;letter-spacing:1.2px;text-transform:uppercase;font-weight:700;margin-bottom:12px">Site Health</div>
    <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:separate;border-spacing:6px 0;margin-bottom:${allGood ? '0' : '14px'}">
      <tr>
        <td width="50%" style="background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.2);border-radius:10px;padding:12px"><div style="font-size:10.5px;color:#a7f3d0;text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Live</div><div style="font-size:22px;font-weight:800;color:#10b981;margin-top:4px">${ok}/${total}</div></td>
        <td width="50%" style="background:${issueCount ? 'rgba(251,191,36,0.06)' : 'rgba(16,185,129,0.06)'};border:1px solid ${issueCount ? 'rgba(251,191,36,0.2)' : 'rgba(16,185,129,0.2)'};border-radius:10px;padding:12px"><div style="font-size:10.5px;color:${issueCount ? '#fde68a' : '#a7f3d0'};text-transform:uppercase;letter-spacing:0.6px;font-weight:700">Issues</div><div style="font-size:22px;font-weight:800;color:${issueCount ? '#fbbf24' : '#10b981'};margin-top:4px">${issueCount}</div></td>
      </tr>
    </table>
    ${issues || (allGood ? '<div style="font-size:13px;color:#a7f3d0;text-align:center;padding:8px 0">All clear bhai. ✓</div>' : '')}
  </div>`;
}

function footerCard(gsc) {
  let cta = '';
  if (!gsc || gsc.error) {
    cta = `<div style="background:linear-gradient(135deg,rgba(125,211,252,0.06),rgba(168,85,247,0.06));border:1px solid rgba(125,211,252,0.2);border-radius:12px;padding:18px;margin-bottom:14px">
      <div style="font-size:14px;font-weight:700;color:#fff;margin-bottom:6px">⚡ Unlock keyword rank tracking</div>
      <div style="font-size:13px;color:#cbd5e1;line-height:1.6">5-min one-time setup: create a Google Cloud service account, share Search Console as a user, add the JSON as <code style="background:rgba(255,255,255,0.08);padding:1px 6px;border-radius:4px;font-size:11.5px">GSC_SA_KEY</code> GitHub secret. Reply "GSC setup" and I'll walk you through it.</div>
    </div>`;
  }
  return `${cta}<div style="text-align:center;font-size:11px;color:#475569;padding:14px 0">Generated by GitHub Actions cron · ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC<br><a href="https://search.google.com/search-console?resource_id=${encodeURIComponent(SITE_URL)}" style="color:#64748b">Open Search Console</a> · <a href="https://www.bing.com/webmasters" style="color:#64748b">Bing Webmaster</a></div>`;
}

// ─── main ─────────────────────────────────────────────────────────────────

async function main() {
  console.log('Fetching GSC data...');
  const gsc = await fetchGscData();
  if (gsc && !gsc.error) console.log(`GSC: ${gsc.queries.length} queries, ${gsc.pages.length} pages, ${gsc.sumRecent.clicks} clicks last 7d`);
  else if (gsc?.error) console.log(`GSC error: ${gsc.error}`);
  else console.log('GSC: not configured (GSC_SA_KEY missing)');

  console.log('Scanning sitemap URLs...');
  const urls = readSitemap();
  const results = [];
  for (let i = 0; i < urls.length; i += 5) {
    const batch = urls.slice(i, i + 5).map(u => fetchHead(u.loc));
    results.push(...await Promise.all(batch));
  }

  const ok = results.filter(r => r.status >= 200 && r.status < 300).length;
  const total = results.length;
  const broken = results.filter(r => r.status >= 400 || r.status === 0).length;

  const date = new Date().toISOString().slice(0, 10);
  let subject;
  if (gsc && !gsc.error) {
    const dC = gsc.sumRecent.clicks - gsc.sumPrev.clicks;
    const trend = dC > 0 ? `▲ ${dC}` : dC < 0 ? `▼ ${Math.abs(dC)}` : '→';
    subject = `📊 ${date} · ${gsc.sumRecent.clicks} clicks ${trend} · pos ${fmtPos(gsc.sumRecent.position)} · ${broken ? `⚠ ${broken} broken` : `${ok}/${total} live`}`;
  } else {
    subject = broken
      ? `⚠ SEO digest ${date}: ${broken} broken URL${broken > 1 ? 's' : ''}, ${ok}/${total} live`
      : `📊 SEO digest ${date}: ${ok}/${total} live · connect GSC for ranking data`;
  }

  const inner = heroCard(gsc, ok, total) + topQueriesCard(gsc) + risingFallingCard(gsc) + topPagesCard(gsc) + healthCard(results, urls) + footerCard(gsc);
  const html = emailShell(inner, subject);

  console.log(`Sending email: ${subject}`);
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${RESEND_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM, to: [TO], subject, html })
  });
  const body = await r.text();
  console.log(`Resend: ${r.status} ${body}`);
  if (r.status >= 400) throw new Error(`Resend failed: ${r.status} ${body}`);
  console.log(`Email delivered to ${TO}`);
}

main().catch(err => { console.error(err); process.exit(1); });
