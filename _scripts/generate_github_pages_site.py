from __future__ import annotations

import html
import re
import shutil
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = ROOT / "docs"
ROOT_INDEX_PATH = ROOT / "index.html"
ROOT_REPORT_DIR = ROOT / "report"
ROOT_ASSETS_DIR = ROOT / "assets"
MARKDOWN_PATH = ROOT / "CMP-X305_coursework_report.md"
SUBMISSION_SOURCE = Path(r"c:\Users\sukhj\OneDrive\Desktop\.-\Coursework Portfolio 1 - Formatted.pdf")
SUBMISSION_FILENAME = "coursework-portfolio-1-formatted.pdf"
SUBMISSION_DEST = SITE_ROOT / "assets" / "docs" / SUBMISSION_FILENAME
LEGACY_DOWNLOADS = [
    SITE_ROOT / "assets" / "docs" / "cyb-report-fixed-v3.pdf",
    ROOT / "assets" / "docs" / "cyb-report-fixed-v3.pdf",
    SITE_ROOT / "assets" / "docs" / "cmp-x305-cybersecurity-portfolio-final.docx",
    ROOT / "assets" / "docs" / "cmp-x305-cybersecurity-portfolio-final.docx",
]
SOURCE_CSS = ROOT / "assets" / "css" / "styles.css"
SOURCE_JS = ROOT / "assets" / "js" / "site.js"
SITE_URL = "https://who-sekhon.github.io/cyb"
OG_IMAGE_PATH = "/assets/img/week-09/figure-30-week-9-nessus-severity-comparison-graph.png"

SECTION_ID_MAP = {
    "1. Introduction": "intro",
    "2. Week 05 - Web Application Security Lab (WPScan)": "week-05",
    "3. Week 07 - OWASP Juice Shop Lab": "week-07",
    "4. Week 08 - Vulnerability Assessment Lab (Nmap and SSH)": "week-08",
    "5. Week 09 - Vulnerability Scanning and Mitigation Lab (Nessus)": "week-09",
    "6. Overall Reflection and Conclusion": "conclusion",
    "7. AI Use Statement": "ai-use",
    "8. References": "references",
}

SECTION_SEQUENCE = [
    "intro",
    "week-05",
    "week-07",
    "week-08",
    "week-09",
    "conclusion",
    "ai-use",
    "references",
]

SECTION_LABELS = {
    "intro": "Introduction",
    "week-05": "Week 05",
    "week-07": "Week 07",
    "week-08": "Week 08",
    "week-09": "Week 09",
    "conclusion": "Conclusion",
    "ai-use": "AI use",
    "references": "References",
}

HEADING_TEXT_FIXES = {
    ("week-09", "5.5 Reflection"): "5.6 Reflection",
}

WEEK_DETAILS = {
    "week-05": {
        "label": "Week 05",
        "title": "Web Application Security Lab",
        "topic": "WPScan against a live WordPress environment",
        "summary": "Automated WordPress reconnaissance exposed patch lag, directory indexing, and XML-RPC attack surface that reduced attacker uncertainty.",
        "tools": "WPScan, Kali Linux, WordPress",
        "outcomes": "LO1, LO3",
        "figures": "6 figures",
        "focus": "Enumeration and hardening",
        "evidence": "Admin access, scanner output, advisory trace, and directory exposure evidence",
        "verdict": "The clearest confirmed issue was unnecessary information disclosure through directory indexing and publicly exposed WordPress metadata.",
        "finding": "Directory listing and WordPress surface disclosure made the site easier to profile.",
        "action": "Disable directory indexes, tighten XML-RPC exposure, and keep WordPress components patched.",
    },
    "week-07": {
        "label": "Week 07",
        "title": "OWASP Juice Shop Lab",
        "topic": "Hands-on exploitation of deliberately vulnerable web behaviour",
        "summary": "Challenge evidence captures DOM XSS, hidden route discovery, weak authentication, and business logic abuse inside Juice Shop.",
        "tools": "OWASP Juice Shop, Browser Workflow",
        "outcomes": "LO1, LO2, LO3",
        "figures": "9 figures",
        "focus": "Application misuse in practice",
        "evidence": "Solved challenge banners, payload execution, and route-discovery captures",
        "verdict": "Week 07 shows the strongest exploit evidence, especially the DOM XSS payload that executes directly in the browser context.",
        "finding": "DOM-based XSS and hidden-route discovery showed how weak client-side controls fail under direct interaction.",
        "action": "Strengthen input handling, remove weak hidden-route assumptions, and protect confidential routes with real access control.",
    },
    "week-08": {
        "label": "Week 08",
        "title": "Vulnerability Assessment Lab",
        "topic": "Reconnaissance with Nmap and secure administration with SSH",
        "summary": "The lab links host discovery to defensive administration by mapping services and then demonstrating secure remote access, key deployment, and tunnelling.",
        "tools": "Nmap, OpenSSH, Kali Linux",
        "outcomes": "LO1, LO2",
        "figures": "8 figures",
        "focus": "Discovery plus secure access",
        "evidence": "IP verification, service enumeration, SSH session setup, and secure tunnel commands",
        "verdict": "The key lesson is not simply that services were visible, but that administrative exposure must be narrowed and protected by better SSH practice.",
        "finding": "Nmap exposed SSH, HTTP, MySQL, and NRPE services that expanded the practical attack surface.",
        "action": "Restrict exposed services, prefer key-based authentication, and hide administrative workflows behind tunnels or firewall rules.",
    },
    "week-09": {
        "label": "Week 09",
        "title": "Vulnerability Scanning and Mitigation",
        "topic": "Nessus-driven vulnerability management and reporting",
        "summary": "Nessus was configured, results were compared across two hosts, and the WordPress host was shown to carry the more important risk profile.",
        "tools": "Nessus Essentials, PDF Evidence Export",
        "outcomes": "LO1, LO2",
        "figures": "7 figures",
        "focus": "Risk comparison and prioritisation",
        "evidence": "Scanner interface, completed jobs, exported PDFs, and severity comparison graph",
        "verdict": "Week 09 is the strongest marker-facing section because it converts evidence into prioritisation, comparison, and concrete remediation.",
        "finding": "The WordPress host carried the only medium-severity issue: SSH Terrapin Prefix Truncation Weakness (CVE-2023-48795).",
        "action": "Patch the affected SSH stack, review enabled algorithms, and re-run a credentialed follow-up scan for higher confidence.",
    },
}

