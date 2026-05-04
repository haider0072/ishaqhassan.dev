#!/usr/bin/env python3
"""
Strip dedicated Resume window/dock/mobile-section, then inject Resume download
section into:
  1. Desktop contact-morph dialog (after Direct Links grid)
  2. Mobile mobile-connect-expanded section (after last mob-connect-card)
  3. Max AI buildContactCardsBlockHTML (after social cards grid)

Idempotent: skips additions/removals already applied.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
MAX_JS = ROOT / 'js' / 'max.js'

# Reusable resume copy
PDF_URL = '/assets/resume/Ishaq_Hassan_Resume.pdf?v=1'
DOCX_URL = '/assets/resume/Ishaq_Hassan_Resume.docx?v=1'
TXT_URL = '/assets/resume/Ishaq_Hassan_Resume.txt?v=1'

# SVG icons (ASCII-clean, share between desktop + mobile + Max)
PDF_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/><path d="M14 2v6h6" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 14l3 3 3-3M12 11v6" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOCX_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="4" y="2" width="16" height="20" rx="2" stroke="#fff" stroke-width="1.6"/><path d="M8 8h8M8 12h8M8 16h5" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/></svg>'
TXT_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="4" y="2" width="16" height="20" rx="2" stroke="#fff" stroke-width="1.6"/><path d="M8 7h8M8 11h8M8 15h8M8 19h6" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/></svg>'

# ============== INDEX.HTML SURGERY ==============
content = INDEX.read_text()

# --- 1) Strip win-resume window markup ---
def strip_balanced_div(c, marker_substr):
    idx = c.find(marker_substr)
    if idx < 0: return c, False
    start = c.rfind('<div', 0, idx + 1)
    if start < 0: return c, False
    depth = 0
    i = start
    while i < len(c):
        if c[i:i+4] == '<div':
            depth += 1; i += 4
        elif c[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                # also gobble trailing space if any
                while i < len(c) and c[i] == ' ': i += 1
                return c[:start] + c[i:], True
        else:
            i += 1
    return c, False

content, removed_win = strip_balanced_div(content, 'id="win-resume"')
print(f'win-resume window removed: {removed_win}')

# --- 2) Strip resume dock icon ---
dock_pattern = re.compile(r'<div class="dock-item"[^>]*onclick="navigate\(\'resume\'\)"[^>]*>.*?</div>\s*</div>\s*<span class="dock-label">Resume</span>\s*</div>', re.DOTALL)
def strip_dock_resume(c):
    # find <div class="dock-item"...navigate('resume')...
    idx = c.find("navigate('resume')")
    if idx < 0: return c, False
    start = c.rfind('<div class="dock-item"', 0, idx)
    if start < 0: return c, False
    depth = 0
    i = start
    while i < len(c):
        if c[i:i+4] == '<div':
            depth += 1; i += 4
        elif c[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                while i < len(c) and c[i] == ' ': i += 1
                return c[:start] + c[i:], True
        else:
            i += 1
    return c, False

content, removed_dock = strip_dock_resume(content)
print(f'resume dock icon removed: {removed_dock}')

# --- 3) Strip mobile resume bento ---
def strip_mobile_bento(c):
    idx = c.find("expandMobileSection(event,'resume')")
    if idx < 0: return c, False
    start = c.rfind('<div class="mob-bento', 0, idx)
    if start < 0: return c, False
    depth = 0
    i = start
    while i < len(c):
        if c[i:i+4] == '<div':
            depth += 1; i += 4
        elif c[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                while i < len(c) and c[i] == ' ': i += 1
                return c[:start] + c[i:], True
        else:
            i += 1
    return c, False

content, removed_bento = strip_mobile_bento(content)
print(f'mobile resume bento removed: {removed_bento}')

# --- 4) Strip mobile-resume-expanded section ---
content, removed_expanded = strip_balanced_div(content, 'id="mobile-resume-expanded"')
print(f'mobile-resume-expanded removed: {removed_expanded}')

# --- 5) ADD resume section to contact-morph dialog (after Direct Links grid) ---
if 'cm-resume-row' not in content:
    # Insert before the closing of the Direct Links grid's parent .cm-content wrapper.
    # Strategy: find the last </a> inside cm-grid then close the grid, then inject our row.
    # Easier: find "Stack Overflow" card's closing </a>, then </div></div></div></div>... wait,
    # cleaner: place our block AFTER the </div> that closes the cm-grid (Direct Links grid).
    # Find Stack Overflow card closing </a> then the closing </div> of cm-grid.
    stack_idx = content.find('ishaq-hassan</div></div> </a>')
    if stack_idx < 0:
        stack_idx = content.find('Stack Overflow</div>')
    # cm-grid end is the </div> that immediately closes the grid containing Stack Overflow
    if stack_idx > 0:
        # Find the next </div> after stack_idx that closes cm-grid (it's immediately after the </a>)
        # Walk forward to find pattern "</a> </div>" which is the end of cm-grid
        # The cm-grid <div> opens once and contains all .cm-card <a> elements
        # We need to find the </div> matching that opening
        cm_grid_start = content.rfind('class="cm-grid"', 0, stack_idx)
        if cm_grid_start > 0:
            # Walk forward from cm_grid_start to find balanced close
            depth = 0
            i = content.rfind('<div', 0, cm_grid_start + 20)
            while i < len(content):
                if content[i:i+4] == '<div':
                    depth += 1; i += 4
                elif content[i:i+6] == '</div>':
                    depth -= 1; i += 6
                    if depth == 0: break
                else:
                    i += 1
            # i is now AFTER the closing </div> of cm-grid
            INSERT = (
                ' <div class="cm-h" style="margin-top:24px">Resume</div>'
                ' <div class="cm-resume-row">'
                ' <a class="cm-resume-card cm-resume-primary" href="' + PDF_URL + '" download>'
                ' <div class="cm-resume-icon">' + PDF_SVG + '</div>'
                ' <div class="cm-resume-text">'
                ' <div class="cm-resume-label">PDF</div>'
                ' <div class="cm-resume-sub">2 pages, ATS clean</div>'
                ' </div>'
                ' <div class="cm-resume-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12l7 7 7-7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
                ' </a>'
                ' <a class="cm-resume-card" href="' + DOCX_URL + '" download>'
                ' <div class="cm-resume-icon">' + DOCX_SVG + '</div>'
                ' <div class="cm-resume-text">'
                ' <div class="cm-resume-label">DOCX</div>'
                ' <div class="cm-resume-sub">Workday, Greenhouse, Lever</div>'
                ' </div>'
                ' <div class="cm-resume-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12l7 7 7-7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
                ' </a>'
                ' <a class="cm-resume-card" href="' + TXT_URL + '" download>'
                ' <div class="cm-resume-icon">' + TXT_SVG + '</div>'
                ' <div class="cm-resume-text">'
                ' <div class="cm-resume-label">Plain Text</div>'
                ' <div class="cm-resume-sub">Legacy ATS, copy paste</div>'
                ' </div>'
                ' <div class="cm-resume-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12l7 7 7-7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
                ' </a>'
                ' </div>'
            )
            content = content[:i] + INSERT + content[i:]
            print('contact-morph resume section injected')
        else:
            print('WARN: cm-grid class not found, skipping desktop contact resume')
    else:
        print('WARN: stack overflow marker not found, skipping desktop contact resume')

# --- 6) ADD resume section to mobile-connect-expanded ---
if 'mob-connect-resume' not in content:
    mc_idx = content.find('id="mobile-connect-expanded"')
    if mc_idx > 0:
        # Find the LAST </a> with class "mob-connect-card" inside this section
        # Approach: find the section's balanced end, then walk back to find last </a>
        start = content.rfind('<div', 0, mc_idx + 1)
        depth = 0
        i = start
        while i < len(content):
            if content[i:i+4] == '<div':
                depth += 1; i += 4
            elif content[i:i+6] == '</div>':
                depth -= 1; i += 6
                if depth == 0: break
            else:
                i += 1
        section_end = i  # one past closing </div>
        # Walk back to find the </a> that closes the last mob-connect-card
        # Look for last "mob-connect-card" then its closing </a>
        section_chunk = content[start:section_end]
        # Find the parent grid/container that holds mob-connect-card items.
        # We just need to insert our resume row right BEFORE the closing </div> chain that matches the grid containing mob-connect-card.
        # Simpler: find the LAST </a> in section, insert OUR row right after it.
        last_a_close = section_chunk.rfind('</a>')
        if last_a_close > 0:
            insert_at = start + last_a_close + 4  # after </a>
            MOB_INSERT = (
                ' <a href="' + PDF_URL + '" download class="mob-connect-card mob-connect-resume mob-connect-resume-primary">'
                ' <div class="mob-connect-glow" style="background:#6366f1"></div>'
                ' <div class="mob-connect-icon" style="background:linear-gradient(135deg,#6366f1,#4f46e5)">' + PDF_SVG + '</div>'
                ' <div><div class="mob-connect-name">Resume PDF</div><div class="mob-connect-handle">2 pages, ATS clean</div></div>'
                ' </a>'
                ' <a href="' + DOCX_URL + '" download class="mob-connect-card mob-connect-resume">'
                ' <div class="mob-connect-glow" style="background:#818cf8"></div>'
                ' <div class="mob-connect-icon" style="background:linear-gradient(135deg,#818cf8,#6366f1)">' + DOCX_SVG + '</div>'
                ' <div><div class="mob-connect-name">DOCX</div><div class="mob-connect-handle">Workday, Greenhouse, Lever</div></div>'
                ' </a>'
                ' <a href="' + TXT_URL + '" download class="mob-connect-card mob-connect-resume">'
                ' <div class="mob-connect-glow" style="background:#a5b4fc"></div>'
                ' <div class="mob-connect-icon" style="background:linear-gradient(135deg,#a5b4fc,#818cf8)">' + TXT_SVG + '</div>'
                ' <div><div class="mob-connect-name">Plain Text</div><div class="mob-connect-handle">Legacy ATS, copy paste</div></div>'
                ' </a>'
            )
            content = content[:insert_at] + MOB_INSERT + content[insert_at:]
            print('mobile-connect resume cards injected')

INDEX.write_text(content)
print(f'index.html new length: {len(content)}')

# ============== MAX.JS UPDATE ==============
m = MAX_JS.read_text()
if 'buildContactCardsBlockHTML' in m and 'max-resume-row' not in m:
    # Replace the function body to also append resume section
    old = '''  function buildContactCardsBlockHTML() {
    return '<div class="max-cards-block">' + buildContactCardsHTML() + '</div>';
  }'''
    new = '''  function buildContactCardsBlockHTML() {
    var resumeRow = (
      '<div class="max-cards-section" style="margin-top:14px;">Resume</div>' +
      '<div class="max-resume-row">' +
        '<a class="max-resume-pill primary" href="' + RESUME_CARD.pdfHref + '" download>' +
          '<span class="max-resume-pill-icon">' +
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none">' +
              '<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/>' +
              '<path d="M14 2v6h6" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/>' +
              '<path d="M9 14l3 3 3-3M12 11v6" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
            '</svg>' +
          '</span>' +
          '<span class="max-resume-pill-text"><span class="max-resume-pill-label">PDF</span><span class="max-resume-pill-sub">2 pages, ATS clean</span></span>' +
        '</a>' +
        '<a class="max-resume-pill" href="' + RESUME_CARD.docxHref + '" download>' +
          '<span class="max-resume-pill-icon">' +
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none">' +
              '<rect x="4" y="2" width="16" height="20" rx="2" stroke="currentColor" stroke-width="1.6"/>' +
              '<path d="M8 8h8M8 12h8M8 16h5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>' +
            '</svg>' +
          '</span>' +
          '<span class="max-resume-pill-text"><span class="max-resume-pill-label">DOCX</span><span class="max-resume-pill-sub">ATS systems</span></span>' +
        '</a>' +
        '<a class="max-resume-pill" href="' + (RESUME_CARD.pageHref || '/resume') + '" onclick="if (typeof navigate===\\'function\\') { navigate(\\'contact\\'); event.preventDefault(); return false; }">' +
          '<span class="max-resume-pill-icon">' +
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none">' +
              '<path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>' +
            '</svg>' +
          '</span>' +
          '<span class="max-resume-pill-text"><span class="max-resume-pill-label">More</span><span class="max-resume-pill-sub">contact dialog</span></span>' +
        '</a>' +
      '</div>'
    );
    return '<div class="max-cards-block">' + buildContactCardsHTML() + resumeRow + '</div>';
  }'''
    if old in m:
        m = m.replace(old, new)
        MAX_JS.write_text(m)
        print('max.js: buildContactCardsBlockHTML extended with resume row')
    else:
        print('WARN: max.js buildContactCardsBlockHTML signature changed, manual edit needed')

print('Done.')
