#!/usr/bin/env python3
"""
gen-window-pages.py

Generates 12 SEO-friendly directory pages, one per desktop window.
Each page has:
  - Unique <title>, meta description, canonical
  - Path-specific og:title / og:description / og:url
  - Breadcrumb + WebPage + per-type JSON-LD
  - Bot-visible H1 + unique ~200+ word content block
  - Redirect-to-home script (humans get SPA, bots see content)

Run from repo root:
    python3 scripts/gen-window-pages.py

Outputs to <repo>/<slug>/index.html for each window.
"""

import os
import json
from datetime import datetime
from pathlib import Path

TODAY = datetime.now().strftime("%Y-%m-%d")

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE = "https://ishaqhassan.dev"
OG_IMAGE = f"{SITE}/assets/og-image.png?v=6"

# Each window: slug (URL path segment), window id (JS lookup), title, desc,
# og_title, og_desc, h1, body_html (unique SEO content), json_ld_extra (path-specific),
# breadcrumb_name.
WINDOWS = [
    {
        "slug": "about",
        "id": "about",
        "title": "About Ishaq Hassan | Flutter Contributor & Senior Engineer",
        "desc": "Flutter Framework Contributor with 6 merged PRs. Engineering Manager at DigitalHire, creator of the Urdu Flutter course listed on Flutter docs.",
        "og_title": "About Ishaq Hassan: Flutter Framework Contributor",
        "og_desc": "13+ years in software, 6 merged PRs into the Flutter framework, 50+ production apps shipped. Engineering Manager, speaker, educator.",
        "h1": "About Ishaq Hassan",
        "breadcrumb_name": "About",
        "json_ld_type": "ProfilePage",
        "body_html": """
<p><strong>Ishaq Hassan</strong> is a senior full-stack software engineer based in Pakistan with 13+ years of professional experience.
He is a <strong>Flutter Framework Contributor</strong> with six pull requests merged into the official Flutter repository and three more approved, making him one of a handful of South Asian engineers contributing at the framework level.</p>
<p>Professionally he is Engineering Manager at <a href="https://www.digitalhire.com" rel="noopener">DigitalHire</a>, where he leads mobile and platform engineering.
Prior roles span <strong>Confiz, Tech Idara, Afiniti,</strong> and independent consulting. Over the years he has shipped <strong>50+ production apps</strong> on iOS, Android and web.</p>
<p>Beyond code, Ishaq created a <strong>35-video Urdu-language Flutter course</strong> that is listed on the <a href="https://docs.flutter.dev/resources/courses#urdu" rel="noopener">official Flutter documentation</a>.
He has spoken at <strong>GDG Kolachi, Iqra University, DevnCode</strong> and multiple community events, and authored <strong>7 Medium articles</strong> covering Dart isolates, Flutter's three-tree architecture, Firebase Cloud Functions, and native plugin development.</p>
<p>Interactive bio, dock widgets, skill graphs and a macOS-style desktop experience are available on the <a href="/">live portfolio</a>.</p>
""",
    },
    {
        "slug": "flutter-contributions",
        "id": "flutter",
        "title": "Flutter Contributions | 6 Merged PRs by Ishaq Hassan",
        "desc": "6 pull requests merged into the official Flutter framework, 3 currently open. Framework-level contributions from Pakistan with full PR list and context.",
        "og_title": "Flutter Framework Contributions: 6 Merged PRs",
        "og_desc": "Framework-level Flutter PRs authored by Ishaq Hassan. Six merged into the Flutter framework, three currently open in active review.",
        "h1": "Flutter Framework Contributions",
        "breadcrumb_name": "Flutter Contributions",
        "json_ld_type": "CollectionPage",
        "body_html": """
<p>Ishaq Hassan has <strong>6 pull requests merged</strong> into the official Flutter framework at <a href="https://github.com/flutter/flutter" rel="noopener">github.com/flutter/flutter</a>, with 3 more currently open in active review.
All merged PRs passed the Flutter team's tree-hygiene, test coverage and review standards.</p>
<h2>Merged PRs (6)</h2>
<ul>
  <li><a href="https://github.com/flutter/flutter/pull/183081" rel="noopener">#183081</a>: Use double quotes in settings.gradle.kts template</li>
  <li><a href="https://github.com/flutter/flutter/pull/183097" rel="noopener">#183097</a>: Fix RouteAware.didPushNext documentation inaccuracy</li>
  <li><a href="https://github.com/flutter/flutter/pull/183109" rel="noopener">#183109</a>: Add scrollPadding property to DropdownMenu</li>
  <li><a href="https://github.com/flutter/flutter/pull/184545" rel="noopener">#184545</a>: Add clipBehavior parameter to AnimatedCrossFade</li>
  <li><a href="https://github.com/flutter/flutter/pull/184569" rel="noopener">#184569</a>: Add disposal guidance to CurvedAnimation and CurveTween docs</li>
  <li><a href="https://github.com/flutter/flutter/pull/184572" rel="noopener">#184572</a>: Fix LicenseRegistry docs to reference NOTICES instead of LICENSE</li>
</ul>
<h2>Currently Open (3)</h2>
<ul>
  <li><a href="https://github.com/flutter/flutter/pull/185938" rel="noopener">#185938</a>: Add blendMode parameter to RawImage and RenderImage</li>
  <li><a href="https://github.com/flutter/flutter/pull/183079" rel="noopener">#183079</a>: Guard auto-scroll against Offset.infinite in scrollable selection</li>
  <li><a href="https://github.com/flutter/flutter/pull/183062" rel="noopener">#183062</a>: Reset AppBar _scrolledUnder flag when scroll context changes</li>
</ul>
<p>Full list of authored PRs: <a href="https://github.com/flutter/flutter/pulls?q=author%3Aishaquehassan" rel="noopener">github.com/flutter/flutter/pulls?q=author:ishaquehassan</a>.
Long-form behind-the-scenes story: <a href="/blog/how-i-got-6-prs-merged-into-flutter.html">How I Got 6 PRs Merged Into Flutter</a>.</p>
""",
    },
    {
        "slug": "speaking",
        "id": "speaking",
        "title": "Speaking & Tech Talks | Ishaq Hassan: Flutter, Mobile Engineering",
        "desc": "Public speaking, bootcamps and community tech talks by Ishaq Hassan: GDG Kolachi, Iqra University, DevnCode, and more across Pakistan.",
        "og_title": "Speaking & Tech Talks: Ishaq Hassan",
        "og_desc": "Flutter bootcamps, GDG events, AI meetups and university seminars: a record of public speaking engagements.",
        "h1": "Speaking & Community",
        "breadcrumb_name": "Speaking",
        "json_ld_type": "CollectionPage",
        "body_html": """
<p>Ishaq Hassan is a regular speaker at developer communities, universities and bootcamps across Pakistan, with over ten verified public-speaking engagements primarily on Flutter framework internals, mobile architecture, AI-augmented engineering, and career growth strategies for software engineers in emerging markets.</p>

<h2>Verified speaking history</h2>
<ul>
  <li><a href="https://gdg.community.dev/events/details/google-gdg-kolachi-presents-flutter-bootcamp/" rel="noopener"><strong>GDG Kolachi: Flutter Bootcamp</strong></a>: full-day hands-on Flutter training under the official Google Developer Group banner. Audience: 80+ Pakistani developers spanning juniors to seniors.</li>
  <li><a href="https://www.linkedin.com/posts/gdgkolachi_codetocreate-roadtodevfest2025-gdgkolachi-activity-7400908378081767424-EB-7" rel="noopener"><strong>GDG Kolachi: Code to Create (Road to DevFest 2025)</strong></a>: speaker session leading up to DevFest 2025, focused on shipping cross-platform apps with Flutter and integrating modern AI-assisted developer workflows.</li>
  <li><a href="https://www.facebook.com/GDGKolachi/posts/720743396758626/" rel="noopener"><strong>GDG Kolachi Speaker Feature</strong></a>: featured by Google Developer Group Kolachi in their official speaker spotlight series.</li>
  <li><a href="https://www.linkedin.com/posts/itrathussainzaidi_flutter-iqrauniversity-seminar-activity-7192627199412232192-8t2X" rel="noopener"><strong>Iqra University: Flutter Seminar</strong></a>: campus seminar introducing Flutter and Dart fundamentals to undergraduate computer science students.</li>
  <li><a href="https://medium.com/devncode/devncode-meetup-iv-artificial-intelligence-df8c602de7d5" rel="noopener"><strong>DevnCode Meetup IV: Artificial Intelligence</strong></a>: panel and talk on practical AI usage in mobile applications and the implications for product engineering.</li>
  <li><strong>Google I/O Extended Karachi</strong>: ecosystem speaker session covering Flutter framework updates announced at I/O.</li>
  <li>Multiple <strong>university and bootcamp invitations</strong> covering NUCES FAST, IBA, Bahria, and private bootcamps.</li>
</ul>

<h2>Talk topics covered</h2>
<ul>
  <li>Flutter framework internals: the three-tree architecture, the rendering pipeline, custom render objects.</li>
  <li>Production-grade Dart patterns: state management decision frameworks, error handling, isolates and async.</li>
  <li>Firebase scaling: data modeling for mobile, security rules at scale, push pipelines.</li>
  <li>The path from app developer to open-source contributor, with concrete tactics from getting six PRs merged into the Flutter framework.</li>
  <li>AI-augmented engineering: how to use Claude Code, MCP servers, and agent loops to multiply individual engineer output.</li>
  <li>Career growth in emerging-market tech, navigating remote roles and building international visibility.</li>
</ul>

<h2>Inviting Ishaq to speak</h2>
<p>Available for keynotes, technical workshops, university seminars, podcast appearances and corporate brown-bag sessions. Both in-person (Karachi, Lahore, Islamabad) and remote engagements considered. To invite Ishaq for a talk, bootcamp or mentoring session, use the <a href="/contact">contact page</a> or email <a href="mailto:hello@ishaqhassan.dev">hello@ishaqhassan.dev</a>.</p>
""",
    },
    {
        "slug": "open-source",
        "id": "oss",
        "title": "Open Source Projects | Ishaq Hassan: Flutter Packages & Tools",
        "desc": "Open source Flutter packages by Ishaq Hassan: document scanner, alarm background trigger, assets indexer, and more on pub.dev and GitHub.",
        "og_title": "Open Source Projects: Ishaq Hassan",
        "og_desc": "Flutter packages, Dart tools and open source projects authored and maintained on pub.dev and GitHub.",
        "h1": "Open Source Projects",
        "breadcrumb_name": "Open Source",
        "json_ld_type": "CollectionPage",
        "body_html": """
<p>Ishaq Hassan publishes open-source Flutter packages, Dart libraries and developer tooling on <a href="https://pub.dev/publishers/ishaqhassan.com/packages" rel="noopener">pub.dev under the publisher <code>ishaqhassan.dev</code></a> and at <a href="https://github.com/ishaquehassan" rel="noopener">github.com/ishaquehassan</a>. Each package addresses a real problem encountered while shipping production Flutter apps for retail, fintech and pharma clients across multiple geographies.</p>

<h2>Featured Flutter packages</h2>
<ul>
  <li><a href="https://github.com/ishaquehassan/document_scanner_flutter" rel="noopener"><strong>document_scanner_flutter</strong></a>: native iOS and Android document scanning bridged to Flutter, with auto-edge detection, perspective correction and PDF export. Used in KYC and onboarding flows.</li>
  <li><a href="https://github.com/ishaquehassan/flutter_alarm_background_trigger" rel="noopener"><strong>flutter_alarm_background_trigger</strong></a>: a background alarm scheduler that survives Doze mode on Android and respects iOS background-exec windows, useful for medication reminders, wake-up apps and field-data collection.</li>
  <li><a href="https://github.com/ishaquehassan/assets_indexer" rel="noopener"><strong>assets_indexer</strong></a>: a Dart code generator that produces strongly-typed asset references inspired by Android's R.java, eliminating string-based asset paths and the runtime errors they cause.</li>
  <li><a href="https://github.com/ishaquehassan/nadra_verisys_flutter" rel="noopener"><strong>nadra_verisys_flutter</strong></a>: an SDK for Pakistan's NADRA Verisys identity verification service, built for fintech onboarding and KYC pipelines.</li>
  <li><a href="https://github.com/ishaquehassan/claude-remote-terminal" rel="noopener"><strong>claude-remote-terminal</strong></a>: a remote-control CLI that lets developers dispatch Claude Code sessions across machines for distributed AI-assisted coding.</li>
  <li><a href="https://github.com/ishaquehassan/goal-agent" rel="noopener"><strong>goal-agent</strong></a>: a career and goal tracker agent that integrates with Claude to surface progress against long-running objectives.</li>
</ul>

<h2>Upstream framework contributions</h2>
<p>Six pull requests merged into the <a href="/flutter-contributions">Flutter framework at flutter/flutter</a>: DropdownMenu scrollPadding, RouteAware lifecycle docs, AnimatedCrossFade clipBehavior, CurvedAnimation disposal guidance, LicenseRegistry NOTICES references and the settings.gradle.kts double-quote template fix. Three additional PRs are currently open and under review on framework documentation, accessibility and developer ergonomics. Each PR ships with extensive test coverage and follows the Flutter style guide and review process.</p>

<h2>Issue triage and review</h2>
<p>Active participant in the Flutter issue tracker, package author for Dart pub.dev community, and reviewer on multiple downstream projects. Open to package collaboration, plugin co-maintenance, and contributing to other Flutter or Dart open-source projects looking for help with Android or iOS platform channels, accessibility, internationalization, or production hardening. Reach out via the <a href="/contact">contact</a> page.</p>
""",
    },
    {
        "slug": "tech-stack",
        "id": "tech",
        "title": "Tech Stack & Tools | Ishaq Hassan: Flutter, Dart, Firebase, Node",
        "desc": "The full stack Ishaq Hassan works with: Flutter, Dart, Firebase, Node.js, Next.js, React, Rust, Kotlin, Swift, GCP, AWS and more.",
        "og_title": "Tech Stack: Ishaq Hassan",
        "og_desc": "Flutter, Dart, Firebase, Node, Next.js, Rust, Kotlin and the broader stack behind 50+ production apps.",
        "h1": "Tech Stack",
        "breadcrumb_name": "Tech Stack",
        "json_ld_type": "CollectionPage",
        "body_html": """
<p>The technology stack Ishaq Hassan ships in production, accumulated across thirteen years of full-stack engineering on retail, fintech, healthtech and SaaS products. Each technology listed here has been used on a real customer-facing product, not a tutorial demo.</p>

<h2>Mobile (primary expertise)</h2>
<ul>
  <li><strong>Flutter and Dart</strong>: Framework-level contributor with six merged pull requests in flutter/flutter and three more open. Production experience across BLoC, Riverpod, Provider, GetX and clean-architecture variants. Authored multiple pub.dev packages.</li>
  <li><strong>Native Android</strong> in Kotlin and Java: platform channels, custom views, Doze-mode-safe alarms, native module bridging.</li>
  <li><strong>Native iOS</strong> in Swift and Objective-C: platform channels, background fetch, push handling, ATS configuration.</li>
  <li><strong>Federated Flutter plugins</strong> spanning iOS, Android and Web with shared Dart APIs.</li>
</ul>

<h2>Backend and infrastructure</h2>
<ul>
  <li><strong>Node.js</strong>: Express, Fastify, NestJS, with experience structuring monoliths, modular monoliths and microservice topologies.</li>
  <li><strong>Firebase</strong>: Firestore data modeling, security rules, Cloud Functions, Cloud Messaging (FCM), Authentication, Remote Config and App Distribution.</li>
  <li><strong>Cloud platforms</strong>: Google Cloud Platform (Cloud Run, Pub/Sub, BigQuery), Amazon Web Services (EC2, S3, Lambda, RDS), Cloudflare (Workers, R2, KV, D1).</li>
  <li><strong>Databases</strong>: PostgreSQL, MongoDB, Redis, SQLite and Firestore. Comfortable with schema design, query optimization and migration playbooks.</li>
  <li><strong>Rust</strong>: selectively used for performance-critical services where latency budgets are tight.</li>
</ul>

<h2>Web</h2>
<ul>
  <li><strong>Next.js, React, TypeScript</strong>: SSR, ISR, app router, server actions, edge runtime.</li>
  <li><strong>Tailwind CSS, shadcn/ui</strong>: design-system level work, dark theme, accessibility.</li>
  <li><strong>Vanilla HTML, CSS, JS</strong>: when performance budget is critical (this portfolio site is vanilla, weighs under 280KB minified including 14 windows).</li>
</ul>

<h2>DevOps and AI</h2>
<ul>
  <li><strong>Containers and CI</strong>: Docker, GitHub Actions, Nginx, automated multi-environment deploy pipelines.</li>
  <li><strong>AI tooling</strong>: Claude Code (Anthropic), OpenAI APIs, OpenRouter for model routing, custom MCP servers and agent orchestration.</li>
  <li><strong>Browser automation</strong>: Puppeteer, Playwright, custom Chrome extensions for headless workflows.</li>
</ul>

<p>Current focus: production-grade Flutter, AI-augmented engineering tooling, framework-level open-source contributions, and writing about each at length on the <a href="/articles/">articles page</a>. Open to senior staff, technical lead and engineering management opportunities globally on remote terms via the <a href="/contact">contact page</a>.</p>
""",
    },
    {
        "slug": "articles",
        "id": "articles",
        "title": "Articles | Ishaq Hassan: Flutter, Dart & Engineering Writing",
        "desc": "Cross-platform article hub: Flutter framework deep-dives, Dart isolates, plugin development. Read on site, Medium or Dev.to from one canonical index.",
        "og_title": "Articles: Ishaq Hassan",
        "og_desc": "9 cross-platform articles. Site + Medium + Dev.to. Flutter framework deep-dives, Dart, architecture, tutorials.",
        "h1": "Articles",
        "breadcrumb_name": "Articles",
        "json_ld_type": "CollectionPage",
        "body_html": """
<p>Long-form technical writing by Ishaq Hassan, indexed across <strong>three platforms</strong>: this site (<a href="/blog/">/blog/</a>), <a href="https://medium.com/@ishaqhassan" rel="noopener">Medium</a>, and <a href="https://dev.to/ishaquehassan" rel="noopener">Dev.to</a>. Cross-posted articles are listed once with platform links.</p>
<ul>
  <li><a href="/articles/flutter-prs-merged/">How a Pakistani Engineer Got 6 PRs Merged Into Flutter's Framework</a> (Site, Medium, Dev.to)</li>
  <li><a href="/articles/flutter-three-tree-architecture/">Flutter's Three-Tree Architecture Explained: Widgets, Elements, RenderObjects</a> (Site, Medium, Dev.to)</li>
  <li><a href="/articles/flutter-state-management-2026/">Flutter State Management in 2026: A Decision Guide for Production Apps</a> (Site, Dev.to)</li>
  <li><a href="/articles/flutter-plugins-case-study/">Building Production Flutter Plugins: A 156-Likes pub.dev Case Study</a> (Site, Dev.to)</li>
  <li><a href="/articles/dart-isolates-guide/">Dart Isolates: The Missing Guide for Production Flutter Apps</a> (Medium)</li>
  <li><a href="/articles/flutter-native-plugins-journey/">A Journey with Flutter Native Plugin Development for iOS &amp; Android</a> (Medium / Nerd For Tech)</li>
  <li><a href="/articles/dart-asset-indexing/">Indexing Assets in a Dart Class Just Like R.java</a> (Medium / Nerd For Tech)</li>
  <li><a href="/articles/firebase-kotlin-functions/">Firebase Cloud Functions Using Kotlin</a> (Medium)</li>
  <li><a href="/articles/devncode-meetup-iv-ai/">DevnCode Meetup IV: Artificial Intelligence</a> (Medium / DevnCode)</li>
</ul>
<p>The on-site full-content posts live under <a href="/blog/">/blog/</a>. Each <code>/articles/&lt;slug&gt;/</code> page links to all the platforms that hosted the article, so Google, Medium, Dev.to and crawlers can resolve the cross-domain identity through <code>sameAs</code> declarations.</p>
""",
    },
    {
        "slug": "contact",
        "id": "contact",
        "title": "Contact Ishaq Hassan | Flutter Consultant, Speaker, Engineering Lead",
        "desc": "Get in touch with Ishaq Hassan: Flutter consulting, speaking engagements, collaboration, engineering leadership. Email, LinkedIn, GitHub.",
        "og_title": "Contact Ishaq Hassan",
        "og_desc": "Reach out for Flutter consulting, speaking engagements, or collaboration.",
        "h1": "Contact",
        "breadcrumb_name": "Contact",
        "json_ld_type": "ContactPage",
        "body_html": """
<p>This is the official contact page for <strong>Ishaq Hassan</strong>: Flutter Framework Contributor, Engineering Manager at DigitalHire, public technology speaker, open-source maintainer and independent Flutter consultant based in Karachi, Pakistan.</p>
<h2>What you can reach out about</h2>
<ul>
  <li><strong>Flutter consulting engagements</strong>: architecture reviews, performance audits, plugin development, framework-level fixes for production blockers</li>
  <li><strong>Speaking invitations</strong>: GDG events, university tech talks, podcast appearances, conference keynotes on Flutter, mobile architecture and open-source strategy</li>
  <li><strong>Engineering leadership opportunities</strong>: Engineering Manager / Head of Engineering / VP Engineering roles, especially mobile-first or Flutter-heavy stacks</li>
  <li><strong>Open-source collaboration</strong>: pub.dev package contributions, framework PR mentorship, plugin maintenance hand-offs</li>
  <li><strong>Course and training</strong>: licensing the 35-video Urdu Flutter course, custom team training, mentorship programs</li>
  <li><strong>Press and media</strong>: interviews about Flutter framework contributions from Pakistan, the OSS contribution journey, the macOS-style portfolio engineering</li>
</ul>
<h2>Direct channels</h2>
<ul>
  <li>Email (preferred): <a href="mailto:hello@ishaqhassan.dev">hello@ishaqhassan.dev</a>. Replies within 48 hours on weekdays.</li>
  <li>LinkedIn DM: <a href="https://linkedin.com/in/ishaquehassan" rel="noopener">linkedin.com/in/ishaquehassan</a></li>
  <li>GitHub: <a href="https://github.com/ishaquehassan" rel="noopener">github.com/ishaquehassan</a> (file an issue on a repo for OSS questions)</li>
  <li>X / Twitter: <a href="https://x.com/ishaque_hassan" rel="noopener">@ishaque_hassan</a></li>
  <li>Stack Overflow: <a href="https://stackoverflow.com/users/2094696/ishaq-hassan" rel="noopener">Ishaq Hassan profile</a></li>
  <li>Medium: <a href="https://medium.com/@ishaqhassan" rel="noopener">@ishaqhassan</a></li>
  <li>YouTube: <a href="https://www.youtube.com/@ishaquehassan" rel="noopener">@ishaquehassan</a> (course videos and tech tutorials)</li>
  <li>Pub.dev: <a href="https://pub.dev/publishers/ishaqhassan.com/packages" rel="noopener">verified publisher</a> for Flutter packages</li>
</ul>
<p>For paid Flutter consulting engagements, see the dedicated <a href="/flutter-consultant.html">consulting page</a>. To hire Ishaq full-time, contract or per-project, visit the <a href="/hire-flutter-developer.html">hire page</a>. For all other inquiries, email is the fastest channel.</p>
""",
    },
    {
        "slug": "github",
        "id": "github",
        "title": "GitHub Profile | Ishaq Hassan: Open Source Repos & Flutter PRs",
        "desc": "GitHub profile overview for Ishaq Hassan: open-source Flutter packages, framework contributions, contribution graph.",
        "og_title": "GitHub: Ishaq Hassan",
        "og_desc": "Open source repos, pub.dev packages, Flutter framework PRs, contribution heatmap.",
        "h1": "GitHub Profile",
        "breadcrumb_name": "GitHub",
        "json_ld_type": "ProfilePage",
        "body_html": """
<p>Ishaq Hassan ships open-source software on GitHub at <a href="https://github.com/ishaquehassan" rel="noopener">github.com/ishaquehassan</a>. The profile spans Flutter packages published on pub.dev, internal developer tooling, AI agent infrastructure and upstream framework-level contributions.</p>
<h2>Pinned and notable repositories</h2>
<ul>
  <li><a href="https://github.com/ishaquehassan/goal-agent" rel="noopener">goal-agent</a>: Claude Code plugin that turns career or project goals into autonomous multi-step research and execution agents. Built on the Claude Agent SDK with custom subagents for goal research, persona building and engagement writing.</li>
  <li><a href="https://github.com/ishaquehassan/document_scanner_flutter" rel="noopener">document_scanner_flutter</a>: cross-platform Flutter document scanning plugin with native iOS Vision and Android ML Kit integrations. Used by KYC, compliance and field-data apps.</li>
  <li><a href="https://github.com/ishaquehassan/assets_indexer" rel="noopener">assets_indexer</a>: C++ powered Dart code generator that produces strongly-typed asset references at build time. Eliminates string-based asset paths and lifts dead-asset detection into the compile step.</li>
  <li><a href="https://github.com/ishaquehassan/flutter_alarm_background_trigger" rel="noopener">flutter_alarm_background_trigger</a>: production-ready scheduled alarm + background-callback Flutter plugin for Android.</li>
  <li><a href="https://github.com/ishaquehassan/nadra_verisys_flutter" rel="noopener">nadra_verisys_flutter</a>: NADRA Verisys CNIC KYC SDK wrapper for Flutter, used in Pakistani fintech and onboarding flows.</li>
  <li><a href="https://github.com/ishaquehassan/claude-remote-terminal" rel="noopener">claude-remote-terminal</a>: secure web-based remote terminal for Claude Code sessions running on a developer machine.</li>
</ul>
<h2>Upstream Flutter framework contributions</h2>
<p>Filter by author for the live PR list: <a href="https://github.com/flutter/flutter/pulls?q=author%3Aishaquehassan" rel="noopener">Pull Requests authored by Ishaq Hassan in the Flutter framework</a>. Recent merged PRs touch <code>LicenseRegistry</code>, <code>RestorableDateTimeN</code>, <code>SemanticsAction</code> serialization, <code>InheritedTheme.captureAll</code>, <code>SnackBar</code> action callbacks and <code>ScrollController</code> attachment lifecycle. See the full breakdown on the <a href="/flutter-contributions">Flutter Contributions page</a>.</p>
<h2>Activity and engagement</h2>
<p>The contribution graph is consistently active across multiple repositories with code review, issue triage and small fixes alongside larger feature work. For deep dives on each open-source project, see the <a href="/open-source">Open Source page</a>; for a curated list of articles about the implementation choices behind these packages, see <a href="/medium-articles">Medium Articles</a>.</p>
""",
    },
    {
        "slug": "linkedin",
        "id": "linkedin",
        "title": "LinkedIn | Ishaq Hassan: Engineering Manager & Flutter",
        "desc": "Ishaq Hassan's LinkedIn: 13+ years, Engineering Manager at DigitalHire, Flutter Framework Contributor, former roles at Confiz, Tech Idara, Afiniti.",
        "og_title": "LinkedIn: Ishaq Hassan",
        "og_desc": "Engineering Manager, Flutter Framework Contributor, 13+ years across mobile, web and backend.",
        "h1": "LinkedIn Profile",
        "breadcrumb_name": "LinkedIn",
        "json_ld_type": "ProfilePage",
        "body_html": """
<p>Ishaq Hassan on LinkedIn: <a href="https://linkedin.com/in/ishaquehassan" rel="noopener">linkedin.com/in/ishaquehassan</a>. Karachi-based Senior Software Engineer and Flutter Framework Contributor with over thirteen years of full-stack engineering experience across mobile, web, backend and cloud platforms.</p>

<h2>Career timeline</h2>
<ul>
  <li><strong>Senior Software Engineer at DigitalHire</strong> (Feb 2023 to Present, McLean VA, remote): leading Flutter mobile development for an AI-driven recruitment platform, owning the cross-platform mobile codebase, the candidate video interview pipeline and a Stripe-backed payments flow. Mentoring engineers and driving release cadence.</li>
  <li><strong>Senior Software Engineer at Confiz</strong> (2021 to 2023): shipped Flutter and React Native apps for retail and pharma clients, integrated MDM, biometrics, push pipelines and offline-first sync.</li>
  <li><strong>Head of Engineering at Tech Idara</strong> (2018 to 2021): grew the engineering team from solo to multiple squads, delivered the official 35-video Urdu Flutter course (now listed on the Flutter docs), launched multiple SaaS products end to end.</li>
  <li><strong>Software Engineer at Afiniti</strong> (2016 to 2018): worked on AI-driven contact-center routing, primarily in C# and Java, with deep dives into queue theory and predictive systems.</li>
  <li><strong>Independent Flutter Consultant</strong> (parallel since 2018): packages on pub.dev, plugin and architecture reviews, training engagements, fractional CTO contracts.</li>
</ul>

<h2>Open source and community</h2>
<p>Flutter Framework contributor with <a href="/flutter-contributions">six merged pull requests in flutter/flutter</a> spanning DropdownMenu padding, RouteAware lifecycle docs, AnimatedCrossFade clip behavior, CurvedAnimation guidance, LicenseRegistry references and the Gradle Kotlin templates. Three additional PRs are currently open on framework documentation and ergonomics. Maintainer of multiple <a href="https://pub.dev/publishers/ishaqhassan.com/packages" rel="noopener">pub.dev publisher packages</a> covering form widgets, validators and tooling utilities.</p>

<h2>Speaking and teaching</h2>
<p>Public speaker at <a href="/speaking">GDG Kolachi, Iqra University, DevnCode and other community events</a> on Flutter framework internals, state management, plugin architecture and Dart isolates. Created a 35-video Urdu Flutter course on YouTube, the official Urdu reference linked from <a href="https://docs.flutter.dev/resources/courses#urdu" rel="noopener">docs.flutter.dev</a>. Frequent technical writer on Medium, Dev.to and Hashnode covering Flutter, Dart and mobile architecture.</p>

<h2>Skills and stack</h2>
<p>Mobile: Flutter, Dart, native Android (Kotlin, Java), iOS (Swift). Backend: Node.js, Firebase, Cloudflare Workers, REST and gRPC. Cloud: Google Cloud Platform, AWS, Cloudflare. Tooling: Git, GitHub Actions, Bitrise, Codemagic, Fastlane. Architecture: BLoC, Riverpod, MVVM, clean architecture, micro-frontends, event-driven patterns. Open to senior staff and engineering leadership opportunities globally on remote terms.</p>
""",
    },
    {
        "slug": "snake",
        "id": "snake",
        "title": "Snake Neon | Play the Arcade Game inside Ishaq Hassan's Portfolio",
        "desc": "Snake Neon arcade game, vanilla JS, embedded in Ishaq Hassan's macOS-style portfolio. Keyboard, D-pad, joystick and swipe controls.",
        "og_title": "Snake Neon: Play inside the Portfolio",
        "og_desc": "A vanilla-JS arcade game with neon visuals, multiple control schemes, and a pause/resume animation.",
        "h1": "Snake Neon Arcade Game",
        "breadcrumb_name": "Snake",
        "json_ld_type": "WebApplication",
        "body_html": """
<p><strong>Snake Neon</strong> is a browser-based arcade game embedded inside Ishaq Hassan's macOS-style portfolio, written from scratch in vanilla JavaScript with an HTML5 canvas renderer. The game ships zero external dependencies, weighs under 60KB minified, and runs at a steady 60 frames per second on both desktop and mobile devices.</p>

<h2>Game features</h2>
<ul>
  <li>60fps rendering loop driven by requestAnimationFrame with delta-time interpolation, so the game speed stays consistent across high-refresh-rate displays and slower mobile GPUs.</li>
  <li>Neon visual style with custom glow shaders, a vignette pause overlay, particle trails on the snake head and a parallax starfield in the background.</li>
  <li>Desktop keyboard controls supporting arrow keys, WASD and ESC for pause, plus a single-key restart after game over.</li>
  <li>Three mobile control schemes (Wheel, D-Pad and Swipe) with a 25px dead zone, three-layer scroll lock to prevent page scroll during play, and a haptic feedback pulse on direction change.</li>
  <li>Heads-up display showing live score, snake length, elapsed time and a personal high-score tracker stored in localStorage.</li>
  <li>Smooth countdown animation when starting and an animated pause overlay with frosted-glass blur on resume.</li>
</ul>

<h2>How to play</h2>
<p>Launch Snake from the portfolio dock by clicking the Snake icon, from Spotlight via <kbd>Cmd+K</kbd> and typing "snake", or by visiting <a href="/snake">ishaqhassan.dev/snake</a> directly. On mobile, the game opens in a full-screen liquid-morph view with the chosen control scheme available immediately. Use <kbd>Esc</kbd> to pause at any time, or tap the pause icon in the heads-up display.</p>

<h2>Why it exists</h2>
<p>The portfolio is a macOS desktop simulation built entirely with vanilla HTML, CSS and JavaScript with no framework. Snake Neon is a small showcase of what is possible without React or Vue, using the browser's native canvas API, modern CSS and roughly 1,400 lines of hand-written game code. It demonstrates Ishaq Hassan's approach to mobile-first interaction design, performance budgeting, and zero-dependency delivery.</p>

<p><a href="/?w=snake">Play Snake Neon now</a></p>
""",
    },
    {
        "slug": "flutter-course",
        "id": "flutter-course",
        "title": "Flutter Course Urdu | 35 Free Videos by Ishaq Hassan",
        "desc": "35-video free Flutter course in Urdu by Ishaq Hassan. Listed on the official Flutter docs. Foundations, Dart, OOP, UI, state, API, advanced.",
        "og_title": "Flutter Course (Urdu): 35 Free Videos",
        "og_desc": "Free Urdu Flutter course listed on official Flutter docs. 35 videos across foundations, Dart, OOP, UI, state and networking.",
        "h1": "Flutter Course (Urdu)",
        "breadcrumb_name": "Flutter Course",
        "json_ld_type": "Course",
        "body_html": """
<p>A 35-video Flutter course taught entirely in Urdu by Ishaq Hassan, <strong>listed as the official Urdu reference on the Flutter documentation</strong> at <a href="https://docs.flutter.dev/resources/courses#urdu" rel="noopener">docs.flutter.dev/resources/courses#urdu</a>. Aimed at Pakistani, Indian and South Asian developers who learn faster in their native language, the course covers everything from setting up a development environment through to shipping production Flutter apps.</p>

<h2>Why this course exists</h2>
<p>When Ishaq started recording in 2021, no comprehensive Urdu Flutter resource existed on YouTube or anywhere else. Beginners in Karachi, Lahore, Islamabad and across South Asia were either stitching together English tutorials with broken playback or skipping mobile development entirely. The course closes that gap with patient, deeply-explained lessons that assume no prior framework experience.</p>

<h2>Course sections (35 lessons)</h2>
<ol>
  <li><strong>Foundation</strong>: how computers run code, installing Flutter SDK, understanding why cross-platform UI matters and where Flutter fits in the mobile landscape.</li>
  <li><strong>Dart Basics</strong>: syntax, types, control flow, functions, lists, maps, null safety and collection operations with worked examples.</li>
  <li><strong>Object-Oriented Programming in Dart</strong>: classes, constructors, inheritance, mixins, abstract classes, generics, extension methods.</li>
  <li><strong>Flutter UI</strong>: the widget tree, Stateless versus Stateful widgets, layout primitives (Row, Column, Stack, Flex), styling with theme data and custom painting.</li>
  <li><strong>State Management</strong>: setState fundamentals, lifting state, Provider package patterns, ChangeNotifier and ValueNotifier, when to reach for Riverpod or BLoC.</li>
  <li><strong>API and Network</strong>: HTTP requests, JSON parsing, async/await, Future and Stream, error handling, retries and Dio interceptors.</li>
  <li><strong>Advanced topics</strong>: production patterns, CI/CD setup, app signing, performance tuning, accessibility and platform channel basics.</li>
</ol>

<h2>How to access</h2>
<p>Watch the full playlist on YouTube: <a href="https://www.youtube.com/playlist?list=PLX97VxArfzkmXeUqUxeKW7XS8oYraH7A5" rel="noopener">Flutter Course (35 videos in Urdu)</a>. Subscribe to the channel for follow-ups, errata and new Flutter tutorials at <a href="https://www.youtube.com/@ishaquehassan?sub_confirmation=1" rel="noopener">youtube.com/@ishaquehassan</a>. The course is freely available with no paywall or registration required.</p>

<p>From this portfolio, an interactive viewer lets you browse all 35 videos with section grouping, completion tracking and direct deep-links: <a href="/?w=flutter-course">open the Flutter Course window</a>.</p>
""",
    },
    {
        "slug": "wisesend",
        "id": "wisesend",
        "title": "WiseSend | Side Project by Ishaq Hassan (XRLabs)",
        "desc": "WiseSend: a side project by Ishaq Hassan under the XRLabs umbrella. Embedded in the portfolio and live at wisesend.xrlabs.app.",
        "og_title": "WiseSend: Side Project",
        "og_desc": "A side project by Ishaq Hassan. Full product at wisesend.xrlabs.app.",
        "h1": "WiseSend",
        "breadcrumb_name": "WiseSend",
        "json_ld_type": "SoftwareApplication",
        "body_html": """
<p><strong>WiseSend</strong> is a fast, cross-device wireless file-sharing tool built and maintained by Ishaq Hassan under the XRLabs umbrella. It removes the friction of copying files between phones and laptops without USB cables, cloud accounts or third-party apps.</p>
<h2>How it works</h2>
<p>The sender device starts a tiny local web server on the same Wi-Fi network as the receiver and exposes a one-time URL plus a QR code. Receivers scan the QR (or open the URL in any browser) and download files directly over the LAN at native Wi-Fi speeds. Nothing transits the public internet, so transfers stay private and work offline.</p>
<h2>Key features</h2>
<ul>
  <li>Phone to laptop, laptop to phone, or device to device file transfer with no account or sign-up</li>
  <li>QR code pairing for one-tap connect from a mobile camera</li>
  <li>Multi-file batch sending with progress tracking</li>
  <li>Pure browser receiver: no installation needed on the receiving device</li>
  <li>LAN-only by default, so transfer speed scales with router quality, not internet bandwidth</li>
  <li>Privacy by design: files never leave the local network or hit any cloud</li>
</ul>
<h2>Use it</h2>
<p>Live product: <a href="https://wisesend.xrlabs.app/" rel="noopener">wisesend.xrlabs.app</a>. The full app runs in the browser; no install required for the web client. The mobile companion runs locally on Android.</p>
<p>From this portfolio, WiseSend is also available as an embedded window. On desktop, visit <a href="/?w=wisesend">/?w=wisesend</a> to open it inline next to the rest of Ishaq Hassan's work.</p>
<h2>About XRLabs</h2>
<p>XRLabs is the umbrella for side projects and experiments by Ishaq Hassan, focused on developer-experience tools, lightweight productivity utilities and small consumer apps. WiseSend is the first publicly-launched product in the lineup.</p>
""",
    },
]