SECTION_NOTES = {
    "intro": {
        "label": "Portfolio framing",
        "summary": "Module context, evidence provenance, and explicit mapping to the coursework learning outcomes.",
    },
    "conclusion": {
        "label": "Integrated reflection",
        "summary": "Cross-lab synthesis of enumeration, exploitation, secure administration, and structured vulnerability reporting.",
    },
    "ai-use": {
        "label": "Academic declaration",
        "summary": "A transparent note describing editorial AI assistance without claiming fabricated evidence or unsupported findings.",
    },
    "references": {
        "label": "Source trail",
        "summary": "IEEE-style references spanning university lab sheets, tool documentation, and the exported Nessus evidence.",
    },
}

IMAGE_PATTERN = re.compile(r"!\[(.*?)\]\(<(.*?)>\)")
URL_PATTERN = re.compile(r"https?://[^\s<]+")
TRAILING_URL_PUNCTUATION = ".,;:)"


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text).strip("-").lower()
    return slug or "item"


def week_slug_from_path(path_text: str) -> str:
    lowered = path_text.lower()
    if "week 5" in lowered:
        return "week-05"
    if "week 7" in lowered:
        return "week-07"
    if "week 8" in lowered:
        return "week-08"
    if "week 9" in lowered:
        return "week-09"
    return "misc"


def read_markdown() -> tuple[str, dict[str, str]]:
    text = MARKDOWN_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    metadata: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        match = re.match(r"\*\*(.+?):\*\*\s*(.+)", stripped)
        if match:
            metadata[match.group(1).strip()] = match.group(2).strip()
    return text, metadata


