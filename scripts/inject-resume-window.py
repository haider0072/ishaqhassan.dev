#!/usr/bin/env python3
"""Surgical insertion of Resume window + dock icon + mobile section into index.html.

Idempotent: skips insertion if markers already present.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'

content = INDEX.read_text()

# Skip if already injected
if 'id="win-resume"' in content:
    print('win-resume already present, skipping window insertion')
else:
    # Build win-resume markup
    WIN_RESUME = (
        '<div class="window has-fshell" id="win-resume" data-accent="indigo" style="width:920px;height:640px;top:30px;left:calc(50% - 460px)">'
        ' <div class="window-toolbar" onmousedown="startDrag(event,\'win-resume\')">'
        ' <div class="wt-left"> <div class="traffic-lights">'
        ' <div class="traffic-light tl-close" onclick="closeWindow(\'resume\')">✕</div>'
        ' <div class="traffic-light tl-minimize" onclick="minimizeWindow(\'resume\')">−</div>'
        ' <div class="traffic-light tl-maximize" onclick="toggleSnapMenu(event,\'resume\')">+'
        '<div class="snap-menu" id="sm-resume">'
        '<div class="snap-menu-item" onclick="snapWindow(\'resume\',\'left-half\',event)">⬅ Tile Left</div>'
        '<div class="snap-menu-item" onclick="snapWindow(\'resume\',\'right-half\',event)">➡ Tile Right</div>'
        '<div class="snap-menu-divider"></div>'
        '<div class="snap-menu-item" onclick="snapWindow(\'resume\',\'top-full\',event)">'
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:8px"><path d="M8 3 H5 a2 2 0 00-2 2 v3 M21 8 V5 a2 2 0 00-2-2 h-3 M3 16 v3 a2 2 0 002 2 h3 M16 21 h3 a2 2 0 002-2 v-3"/></svg>Full Screen</div>'
        '<div class="snap-menu-divider"></div>'
        '<div class="snap-menu-item" onclick="snapWindow(\'resume\',\'topleft-quarter\',event)">◰ Top Left</div>'
        '<div class="snap-menu-item" onclick="snapWindow(\'resume\',\'topright-quarter\',event)">◳ Top Right</div>'
        '<div class="snap-menu-item" onclick="snapWindow(\'resume\',\'bottomleft-quarter\',event)">◱ Bottom Left</div>'
        '<div class="snap-menu-item" onclick="snapWindow(\'resume\',\'bottomright-quarter\',event)">◲ Bottom Right</div>'
        '</div></div>'
        ' </div> </div>'
        ' <div class="wt-right"> <div class="wt-title">Resume</div> </div>'
        ' </div>'
        ' <div class="window-loader" id="loader-resume"><div class="loader-spinner"></div></div>'
        ' <div class="window-body">'
        ' <aside class="fshell-sidebar">'
        ' <div class="sb-search-wrap"> <div class="sb-search">'
        ' <span class="sb-search-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="7" cy="7" r="5"/><path d="M11 11l3 3" stroke-linecap="round"/></svg></span>'
        ' <input type="search" class="sb-search-input" placeholder="Search resume" oninput="fshellSearch(this,\'resume\')">'
        ' </div> </div>'
        ' <div class="sb-section">'
        ' <div class="sb-label">Sections</div>'
        ' <button type="button" class="sb-item sb-active" data-fshell-filter="all" onclick="fshellFilter(this,\'resume\',\'all\')">'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="2" fill="currentColor"/></svg></span>'
        ' <span class="sb-text">Overview</span> </button>'
        ' <button type="button" class="sb-item" data-fshell-filter="experience" onclick="fshellFilter(this,\'resume\',\'experience\')">'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="4" width="12" height="9" rx="1.5"/><path d="M5 4 V3 a1 1 0 011-1 h4 a1 1 0 011 1 V4"/></svg></span>'
        ' <span class="sb-text">Experience</span> <span class="sb-badge">9</span> </button>'
        ' <button type="button" class="sb-item" data-fshell-filter="skills" onclick="fshellFilter(this,\'resume\',\'skills\')">'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 8 L8 2 L14 8 L8 14 Z"/></svg></span>'
        ' <span class="sb-text">Technical Skills</span> </button>'
        ' <button type="button" class="sb-item" data-fshell-filter="education" onclick="fshellFilter(this,\'resume\',\'education\')">'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 6 L8 2 L15 6 L8 10 Z"/><path d="M4 8 V12 a4 1.5 0 008 0 V8"/></svg></span>'
        ' <span class="sb-text">Education</span> </button>'
        ' <button type="button" class="sb-item" data-fshell-filter="oss" onclick="fshellFilter(this,\'resume\',\'oss\')">'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="6"/><path d="M8 4 V12 M4 8 H12"/></svg></span>'
        ' <span class="sb-text">Open Source</span> </button>'
        ' <button type="button" class="sb-item" data-fshell-filter="speaking" onclick="fshellFilter(this,\'resume\',\'speaking\')">'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 6 H8 L13 3 V13 L8 10 H3 Z"/></svg></span>'
        ' <span class="sb-text">Speaking</span> </button>'
        ' <button type="button" class="sb-item" data-fshell-filter="recognition" onclick="fshellFilter(this,\'resume\',\'recognition\')">'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="6" r="4"/><path d="M5 10 L4 14 L8 12 L12 14 L11 10"/></svg></span>'
        ' <span class="sb-text">Recognition</span> </button>'
        ' </div>'
        ' <div class="sb-section">'
        ' <div class="sb-label">Download</div>'
        ' <a class="sb-item sb-download" href="/assets/resume/Ishaq_Hassan_Resume.pdf?v=1" download>'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 11 V13 a1 1 0 001 1 h8 a1 1 0 001-1 V11"/><path d="M5 7 L8 10 L11 7"/><path d="M8 2 V10"/></svg></span>'
        ' <span class="sb-text">PDF (2 pages)</span> </a>'
        ' <a class="sb-item sb-download" href="/assets/resume/Ishaq_Hassan_Resume.docx?v=1" download>'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="2" width="10" height="12" rx="1"/><path d="M5 6 H11 M5 9 H11 M5 12 H8"/></svg></span>'
        ' <span class="sb-text">DOCX (ATS)</span> </a>'
        ' <a class="sb-item sb-download" href="/assets/resume/Ishaq_Hassan_Resume.txt?v=1" download>'
        ' <span class="sb-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="2" width="10" height="12" rx="1"/><path d="M5 5 H11 M5 7.5 H11 M5 10 H11 M5 12.5 H9"/></svg></span>'
        ' <span class="sb-text">Plain Text</span> </a>'
        ' </div>'
        ' </aside>'
        ' <div class="fshell-content resume-content" data-filter="all">'
        # === OVERVIEW ===
        ' <article class="resume-hero" data-filter-val="overview">'
        ' <div class="resume-hero-name">Ishaq Hassan</div>'
        ' <div class="resume-hero-role">Senior Software Engineer · Flutter Framework Contributor</div>'
        ' <div class="resume-hero-loc">Karachi, Pakistan · Open to Remote (Global) · 13+ years</div>'
        ' <div class="resume-hero-contact">'
        ' <a href="mailto:hello@ishaqhassan.dev">hello@ishaqhassan.dev</a> · '
        ' <a href="tel:+923452993669">+92-345-2993669</a> · '
        ' <a href="https://linkedin.com/in/ishaquehassan" target="_blank" rel="noopener">LinkedIn</a> · '
        ' <a href="https://github.com/ishaquehassan" target="_blank" rel="noopener">GitHub</a>'
        ' </div>'
        ' <p class="resume-summary">Senior Software Engineer and Flutter framework contributor with 13+ years of full-stack experience shipping 50+ production mobile and web applications. One of the few Pakistani engineers with code merged into the official Flutter framework: 6 Pull Requests merged into <code>flutter/flutter</code>, 3 currently under review. Currently leading mobile engineering at DigitalHire, an AI-powered recruitment platform serving 9+ enterprise ATS integrations. Author of the only Urdu Flutter course officially listed on the Flutter documentation.</p>'
        ' <div class="resume-cta-row">'
        ' <a class="resume-cta-primary" href="/assets/resume/Ishaq_Hassan_Resume.pdf?v=1" download>Download PDF</a>'
        ' <a class="resume-cta-ghost" href="/assets/resume/Ishaq_Hassan_Resume.docx?v=1" download>DOCX (ATS)</a>'
        ' <a class="resume-cta-ghost" href="/assets/resume/Ishaq_Hassan_Resume.txt?v=1" download>Plain Text</a>'
        ' </div>'
        ' </article>'
        # === EXPERIENCE ===
        ' <h3 class="resume-section-title" data-filter-val="experience">Professional Experience</h3>'
        # 1. DigitalHire
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="pr-status pr-merged">Current</div>'
        ' <div class="resume-job-title">Senior Software Engineer & Technical Lead</div>'
        ' <div class="resume-job-meta"><strong>DigitalHire</strong> · McLean, Virginia (Remote) · Feb 2023 to Present</div>'
        ' <ul class="resume-bullets">'
        ' <li>Lead mobile and platform engineering for the world\'s first integrated talent engine, an AI-powered recruitment platform combining video job boards, on-demand video interviews, and an AI recruiting agent.</li>'
        ' <li>Architected and shipped the cross-platform mobile application using Flutter for iOS, Android, and Web from a single codebase, cutting mobile engineering effort by 60% versus separate native stacks.</li>'
        ' <li>Drove platform integrations across 9+ Applicant Tracking Systems including Greenhouse, Workday, and iCIMS, enabling enterprise customers to plug DigitalHire into existing hiring pipelines.</li>'
        ' <li>Improved customer hiring metrics: 50% reduction in time-to-hire, 40% lower cost-to-hire, 70% faster screening through video resumes.</li>'
        ' <li>Mentor distributed engineering team of 6+ engineers across mobile, backend, and AI agent components; lead architecture reviews and technical hiring.</li>'
        ' </ul>'
        ' <div class="resume-stack">Flutter · Dart · Node.js · NestJS · PostgreSQL · Next.js · Python · React Native · Kotlin · Firebase · Docker</div>'
        ' </article>'
        # 2. Flutter OSS
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="pr-status pr-approved">Open Source</div>'
        ' <div class="resume-job-title">Open Source Contributor, Flutter Framework</div>'
        ' <div class="resume-job-meta"><strong>Flutter (Google)</strong> · <a href="https://github.com/flutter/flutter/pulls?q=author%3Aishaquehassan" target="_blank" rel="noopener">flutter/flutter</a> · 2026 to Present</div>'
        ' <ul class="resume-bullets">'
        ' <li>Merged 6 Pull Requests into the official Flutter framework repository, with 3 additional PRs under review. Code ships to millions of Flutter developers worldwide through framework releases.</li>'
        ' <li>Areas: widget rendering, animation APIs, parameter forwarding, AnimatedCrossFade internals, DropdownMenu enhancements, RawImage and RenderImage rendering, documentation accuracy.</li>'
        ' <li>Notable merged PRs: <code>clipBehavior</code> on AnimatedCrossFade (#184545), <code>scrollPadding</code> on DropdownMenu (#183109), CurvedAnimation/CurveTween disposal docs (#184569).</li>'
        ' </ul>'
        ' </article>'
        # 3. Tech Idara
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="resume-job-title">Senior Flutter Instructor</div>'
        ' <div class="resume-job-meta"><strong>Tech Idara</strong> · Remote · Dec 2021 to Sep 2024</div>'
        ' <ul class="resume-bullets">'
        ' <li>Authored, recorded, and shipped a 35-video Flutter development course in Urdu, the only Urdu-language Flutter course officially listed on <code>docs.flutter.dev/resources/courses</code>.</li>'
        ' <li>Curriculum covers Dart fundamentals, OOP, Flutter UI, state management, networking, testing, CI/CD, and deployment. Course has trained 10,000+ developers across Pakistan and the Urdu-speaking world.</li>'
        ' </ul>'
        ' </article>'
        # 4. AeroGlobe
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="resume-job-title">Technical Lead</div>'
        ' <div class="resume-job-meta"><strong>AeroGlobe</strong> · Remote · Jun 2022 to May 2024</div>'
        ' <ul class="resume-bullets">'
        ' <li>Led mobile and frontend engineering for travel technology products serving 100,000+ monthly users. Designed React Native architecture, defined API contracts with Python backend, and shipped 4+ customer-facing booking flows.</li>'
        ' <li>Owned mobile release process, performance optimization, and engineering quality bar across a team of 5+ engineers.</li>'
        ' </ul>'
        ' </article>'
        # 5. Sastaticket
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="resume-job-title">Engineering Consultant</div>'
        ' <div class="resume-job-meta"><strong>Sastaticket.pk</strong> · Remote · Jan 2022 to Mar 2024</div>'
        ' <ul class="resume-bullets">'
        ' <li>Consulted on Flutter mobile architecture, CI/CD pipelines using GitHub Actions, and release engineering for one of Pakistan\'s largest online travel platforms.</li>'
        ' <li>Migrated build process from manual to automated tagged releases with signed builds for both Play Store and App Store, cutting release cycle time by 70%.</li>'
        ' </ul>'
        ' </article>'
        # 6. Pocket Systems
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="resume-job-title">Senior Software Engineer</div>'
        ' <div class="resume-job-meta"><strong>Pocket Systems</strong> · Remote · Jan 2020 to Dec 2022</div>'
        ' <ul class="resume-bullets">'
        ' <li>Built React Native applications and socket programming services for 5+ international B2B clients across the United States and Europe, owning real-time messaging stack and end-to-end delivery for production traffic of 50,000+ daily messages.</li>'
        ' </ul>'
        ' </article>'
        # 7. Optimyse
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="resume-job-title">Lead Software Engineer</div>'
        ' <div class="resume-job-meta"><strong>Optimyse</strong> · Estonia (Remote) · Feb 2019 to Dec 2021</div>'
        ' <ul class="resume-bullets">'
        ' <li>Led full-stack engineering teams of 4+ engineers shipping cross-platform mobile applications. Mentored engineers across Estonia and Pakistan time zones, owned hiring, sprint planning for 2+ week cycles, and architecture decisions.</li>'
        ' </ul>'
        ' </article>'
        # 8. Cyber Avanza
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="resume-job-title">Senior Software Engineer</div>'
        ' <div class="resume-job-meta"><strong>Cyber Avanza</strong> · Karachi, Pakistan · Sep 2016 to Dec 2018</div>'
        ' <ul class="resume-bullets">'
        ' <li>Shipped 8+ native Android (Kotlin, Java) and iOS (Swift, Objective-C) applications for international clients across e-commerce and on-demand services, supporting 1M+ combined downloads on the Play Store and App Store.</li>'
        ' </ul>'
        ' </article>'
        # 9. VividVisionz
        ' <article class="pr-card resume-job" data-filter-val="experience">'
        ' <div class="resume-job-title">Mobile and Web Developer</div>'
        ' <div class="resume-job-meta"><strong>VividVisionz</strong> · Karachi, Pakistan · Feb 2013 to Feb 2019</div>'
        ' <ul class="resume-bullets">'
        ' <li>Built and shipped 30+ Android, iOS, and web applications across six years using PHP, MySQL, JavaScript, native Android, and native iOS.</li>'
        ' </ul>'
        ' </article>'
        # === SKILLS ===
        ' <h3 class="resume-section-title" data-filter-val="skills">Technical Skills</h3>'
        ' <article class="resume-skill-block" data-filter-val="skills">'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">Mobile</div><div class="resume-skill-chips">'
        ' <span>Flutter</span><span>Dart</span><span>Android (Kotlin, Java)</span><span>iOS (Swift, Objective-C)</span><span>React Native</span><span>Cross-Platform</span><span>Platform Channels</span><span>FFI</span>'
        ' </div></div>'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">Frontend</div><div class="resume-skill-chips">'
        ' <span>TypeScript</span><span>JavaScript</span><span>React</span><span>Next.js</span><span>HTML5</span><span>CSS3</span><span>Web Performance</span><span>SSR</span>'
        ' </div></div>'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">Backend</div><div class="resume-skill-chips">'
        ' <span>Node.js</span><span>NestJS</span><span>Python</span><span>Go</span><span>Spring Boot</span><span>PHP</span><span>REST APIs</span><span>GraphQL</span><span>Microservices</span><span>Serverless</span><span>Cloudflare Workers</span>'
        ' </div></div>'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">Databases</div><div class="resume-skill-chips">'
        ' <span>PostgreSQL</span><span>MySQL</span><span>MongoDB</span><span>Firebase Firestore</span><span>Redis</span><span>SQLite</span><span>Floor</span>'
        ' </div></div>'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">Cloud / DevOps</div><div class="resume-skill-chips">'
        ' <span>Firebase</span><span>AWS</span><span>GCP</span><span>Cloudflare</span><span>Docker</span><span>GitHub Actions</span><span>CI/CD</span><span>Linux</span><span>Nginx</span>'
        ' </div></div>'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">Architecture</div><div class="resume-skill-chips">'
        ' <span>Clean Architecture</span><span>DDD</span><span>Event-Driven</span><span>BLoC</span><span>Provider</span><span>Riverpod</span><span>Redux</span><span>MVVM</span><span>Microservices</span><span>Monorepo</span>'
        ' </div></div>'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">AI Integration</div><div class="resume-skill-chips">'
        ' <span>OpenAI API</span><span>Anthropic Claude API</span><span>OpenRouter</span><span>RAG Pipelines</span><span>Prompt Engineering</span>'
        ' </div></div>'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">Testing</div><div class="resume-skill-chips">'
        ' <span>Unit Testing</span><span>Widget Testing</span><span>Integration Testing</span><span>Flutter Driver</span><span>Jest</span><span>JUnit</span><span>XCTest</span><span>TDD</span>'
        ' </div></div>'
        ' <div class="resume-skill-row"><div class="resume-skill-cat">Leadership</div><div class="resume-skill-chips">'
        ' <span>Engineering Management</span><span>Technical Mentorship</span><span>Code Review</span><span>Hiring</span><span>Architecture Reviews</span><span>Cross-Functional</span><span>Agile</span><span>Scrum</span>'
        ' </div></div>'
        ' </article>'
        # === EDUCATION ===
        ' <h3 class="resume-section-title" data-filter-val="education">Education</h3>'
        ' <article class="pr-card" data-filter-val="education">'
        ' <div class="resume-job-title">Aptech Computer Education</div>'
        ' <div class="resume-job-meta">ACCP, Computer Software Engineering · Karachi, Pakistan · 2012 to 2016</div>'
        ' </article>'
        ' <article class="pr-card" data-filter-val="education">'
        ' <div class="resume-job-title">Board of Intermediate Education, Karachi</div>'
        ' <div class="resume-job-meta">Intermediate of Computer Science (ICS) · Karachi, Pakistan · 2012 to 2014</div>'
        ' </article>'
        ' <article class="pr-card" data-filter-val="education">'
        ' <div class="resume-job-title">Bahadurabad Foundation School</div>'
        ' <div class="resume-job-meta">Matriculation, Computer Science · Karachi, Pakistan · 2011 to 2013</div>'
        ' <div class="resume-job-meta" style="margin-top:6px">Activities: Programming, Application Development, Research</div>'
        ' </article>'
        # === OPEN SOURCE ===
        ' <h3 class="resume-section-title" data-filter-val="oss">Open Source Projects</h3>'
        ' <article class="pr-card" data-filter-val="oss">'
        ' <div class="resume-job-title"><a href="https://github.com/ishaquehassan/document_scanner_flutter" target="_blank" rel="noopener">document_scanner_flutter</a> <span class="resume-stars">63 ★ · 135 forks</span></div>'
        ' <div class="resume-job-meta">Production Flutter plugin for iOS and Android document scanning with native camera, edge detection, and perspective correction. Listed on the official Flutter documentation.</div>'
        ' </article>'
        ' <article class="pr-card" data-filter-val="oss">'
        ' <div class="resume-job-title"><a href="https://github.com/ishaquehassan/flutter_alarm_background_trigger" target="_blank" rel="noopener">flutter_alarm_background_trigger</a> <span class="resume-stars">14 ★</span></div>'
        ' <div class="resume-job-meta">Native Kotlin alarm plugin for Flutter, launches apps from background at specific times.</div>'
        ' </article>'
        ' <article class="pr-card" data-filter-val="oss">'
        ' <div class="resume-job-title"><a href="https://github.com/ishaquehassan/assets_indexer" target="_blank" rel="noopener">assets_indexer</a> <span class="resume-stars">9 ★</span></div>'
        ' <div class="resume-job-meta">Auto-generates strongly-typed Dart asset references for Flutter projects.</div>'
        ' </article>'
        ' <article class="pr-card" data-filter-val="oss">'
        ' <div class="resume-job-title"><a href="https://github.com/ishaquehassan/goal-agent" target="_blank" rel="noopener">goal-agent</a></div>'
        ' <div class="resume-job-meta">AI-powered career goal agent for Claude Code with cross-platform automation.</div>'
        ' </article>'
        ' <article class="pr-card" data-filter-val="oss">'
        ' <div class="resume-job-title"><a href="https://github.com/ishaquehassan/claude-remote-terminal" target="_blank" rel="noopener">claude-remote-terminal</a></div>'
        ' <div class="resume-job-meta">Mobile remote terminal for Claude AI coding sessions over WebSocket PTY.</div>'
        ' </article>'
        # === SPEAKING ===
        ' <h3 class="resume-section-title" data-filter-val="speaking">Speaking Engagements</h3>'
        ' <article class="pr-card" data-filter-val="speaking">'
        ' <ul class="resume-bullets">'
        ' <li><strong>Panel Speaker</strong>, "Scaling Products with Flutter," DevFest Karachi 2021, GDG Kolachi.</li>'
        ' <li><strong>Speaker</strong>, Google I/O Extended Karachi, GDG Kolachi.</li>'
        ' <li><strong>Lead Instructor</strong>, Flutter Bootcamp, GDG Kolachi.</li>'
        ' <li><strong>Speaker</strong>, Flutter Seminar, Iqra University.</li>'
        ' <li><strong>Inaugural Speaker</strong>, Facebook Developer Circle, The Nest I/O.</li>'
        ' <li>5+ additional events across GDG Kolachi, universities, and tech communities.</li>'
        ' </ul>'
        ' </article>'
        # === RECOGNITION ===
        ' <h3 class="resume-section-title" data-filter-val="recognition">Recognition</h3>'
        ' <article class="pr-card" data-filter-val="recognition">'
        ' <ul class="resume-bullets">'
        ' <li><strong>6 merged Pull Requests</strong> into Google\'s official Flutter framework, with 3 currently under review.</li>'
        ' <li><strong>Author</strong> of the only Urdu Flutter course listed on <code>docs.flutter.dev/resources/courses</code>.</li>'
        ' <li><strong>Official Mentor</strong> at GDG Kolachi (Google Developer Groups), Karachi chapter.</li>'
        ' <li><strong>9,800+ GitHub contributions</strong> across 175 public repositories with 222 followers.</li>'
        ' </ul>'
        ' </article>'
        ' </div>'
        ' </div>'
        '</div> '
    )

    # Insert after win-wisesend (just before <div id="mobile-app">)
    marker = ' <div id="mobile-app">'
    pos = content.find(marker)
    if pos < 0:
        raise SystemExit('Cannot find <div id="mobile-app"> marker')
    content = content[:pos] + WIN_RESUME + content[pos:]
    print(f'Inserted win-resume at position {pos}')

# === DOCK ICON ===
if "navigate('resume')" in content:
    print('resume dock-item already present, skipping')
else:
    DOCK_ITEM = (
        '<div class="dock-item" onclick="navigate(\'resume\')" role="button" aria-label="Open Resume"> '
        '<div class="dock-tooltip">Resume</div> '
        '<div class="dock-icon resume"> '
        '<svg width="28" height="28" viewBox="0 0 40 40" fill="none">'
        '<rect x="8" y="3" width="24" height="34" rx="3" fill="#fff"/>'
        '<path d="M14 12 H26 M14 18 H26 M14 24 H22" stroke="#4f46e5" stroke-width="2.4" stroke-linecap="round"/>'
        '<circle cx="32" cy="11" r="6" fill="#6366f1"/>'
        '<path d="M29 11 L31 13 L35 9" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
        '</svg> '
        '</div> <span class="dock-label">Resume</span> </div>'
    )
    # Insert after articles dock-item
    articles_dock = '<div class="dock-item" onclick="navigate(\'articles\')"'
    pos = content.find(articles_dock)
    if pos < 0:
        raise SystemExit('Cannot find articles dock-item')
    # Find balanced end of this div
    depth = 0
    i = pos
    while i < len(content):
        if content[i:i+4] == '<div':
            depth += 1; i += 4
        elif content[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0: break
        else: i += 1
    content = content[:i] + ' ' + DOCK_ITEM + content[i:]
    print(f'Inserted resume dock-item at position {i}')

# === MOBILE BENTO CARD ===
if "expandMobileSection(event,'resume')" in content:
    print('mobile resume bento already present, skipping')
else:
    BENTO = (
        '<div class="mob-bento mobile-section-card" onclick="expandMobileSection(event,\'resume\')" data-accent="indigo"> '
        '<div class="mob-card-glow"></div> '
        '<span class="mob-bento-badge">PDF</span> '
        '<span class="mob-bento-icon">📄</span> '
        '<span class="mob-bento-title">Resume</span> '
        '</div>'
    )
    # Insert before mobile-articles bento (so order: about, prs, resume, ...)
    # Actually insert AFTER articles so order is: ..., articles, resume, ...
    articles_bento = '<div class="mob-bento mobile-section-card" onclick="expandMobileSection(event,\'articles\')"'
    pos = content.find(articles_bento)
    if pos < 0:
        raise SystemExit('Cannot find articles mobile bento')
    depth = 0
    i = pos
    while i < len(content):
        if content[i:i+4] == '<div':
            depth += 1; i += 4
        elif content[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0: break
        else: i += 1
    content = content[:i] + ' ' + BENTO + content[i:]
    print(f'Inserted mobile resume bento at position {i}')

# === MOBILE EXPANDED SECTION ===
if 'id="mobile-resume-expanded"' in content:
    print('mobile-resume-expanded already present, skipping')
else:
    BACK_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>'
    MOB_EXPANDED = (
        '<div id="mobile-resume-expanded" class="mobile-expanded" style="display:none">'
        ' <div class="mobile-expanded-header">'
        ' <button class="mobile-back-btn" onclick="closeMobileSection(\'resume\')">' + BACK_SVG + '</button>'
        ' <div class="mobile-expanded-title">Resume</div>'
        ' <div style="width:40px"></div>'
        ' </div>'
        ' <div class="mobile-expanded-content">'
        ' <div class="mob-resume-stage">'
        ' <div class="mob-resume-hero">'
        ' <div class="mob-resume-name">Ishaq Hassan</div>'
        ' <div class="mob-resume-role">Senior Software Engineer · Flutter Framework Contributor</div>'
        ' <div class="mob-resume-loc">Karachi, Pakistan · 13+ years · Open to Remote</div>'
        ' <div class="mob-resume-cta-row">'
        ' <a class="mob-resume-btn primary" href="/assets/resume/Ishaq_Hassan_Resume.pdf?v=1" download>Download PDF</a>'
        ' <a class="mob-resume-btn ghost" href="/assets/resume/Ishaq_Hassan_Resume.docx?v=1" download>DOCX</a>'
        ' </div>'
        ' </div>'
        ' <div class="mob-resume-section">'
        ' <h3 class="mob-resume-h3">Summary</h3>'
        ' <p>Senior Software Engineer and Flutter framework contributor with 13+ years shipping 50+ production mobile and web apps. 6 PRs merged into <code>flutter/flutter</code> (3 under review). Currently leading mobile engineering at DigitalHire. Author of the only Urdu Flutter course listed on Flutter docs.</p>'
        ' </div>'
        ' <div class="mob-resume-section">'
        ' <h3 class="mob-resume-h3">Experience</h3>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Senior Software Engineer & Technical Lead</div><div class="mob-resume-job-meta">DigitalHire · Feb 2023 to Present</div><p>Lead mobile + platform engineering for AI-powered recruitment platform. Flutter app for iOS/Android/Web. 9+ ATS integrations. Mentor 6+ engineers.</p></div>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Open Source · Flutter Framework</div><div class="mob-resume-job-meta">flutter/flutter · 2026 to Present</div><p>6 merged + 3 open PRs. Widget rendering, animation APIs, AnimatedCrossFade, DropdownMenu, RawImage.</p></div>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Senior Flutter Instructor</div><div class="mob-resume-job-meta">Tech Idara · Dec 2021 to Sep 2024</div><p>35-video Urdu Flutter course. Listed on docs.flutter.dev/resources/courses. 10,000+ trained.</p></div>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Technical Lead</div><div class="mob-resume-job-meta">AeroGlobe · Jun 2022 to May 2024</div><p>Led mobile + frontend for travel tech serving 100K+ users monthly. React Native + Python.</p></div>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Engineering Consultant</div><div class="mob-resume-job-meta">Sastaticket.pk · Jan 2022 to Mar 2024</div><p>Flutter mobile architecture, GitHub Actions CI/CD. 70% release cycle reduction.</p></div>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Senior Software Engineer</div><div class="mob-resume-job-meta">Pocket Systems · Jan 2020 to Dec 2022</div><p>React Native + socket programming for 5+ international B2B clients. 50K+ daily messages.</p></div>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Lead Software Engineer</div><div class="mob-resume-job-meta">Optimyse Estonia · Feb 2019 to Dec 2021</div><p>Led 4+ engineers across Estonia + Pakistan time zones.</p></div>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Senior Software Engineer</div><div class="mob-resume-job-meta">Cyber Avanza · Sep 2016 to Dec 2018</div><p>8+ native Android (Kotlin/Java) + iOS (Swift/Objective-C) apps. 1M+ combined downloads.</p></div>'
        ' <div class="mob-resume-job"><div class="mob-resume-job-title">Mobile and Web Developer</div><div class="mob-resume-job-meta">VividVisionz · Feb 2013 to Feb 2019</div><p>30+ Android, iOS, web apps. PHP, MySQL, JavaScript, native mobile.</p></div>'
        ' </div>'
        ' <div class="mob-resume-section">'
        ' <h3 class="mob-resume-h3">Technical Skills</h3>'
        ' <div class="mob-resume-skill"><strong>Mobile:</strong> Flutter, Dart, Android, iOS, React Native, Kotlin, Swift, Platform Channels, FFI</div>'
        ' <div class="mob-resume-skill"><strong>Frontend:</strong> TypeScript, JavaScript, React, Next.js, HTML5, CSS3</div>'
        ' <div class="mob-resume-skill"><strong>Backend:</strong> Node.js, NestJS, Python, Go, Spring Boot, PHP, REST, GraphQL, Microservices, Cloudflare Workers</div>'
        ' <div class="mob-resume-skill"><strong>Databases:</strong> PostgreSQL, MySQL, MongoDB, Firebase Firestore, Redis, SQLite</div>'
        ' <div class="mob-resume-skill"><strong>Cloud / DevOps:</strong> Firebase, AWS, GCP, Docker, GitHub Actions, CI/CD, Linux, Nginx</div>'
        ' <div class="mob-resume-skill"><strong>AI:</strong> OpenAI API, Claude API, OpenRouter, RAG, Prompt Engineering</div>'
        ' <div class="mob-resume-skill"><strong>Leadership:</strong> Engineering Management, Mentorship, Code Review, Hiring, Agile, Scrum</div>'
        ' </div>'
        ' <div class="mob-resume-section">'
        ' <h3 class="mob-resume-h3">Education</h3>'
        ' <div class="mob-resume-edu"><strong>Aptech Computer Education</strong> · ACCP, Computer Software Engineering · 2012 to 2016</div>'
        ' <div class="mob-resume-edu"><strong>Board of Intermediate Education, Karachi</strong> · ICS · 2012 to 2014</div>'
        ' <div class="mob-resume-edu"><strong>Bahadurabad Foundation School</strong> · Matriculation, Computer Science · 2011 to 2013</div>'
        ' </div>'
        ' <div class="mob-resume-section">'
        ' <h3 class="mob-resume-h3">Open Source</h3>'
        ' <ul class="mob-resume-list">'
        ' <li><strong>document_scanner_flutter</strong> (63 ★, 135 forks): Flutter document scanner plugin, on official docs</li>'
        ' <li><strong>flutter_alarm_background_trigger</strong> (14 ★): Native Kotlin alarm plugin</li>'
        ' <li><strong>assets_indexer</strong> (9 ★): Auto-generated typed Dart asset references</li>'
        ' <li><strong>goal-agent</strong>: AI career goal agent for Claude Code</li>'
        ' <li><strong>claude-remote-terminal</strong>: Mobile remote terminal for Claude AI</li>'
        ' </ul>'
        ' </div>'
        ' <div class="mob-resume-section">'
        ' <h3 class="mob-resume-h3">Speaking</h3>'
        ' <ul class="mob-resume-list">'
        ' <li>Panel Speaker, "Scaling Products with Flutter," DevFest Karachi 2021, GDG Kolachi</li>'
        ' <li>Speaker, Google I/O Extended Karachi, GDG Kolachi</li>'
        ' <li>Lead Instructor, Flutter Bootcamp, GDG Kolachi</li>'
        ' <li>Speaker, Flutter Seminar, Iqra University</li>'
        ' <li>Inaugural Speaker, Facebook Developer Circle, The Nest I/O</li>'
        ' </ul>'
        ' </div>'
        ' <div class="mob-resume-section">'
        ' <h3 class="mob-resume-h3">Recognition</h3>'
        ' <ul class="mob-resume-list">'
        ' <li>6 merged PRs into Google\'s official Flutter framework</li>'
        ' <li>Author of only Urdu Flutter course on docs.flutter.dev</li>'
        ' <li>Official Mentor at GDG Kolachi</li>'
        ' <li>9,800+ GitHub contributions, 175 public repos</li>'
        ' </ul>'
        ' </div>'
        ' <div class="mob-resume-section mob-resume-cta-section">'
        ' <h3 class="mob-resume-h3">Download</h3>'
        ' <div class="mob-resume-cta-grid">'
        ' <a class="mob-resume-btn primary" href="/assets/resume/Ishaq_Hassan_Resume.pdf?v=1" download>📄 PDF (2 pages)</a>'
        ' <a class="mob-resume-btn ghost" href="/assets/resume/Ishaq_Hassan_Resume.docx?v=1" download>📋 DOCX (ATS)</a>'
        ' <a class="mob-resume-btn ghost" href="/assets/resume/Ishaq_Hassan_Resume.txt?v=1" download>📃 Plain Text</a>'
        ' </div>'
        ' </div>'
        ' </div>'
        ' </div>'
        '</div> '
    )
    # Insert after mobile-articles-expanded
    art_marker = '<div id="mobile-articles-expanded"'
    pos = content.find(art_marker)
    if pos < 0:
        raise SystemExit('Cannot find mobile-articles-expanded')
    depth = 0
    i = pos
    while i < len(content):
        if content[i:i+4] == '<div':
            depth += 1; i += 4
        elif content[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0: break
        else: i += 1
    content = content[:i] + ' ' + MOB_EXPANDED + content[i:]
    print(f'Inserted mobile-resume-expanded at position {i}')

INDEX.write_text(content)
print(f'\nTotal length: {len(content)}')
print('Done.')