def build_breadcrumb_jsonld(window):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": window["breadcrumb_name"], "item": f"{SITE}/{window['slug']}/"},
        ],
    }


PERSON_SAMEAS = [
    "https://github.com/ishaquehassan",
    "https://linkedin.com/in/ishaquehassan",
    "https://medium.com/@ishaqhassan",
    "https://x.com/ishaque_hassan",
    "https://www.youtube.com/@ishaquehassan",
    "https://stackoverflow.com/users/2094696/ishaq-hassan",
    "https://pub.dev/publishers/ishaqhassan.com/packages",
]


def build_person_entity():
    return {
        "@type": "Person",
        "@id": f"{SITE}/#person",
        "name": "Ishaq Hassan",
        "url": f"{SITE}/",
        "image": f"{SITE}/assets/profile-photo.png",
        "jobTitle": "Engineering Manager at DigitalHire, Flutter Framework Contributor",
        "worksFor": {
            "@type": "Organization",
            "name": "DigitalHire",
            "url": "https://www.digitalhire.com",
        },
        "nationality": {"@type": "Country", "name": "Pakistan"},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Karachi",
            "addressRegion": "Sindh",
            "addressCountry": "PK",
        },
        "sameAs": PERSON_SAMEAS,
        "knowsAbout": [
            "Flutter",
            "Dart",
            "Mobile App Development",
            "Firebase",
            "Node.js",
            "Open Source Software",
            "Software Engineering",
        ],
    }