def copy_if_changed(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and source.read_bytes() == destination.read_bytes():
        return
    shutil.copy2(source, destination)


def copy_submission_file() -> None:
    if not SUBMISSION_SOURCE.exists():
        raise FileNotFoundError(f"Missing submission source: {SUBMISSION_SOURCE}")
    copy_if_changed(SUBMISSION_SOURCE, SUBMISSION_DEST)


def remove_legacy_downloads() -> None:
    for path in LEGACY_DOWNLOADS:
        if path.exists():
            path.unlink()


def copy_images(markdown_text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    counts: dict[str, int] = {}
    for alt, source_text in IMAGE_PATTERN.findall(markdown_text):
        source_path = ROOT / Path(source_text)
        if not source_path.exists():
            raise FileNotFoundError(f"Missing image referenced in markdown: {source_path}")
        week_slug = week_slug_from_path(source_text)
        counts[week_slug] = counts.get(week_slug, 0) + 1
        number_match = re.search(r"Figure\s+(\d+)", alt)
        figure_number = int(number_match.group(1)) if number_match else counts[week_slug]
        figure_title = re.sub(r"^Figure\s+\d+\s*-\s*", "", alt).strip()
        filename = f"figure-{figure_number:02d}-{slugify(figure_title)}{source_path.suffix.lower()}"
        relative_dest = Path("assets") / "img" / week_slug / filename
        absolute_dest = SITE_ROOT / relative_dest
        copy_if_changed(source_path, absolute_dest)
        mapping[source_text] = relative_dest.as_posix()
    return mapping


def write_brand_assets() -> None:
    icon_path = SITE_ROOT / "assets" / "icons" / "cyb-mark.svg"
    icon_path.parent.mkdir(parents=True, exist_ok=True)
    icon_path.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" role="img" aria-label="CYB mark">
  <defs>
    <linearGradient id="shield" x1="0%" x2="100%" y1="0%" y2="100%">
      <stop offset="0%" stop-color="#143f56"/>
      <stop offset="100%" stop-color="#9b6e37"/>
    </linearGradient>
  </defs>
  <rect width="96" height="96" rx="24" fill="#13263b"/>
  <path d="M48 12 72 21v20c0 19-11 33-24 43C35 74 24 60 24 41V21l24-9Z" fill="url(#shield)"/>
  <text x="48" y="56" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="22" font-weight="700" fill="#fff">CYB</text>
</svg>
""",
        encoding="utf-8",
    )


def copy_shared_assets() -> None:
    if not SOURCE_CSS.exists():
        raise FileNotFoundError(f"Missing stylesheet source: {SOURCE_CSS}")
    if not SOURCE_JS.exists():
        raise FileNotFoundError(f"Missing script source: {SOURCE_JS}")
    copy_if_changed(SOURCE_CSS, SITE_ROOT / "assets" / "css" / "styles.css")
    copy_if_changed(SOURCE_JS, SITE_ROOT / "assets" / "js" / "site.js")


def format_inline(text: str) -> str:
    code_tokens: dict[str, str] = {}

    def stash_code(match: re.Match[str]) -> str:
        token = f"CODETOKEN{len(code_tokens)}"
        code_tokens[token] = html.escape(match.group(1))
        return token

    text = re.sub(r"`([^`]+)`", stash_code, text)
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)

    def linkify(match: re.Match[str]) -> str:
        raw_url = match.group(0)
        url = raw_url
        suffix = ""
        while url and url[-1] in TRAILING_URL_PUNCTUATION:
            suffix = url[-1] + suffix
            url = url[:-1]
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>{suffix}'

    escaped = URL_PATTERN.sub(linkify, escaped)
    for token, code_html in code_tokens.items():
        escaped = escaped.replace(token, f"<code>{code_html}</code>")
    return escaped


def render_table(table_lines: list[str]) -> str:
    rows = []
    for line in table_lines:
        cells = [format_inline(cell.strip()) for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = rows[2:]
    header_html = "".join(f'<th scope="col">{cell}</th>' for cell in header)
    body_html = ["<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in body]
    return '<div class="table-wrap"><table class="report-table"><thead><tr>' + header_html + "</tr></thead><tbody>" + "".join(body_html) + "</tbody></table></div>"


def render_reference_list(items: list[str]) -> str:
    parts = ['<ol class="reference-list">']
    for item in items:
        match = re.match(r"\[(\d+)\]\s*(.+)", item.strip())
        if match:
            parts.append(f'<li value="{int(match.group(1))}">{format_inline(match.group(2))}</li>')
    parts.append("</ol>")
    return "".join(parts)


DOSSIER_CARDS = [
    {
        "title": "Assessment Context",
        "text": "The site packages the coursework as a marker-friendly academic portfolio rather than a generic personal homepage, keeping the original evidence trail and assessment alignment visible.",
    },
    {
        "title": "Lab Environment",
        "text": "All activity was completed in an isolated teaching environment using Kali Linux against WordPress, OWASP Juice Shop, Ubuntu, and Nessus-scanned targets.",
    },
    {
        "title": "Evidence and Ethics",
        "text": "The report is evidence-led and sandbox-bound: screenshots, commands, and exported reports come from lab work rather than unauthorised testing.",
    },
]

REVIEW_CARDS = [
    {
        "title": "Start with the abstract",
        "text": "Use the homepage and report abstract for a quick view of the labs, strongest findings, and remediation priorities.",
        "href": "report/index.html#report-abstract",
        "label": "Read abstract",
    },
    {
        "title": "Inspect the full report",
        "text": "Each week keeps its original aim, method, evidence, findings, and reflection, with anchored navigation and expandable figures.",
        "href": "report/index.html",
        "label": "Open report",
    },
    {
        "title": "Cross-check the PDF",
        "text": "The downloadable PDF is the formal submission artifact for institutional review and record-keeping.",
        "href": f"assets/docs/{SUBMISSION_FILENAME}",
        "label": "Open PDF",
    },
]

KEY_FINDINGS = [
    {
        "title": "WordPress information disclosure",
        "text": "WPScan confirmed theme metadata, XML-RPC exposure, and directory indexing that lowered attacker effort.",
        "evidence": "Week 05",
    },
    {
        "title": "DOM XSS in Juice Shop",
        "text": "The browser executed an injected payload, providing the clearest direct exploit evidence in the portfolio.",
        "evidence": "Week 07",
    },
    {
        "title": "Broad service visibility",
        "text": "Nmap showed multiple exposed administrative and application services, reinforcing the need for tighter service scope.",
        "evidence": "Week 08",
    },
    {
        "title": "Nessus prioritised the WordPress host",
        "text": "The WordPress machine was the only scanned host with a medium-severity finding, centred on the SSH Terrapin weakness.",
        "evidence": "Week 09",
    },
]

PRIORITY_ACTIONS = [
    {
        "title": "Reduce avoidable exposure",
        "text": "Disable directory listing, review XML-RPC necessity, and remove unnecessary information leakage from public application surfaces.",
    },
    {
        "title": "Harden application trust boundaries",
        "text": "Improve input validation, remove weak hidden-route assumptions, and protect sensitive documents and admin flows with real access control.",
    },
    {
        "title": "Tighten administrative access",
        "text": "Restrict service exposure, prefer key-based SSH administration, and place management access behind controlled tunnels or firewall policy.",
    },
    {
        "title": "Re-scan after remediation",
        "text": "Patch SSH-related issues, then run follow-up Nessus scans with credentials where appropriate to improve confidence and depth.",
    },
]

LIMITATION_NOTES = [
    {
        "title": "Unauthenticated Nessus scope",
        "text": "The captured Nessus evidence shows authentication failed on at least one scan, so the Week 09 results remain valuable but intentionally limited in depth.",
    },
    {
        "title": "Deliberately vulnerable app context",
        "text": "OWASP Juice Shop is a training target, so its evidence is strongest for demonstrating concepts and exploitation workflow rather than real-world prevalence.",
    },
    {
        "title": "One Week 07 task is summary-backed",
        "text": "The Confidential Document task is referenced through the solved-challenge overview rather than a separate full-page evidence capture, which should be made explicit to reviewers.",
    },
]

METHOD_MATRIX = [
    (
        "WPScan",
        "WordPress reconnaissance and surface mapping",
        "Theme disclosure, plugin history, XML-RPC exposure, and directory listing output",
        "Supports analysis of attacker profiling risk and basic hardening priorities.",
    ),
    (
        "OWASP Juice Shop",
        "Interactive exploitation and weak-behaviour discovery",
        "Challenge banners, DOM XSS execution, route discovery, and logic-abuse evidence",
        "Shows how confidentiality and integrity fail in a live application context.",
    ),
    (
        "Nmap + SSH",
        "Reconnaissance paired with secure remote administration",
        "Host discovery, service enumeration, key deployment, and tunnelling commands",
        "Links discovery to defensive operational practice instead of treating them separately.",
    ),
    (
        "Nessus",
        "Structured vulnerability management and prioritisation",
        "Two completed scans, exported reports, severity summaries, and comparison graph",
        "Elevates the report from one-off testing into auditable vulnerability handling.",
    ),
]

OUTCOME_CARDS = [
    ("LO1", "Investigate vulnerabilities and identify practical mitigations across web, network, and host services."),
    ("LO2", "Demonstrate confidentiality, integrity, and availability through secure remote administration and prioritised remediation."),
    ("LO3", "Evaluate privacy and anonymity risks created by information leakage, insecure browsing behaviour, and weak application design."),
]

TOOL_CARDS = [
    ("WPScan", "WordPress reconnaissance, plugin and theme discovery, and XML-RPC attack-surface analysis."),
    ("OWASP Juice Shop", "A deliberately vulnerable application used to evidence authentication abuse, XSS, business logic issues, and hidden content discovery."),
    ("Nmap", "Subnet host discovery and exposed service enumeration across the isolated lab network."),
    ("SSH", "Encrypted administration, key-based access, local port forwarding, and shared connection control."),
    ("Nessus", "Structured vulnerability scanning, severity review, report export, and mitigation planning."),
]

REPORT_ABSTRACT_PARAGRAPHS = [
    "Across four practical labs, this portfolio documents reconnaissance, exploitation, secure administration, and vulnerability management in an isolated teaching environment. The strongest confirmed issues include WordPress information disclosure, DOM-based XSS in OWASP Juice Shop, exposed administrative service visibility, and a Nessus-identified SSH Terrapin weakness affecting the WordPress host.",
    "The report is designed to be reviewed in layers: section summaries establish context, figures document evidence, findings tables convert observations into security impact, and reflections explain what should be prioritised next.",
]

REPORT_REVIEW_NOTES = [
    "Use the abstract first for the shortest route through the submission.",
    "Treat week verdicts as the quickest statement of what each lab proved.",
    "Expand figures when you need to inspect raw evidence in more detail.",
]

FEATURED_EVIDENCE = {
    "src": "assets/img/week-09/figure-30-week-9-nessus-severity-comparison-graph.png",
    "title": "Featured evidence",
    "caption": "Week 09 severity comparison graph: the WordPress host carried the only medium-severity issue in the captured Nessus evidence.",
}


def render_head(title: str, description: str, canonical_path: str, path_prefix: str) -> str:
    canonical_url = f"{SITE_URL}{canonical_path}"
    og_image_url = f"{SITE_URL}{OG_IMAGE_PATH}"
    return f"""
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="theme-color" content="#112338" />
    <link rel="canonical" href="{canonical_url}" />
    <link rel="icon" href="{path_prefix}assets/icons/cyb-mark.svg" type="image/svg+xml" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical_url}" />
    <meta property="og:image" content="{og_image_url}" />
    <meta property="og:image:alt" content="Week 09 Nessus severity comparison graph used as the featured evidence image for the portfolio." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{og_image_url}" />
    <script>document.documentElement.classList.add("js");</script>
    <link rel="stylesheet" href="{path_prefix}assets/css/styles.css" />
  </head>
"""


def render_skip_link() -> str:
    return '<a class="skip-link" href="#main-content">Skip to main content</a>'


def render_progress_bar() -> str:
    return '<div class="scroll-progress" aria-hidden="true"><span class="scroll-progress__bar" data-progress-bar></span></div>'


def render_header(path_prefix: str, active: str) -> str:
    home_href = f"{path_prefix}index.html" if path_prefix else "index.html"
    report_href = f"{path_prefix}report/index.html"
    submission_href = f"{path_prefix}assets/docs/{SUBMISSION_FILENAME}"
    home_current = ' aria-current="page"' if active == "home" else ""
    report_current = ' aria-current="page"' if active == "report" else ""
    return f"""
    <header class="site-header">
      <a class="brand" href="{home_href}">
        <span class="brand-mark">CYB</span>
        <span class="brand-text">
          <strong>CMP-X305</strong>
          <span>Cyber Security Portfolio</span>
        </span>
      </a>
      <nav class="site-nav" aria-label="Primary">
        <a href="{home_href}"{home_current}>Overview</a>
        <a href="{report_href}"{report_current}>Full report</a>
        <a href="{submission_href}">Submission PDF</a>
      </nav>
    </header>
"""


def render_footer(path_prefix: str) -> str:
    home_href = f"{path_prefix}index.html" if path_prefix else "index.html"
    report_href = f"{path_prefix}report/index.html"
    submission_href = f"{path_prefix}assets/docs/{SUBMISSION_FILENAME}"
    return f"""
    <footer class="site-footer">
      <p>Static academic portfolio prepared for GitHub Pages project-site deployment.</p>
      <p><a href="{home_href}">Overview</a> · <a href="{report_href}">Full report</a> · <a href="{submission_href}">PDF</a></p>
    </footer>
"""


def render_lightbox(path_prefix: str) -> str:
    return f"""
    <div class="lightbox" data-lightbox hidden>
      <button class="lightbox-backdrop" type="button" aria-label="Close expanded figure" data-lightbox-close></button>
      <div class="lightbox-dialog" role="dialog" aria-modal="true" aria-label="Expanded report figure" tabindex="-1">
        <button class="lightbox-close" type="button" data-lightbox-close>Close</button>
        <button class="lightbox-nav lightbox-nav--prev" type="button" aria-label="View previous figure" data-lightbox-prev>Previous</button>
        <img src="{path_prefix}assets/img/week-09/figure-30-week-9-nessus-severity-comparison-graph.png" alt="" data-lightbox-image />
        <button class="lightbox-nav lightbox-nav--next" type="button" aria-label="View next figure" data-lightbox-next>Next</button>
        <p class="lightbox-caption" data-lightbox-caption></p>
      </div>
    </div>
"""


def render_marker_cards() -> str:
    cards = []
    for card in REVIEW_CARDS:
        cards.append(
            f"""
            <article class="review-card panel panel--paper" data-reveal>
              <p class="section-kicker">Review route</p>
              <h3>{card["title"]}</h3>
              <p>{card["text"]}</p>
              <a class="text-link" href="{card["href"]}">{card["label"]}</a>
            </article>
"""
        )
    return "\n".join(cards)


def render_finding_cards() -> str:
    cards = []
    for item in KEY_FINDINGS:
        cards.append(
            f"""
            <article class="finding-card panel panel--paper" data-reveal>
              <p class="finding-card__label">{item["evidence"]}</p>
              <h3>{item["title"]}</h3>
              <p>{item["text"]}</p>
            </article>
"""
        )
    return "\n".join(cards)


def render_priority_cards() -> str:
    cards = []
    for item in PRIORITY_ACTIONS:
        cards.append(
            f"""
            <article class="priority-card panel panel--paper" data-reveal>
              <h3>{item["title"]}</h3>
              <p>{item["text"]}</p>
            </article>
"""
        )
    return "\n".join(cards)


def render_limitation_cards() -> str:
    cards = []
    for item in LIMITATION_NOTES:
        cards.append(
            f"""
            <article class="limitation-card panel panel--paper" data-reveal>
              <h3>{item["title"]}</h3>
              <p>{item["text"]}</p>
            </article>
"""
        )
    return "\n".join(cards)


def render_dossier_cards() -> str:
    cards = []
    for card in DOSSIER_CARDS:
        cards.append(
            f"""
            <article class="dossier-card panel panel--paper" data-reveal>
              <p class="section-kicker">Assessment note</p>
              <h3>{card["title"]}</h3>
              <p>{card["text"]}</p>
            </article>
"""
        )
    return "\n".join(cards)


def render_week_cards() -> str:
    cards = []
    for week_id in ("week-05", "week-07", "week-08", "week-09"):
        details = WEEK_DETAILS[week_id]
        cards.append(
            f"""
            <article class="week-card panel panel--paper" data-reveal>
              <div class="week-card__eyebrow">
                <span>{details["label"]}</span>
                <span>{details["outcomes"]}</span>
              </div>
              <h3>{details["title"]}</h3>
              <p class="week-card__topic">{details["topic"]}</p>
              <p>{details["summary"]}</p>
              <dl class="metric-grid">
                <div><dt>Tools</dt><dd>{details["tools"]}</dd></div>
                <div><dt>Evidence</dt><dd>{details["figures"]}</dd></div>
                <div><dt>Focus</dt><dd>{details["focus"]}</dd></div>
              </dl>
              <div class="week-card__insight">
                <div><dt>Top finding</dt><dd>{details["finding"]}</dd></div>
                <div><dt>Priority action</dt><dd>{details["action"]}</dd></div>
              </div>
              <div class="card-footer">
                <span>{details["evidence"]}</span>
                <a class="text-link" href="report/index.html#{week_id}">Read section</a>
              </div>
            </article>
"""
        )
    return "\n".join(cards)


def render_tool_cards() -> str:
    return "\n".join(
        f"""
            <article class="tool-card panel panel--paper" data-reveal>
              <h3>{name}</h3>
              <p>{description}</p>
            </article>
"""
        for name, description in TOOL_CARDS
    )


def render_outcome_cards() -> str:
    return "\n".join(
        f"""
            <article class="outcome-card panel panel--paper" data-reveal>
              <p class="section-kicker">{code}</p>
              <p>{text}</p>
            </article>
"""
        for code, text in OUTCOME_CARDS
    )


def render_method_rows() -> str:
    rows = []
    for tool, role, evidence, value in METHOD_MATRIX:
        rows.append("<tr>" + f"<td>{tool}</td><td>{role}</td><td>{evidence}</td><td>{value}</td>" + "</tr>")
    return "".join(rows)


def render_report_summary() -> str:
    notes = "".join(f"<li>{format_inline(item)}</li>" for item in REPORT_REVIEW_NOTES)
    return f"""
          <section class="report-summary panel panel--paper" id="report-abstract" data-reveal>
            <div class="report-summary__grid">
              <div class="report-summary__copy">
                <p class="section-kicker">Abstract and review guide</p>
                <h2>What this coursework demonstrates</h2>
                <p>{REPORT_ABSTRACT_PARAGRAPHS[0]}</p>
                <p>{REPORT_ABSTRACT_PARAGRAPHS[1]}</p>
                <ul class="plain-list">{notes}</ul>
              </div>
              <div class="report-summary__stack">
                <article class="summary-panel summary-panel--navy panel panel--navy">
                  <p class="section-kicker">Top risk signal</p>
                  <h3>Week 09 provided the clearest prioritisation evidence</h3>
                  <p>The Nessus comparison graph and exported reports showed the WordPress host as the only target with a medium-severity issue in the captured scan set.</p>
                </article>
                <article class="summary-panel panel panel--paper">
                  <p class="section-kicker">Scope note</p>
                  <p>The report preserves the original lab narrative, but adds faster review cues such as week verdicts, remediation priorities, and anchored evidence navigation.</p>
                </article>
              </div>
            </div>
          </section>
"""


def render_section_header(section_id: str, heading_text: str) -> str:
    week_details = WEEK_DETAILS.get(section_id)
    if week_details:
        return (
            '<div class="section-intro section-intro--week">'
            '<div class="section-intro__main">'
            f'<p class="section-kicker">{week_details["label"]}</p>'
            f"<h2>{format_inline(heading_text)}</h2>"
            f'<p class="section-summary">{week_details["summary"]}</p>'
            f'<div class="section-verdict"><strong>Week verdict:</strong> {week_details["verdict"]}</div>'
            "</div>"
            '<dl class="section-intro__meta">'
            f'<div><dt>Topic</dt><dd>{week_details["topic"]}</dd></div>'
            f'<div><dt>Tools</dt><dd>{week_details["tools"]}</dd></div>'
            f'<div><dt>Learning outcomes</dt><dd>{week_details["outcomes"]}</dd></div>'
            f'<div><dt>Top finding</dt><dd>{week_details["finding"]}</dd></div>'
            f'<div><dt>Priority action</dt><dd>{week_details["action"]}</dd></div>'
            "</dl>"
            "</div>"
        )

    note = SECTION_NOTES.get(section_id, {"label": "Portfolio section", "summary": ""})
    return (
        '<div class="section-intro">'
        f'<p class="section-kicker">{note["label"]}</p>'
        f"<h2>{format_inline(heading_text)}</h2>"
        f'<p class="section-summary">{note["summary"]}</p>'
        "</div>"
    )


def render_section_close(current_section_id: str) -> str:
    if current_section_id not in SECTION_SEQUENCE:
        return '<div class="section-actions"><a class="text-link" href="#report-top">Back to top</a></div></section>'
    index = SECTION_SEQUENCE.index(current_section_id)
    prev_id = SECTION_SEQUENCE[index - 1] if index > 0 else None
    next_id = SECTION_SEQUENCE[index + 1] if index + 1 < len(SECTION_SEQUENCE) else None
    prev_html = (
        f'<a class="section-nav__link" href="#{prev_id}"><span>Previous</span><strong>{SECTION_LABELS[prev_id]}</strong></a>'
        if prev_id
        else ""
    )
    next_html = (
        f'<a class="section-nav__link section-nav__link--next" href="#{next_id}"><span>Next</span><strong>{SECTION_LABELS[next_id]}</strong></a>'
        if next_id
        else ""
    )
    nav_html = f'<div class="section-actions__nav">{prev_html}{next_html}</div>' if (prev_html or next_html) else ""
    return f'<div class="section-actions">{nav_html}<a class="text-link" href="#report-top">Back to top</a></div></section>'


def render_report_content(markdown_text: str, image_map: dict[str, str]) -> str:
    lines = markdown_text.splitlines()
    first_section = next(index for index, line in enumerate(lines) if line.startswith("## "))
    body_lines = lines[first_section:]
    parts: list[str] = []
    paragraph_lines: list[str] = []
    list_items: list[str] = []
    list_class = "plain-list"
    open_section = False
    current_section_id = ""
    pending_key_points_list = False
    figure_counter = 0
    index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            parts.append(f"<p>{format_inline(' '.join(line.strip() for line in paragraph_lines))}</p>")
            paragraph_lines = []

    def flush_list() -> None:
        nonlocal list_items, list_class
        if list_items:
            items_html = "".join(f"<li>{format_inline(item)}</li>" for item in list_items)
            parts.append(f'<ul class="{list_class}">{items_html}</ul>')
            list_items = []
            list_class = "plain-list"

    while index < len(body_lines):
        line = body_lines[index]
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            index += 1
            continue

        if stripped == "---":
            flush_paragraph()
            flush_list()
            parts.append('<hr class="report-divider" />')
            pending_key_points_list = False
            index += 1
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            pending_key_points_list = False
            if open_section:
                parts.append(render_section_close(current_section_id))
            heading_text = line[3:].strip()
            current_section_id = SECTION_ID_MAP.get(heading_text, slugify(heading_text))
            section_class = "report-section panel panel--paper"
            if current_section_id in WEEK_DETAILS:
                section_class += " report-section--week"
            parts.append(f'<section class="{section_class}" id="{current_section_id}" data-section="{current_section_id}" data-reveal>{render_section_header(current_section_id, heading_text)}')
            open_section = True
            index += 1
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            pending_key_points_list = False
            heading_text = line[4:].strip()
            display_heading = HEADING_TEXT_FIXES.get((current_section_id, heading_text), heading_text)
            sub_id = f"{current_section_id}-{slugify(display_heading)}"
            parts.append(f'<h3 id="{sub_id}">{format_inline(display_heading)}</h3>')
            index += 1
            continue

        if line.startswith("#### "):
            flush_paragraph()
            flush_list()
            pending_key_points_list = False
            heading_text = line[5:].strip()
            display_heading = HEADING_TEXT_FIXES.get((current_section_id, heading_text), heading_text)
            sub_id = f"{current_section_id}-{slugify(display_heading)}"
            parts.append(f'<h4 id="{sub_id}">{format_inline(display_heading)}</h4>')
            index += 1
            continue

        image_match = IMAGE_PATTERN.match(stripped)
        if image_match:
            flush_paragraph()
            flush_list()
            pending_key_points_list = False
            alt_text, source_text = image_match.groups()
            mapped_source = image_map[source_text]
            caption = alt_text
            look_ahead = index + 1
            while look_ahead < len(body_lines) and not body_lines[look_ahead].strip():
                look_ahead += 1
            if look_ahead < len(body_lines) and body_lines[look_ahead].strip().startswith("*Figure"):
                caption = body_lines[look_ahead].strip().strip("*")
                index = look_ahead
            number_match = re.search(r"Figure\s+(\d+)", alt_text)
            figure_number = number_match.group(1) if number_match else str(figure_counter + 1)
            figure_id = f"figure-{int(figure_number):02d}" if figure_number.isdigit() else f"figure-{slugify(figure_number)}"
            parts.append(
                f'<figure class="report-figure" id="{figure_id}" data-reveal>'
                f'<button class="figure-button" type="button" data-lightbox-src="../{mapped_source}" data-lightbox-alt="{html.escape(caption)}" data-lightbox-index="{figure_counter}">'
                f'<img src="../{mapped_source}" alt="{html.escape(caption)}" loading="lazy" decoding="async" />'
                '<span class="figure-button__hint">Expand figure</span>'
                "</button>"
                f"<figcaption>{format_inline(caption)}</figcaption>"
                "</figure>"
            )
            figure_counter += 1
            index += 1
            continue

        if stripped.startswith("|"):
            flush_paragraph()
            flush_list()
            pending_key_points_list = False
            table_lines = []
            while index < len(body_lines) and body_lines[index].strip().startswith("|"):
                table_lines.append(body_lines[index])
                index += 1
            parts.append(render_table(table_lines))
            continue

        if re.match(r"\[\d+\]\s+", stripped) and current_section_id == "references":
            flush_paragraph()
            flush_list()
            pending_key_points_list = False
            reference_lines = []
            while index < len(body_lines):
                candidate = body_lines[index].strip()
                if not candidate:
                    index += 1
                    continue
                if body_lines[index].startswith("## "):
                    break
                if re.match(r"\[\d+\]\s+", candidate):
                    reference_lines.append(candidate)
                    index += 1
                    continue
                break
            parts.append(render_reference_list(reference_lines))
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if not list_items:
                list_class = "evidence-list" if pending_key_points_list else "plain-list"
            list_items.append(stripped[2:].strip())
            pending_key_points_list = False
            index += 1
            continue

        if stripped.startswith("**Key points shown in Figure"):
            flush_paragraph()
            flush_list()
            parts.append(f'<p class="key-points-label">{format_inline(stripped)}</p>')
            pending_key_points_list = True
            index += 1
            continue

        pending_key_points_list = False
        paragraph_lines.append(stripped)
        index += 1

    flush_paragraph()
    flush_list()
    if open_section:
        parts.append(render_section_close(current_section_id))
    return "\n".join(parts)


def render_homepage(metadata: dict[str, str], figure_count: int) -> str:
    student_name = metadata.get("Student name", "Sukhjeet Singh Sekhon")
    submission_date = metadata.get("Submission date", "31 March 2026")
    description = "An academic GitHub Pages portfolio for CMP-X305, presenting four cyber security labs with structured evidence, analysis, reflection, and downloadable submission material."
    submission_href = f"assets/docs/{SUBMISSION_FILENAME}"
    return f"""<!doctype html>
<html lang="en">
{render_head("CMP-X305 Cyber Security Portfolio", description, "/", "")}
  <body class="page-home">
    {render_progress_bar()}
    {render_skip_link()}
    <div class="page-glow page-glow--one" aria-hidden="true"></div>
    <div class="page-glow page-glow--two" aria-hidden="true"></div>
    <div class="site-shell">
      {render_header("", "home")}
      <main id="main-content">
        <section class="hero panel panel--hero" data-reveal>
          <div class="hero__copy">
            <p class="section-kicker">Cyber Security Coursework · University of Roehampton</p>
            <h1>CMP-X305 Cyber Security Coursework Portfolio</h1>
            <p class="hero__lede">Across four practical labs, this site presents evidence-led coursework on reconnaissance, exploitation, secure administration, and vulnerability management in an isolated teaching environment.</p>
            <p class="hero__abstract">The strongest confirmed issues include WordPress information disclosure, DOM-based XSS in OWASP Juice Shop, exposed administrative service visibility, and a Nessus-identified SSH Terrapin weakness affecting the WordPress host. Each lab section pairs the captured evidence with analysis, limitations, and practical mitigation.</p>
            <div class="hero__actions">
              <a class="button" href="report/index.html">Open full report</a>
              <a class="button button--secondary" href="{submission_href}">Download submission PDF</a>
            </div>
            <ul class="hero-stats">
              <li><strong>4</strong><span>labs completed</span></li>
              <li><strong>{figure_count}</strong><span>evidence figures</span></li>
              <li><strong>5</strong><span>core tools used</span></li>
              <li><strong>1</strong><span>formal PDF submission</span></li>
            </ul>
          </div>
          <aside class="hero__aside">
            <article class="aside-card panel panel--navy">
              <p class="section-kicker">Marker snapshot</p>
              <dl class="meta-list">
                <div><dt>Student</dt><dd>{html.escape(student_name)}</dd></div>
                <div><dt>Module</dt><dd>Cyber Security (CMP-X305)</dd></div>
                <div><dt>Submission date</dt><dd>{html.escape(submission_date)}</dd></div>
                <div><dt>Environment</dt><dd>Sandboxed VirtualBox lab with Kali Linux, WordPress, Juice Shop, Ubuntu, and Nessus targets</dd></div>
              </dl>
            </article>
            <article class="aside-card panel panel--paper hero-visual">
              <p class="section-kicker">{FEATURED_EVIDENCE["title"]}</p>
              <div class="hero-visual__frame"><img src="{FEATURED_EVIDENCE["src"]}" alt="{FEATURED_EVIDENCE["caption"]}" loading="lazy" decoding="async" /></div>
              <p class="hero-visual__caption">{FEATURED_EVIDENCE["caption"]}</p>
            </article>
          </aside>
        </section>

        <section class="section-block"><div class="section-heading" data-reveal><p class="section-kicker">Review route</p><h2>The quickest way to assess the submission</h2><p>Use the site as a structured review surface: start with the abstract, inspect week verdicts and figures, then open the PDF for the formal submission copy if needed.</p></div><div class="review-grid">{render_marker_cards()}</div></section>

        <section class="section-block"><div class="section-heading" data-reveal><p class="section-kicker">Key findings</p><h2>The strongest security results at a glance</h2><p>This view surfaces the most marker-relevant findings before the longer narrative begins.</p></div><div class="findings-grid">{render_finding_cards()}</div></section>

        <section class="section-block"><div class="section-heading" data-reveal><p class="section-kicker">Assessment context</p><h2>How the submission is framed</h2><p>The site keeps the coursework academically grounded while improving the route a reviewer takes through the evidence.</p></div><div class="dossier-grid">{render_dossier_cards()}</div></section>

        <section class="section-block"><div class="section-heading" data-reveal><p class="section-kicker">Lab sequence</p><h2>Four linked investigations across web, network, and host security</h2><p>Each card exposes the top finding and most important next action, so the homepage behaves more like an academic dashboard than a brochure.</p></div><div class="week-grid">{render_week_cards()}</div></section>

        <section class="section-block section-block--split"><div class="split-grid"><div><div class="section-heading" data-reveal><p class="section-kicker">Priority mitigations</p><h2>What should be fixed first</h2><p>The portfolio is strongest when the evidence is connected to concrete defensive action rather than presented as isolated lab output.</p></div><div class="priority-grid">{render_priority_cards()}</div></div><div><div class="section-heading" data-reveal><p class="section-kicker">Limitations</p><h2>What the evidence does not claim</h2><p>Surfacing limitations strengthens academic credibility by making scope and confidence explicit.</p></div><div class="priority-grid">{render_limitation_cards()}</div></div></div></section>

        <section class="section-block section-block--split"><div class="section-heading" data-reveal><p class="section-kicker">Method matrix</p><h2>How the tools map to academic value</h2><p>The portfolio is strongest when the tooling is tied directly to evidence, interpretation, and module learning outcomes rather than treated as a tool list.</p></div><div class="panel panel--paper matrix-panel" data-reveal><div class="table-wrap"><table class="report-table report-table--matrix"><thead><tr><th scope="col">Tool</th><th scope="col">Primary role</th><th scope="col">Evidence produced</th><th scope="col">Academic value</th></tr></thead><tbody>{render_method_rows()}</tbody></table></div></div></section>

        <section class="section-block"><div class="section-heading" data-reveal><p class="section-kicker">Learning outcomes</p><h2>Direct alignment with the module brief</h2></div><div class="outcome-grid">{render_outcome_cards()}</div></section>
        <section class="section-block"><div class="section-heading" data-reveal><p class="section-kicker">Security toolkit</p><h2>Tools used across the coursework</h2><p>The methods span reconnaissance, exploitation, secure administration, and vulnerability management so the portfolio reads as a coherent security workflow rather than isolated tasks.</p></div><div class="tool-grid">{render_tool_cards()}</div></section>

        <section class="section-block"><div class="cta-panel panel panel--navy" data-reveal><div><p class="section-kicker">Review options</p><h2>Choose the format that best fits the review</h2><p>Use the site for anchored navigation, summary panels, and figure expansion, or open the PDF for the formal submission artifact.</p></div><div class="cta-actions"><a class="button button--light" href="report/index.html">Enter full report</a><a class="button button--ghost-light" href="{submission_href}">Download PDF</a></div></div></section>
      </main>
      {render_footer("")}
    </div>
    {render_lightbox("")}
    <script src="assets/js/site.js" defer></script>
  </body>
</html>
"""


def render_report_page(metadata: dict[str, str], report_content: str, figure_count: int) -> str:
    student_name = metadata.get("Student name", "Sukhjeet Singh Sekhon")
    submission_date = metadata.get("Submission date", "31 March 2026")
    submission_href = f"../assets/docs/{SUBMISSION_FILENAME}"
    toc_items = [(section_id, SECTION_LABELS[section_id]) for section_id in SECTION_SEQUENCE]
    toc_html = "".join(
        f'<li><a href="#{section_id}">{label}</a></li>' for section_id, label in toc_items
    )
    shortcut_html = "".join(
        f'<a href="#{section_id}">{label}</a>' for section_id, label in toc_items
    )
    description = "The full CMP-X305 cyber security portfolio report, including evidence figures, findings tables, reflective analysis, and academic references."
    abstract_html = "".join(
        f"<p>{html.escape(paragraph)}</p>" for paragraph in REPORT_ABSTRACT_PARAGRAPHS
    )
    review_notes_html = "".join(
        f'<li>{format_inline(note)}</li>' for note in REPORT_REVIEW_NOTES
    )
    return f"""<!doctype html>
<html lang="en">
{render_head("Full Report · CMP-X305 Cyber Security Portfolio", description, "/report/", "../")}
  <body class="page-report">
    {render_progress_bar()}
    {render_skip_link()}
    <div class="page-glow page-glow--one" aria-hidden="true"></div>
    <div class="page-glow page-glow--two" aria-hidden="true"></div>
    <div class="site-shell">
      {render_header("../", "report")}
      <main id="main-content" class="report-layout">
        <aside class="report-sidebar">
          <div class="panel panel--navy sidebar-card">
            <p class="section-kicker">Report navigation</p>
            <h2>Section index</h2>
            <ol class="toc-list">
              {toc_html}
            </ol>
            <a class="button button--light button--block" href="{submission_href}">Open submission PDF</a>
          </div>
          <div class="panel panel--paper sidebar-card">
            <p class="section-kicker">Quick facts</p>
            <dl class="meta-list">
              <div><dt>Student</dt><dd>{html.escape(student_name)}</dd></div>
              <div><dt>Figures</dt><dd>{figure_count} evidence figures</dd></div>
              <div><dt>Submission date</dt><dd>{html.escape(submission_date)}</dd></div>
              <div><dt>Route</dt><dd>Project-site GitHub Pages deployment</dd></div>
            </dl>
          </div>
        </aside>

        <div class="report-main">
          <section class="report-hero panel panel--hero" id="report-top" data-reveal>
            <div class="report-hero__content">
              <p class="section-kicker">Evidence-rich report route</p>
              <h1>CMP-X305 Cyber Security Coursework Portfolio</h1>
              <p class="hero__lede">This route keeps the coursework narrative academically close to the written submission while improving review speed through anchored sections, summary panels, and expandable evidence figures.</p>
              <div class="report-shortcuts">
                {shortcut_html}
              </div>
            </div>
          </section>

          <section class="report-summary" id="report-abstract" data-reveal>
            <div class="report-summary__grid">
              <article class="summary-panel panel panel--paper">
                <p class="section-kicker">Abstract</p>
                <h2>What this report establishes</h2>
                {abstract_html}
              </article>
              <div class="report-summary__stack">
                <article class="summary-panel panel panel--navy">
                  <p class="section-kicker">How to review</p>
                  <ul class="plain-list plain-list--light">
                    {review_notes_html}
                  </ul>
                </article>
                <article class="summary-panel panel panel--paper">
                  <p class="section-kicker">Cross-lab emphasis</p>
                  <p>The strongest overall pattern is the movement from discovery to prioritisation: reconnaissance exposed attack surface, exploitation demonstrated unsafe trust assumptions, secure administration reduced exposure, and Nessus scanning turned raw findings into a ranked remediation view.</p>
                </article>
              </div>
            </div>
          </section>

          {report_content}
        </div>
      </main>
      {render_footer("../")}
    </div>
    {render_lightbox("../")}
    <script src="../assets/js/site.js" defer></script>
  </body>
</html>
"""


def ensure_directories() -> None:
    (SITE_ROOT / "report").mkdir(parents=True, exist_ok=True)
    (SITE_ROOT / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (SITE_ROOT / "assets" / "js").mkdir(parents=True, exist_ok=True)
    (SITE_ROOT / "assets" / "icons").mkdir(parents=True, exist_ok=True)
    (SITE_ROOT / "assets" / "img").mkdir(parents=True, exist_ok=True)
    (SITE_ROOT / ".nojekyll").write_text("", encoding="utf-8")


def write_pages(homepage_html: str, report_html: str) -> None:
    (SITE_ROOT / "index.html").write_text(homepage_html, encoding="utf-8")
    (SITE_ROOT / "report" / "index.html").write_text(report_html, encoding="utf-8")


def mirror_pages_to_repo_root() -> None:
    ROOT_INDEX_PATH.write_text((SITE_ROOT / "index.html").read_text(encoding="utf-8"), encoding="utf-8")
    ROOT_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT_REPORT_DIR / "index.html").write_text(
        (SITE_ROOT / "report" / "index.html").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    shutil.copytree(SITE_ROOT / "assets", ROOT_ASSETS_DIR, dirs_exist_ok=True)
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    ensure_directories()
    markdown_text, metadata = read_markdown()
    copy_submission_file()
    write_brand_assets()
    copy_shared_assets()
    image_map = copy_images(markdown_text)
    report_content = render_report_content(markdown_text, image_map)
    homepage_html = render_homepage(metadata, len(image_map))
    report_html = render_report_page(metadata, report_content, len(image_map))
    write_pages(homepage_html, report_html)
    mirror_pages_to_repo_root()
    remove_legacy_downloads()
    print("GitHub Pages site generated in docs/ and mirrored to repo root/")


if __name__ == "__main__":
    main()
