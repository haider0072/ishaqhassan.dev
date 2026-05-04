#!/usr/bin/env node
/**
 * GSC sitemap resubmit + URL inspection report.
 *
 * For each URL in sitemap.xml:
 *   1. Resubmit sitemap.xml to GSC
 *   2. Inspect URL via Search Console URL Inspection API
 *   3. Print: indexing state + last crawl date + clickable inspectionResultLink
 *      (the inspectionResultLink is the only way to deep-link a user into the
 *      GSC URL Inspection panel for a specific URL — raw URL gives 404)
 *
 * Required env: GSC_OAUTH (authorized_user JSON with refresh_token)
 * Optional env: GSC_QUOTA_PROJECT (defaults to ishaqhassan-dev)
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname);
const SITE = 'sc-domain:ishaqhassan.dev';
const GSC_OAUTH = process.env.GSC_OAUTH;
const GSC_QUOTA_PROJECT = process.env.GSC_QUOTA_PROJECT || 'ishaqhassan-dev';

if (!GSC_OAUTH) { console.error('GSC_OAUTH env missing'); process.exit(1); }

function readSitemap() {
  const xml = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  const out = [];
  for (const b of xml.split('<url>').slice(1)) {
    const loc = b.match(/<loc>([^<]+)<\/loc>/)?.[1]?.trim();
    if (loc) out.push(loc);
  }
  return out;
}

async function gscAccessToken(oauthJson) {
  const cred = typeof oauthJson === 'string' ? JSON.parse(oauthJson) : oauthJson;
  if (cred.type !== 'authorized_user' || !cred.refresh_token) {
    throw new Error('GSC_OAUTH must be authorized_user JSON with refresh_token');
  }
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: cred.client_id,
      client_secret: cred.client_secret,
      refresh_token: cred.refresh_token,
      grant_type: 'refresh_token'
    }).toString()
  });
  if (!r.ok) throw new Error(`OAuth refresh failed: ${r.status} ${await r.text()}`);
  return (await r.json()).access_token;
}

async function submitSitemap(token, feedpath) {
  const url = `https://searchconsole.googleapis.com/webmasters/v3/sites/${encodeURIComponent(SITE)}/sitemaps/${encodeURIComponent(feedpath)}`;
  const r = await fetch(url, {
    method: 'PUT',
    headers: {
      Authorization: `Bearer ${token}`,
      'x-goog-user-project': GSC_QUOTA_PROJECT
    }
  });
  return { ok: r.ok, status: r.status, body: r.ok ? 'OK' : await r.text() };
}

async function inspectUrl(token, url) {
  const r = await fetch('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      'x-goog-user-project': GSC_QUOTA_PROJECT
    },
    body: JSON.stringify({ inspectionUrl: url, siteUrl: SITE })
  });
  if (!r.ok) return { error: `${r.status} ${(await r.text()).slice(0, 200)}` };
  const j = await r.json();
  const idx = j.inspectionResult?.indexStatusResult || {};
  return {
    verdict: idx.verdict || 'UNKNOWN',
    coverageState: idx.coverageState || '',
    crawledAs: idx.crawledAs || '',
    lastCrawl: idx.lastCrawlTime || '',
    pageFetchState: idx.pageFetchState || '',
    indexingState: idx.indexingState || '',
    referringUrls: (idx.referringUrls || []).slice(0, 3),
    googleCanonical: idx.googleCanonical || '',
    userCanonical: idx.userCanonical || '',
    inspectionResultLink: j.inspectionResult?.inspectionResultLink || ''
  };
}

const main = async () => {
  console.log('### GSC Resubmit + Inspection Report ###\n');

  const token = await gscAccessToken(GSC_OAUTH);
  const urls = readSitemap();

  console.log(`Sitemap URLs: ${urls.length}`);

  // 1. Resubmit sitemap
  console.log('\n[1] Resubmitting sitemap...');
  const sm = await submitSitemap(token, 'https://ishaqhassan.dev/sitemap.xml');
  console.log(`  Sitemap submit: status=${sm.status} ok=${sm.ok}`);
  if (!sm.ok) console.log(`  Body: ${sm.body}`);

  // 2. Inspect every URL (rate-limited)
  console.log('\n[2] Inspecting every URL (this is rate-limited, may take ~3 min)...\n');
  const results = [];
  for (let i = 0; i < urls.length; i++) {
    const u = urls[i];
    const r = await inspectUrl(token, u);
    results.push({ url: u, ...r });
    const flag = r.verdict === 'PASS' ? '✓' : (r.verdict === 'NEUTRAL' ? '~' : (r.verdict === 'FAIL' ? '✗' : '?'));
    console.log(`  [${flag}] ${u}`);
    console.log(`       verdict=${r.verdict} coverage=${r.coverageState}`);
    if (r.error) console.log(`       ERROR: ${r.error}`);
    // Throttle: GSC URL Inspection limits ~600/day; spread sub-1Hz to be safe.
    await new Promise(r => setTimeout(r, 700));
  }

  // 3. Categorize
  const indexed = results.filter(r => r.verdict === 'PASS');
  const neutral = results.filter(r => r.verdict === 'NEUTRAL');
  const failed = results.filter(r => r.verdict === 'FAIL' || (!['PASS', 'NEUTRAL'].includes(r.verdict) && !r.error));
  const errored = results.filter(r => r.error);

  console.log('\n### Summary ###');
  console.log(`  Indexed (PASS):     ${indexed.length}`);
  console.log(`  Discovered/neutral: ${neutral.length}`);
  console.log(`  Excluded/failed:    ${failed.length}`);
  console.log(`  API errors:         ${errored.length}`);

  // Print URLs that need manual indexing requests
  console.log('\n### URLs needing manual indexing request ###');
  console.log('(Open each link in browser → click "Request Indexing")\n');
  const need = [...neutral, ...failed].filter(r => r.inspectionResultLink);
  need.forEach(r => {
    console.log(`URL: ${r.url}`);
    console.log(`  state: ${r.coverageState}`);
    console.log(`  inspect: ${r.inspectionResultLink}`);
    console.log();
  });

  if (errored.length) {
    console.log('\n### URLs with API errors ###');
    errored.forEach(r => console.log(`  ${r.url}: ${r.error}`));
  }
};

main().catch(e => { console.error(e); process.exit(1); });