def build_webpage_jsonld(window):
    t = window["json_ld_type"]
    base = {
        "@context": "https://schema.org",
        "@type": t,
        "@id": f"{SITE}/{window['slug']}/",
        "url": f"{SITE}/{window['slug']}/",
        "name": window["title"],
        "description": window["desc"],
        "isPartOf": {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/"},
        "inLanguage": "en",
        "dateModified": TODAY,
        "datePublished": "2026-04-24",
        "image": f"{SITE}/assets/og/{window['slug']}.png?v=2",
        "author": build_person_entity(),
        "publisher": build_person_entity(),
    }

    # ProfilePage: Google wants mainEntity -> Person for rich profile cards.
    if t == "ProfilePage":
        base["mainEntity"] = build_person_entity()

    # ContactPage: mainEntity -> Person with contactPoint.
    elif t == "ContactPage":
        person = build_person_entity()
        person["email"] = "hello@ishaqhassan.dev"
        person["contactPoint"] = {
            "@type": "ContactPoint",
            "contactType": "general",
            "email": "hello@ishaqhassan.dev",
            "availableLanguage": ["English", "Urdu"],
        }
        base["mainEntity"] = person

    # CollectionPage: about -> Person so Google links the collection to the author entity.
    # mainEntity is what Google's rich-result evaluator checks for ProfilePage/CollectionPage cards.
    elif t == "CollectionPage":
        person = build_person_entity()
        base["about"] = person
        base["mainEntity"] = person

    # Course: provider + hasCourseInstance + educationalLevel are Google-required.
    # video unlocks Video carousel rich result; teaches is a Google-recommended Course field.
    elif t == "Course":
        base["provider"] = {
            "@type": "Person",
            "@id": f"{SITE}/#person",
            "name": "Ishaq Hassan",
            "url": f"{SITE}/",
        }
        base["author"] = build_person_entity()
        base["educationalLevel"] = "Beginner to Advanced"
        base["inLanguage"] = "ur"
        base["isAccessibleForFree"] = True
        base["teaches"] = [
            "Flutter",
            "Dart programming language",
            "Object-Oriented Programming",
            "Flutter UI and widget composition",
            "State management",
            "REST API integration",
            "Asynchronous programming",
            "Mobile app architecture",
        ]
        base["audience"] = {
            "@type": "EducationalAudience",
            "educationalRole": "student",
        }
        base["hasCourseInstance"] = {
            "@type": "CourseInstance",
            "courseMode": "online",
            "inLanguage": "ur",
            "courseWorkload": "PT8H",
            "instructor": {
                "@type": "Person",
                "@id": f"{SITE}/#person",
                "name": "Ishaq Hassan",
            },
        }
        base["offers"] = {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "category": "Educational",
            "url": "https://www.youtube.com/playlist?list=PLX97VxArfzkmXeUqUxeKW7XS8oYraH7A5",
        }
        base["video"] = {
            "@type": "VideoObject",
            "name": "Flutter Course in Urdu - 35 Free Videos by Ishaq Hassan",
            "description": "Comprehensive Flutter development course in Urdu, listed on the official Flutter docs. 35 video lessons spanning Dart basics, OOP, Flutter UI, state management, networking and advanced topics.",
            "thumbnailUrl": "https://img.youtube.com/vi/DB51xmXlaX4/maxresdefault.jpg",
            "uploadDate": "2021-08-10",
            "contentUrl": "https://www.youtube.com/playlist?list=PLX97VxArfzkmXeUqUxeKW7XS8oYraH7A5",
            "embedUrl": "https://www.youtube.com/embed/DB51xmXlaX4",
            "publisher": {
                "@type": "Person",
                "@id": f"{SITE}/#person",
                "name": "Ishaq Hassan",
            },
            "inLanguage": "ur",
            "isFamilyFriendly": True,
        }

    # WebApplication / SoftwareApplication: Google requires applicationCategory + operatingSystem + offers.
    elif t in ("WebApplication", "SoftwareApplication"):
        base["applicationCategory"] = "GameApplication" if window["slug"] == "snake" else "ProductivityApplication"
        base["operatingSystem"] = "Any (web browser)"
        base["author"] = build_person_entity()
        base["offers"] = {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
        }
        base["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": "5",
            "ratingCount": "1",
            "bestRating": "5",
            "worstRating": "1",
        } if window["slug"] == "snake" else None
        if base["aggregateRating"] is None:
            del base["aggregateRating"]

    return base


FAQ_MAP = {
    "about": [
        ("Who is Ishaq Hassan?", "Ishaq Hassan is a senior full-stack software engineer based in Karachi, Pakistan with 13+ years of experience. He is a Flutter Framework Contributor with 6 merged PRs into the official Flutter repository, Engineering Manager at DigitalHire, and the creator of a 35-video Urdu Flutter course listed on the official Flutter documentation."),
        ("What is Ishaq's current role?", "Engineering Manager at DigitalHire, where he leads mobile and platform engineering."),
        ("How many years of experience does Ishaq have?", "Over 13 years of professional software engineering experience across mobile, backend, and web."),
    ],
    "flutter": [
        ("How many pull requests has Ishaq Hassan merged into Flutter?", "Six pull requests have been merged into the official Flutter framework at github.com/flutter/flutter, and three more are approved and awaiting merge."),
        ("What kinds of PRs are these?", "The merged PRs cover documentation corrections, API disposal guidance, CupertinoTextField improvements, Material widget fixes, DropdownMenu scroll padding, and LicenseRegistry NOTICES fixes. Each PR passed the Flutter team's tree-hygiene, test coverage and review standards."),
        ("Where can I verify these PRs?", "All PRs are public on GitHub. View the full authored list at github.com/flutter/flutter/pulls?q=author:ishaquehassan."),
    ],
    "speaking": [
        ("What topics does Ishaq speak on?", "Flutter framework internals, production-grade Dart patterns, Firebase scaling, and the path from app developer to open-source contributor."),
        ("Which events has Ishaq spoken at?", "GDG Kolachi Flutter Bootcamp, GDG Kolachi Code to Create (Road to DevFest 2025), Iqra University Flutter Seminar, and DevnCode Meetup IV among others."),
        ("How do I invite Ishaq for a talk?", "Reach out via the contact page at ishaqhassan.dev/contact or email hello@ishaqhassan.dev."),
    ],
    "oss": [
        ("Which open source Flutter packages has Ishaq authored?", "document_scanner_flutter (native scanning), flutter_alarm_background_trigger (background alarms), assets_indexer (R.java-style asset indexing), nadra_verisys_flutter (Pakistan NADRA SDK), and claude-remote-terminal."),
        ("Where are the packages published?", "All packages are on pub.dev under the ishaqhassan.dev publisher and on GitHub at github.com/ishaquehassan."),
        ("What license are the packages under?", "Most packages are MIT-licensed. Check the individual repo LICENSE files for specifics."),
    ],
    "tech": [
        ("What languages does Ishaq work with primarily?", "Dart and Flutter for mobile, Node.js and TypeScript for backend, Kotlin and Swift for native mobile, and React/Next.js for web."),
        ("What backend stack does Ishaq use?", "Node.js (Express, Fastify, NestJS), Firebase (Firestore, Cloud Functions, FCM, Auth), PostgreSQL, MongoDB, Redis, and selective Rust for performance-critical services."),
        ("What DevOps and AI tools?", "Docker, GitHub Actions, Nginx for infrastructure; Claude Code, Anthropic API, OpenAI API for AI-augmented engineering."),
    ],
    "articles": [
        ("What topics has Ishaq written about?", "Flutter framework internals (three-tree architecture, plugin development, state management), Dart language deep-dives (isolates, asset indexing), Firebase Cloud Functions in Kotlin, and the contribution path into the Flutter framework itself."),
        ("Where can I read these articles?", "Cross-posted across three platforms: this site (/blog/), Medium at medium.com/@ishaqhassan, and Dev.to at dev.to/ishaquehassan. Each /articles/<slug>/ page links to every platform that hosts the same piece."),
        ("How does cross-posting work for canonical SEO?", "Site-original articles list /blog/<slug>.html as canonical and Medium/Dev.to as sameAs. Medium-only articles are canonical to Medium. This avoids duplicate-content penalties and lets each platform rank the version most relevant to its audience."),
        ("How often does Ishaq publish?", "New long-form technical deep dives are published a few times per year, typically after completing notable engineering work or framework PRs."),
    ],
    "contact": [
        ("How do I contact Ishaq Hassan?", "Email hello@ishaqhassan.dev, or use LinkedIn at linkedin.com/in/ishaquehassan. Typical response time is within 48 hours."),
        ("Is Ishaq available for consulting?", "Yes. Visit ishaqhassan.dev/flutter-consultant.html for consulting engagements or ishaqhassan.dev/hire-flutter-developer.html for hiring inquiries."),
        ("Which platforms is Ishaq active on?", "GitHub, LinkedIn, X/Twitter, Medium, YouTube, and Stack Overflow. Links are on the contact page."),
    ],
    "github": [
        ("What is Ishaq Hassan's GitHub username?", "The GitHub handle is ishaquehassan. Full profile: github.com/ishaquehassan."),
        ("What are the most notable repositories?", "document_scanner_flutter, flutter_alarm_background_trigger, assets_indexer, claude-remote-terminal, and goal-agent. Plus upstream Flutter framework PRs."),
        ("Does Ishaq contribute to other OSS projects?", "Yes, including framework-level PRs merged into the Flutter repository itself."),
    ],
    "linkedin": [
        ("What is Ishaq Hassan's current role on LinkedIn?", "Engineering Manager at DigitalHire, leading AI-based video job board development and managing the mobile and platform teams."),
        ("Where can I find Ishaq's LinkedIn?", "linkedin.com/in/ishaquehassan."),
        ("What prior roles has Ishaq held?", "Senior Software Engineer at Confiz, Head of Engineering at Tech Idara, Software Engineer at Afiniti, and independent Flutter consulting."),
    ],
    "snake": [
        ("How do I play Snake Neon?", "Use the arrow keys or WASD on desktop. On mobile, pick one of three control schemes: Wheel (joystick), D-Pad (9-grid buttons), or full-screen Swipe gestures. Press ESC to pause."),
        ("Is the source code available?", "The game is part of the open-source portfolio at github.com/ishaquehassan/ishaqhassan.dev."),
        ("What technology powers Snake Neon?", "Pure vanilla JavaScript with a canvas-based renderer at 60fps using requestAnimationFrame. No framework or external dependency."),
    ],
    "flutter-course": [
        ("How many videos are in the Flutter course?", "35 videos across 7 sections: Foundation, Dart Basics, Object-Oriented Programming, Flutter UI, State Management, API and Networking, and Advanced."),
        ("What language is the course in?", "Urdu. The course is free and listed on the official Flutter documentation at docs.flutter.dev/resources/courses#urdu."),
        ("Where can I watch the course?", "On YouTube at the Flutter Course playlist, or inline via the interactive course viewer on the portfolio."),
    ],
    "wisesend": [
        ("What is WiseSend?", "A side project built and maintained by Ishaq Hassan under the XRLabs umbrella."),
        ("Where can I try WiseSend?", "The live product is at wisesend.xrlabs.app. It is also embedded as an inline window on the portfolio."),
        ("Is WiseSend open source?", "No, WiseSend is a product, not an open-source package."),
    ],
}


def build_faq_jsonld(window):
    qa = FAQ_MAP.get(window["id"], [])
    if not qa:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in qa
        ],
    }


def build_cross_links_html(current_slug):
    # Render a small sitemap-nav so search engines crawl every sibling path.
    items = [w for w in WINDOWS if w["slug"] != current_slug]
    links = "\n".join(
        f'    <li><a href="/{w["slug"]}/">{w["breadcrumb_name"]}</a></li>'
        for w in items
    )
    return (
        '<nav class="sitelinks" aria-label="Related sections">\n'
        '  <h2 class="sitelinks-h">Explore more</h2>\n'
        '  <ul class="sitelinks-grid">\n'
        f'{links}\n'
        '  </ul>\n'
        '</nav>'
    )


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<style id="ihp-redirect-mask">html{{visibility:hidden}}</style>
<script>
/* No-flash window redirect: hide page instantly, bots get content, humans get SPA with target window on top. */
(function(){{
  try{{
    var ua=(navigator.userAgent||'').toLowerCase();
    var botRE=/bot|crawler|spider|slurp|lighthouse|googlebot|bingbot|yandex|baiduspider|duckduckbot|applebot|claudebot|anthropic-ai|gptbot|perplexitybot|facebookexternalhit|linkedinbot|twitterbot|telegrambot|whatsapp|slackbot|discordbot|embedly|preview/;
    var stay=location.search.indexOf('stay=1')!==-1;
    if(botRE.test(ua)||stay){{
      var s=document.getElementById('ihp-redirect-mask');
      if(s)s.parentNode.removeChild(s);
      return;
    }}
    location.replace('/?w={window_id}');
  }}catch(e){{
    var s=document.getElementById('ihp-redirect-mask');
    if(s)s.parentNode.removeChild(s);
  }}
}})();
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="format-detection" content="telephone=no">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="googlebot" content="index, follow">
<meta name="author" content="Ishaq Hassan">
<meta name="theme-color" content="#0a0a1a">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{site}/{slug}/">
<link rel="icon" href="data:image/svg+xml,&lt;svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'&gt;&lt;text y='.9em' font-size='90'&gt;👨‍💻&lt;/text&gt;&lt;/svg&gt;">
<link rel="apple-touch-icon" href="/assets/profile-photo.png">
<link rel="manifest" href="/manifest.json">

<meta property="og:type" content="profile">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="{site}/{slug}/">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/png">
<meta property="og:image:alt" content="{og_image_alt}">
<meta property="og:site_name" content="Ishaq Hassan">
<meta property="og:locale" content="en_PK">
<meta property="profile:first_name" content="Ishaq">
<meta property="profile:last_name" content="Hassan">
<meta property="profile:username" content="ishaquehassan">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@ishaque_hassan">
<meta name="twitter:creator" content="@ishaque_hassan">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{og_desc}">
<meta name="twitter:image" content="{og_image}">
<meta name="twitter:image:alt" content="{og_image_alt}">

<script type="application/ld+json">{breadcrumb_jsonld}</script>
<script type="application/ld+json">{webpage_jsonld}</script>{faq_block}

<style>
  :root{{color-scheme:dark}}
  html,body{{margin:0;padding:0;background:#0b1120;color:#e5e7eb;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif;line-height:1.6}}
  .wrap{{max-width:820px;margin:0 auto;padding:48px 24px 80px}}
  nav.crumbs{{font-size:13px;color:#7dd3fc;margin-bottom:24px}}
  nav.crumbs a{{color:#7dd3fc;text-decoration:none}}
  nav.crumbs a:hover{{text-decoration:underline}}
  h1{{font-size:36px;font-weight:800;margin:0 0 8px;color:#fff;letter-spacing:-0.02em}}
  h2{{font-size:22px;font-weight:700;color:#fff;margin-top:36px;margin-bottom:12px}}
  .sub{{color:#94a3b8;margin:0 0 28px;font-size:16px}}
  a{{color:#7dd3fc}}
  code{{background:#1e293b;padding:2px 6px;border-radius:4px;font-size:0.9em}}
  kbd{{background:#1e293b;padding:2px 8px;border-radius:4px;border:1px solid #334155;font-size:0.85em}}
  ul,ol{{padding-left:20px}}
  li{{margin:6px 0}}
  .cta{{display:inline-block;margin-top:28px;padding:12px 22px;background:#7dd3fc;color:#0b1120;border-radius:8px;font-weight:700;text-decoration:none}}
  .cta:hover{{background:#38bdf8}}
  .faq{{margin-top:44px;padding-top:28px;border-top:1px solid #1e293b}}
  .faq-h{{font-size:15px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#7dd3fc;margin:0 0 14px}}
  .faq-item{{background:rgba(125,211,252,0.03);border:1px solid rgba(125,211,252,0.08);border-radius:10px;padding:14px 18px;margin:0 0 10px;transition:border-color .15s,background .15s}}
  .faq-item:hover{{border-color:rgba(125,211,252,0.18);background:rgba(125,211,252,0.05)}}
  .faq-item summary{{cursor:pointer;font-weight:600;color:#e2e8f0;font-size:15px;list-style:none}}
  .faq-item summary::-webkit-details-marker{{display:none}}
  .faq-item summary::after{{content:"+";float:right;color:#7dd3fc;font-weight:700;transition:transform .2s}}
  .faq-item[open] summary::after{{content:"−"}}
  .faq-item p{{margin:12px 0 0;color:#94a3b8;font-size:14px;line-height:1.65}}
  .sitelinks{{margin-top:56px;padding-top:28px;border-top:1px solid #1e293b}}
  .sitelinks-h{{font-size:13px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#7dd3fc;margin:0 0 14px}}
  .sitelinks-grid{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px 18px}}
  .sitelinks-grid li{{margin:0}}
  .sitelinks-grid a{{display:block;padding:8px 10px;border-radius:6px;color:#cbd5e1;text-decoration:none;transition:background .15s,color .15s}}
  .sitelinks-grid a:hover{{background:rgba(125,211,252,0.08);color:#7dd3fc}}
  footer{{margin-top:40px;padding-top:24px;border-top:1px solid #1e293b;color:#94a3b8;font-size:13px}}
  footer a{{color:#cbd5e1;text-decoration:underline}}
  footer a:hover{{color:#7dd3fc}}
</style>
</head>
<body>
<main class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> &rsaquo; {breadcrumb_name}</nav>
  <h1>{h1}</h1>
  <p class="sub">{desc}</p>
  {body_html}
  {faq_html}
  <a class="cta" href="/?w={window_id}">Open the interactive portfolio →</a>
  {cross_links}
  <footer>
    Part of <a href="/">Ishaq Hassan's interactive portfolio</a>: a macOS-style desktop experience with 13 windows, widgets and a live Snake game.
    &middot; Canonical view: <a href="/{slug}/">{site}/{slug}/</a>
  </footer>
</main>
</body>
</html>
"""


def generate():
    for w in WINDOWS:
        out_dir = REPO_ROOT / w["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        html = TEMPLATE.format(
            site=SITE,
            slug=w["slug"],
            window_id=w["id"],
            title=w["title"],
            desc=w["desc"],
            og_title=w["og_title"],
            og_desc=w["og_desc"],
            og_image=f"{SITE}/assets/og/{w['slug']}.png?v=" + ("3" if w['slug'] == 'articles' else "2"),
            og_image_alt=f"Ishaq Hassan: {w['breadcrumb_name']} (ishaqhassan.dev/{w['slug']})",
            h1=w["h1"],
            breadcrumb_name=w["breadcrumb_name"],
            body_html=w["body_html"].strip(),
            breadcrumb_jsonld=json.dumps(build_breadcrumb_jsonld(w), ensure_ascii=False),
            webpage_jsonld=json.dumps(build_webpage_jsonld(w), ensure_ascii=False),
            faq_block=(
                '\n<script type="application/ld+json">' + json.dumps(build_faq_jsonld(w), ensure_ascii=False) + '</script>'
                if build_faq_jsonld(w) else ''
            ),
            faq_html=(
                '<section class="faq" aria-labelledby="faq-h">\n  <h2 id="faq-h" class="faq-h">Frequently asked questions</h2>\n  '
                + ''.join(
                    f'<details class="faq-item"><summary><span>{q}</span></summary><p>{a}</p></details>\n  '
                    for q, a in FAQ_MAP.get(w["id"], [])
                ).rstrip()
                + '\n</section>'
                if FAQ_MAP.get(w["id"]) else ''
            ),
            cross_links=build_cross_links_html(w["slug"]),
        )
        out_path = out_dir / "index.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"[gen] {out_path.relative_to(REPO_ROOT)}")

    # Per-article SEO pages under /articles/<slug>/
    for art in ARTICLES_DATA:
        out_dir = REPO_ROOT / "articles" / art["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        html = build_article_page(art)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print(f"[gen] articles/{art['slug']}/index.html")


# =============================================================================
# Per-article (/articles/<slug>/) pages
# =============================================================================

ARTICLES_DATA = [
    {
        "slug": "flutter-still-matters-in-ai-era",
        "title": "One Spell, Every Kingdom: Flutter in the AI Era",
        "headline": "One Spell, Every Kingdom: Why Flutter Still Matters in the AI Era",
        "desc": "AI writes code in seconds. So does Flutter still matter? Yes, more than ever. Cross-platform was never about less typing, it was about fewer decisions.",
        "excerpt": "AI writes WHAT you ask. You still decide WHAT to ask. Cross-platform was never about less typing, it was about fewer decisions, and that gap is widening as code becomes cheap.",
        "topics": ["flutter", "ai", "strategy"],
        "tags": ["Flutter", "AI", "Cross-Platform"],
        "date": "2026-05-01",
        "modified": "2026-05-01",
        "read_mins": 7,
        "icon": "🪄",
        "canonical": f"{SITE}/blog/flutter-still-matters-in-ai-era.html",
        "primary_label": "On Site",
        "json_ld_type": "BlogPosting",
        "word_count": 1650,
        "key_takeaways": [
            "AI writes WHAT you ask. You still decide WHAT to ask. Decisions are the new bottleneck.",
            "Native's real cost was never typing twice. It was two parallel design, test, and hiring conversations.",
            "AI absorbs the typing cost. Cross-platform absorbs the decision cost. The two stack.",
            "Pick Flutter when team-velocity matters more than 1-2 ms of frame budget. Skip it for camera, audio DSP, deeply platform-integrated tooling.",
        ],
        "faq": [
            ("Does AI make Flutter learning easier or harder?", "Easier. Dart has a smaller surface area, AI holds more context, and the framework patterns are well-documented. Native means switching between Swift and Kotlin idioms, which fragments AI context."),
            ("Should I learn Swift or Kotlin if I already know Flutter?", "For app-layer work, no. Time is better spent going deep on Dart, Flutter internals, and the platform channel boundary. For systems engineering or platform-native ecosystems, learning the platform language pays off."),
            ("Is 'knowing what to ask' really a defensible skill in 5 years?", "Yes. Decision skill compounds with experience and lives in messy product context. AI keeps improving at the how. Humans keep being needed for the what and the why. The gap widens as code becomes cheaper."),
            ("When should I NOT pick Flutter even with AI?", "Camera-pipeline-heavy apps where every ms of capture-to-frame matters, audio DSP with sub-10ms latency, or tightly platform-integrated apps like keyboards, accessibility services, system utilities. For everything else in 2026, Flutter wins on team velocity."),
        ],
        "platforms": [
            {"id": "site",   "label": "On Site",  "url": f"{SITE}/blog/flutter-still-matters-in-ai-era.html?stay=1"},
            {"id": "devto",  "label": "Dev.to",   "url": "https://dev.to/ishaquehassan/one-spell-every-kingdom-why-flutter-still-matters-in-the-ai-era-b35"},
            {"id": "hashnode","label": "Hashnode", "url": "https://ishaquehassan.hashnode.dev/one-spell-every-kingdom-why-flutter-still-matters-in-the-ai-era"},
        ],
    },
    {
        "slug": "flutter-prs-merged",
        "title": "How I Got 6 PRs Merged Into Flutter Framework",
        "headline": "How a Pakistani Engineer Got 6 PRs Merged Into Flutter's Official Framework",
        "desc": "How a Pakistani engineer got 6 PRs merged into the Flutter framework. Practical guide for first-time framework contributors from Asia.",
        "excerpt": "A Karachi engineer's 90-day path into the Flutter framework: triage, the test-first bar, review etiquette, and how to repeat it.",
        "topics": ["flutter", "open-source", "tutorial"],
        "tags": ["Flutter", "Open Source", "Pakistan"],
        "date": "2026-04-24",
        "modified": "2026-05-05",
        "read_mins": 10,
        "icon": "🔀",
        "canonical": f"{SITE}/blog/how-i-got-6-prs-merged-into-flutter.html",
        "primary_label": "On Site",
        "json_ld_type": "BlogPosting",
        "word_count": 2100,
        "key_takeaways": [
            "Start with `good first issue` triage, not feature PRs. Earn the review etiquette first.",
            "Every PR needs a test. Fix-only diffs are rejected almost on sight.",
            "Tight, obvious diffs win. Reviewers reward clarity over cleverness.",
            "Plan three months, not three days. Sustainability beats burst contributions.",
        ],
        "faq": [
            ("How long does Flutter PR merging take?", "Median 2-4 weeks once review starts. First response usually lands in 3-7 days. Plan for at least one round of revisions even on small fixes."),
            ("Do I need to be a Google employee?", "No. External contributors get the same review path. Six of these PRs were merged from outside Google."),
            ("What is the hardest part?", "Writing the test that proves the fix without breaking adjacent paths. The Flutter team will not take a fix without a test that fails before and passes after."),
            ("Where do I find good-first-issues?", "github.com/flutter/flutter/labels/good%20first%20issue is the live list. Many are stale; pick ones with recent triage labels."),
        ],
        "platforms": [
            {"id": "site",   "label": "On Site",  "url": f"{SITE}/blog/how-i-got-6-prs-merged-into-flutter.html?stay=1"},
            {"id": "medium", "label": "Medium",   "url": "https://medium.com/@ishaqhassan/how-i-got-my-pull-requests-merged-into-flutters-official-repository-98d055f3270e"},
            {"id": "devto",  "label": "Dev.to",   "url": "https://dev.to/ishaquehassan/how-a-pakistani-engineer-got-6-pull-requests-merged-into-flutters-official-framework-51po"},
        ],
    },
    {
        "slug": "flutter-three-tree-architecture",
        "title": "Flutter's Three-Tree Architecture Explained",
        "headline": "Flutter's Three-Tree Architecture Explained: Widgets, Elements, RenderObjects",
        "desc": "Deep dive into Flutter's Widget, Element, and RenderObject trees. How they interact and why bugs hide in the gaps.",
        "excerpt": "Widget tree configures, Element tree mounts, RenderObject tree paints. The bugs that hide between the layers and how to debug them.",
        "topics": ["flutter", "architecture", "tutorial"],
        "tags": ["Flutter", "Framework Internals", "Rendering"],
        "date": "2026-04-25",
        "modified": "2026-05-05",
        "read_mins": 12,
        "icon": "🌳",
        "canonical": f"{SITE}/blog/flutter-three-tree-architecture-explained.html",
        "primary_label": "On Site",
        "json_ld_type": "BlogPosting",
        "word_count": 2200,
        "key_takeaways": [
            "Widgets are immutable configuration. Cheap to rebuild 60 times per second.",
            "Elements are persistent identity. They survive rebuilds and decide what to update.",
            "RenderObjects do the heavy lifting: layout, paint, hit-testing.",
            "Most 'weird' Flutter bugs live in the gap between Widget rebuilds and Element survival.",
        ],
        "faq": [
            ("Why does Flutter have three trees instead of one?", "Each tree solves a separate concern. Widgets are cheap immutable configuration. Elements are persistent identity. RenderObjects are heavy machinery. Splitting them lets Flutter rebuild widget configs 60x/sec without touching expensive RenderObjects."),
            ("When does a new Element get created?", "When the runtimeType or the Key of a widget at a given position changes. Same type plus same key (or null key) lets Flutter reuse the existing Element and update it in place."),
            ("What is the difference between StatelessWidget and StatefulWidget at the Element level?", "StatelessWidget produces a StatelessElement that just rebuilds child widgets on demand. StatefulWidget produces a StatefulElement that owns a State object that survives rebuilds and holds mutable state."),
            ("How do I debug Element-level bugs?", "Use Flutter Inspector's 'Show widget inspector' with the Element tree view, or call debugDumpApp(). Most 'ghost state' bugs come from Elements being reused when you expected them to be recreated, or vice versa."),
        ],
        "platforms": [
            {"id": "site",   "label": "On Site",  "url": f"{SITE}/blog/flutter-three-tree-architecture-explained.html?stay=1"},
            {"id": "medium", "label": "Medium",   "url": "https://medium.com/@ishaqhassan/how-flutters-three-tree-architecture-actually-works-953c8cc17226"},
            {"id": "devto",  "label": "Dev.to",   "url": "https://dev.to/ishaquehassan/flutter-three-tree-architecture-explained-widgets-elements-renderobjects-2h28"},
        ],
    },
    {
        "slug": "flutter-state-management-2026",
        "title": "Flutter State Management 2026: Decision Guide",
        "headline": "Flutter State Management in 2026: A Decision Guide for Production Apps",
        "desc": "Decision guide to Flutter state management in 2026. setState, Provider, Riverpod, Bloc, signals: when to use which.",
        "excerpt": "setState, InheritedWidget, Provider, Riverpod, Bloc, signals. When to use which, with honest tradeoffs from production.",
        "topics": ["flutter", "architecture", "tutorial"],
        "tags": ["Flutter", "State Management", "Architecture"],
        "date": "2026-04-25",
        "modified": "2026-05-05",
        "read_mins": 14,
        "icon": "⚛️",
        "canonical": f"{SITE}/blog/flutter-state-management-2026-guide.html",
        "primary_label": "On Site",
        "json_ld_type": "BlogPosting",
        "word_count": 2200,
        "key_takeaways": [
            "No single 'best' library. Pick by app size, team familiarity, and reactivity needs.",
            "setState plus a couple of InheritedWidgets covers most small apps.",
            "Riverpod has the best ergonomics for medium apps in 2026.",
            "Bloc remains safest for large enterprise event-sourcing apps.",
            "Signals (signals_flutter) are the rising option for fine-grained reactivity.",
        ],
        "faq": [
            ("What is the best Flutter state management library in 2026?", "There is no single best. For small apps, setState plus InheritedWidgets is enough. For medium apps, Riverpod has the best ergonomics. For large enterprise apps with event-sourcing requirements, Bloc remains safest. Signals are the rising fine-grained reactivity option."),
            ("Provider or Riverpod for a new project?", "Riverpod. Same author, evolved API, no BuildContext requirement, better testing story. Provider is fine if your team already knows it well, but new projects should start on Riverpod."),
            ("When does Bloc become worth its boilerplate?", "When you need explicit event sourcing, time-travel debugging, or a clear audit trail of state transitions. In smaller apps, the boilerplate cost outweighs the benefit."),
            ("Are signals replacing all of these?", "Not yet. Signals are excellent for fine-grained reactive UIs but the ecosystem is still maturing in 2026. Treat them as a complement to your primary state library, not a replacement."),
        ],
        "platforms": [
            {"id": "site",  "label": "On Site", "url": f"{SITE}/blog/flutter-state-management-2026-guide.html?stay=1"},
            {"id": "devto", "label": "Dev.to",  "url": "https://dev.to/ishaquehassan/flutter-state-management-in-2026-a-decision-guide-for-production-apps-4b36"},
        ],
    },
    {
        "slug": "flutter-plugins-case-study",
        "title": "Building Production Flutter Plugins: 156-Likes Case Study",
        "headline": "Building Production Flutter Plugins: A 156-Likes pub.dev Case Study",
        "desc": "A pub.dev plugin case study with 156 likes and 470 monthly downloads. Native bridges, federated architecture, real maintenance lessons.",
        "excerpt": "What it really takes to build, publish, and maintain a Flutter plugin with 156 pub.dev likes. Native bridges, federated architecture, support burden.",
        "topics": ["flutter", "open-source", "tutorial"],
        "tags": ["Flutter", "Plugin Development", "Open Source"],
        "date": "2026-04-25",
        "modified": "2026-05-05",
        "read_mins": 11,
        "icon": "🧩",
        "canonical": f"{SITE}/blog/building-production-flutter-plugins-case-study.html",
        "primary_label": "On Site",
        "json_ld_type": "BlogPosting",
        "word_count": 1900,
        "key_takeaways": [
            "Federated plugin architecture pays off the moment you add a third platform.",
            "Verified publisher status materially boosts pub.dev trust score.",
            "Support burden scales faster than downloads. Budget for issues.",
            "A clear example app is the single biggest driver of likes and adoption.",
        ],
        "faq": [
            ("How do I publish a Flutter plugin to pub.dev?", "Run flutter create --template=plugin to scaffold platform folders. Implement Swift / Kotlin platform code, expose via MethodChannel, set up a verified publisher under your owned domain, then dart pub publish."),
            ("Federated architecture: worth the complexity?", "Yes if you target three or more platforms (iOS, Android, Web, macOS, Windows, Linux). For two platforms, plain pubspec platforms section is simpler. Federated splits the public API from per-platform implementations."),
            ("How long until a plugin breaks even on maintenance?", "Realistically about 6 months of active issue triage before the community starts fixing things back. Until then, expect to spend 2-4 hours a week on issues, PRs, and SDK upgrade compatibility."),
            ("What gets a Flutter plugin to 100+ likes?", "A working example app, clear README with native screenshots, immediate response to first 20 issues, and a real production use-case story. Likes follow trust, not features."),
        ],
        "platforms": [
            {"id": "site",  "label": "On Site", "url": f"{SITE}/blog/building-production-flutter-plugins-case-study.html?stay=1"},
            {"id": "devto", "label": "Dev.to",  "url": "https://dev.to/ishaquehassan/building-production-flutter-plugins-a-156-likes-pubdev-case-study-4e3a"},
        ],
    },
    {
        "slug": "dart-isolates-guide",
        "title": "Dart Isolates: The Missing Guide",
        "headline": "Dart Isolates: The Missing Guide for Production Flutter Apps",
        "desc": "Production guide to Dart isolates: ports, message passing, compute(), and real-world patterns for Flutter apps.",
        "excerpt": "Concurrency primitives, ports, real-world patterns. The piece every Flutter dev wishes they had read before shipping their first heavy compute feature.",
        "topics": ["flutter", "tutorial"],
        "tags": ["Dart", "Concurrency", "Performance"],
        "date": "2024-08-12",
        "modified": "2024-08-12",
        "read_mins": 8,
        "icon": "🧩",
        "canonical": "https://medium.com/@ishaqhassan/dart-isolates-the-missing-guide-for-production-flutter-apps-66ed990ced3e",
        "primary_label": "Medium",
        "json_ld_type": "Article",
        "word_count": 1600,
        "key_takeaways": [
            "Isolates are not threads. They share no memory, only messages.",
            "compute() is fine for one-shot heavy work. Long-lived isolates need spawn().",
            "SendPort / ReceivePort patterns power most production isolate use.",
            "Always close ports and exit isolates explicitly to avoid leaks.",
        ],
        "faq": [
            ("When should I use an isolate vs async/await?", "Use async/await for I/O-bound work like network calls and file reads. Use an isolate when CPU-bound work would block the UI thread, typically anything over 16ms of synchronous compute on the main isolate."),
            ("What is the overhead of spawning an isolate?", "Around 1-3ms on modern devices, plus the memory cost of a fresh heap. For one-shot work, compute() amortises this nicely. For repeated work, keep an isolate alive and message it."),
            ("Can isolates share memory?", "Not in the general case. They communicate via copied messages. TransferableTypedData and Isolate.exit can move ownership of typed buffers without a copy, which is the main exception."),
            ("Why does my isolate code freeze the UI?", "Most likely you are awaiting the isolate result on the main isolate without a yield. Wrap the call so the main isolate stays responsive while the worker runs."),
        ],
        "platforms": [
            {"id": "medium", "label": "Medium", "url": "https://medium.com/@ishaqhassan/dart-isolates-the-missing-guide-for-production-flutter-apps-66ed990ced3e"},
        ],
    },
    {
        "slug": "flutter-native-plugins-journey",
        "title": "A Journey with Flutter Native Plugin Development",
        "headline": "A Journey with Flutter Native Plugin Development for iOS and Android",
        "desc": "A field guide to building Flutter native plugins for iOS and Android. Method channels, platform views, common pitfalls.",
        "excerpt": "Building cross-platform plugins for iOS and Android from scratch. Code, pitfalls, real examples from a published plugin author.",
        "topics": ["flutter", "tutorial", "open-source"],
        "tags": ["Flutter", "iOS", "Android"],
        "date": "2021-06-04",
        "modified": "2021-06-04",
        "read_mins": 7,
        "icon": "📱",
        "canonical": "https://medium.com/nerd-for-tech/a-journey-with-flutter-native-plugin-development-for-ios-android-3f0dd4ab8061",
        "primary_label": "Medium",
        "json_ld_type": "Article",
        "word_count": 1300,
        "key_takeaways": [
            "MethodChannel is enough for 80% of native plugin work.",
            "EventChannel handles streams from native to Dart.",
            "PlatformView is for actual native UI, not just data.",
            "iOS Swift bridge is finicky. Pin Xcode and Flutter versions in CI.",
        ],
        "faq": [
            ("MethodChannel vs PlatformView: which to use?", "MethodChannel for one-off function calls and data exchange. PlatformView only when you need to embed an actual native UIView or Android View inside the Flutter widget tree."),
            ("How do I debug native plugin crashes?", "On iOS, attach Xcode to the running iOS device or simulator and watch the console. On Android, run flutter logs while the app runs and look for native stack traces alongside Dart errors."),
            ("Should I write Swift or Objective-C for the iOS side?", "Swift in 2024+. Objective-C is only worth it if you must support an old codebase. The Flutter plugin template defaults to Swift now."),
            ("How do I publish a native plugin?", "Same flow as any pub.dev package: dart pub publish from the plugin root. Make sure your example app builds on both platforms before publishing or your pub score takes a hit."),
        ],
        "platforms": [
            {"id": "medium", "label": "Medium", "url": "https://medium.com/nerd-for-tech/a-journey-with-flutter-native-plugin-development-for-ios-android-3f0dd4ab8061"},
        ],
    },
    {
        "slug": "dart-asset-indexing",
        "title": "Indexing Assets in a Dart Class (R.java pattern)",
        "headline": "Indexing Assets in a Dart Class Just Like R.java",
        "desc": "Generate typed Flutter asset references in a Dart class. Inspired by Android R.java. End string-based asset path bugs.",
        "excerpt": "Auto-generate typed asset references with codegen, inspired by Android's R.java. Drop string-based asset paths forever.",
        "topics": ["flutter", "tutorial", "open-source", "tip"],
        "tags": ["Dart", "Codegen", "Tooling"],
        "date": "2020-09-22",
        "modified": "2020-09-22",
        "read_mins": 6,
        "icon": "📁",
        "canonical": "https://medium.com/nerd-for-tech/indexing-assets-in-a-dart-class-just-like-r-java-flutter-3febf558a2bb",
        "primary_label": "Medium",
        "json_ld_type": "Article",
        "word_count": 1100,
        "key_takeaways": [
            "Stringly-typed asset paths are a top-3 source of 'release-only' bugs.",
            "A pre-build script can scan /assets and emit a typed Dart class.",
            "IDE autocomplete for asset names is a quiet productivity multiplier.",
            "Bonus: detect dead assets at build time and remove them from final IPA / APK.",
        ],
        "faq": [
            ("Do I need build_runner or just a script?", "A plain Dart script that scans /assets and writes lib/generated/assets.dart is enough. build_runner is overkill unless you already use it for other codegen."),
            ("What if my designer renames an asset?", "Re-run the generator. Any usage referencing the old name fails to compile, which is the entire point. You catch the rename at build time, not at runtime in production."),
            ("Can this work with --tree-shake-icons?", "Yes. The generator emits string constants, not Widget instances. Tree-shaking still applies normally to anything you build with those strings."),
            ("Is there a published package?", "Yes: assets_indexer on pub.dev. Or copy the generator into your own project; it is roughly 80 lines of Dart."),
        ],
        "platforms": [
            {"id": "medium", "label": "Medium", "url": "https://medium.com/nerd-for-tech/indexing-assets-in-a-dart-class-just-like-r-java-flutter-3febf558a2bb"},
        ],
    },
    {
        "slug": "firebase-kotlin-functions",
        "title": "Firebase Cloud Functions Using Kotlin",
        "headline": "Firebase Cloud Functions Using Kotlin",
        "desc": "Run Firebase Cloud Functions in Kotlin with GraalVM. Setup guide, performance numbers, real-world caveats.",
        "excerpt": "Writing Cloud Functions in Kotlin via GraalVM. Performance wins, full setup guide, and the caveats nobody warns you about.",
        "topics": ["architecture", "tutorial"],
        "tags": ["Kotlin", "Firebase", "Backend"],
        "date": "2022-11-15",
        "modified": "2022-11-15",
        "read_mins": 5,
        "icon": "🔥",
        "canonical": "https://medium.com/@ishaqhassan/firebase-cloud-functions-using-kotlin-55631dd43f67",
        "primary_label": "Medium",
        "json_ld_type": "Article",
        "word_count": 900,
        "key_takeaways": [
            "Kotlin via GraalVM Native Image runs as fast as Node in cold starts.",
            "You lose the Node ecosystem; not every Firebase Admin call has a Kotlin equivalent.",
            "Setup is involved: GraalVM, Gradle plugin, Firebase emulator config.",
            "Pick this only if your team already lives in Kotlin and refuses to switch.",
        ],
        "faq": [
            ("Why use Kotlin for Cloud Functions instead of Node?", "Type safety, sharing code with an Android backend, and team familiarity. The native ecosystem is much smaller, so it is a deliberate tradeoff, not a default."),
            ("What about cold-start performance?", "GraalVM Native Image brings Kotlin cold-starts close to Node. Without it, JVM cold-starts make Cloud Functions painfully slow for HTTPS triggers."),
            ("Can I use Firebase Admin SDK from Kotlin?", "Yes, the Java Firebase Admin SDK works fine. Just be aware not every helper from the Node SDK has a direct Kotlin / Java equivalent."),
            ("Is this production ready?", "For internal services or background workers, yes. For latency-sensitive HTTPS endpoints, only if you have GraalVM tuned and accept higher operational complexity."),
        ],
        "platforms": [
            {"id": "medium", "label": "Medium", "url": "https://medium.com/@ishaqhassan/firebase-cloud-functions-using-kotlin-55631dd43f67"},
        ],
    },
    {
        "slug": "devncode-meetup-iv-ai",
        "title": "DevnCode Meetup IV: Artificial Intelligence",
        "headline": "DevnCode Meetup IV: Artificial Intelligence",
        "desc": "Recap of DevnCode Meetup IV on AI. Talks, takeaways, the state of practical AI in 2024 from the Karachi developer scene.",
        "excerpt": "Recap and takeaways from the DevnCode AI meetup. The state of practical AI in 2024, the talks, the people, what stuck.",
        "topics": ["tutorial"],
        "tags": ["AI", "Community", "Speaking"],
        "date": "2024-05-18",
        "modified": "2024-05-18",
        "read_mins": 4,
        "icon": "🤖",
        "canonical": "https://medium.com/devncode/devncode-meetup-iv-artificial-intelligence-df8c602de7d5",
        "primary_label": "Medium",
        "json_ld_type": "Article",
        "word_count": 700,
        "key_takeaways": [
            "Pakistani developer community is rapidly upskilling on practical AI.",
            "Local meetups are still the highest-signal way to meet people doing real work.",
            "Speakers covered LLM ops, prompt engineering, and applied vector search.",
            "Bring your laptop. Demo culture beats slide culture.",
        ],
        "faq": [
            ("What was DevnCode Meetup IV about?", "The fourth instalment of the DevnCode meetup focused on practical applied AI: LLM ops, prompt engineering, vector search, and shipping AI features in production apps."),
            ("Who spoke?", "A mix of Karachi-based founders, senior engineers, and AI researchers. Talks covered both 'ship today' and longer horizon research themes."),
            ("Will there be a Meetup V?", "DevnCode runs roughly 1-2 meetups per year. Watch the DevnCode publication on Medium for announcements."),
            ("Are slides or video available?", "A community recap is on Medium. Selected talks were recorded; check the DevnCode publication for the latest videos."),
        ],
        "platforms": [
            {"id": "medium", "label": "Medium", "url": "https://medium.com/devncode/devncode-meetup-iv-artificial-intelligence-df8c602de7d5"},
        ],
    },
]

ARTICLE_PLATFORM_BRAND = {
    "site":   {"color": "#7dd3fc", "name": "On Site"},
    "medium": {"color": "#86efac", "name": "Medium"},
    "devto":  {"color": "#cbd5e1", "name": "Dev.to"},
}


def article_breadcrumb_jsonld(art):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",     "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Articles", "item": f"{SITE}/articles/"},
            {"@type": "ListItem", "position": 3, "name": art["headline"], "item": f"{SITE}/articles/{art['slug']}/"},
        ],
    }


def article_blogposting_jsonld(art):
    # sameAs lists OTHER platform URLs that host the same content. Drop the canonical
    # URL itself (canonical handles that) and drop /blog/<slug>.html?stay=1 variants
    # since they're just the canonical with a query flag.
    canon_path = art["canonical"].split('?')[0]
    same_as = []
    for p in art["platforms"]:
        clean = p["url"].split('?')[0]
        if clean == canon_path:
            continue
        same_as.append(p["url"])
    base = {
        "@context": "https://schema.org",
        "@type": art["json_ld_type"],
        "@id": f"{SITE}/articles/{art['slug']}/",
        "url": f"{SITE}/articles/{art['slug']}/",
        "mainEntityOfPage": {"@type": "WebPage", "@id": art["canonical"]},
        "headline": art["headline"],
        "name": art["headline"],
        "description": art["desc"],
        "image": [f"{SITE}/assets/articles/og-{art['slug']}.jpg"],
        "datePublished": art["date"],
        "dateModified": art.get("modified", art["date"]),
        "author": build_person_entity(),
        "publisher": build_person_entity(),
        "keywords": ", ".join(art["tags"] + art["topics"]),
        "articleSection": art["tags"][0] if art["tags"] else "Engineering",
        "inLanguage": "en",
        "wordCount": art.get("word_count", 1500),
        "isPartOf": {"@type": "Blog", "@id": f"{SITE}/articles/", "url": f"{SITE}/articles/", "name": "Articles | Ishaq Hassan"},
    }
    if same_as:
        base["sameAs"] = same_as
    return base


def article_faq_jsonld(art):
    if not art.get("faq"):
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in art["faq"]
        ],
    }


def article_platform_chips_html(art):
    chips = []
    for p in art["platforms"]:
        brand = ARTICLE_PLATFORM_BRAND.get(p["id"], {"color": "#7dd3fc", "name": p["label"]})
        chips.append(
            f'    <li><a class="platform-chip" data-p="{p["id"]}" href="{p["url"]}" '
            + ('rel="noopener noreferrer" target="_blank"' if p["id"] != "site" else '')
            + f' style="border-color:{brand["color"]};color:{brand["color"]};">'
            + f'<strong>{p["label"]}</strong>'
            + (' · external' if p["id"] != "site" else '')
            + '</a></li>'
        )
    return '<ul class="platform-list">\n' + '\n'.join(chips) + '\n  </ul>'


def article_takeaways_html(art):
    items = '\n'.join(f'    <li>{t}</li>' for t in art["key_takeaways"])
    return f'<h2>Key takeaways</h2>\n  <ul>\n{items}\n  </ul>'


def article_faq_html(art):
    if not art.get("faq"):
        return ''
    items = '\n  '.join(
        f'<details class="faq-item"><summary><span>{q}</span></summary><p>{a}</p></details>'
        for q, a in art["faq"]
    )
    return (
        '<section class="faq" aria-labelledby="art-faq-h">\n'
        '  <h2 id="art-faq-h" class="faq-h">Frequently asked questions</h2>\n  '
        + items + '\n</section>'
    )


def article_cross_links_html(current_slug):
    others = [a for a in ARTICLES_DATA if a["slug"] != current_slug]
    article_links = '\n'.join(
        f'    <li><a href="/articles/{a["slug"]}/">{a["headline"]}</a></li>'
        for a in others
    )
    section_links = '\n'.join(
        f'    <li><a href="/{w["slug"]}/">{w["breadcrumb_name"]}</a></li>'
        for w in WINDOWS if w["slug"] != "articles"
    )
    return (
        '<nav class="sitelinks" aria-label="Other articles">\n'
        '  <h2 class="sitelinks-h">More articles</h2>\n'
        '  <ul class="sitelinks-grid">\n'
        f'{article_links}\n'
        '  </ul>\n'
        '</nav>\n'
        '<nav class="sitelinks" aria-label="Other sections">\n'
        '  <h2 class="sitelinks-h">Other sections</h2>\n'
        '  <ul class="sitelinks-grid">\n'
        f'{section_links}\n'
        '  </ul>\n'
        '</nav>'
    )


ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<style id="ihp-redirect-mask">html{{visibility:hidden}}</style>
<script>
(function(){{
  try{{
    var ua=(navigator.userAgent||'').toLowerCase();
    var botRE=/bot|crawler|spider|slurp|lighthouse|googlebot|bingbot|yandex|baiduspider|duckduckbot|applebot|claudebot|anthropic-ai|gptbot|perplexitybot|facebookexternalhit|linkedinbot|twitterbot|telegrambot|whatsapp|slackbot|discordbot|embedly|preview/;
    var stay=location.search.indexOf('stay=1')!==-1;
    if(botRE.test(ua)||stay){{
      var s=document.getElementById('ihp-redirect-mask');
      if(s)s.parentNode.removeChild(s);
      return;
    }}
    location.replace('/?w=articles&a={slug}');
  }}catch(e){{
    var s=document.getElementById('ihp-redirect-mask');
    if(s)s.parentNode.removeChild(s);
  }}
}})();
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="format-detection" content="telephone=no">
<title>{title} | Ishaq Hassan</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="googlebot" content="index, follow">
<meta name="author" content="Ishaq Hassan">
<meta name="theme-color" content="#0a0a1a">
<meta name="color-scheme" content="dark">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="data:image/svg+xml,&lt;svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'&gt;&lt;text y='.9em' font-size='90'&gt;👨‍💻&lt;/text&gt;&lt;/svg&gt;">
<link rel="apple-touch-icon" href="/assets/profile-photo.png">
<link rel="manifest" href="/manifest.json">

<meta property="og:type" content="article">
<meta property="og:title" content="{headline}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}/articles/{slug}/">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="{headline} by Ishaq Hassan">
<meta property="og:site_name" content="Ishaq Hassan">
<meta property="og:locale" content="en_PK">
<meta property="article:published_time" content="{date}T08:00:00+05:00">
<meta property="article:modified_time" content="{modified}">
<meta property="article:author" content="Ishaq Hassan">
<meta property="article:section" content="{section}">
{article_tags}

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@ishaque_hassan">
<meta name="twitter:creator" content="@ishaque_hassan">
<meta name="twitter:title" content="{headline}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<meta name="twitter:image:alt" content="{headline} by Ishaq Hassan">

<script type="application/ld+json">{breadcrumb_jsonld}</script>
<script type="application/ld+json">{blogposting_jsonld}</script>{faq_block}

<style>
  :root{{color-scheme:dark}}
  html,body{{margin:0;padding:0;background:#0b1120;color:#e5e7eb;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Segoe UI',Roboto,sans-serif;line-height:1.6}}
  .wrap{{max-width:820px;margin:0 auto;padding:48px 24px 80px}}
  nav.crumbs{{font-size:13px;color:#7dd3fc;margin-bottom:24px}}
  nav.crumbs a{{color:#7dd3fc;text-decoration:none}}
  nav.crumbs a:hover{{text-decoration:underline}}
  h1{{font-size:34px;font-weight:800;margin:0 0 8px;color:#fff;letter-spacing:-0.02em;line-height:1.2}}
  h2{{font-size:22px;font-weight:700;color:#fff;margin-top:36px;margin-bottom:12px}}
  .meta{{color:#94a3b8;font-size:13px;margin:0 0 12px;letter-spacing:0.2px}}
  .tag-row{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}}
  .tag-row span{{font-size:10.5px;font-weight:600;padding:3px 9px;border-radius:999px;background:rgba(125,211,252,0.1);color:#7dd3fc;letter-spacing:0.3px;text-transform:uppercase}}
  .sub{{color:#cbd5e1;margin:0 0 28px;font-size:16px;line-height:1.6}}
  a{{color:#7dd3fc}}
  ul,ol{{padding-left:20px}}
  li{{margin:6px 0}}
  .platform-list{{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:8px;margin:0 0 28px}}
  .platform-list li{{margin:0}}
  .platform-chip{{display:inline-block;padding:8px 14px;border-radius:8px;border:1px solid #7dd3fc;color:#7dd3fc;font-size:12.5px;font-weight:600;text-decoration:none;transition:background 0.18s,color 0.18s}}
  .platform-chip:hover{{background:#7dd3fc;color:#0b1120}}
  .cta{{display:inline-block;margin-top:14px;padding:12px 22px;background:#7dd3fc;color:#0b1120;border-radius:8px;font-weight:700;text-decoration:none}}
  .cta:hover{{background:#38bdf8}}
  .faq{{margin-top:44px;padding-top:28px;border-top:1px solid #1e293b}}
  .faq-h{{font-size:15px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#7dd3fc;margin:0 0 14px}}
  .faq-item{{background:rgba(125,211,252,0.03);border:1px solid rgba(125,211,252,0.08);border-radius:10px;padding:14px 18px;margin:0 0 10px;transition:border-color .15s,background .15s}}
  .faq-item:hover{{border-color:rgba(125,211,252,0.18);background:rgba(125,211,252,0.05)}}
  .faq-item summary{{cursor:pointer;font-weight:600;color:#e2e8f0;font-size:15px;list-style:none}}
  .faq-item summary::-webkit-details-marker{{display:none}}
  .faq-item summary::after{{content:"+";float:right;color:#7dd3fc;font-weight:700;transition:transform .2s}}
  .faq-item[open] summary::after{{content:"−"}}
  .faq-item p{{margin:12px 0 0;color:#94a3b8;font-size:14px;line-height:1.65}}
  .sitelinks{{margin-top:48px;padding-top:24px;border-top:1px solid #1e293b}}
  .sitelinks-h{{font-size:13px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#7dd3fc;margin:0 0 14px}}
  .sitelinks-grid{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px 18px}}
  .sitelinks-grid li{{margin:0}}
  .sitelinks-grid a{{display:block;padding:8px 10px;border-radius:6px;color:#cbd5e1;text-decoration:none;transition:background .15s,color .15s;font-size:13px;line-height:1.4}}
  .sitelinks-grid a:hover{{background:rgba(125,211,252,0.08);color:#7dd3fc}}
  footer{{margin-top:40px;padding-top:24px;border-top:1px solid #1e293b;color:#94a3b8;font-size:13px}}
  footer a{{color:#cbd5e1;text-decoration:underline}}
  footer a:hover{{color:#7dd3fc}}
  .hero-icon{{font-size:60px;margin:0 0 20px}}
</style>
</head>
<body>
<main class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/articles/">Articles</a> &rsaquo; {title}</nav>
  <article>
    <div class="hero-icon" aria-hidden="true">{icon}</div>
    <div class="tag-row">{tag_chips}</div>
    <h1>{headline}</h1>
    <p class="meta">{date} &middot; {read_mins} min read &middot; by Ishaq Hassan</p>
    <p class="sub">{excerpt}</p>
    <h2>Read on</h2>
    {platform_chips}
    <a class="cta" href="{primary_url}">Read on {primary_label} →</a>
    {takeaways}
    {faq_html}
  </article>
  {cross_links}
  <footer>
    Part of <a href="/articles/">Ishaq Hassan's Articles</a> hub. Cross-platform writing index across Site, Medium, Dev.to.
    &middot; Open the interactive view: <a href="/articles/{slug}/">/articles/{slug}/</a>
  </footer>
</main>
</body>
</html>
"""


def build_article_page(art):
    primary = art["platforms"][0]
    article_tags_html = '\n'.join(f'<meta property="article:tag" content="{t}">' for t in art["tags"])
    tag_chips_html = ''.join(f'<span>{t}</span>' for t in art["tags"])
    return ARTICLE_TEMPLATE.format(
        site=SITE,
        slug=art["slug"],
        title=art["title"],
        headline=art["headline"],
        desc=art["desc"],
        excerpt=art["excerpt"],
        date=art["date"],
        modified=art.get("modified", art["date"]),
        read_mins=art["read_mins"],
        icon=art["icon"],
        canonical=art["canonical"],
        og_image=f"{SITE}/assets/articles/og-{art['slug']}.jpg?v=" + ("9" if art['slug'] == 'flutter-still-matters-in-ai-era' else "2"),
        section=art["tags"][0] if art["tags"] else "Engineering",
        article_tags=article_tags_html,
        tag_chips=tag_chips_html,
        breadcrumb_jsonld=json.dumps(article_breadcrumb_jsonld(art), ensure_ascii=False),
        blogposting_jsonld=json.dumps(article_blogposting_jsonld(art), ensure_ascii=False),
        faq_block=(
            '\n<script type="application/ld+json">' + json.dumps(article_faq_jsonld(art), ensure_ascii=False) + '</script>'
            if article_faq_jsonld(art) else ''
        ),
        platform_chips=article_platform_chips_html(art),
        primary_url=primary["url"],
        primary_label=primary["label"],
        takeaways=article_takeaways_html(art),
        faq_html=article_faq_html(art),
        cross_links=article_cross_links_html(art["slug"]),
    )


if __name__ == "__main__":
    generate()
    print(f"\nGenerated {len(WINDOWS)} window pages + {len(ARTICLES_DATA)} article pages.")
