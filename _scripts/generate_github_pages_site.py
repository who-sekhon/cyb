from __future__ import annotations

import html
import re
import shutil
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = ROOT / "docs"
MARKDOWN_PATH = ROOT / "CMP-X305_coursework_report.md"
PDF_SOURCE = Path(r"c:\Users\sukhj\Downloads\cyb report_fixed_v3.pdf")
PDF_DEST = SITE_ROOT / "assets" / "docs" / "cyb-report-fixed-v3.pdf"


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


WEEK_DETAILS = {
    "week-05": {
        "label": "Week 05",
        "title": "Web Application Security Lab",
        "topic": "WPScan against a live WordPress environment",
        "summary": "Automated WordPress reconnaissance exposed theme metadata, directory indexing, patch lag, and XML-RPC attack surface that all reduce attacker uncertainty.",
        "tools": "WPScan, Kali Linux, WordPress",
        "outcomes": "LO1, LO3",
        "figures": "6 figures",
        "focus": "Enumeration and hardening",
        "evidence": "Admin access, scanner output, advisory trace, and directory exposure evidence",
    },
    "week-07": {
        "label": "Week 07",
        "title": "OWASP Juice Shop Lab",
        "topic": "Hands-on exploitation of deliberately vulnerable web behaviour",
        "summary": "Challenge evidence covers DOM XSS, hidden route discovery, business logic abuse, weak authentication, and confidentiality failures inside Juice Shop.",
        "tools": "OWASP Juice Shop, Browser Workflow",
        "outcomes": "LO1, LO2, LO3",
        "figures": "9 figures",
        "focus": "Application misuse in practice",
        "evidence": "Solved challenge banners, payload execution, and route-discovery captures",
    },
    "week-08": {
        "label": "Week 08",
        "title": "Vulnerability Assessment Lab",
        "topic": "Reconnaissance with Nmap and secure administration with SSH",
        "summary": "The lab ties network discovery to defensive administration by mapping exposed services and then demonstrating secure remote access, key deployment, tunnelling, and control options.",
        "tools": "Nmap, OpenSSH, Kali Linux",
        "outcomes": "LO1, LO2",
        "figures": "8 figures",
        "focus": "Discovery plus secure access",
        "evidence": "IP verification, service enumeration, SSH session setup, and secure tunnel commands",
    },
    "week-09": {
        "label": "Week 09",
        "title": "Vulnerability Scanning and Mitigation",
        "topic": "Nessus-driven vulnerability management and reporting",
        "summary": "Nessus was configured, scan results compared across two hosts, and the WordPress machine was shown to carry the higher-risk profile due to the SSH Terrapin weakness.",
        "tools": "Nessus Essentials, PDF Evidence Export",
        "outcomes": "LO1, LO2",
        "figures": "7 figures",
        "focus": "Risk comparison and prioritisation",
        "evidence": "Scanner interface, completed jobs, exported PDFs, and severity comparison graph",
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


DOSSIER_CARDS = [
    {
        "title": "Assessment Framing",
        "text": "The site publishes the coursework as a structured academic portfolio rather than a raw document dump, keeping the original evidence trail but improving navigation and clarity.",
    },
    {
        "title": "Lab Environment",
        "text": "The portfolio reflects practical work completed in a sandboxed VirtualBox lab using Kali Linux against WordPress, Juice Shop, Ubuntu, and Nessus-driven targets.",
    },
    {
        "title": "Publication Model",
        "text": "A concise homepage acts as the academic front door, while the full report route preserves the detailed narrative, tables, reflections, and public screenshots.",
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
    (
        "LO1",
        "Investigate vulnerabilities and identify practical mitigations across web, network, and host services.",
    ),
    (
        "LO2",
        "Demonstrate confidentiality, integrity, and availability through secure remote administration and prioritised remediation.",
    ),
    (
        "LO3",
        "Evaluate privacy and anonymity risks created by information leakage, insecure browsing behaviour, and weak application design.",
    ),
]


TOOL_CARDS = [
    ("WPScan", "WordPress reconnaissance, plugin and theme discovery, and XML-RPC attack-surface analysis."),
    ("OWASP Juice Shop", "A deliberately vulnerable application used to evidence authentication abuse, XSS, business logic issues, and hidden content discovery."),
    ("Nmap", "Subnet host discovery and exposed service enumeration across the isolated lab network."),
    ("SSH", "Encrypted administration, key-based access, local port forwarding, and shared connection control."),
    ("Nessus", "Structured vulnerability scanning, severity review, report export, and mitigation planning."),
]


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


def copy_pdf() -> None:
    if not PDF_SOURCE.exists():
        raise FileNotFoundError(f"Missing PDF source: {PDF_SOURCE}")
    PDF_DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PDF_SOURCE, PDF_DEST)


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
        absolute_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, absolute_dest)
        mapping[source_text] = relative_dest.as_posix()

    return mapping


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
        return f'<a href="{url}" target="_blank" rel="noreferrer">{url}</a>{suffix}'

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
    header_html = "".join(f"<th>{cell}</th>" for cell in header)
    body_html = []

    for row in body:
        body_html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")

    return (
        '<div class="table-wrap">'
        '<table class="report-table">'
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(body_html)}</tbody>"
        "</table>"
        "</div>"
    )


def render_reference_list(items: list[str]) -> str:
    parts = ['<ol class="reference-list">']
    for item in items:
        match = re.match(r"\[(\d+)\]\s*(.+)", item.strip())
        if not match:
            continue
        parts.append(f'<li value="{int(match.group(1))}">{format_inline(match.group(2))}</li>')
    parts.append("</ol>")
    return "".join(parts)


def render_lightbox(path_prefix: str) -> str:
    return f"""
    <div class="lightbox" data-lightbox hidden>
      <button class="lightbox-backdrop" type="button" aria-label="Close expanded figure" data-lightbox-close></button>
      <div class="lightbox-dialog" role="dialog" aria-modal="true" aria-label="Expanded report figure">
        <button class="lightbox-close" type="button" data-lightbox-close>Close</button>
        <img src="{path_prefix}assets/img/week-05/figure-01-wordpress-admin-dashboard.png" alt="" data-lightbox-image />
        <p class="lightbox-caption" data-lightbox-caption></p>
      </div>
    </div>
    """


def render_skip_link() -> str:
    return '<a class="skip-link" href="#main-content">Skip to main content</a>'


def render_progress_bar() -> str:
    return '<div class="scroll-progress" aria-hidden="true"><span class="scroll-progress__bar" data-progress-bar></span></div>'


def render_header(path_prefix: str, active: str) -> str:
    home_href = path_prefix or "./"
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
        <a href="{path_prefix}report/"{report_current}>Full report</a>
        <a href="{path_prefix}assets/docs/cyb-report-fixed-v3.pdf">Submission PDF</a>
      </nav>
    </header>
    """


def render_footer(path_prefix: str) -> str:
    home_href = path_prefix or "./"
    return f"""
    <footer class="site-footer">
      <p>Static academic portfolio prepared for GitHub Pages project-site deployment.</p>
      <p><a href="{home_href}">Overview</a> · <a href="{path_prefix}report/">Full report</a> · <a href="{path_prefix}assets/docs/cyb-report-fixed-v3.pdf">PDF</a></p>
    </footer>
    """


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
              <div class="card-footer">
                <span>{details["evidence"]}</span>
                <a class="text-link" href="report/#{week_id}">Read section</a>
              </div>
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
              <p class="section-kicker">Portfolio note</p>
              <h3>{card["title"]}</h3>
              <p>{card["text"]}</p>
            </article>
            """
        )
    return "\n".join(cards)


def render_tool_cards() -> str:
    cards = []
    for name, description in TOOL_CARDS:
        cards.append(
            f"""
            <article class="tool-card panel panel--paper" data-reveal>
              <h3>{name}</h3>
              <p>{description}</p>
            </article>
            """
        )
    return "\n".join(cards)


def render_outcome_cards() -> str:
    cards = []
    for code, text in OUTCOME_CARDS:
        cards.append(
            f"""
            <article class="outcome-card panel panel--paper" data-reveal>
              <p class="section-kicker">{code}</p>
              <p>{text}</p>
            </article>
            """
        )
    return "\n".join(cards)


def render_method_rows() -> str:
    rows = []
    for tool, role, evidence, value in METHOD_MATRIX:
        rows.append(
            "<tr>"
            f"<td>{tool}</td>"
            f"<td>{role}</td>"
            f"<td>{evidence}</td>"
            f"<td>{value}</td>"
            "</tr>"
        )
    return "".join(rows)


def render_section_header(section_id: str, heading_text: str) -> str:
    week_details = WEEK_DETAILS.get(section_id)
    if week_details:
        return (
            '<div class="section-intro section-intro--week">'
            '<div class="section-intro__main">'
            f'<p class="section-kicker">{week_details["label"]}</p>'
            f"<h2>{format_inline(heading_text)}</h2>"
            f'<p class="section-summary">{week_details["summary"]}</p>'
            "</div>"
            '<dl class="section-intro__meta">'
            f'<div><dt>Topic</dt><dd>{week_details["topic"]}</dd></div>'
            f'<div><dt>Tools</dt><dd>{week_details["tools"]}</dd></div>'
            f'<div><dt>Learning outcomes</dt><dd>{week_details["outcomes"]}</dd></div>'
            f'<div><dt>Evidence focus</dt><dd>{week_details["focus"]}</dd></div>'
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


def render_section_close() -> str:
    return '<div class="section-actions"><a class="text-link" href="#report-top">Back to top</a></div></section>'


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
    index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(line.strip() for line in paragraph_lines)
            parts.append(f"<p>{format_inline(text)}</p>")
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
                parts.append(render_section_close())

            heading_text = line[3:].strip()
            current_section_id = SECTION_ID_MAP.get(heading_text, slugify(heading_text))
            section_class = "report-section panel panel--paper"
            if current_section_id in WEEK_DETAILS:
                section_class += " report-section--week"
            parts.append(
                f'<section class="{section_class}" id="{current_section_id}" data-section="{current_section_id}" data-reveal>'
                f"{render_section_header(current_section_id, heading_text)}"
            )
            open_section = True
            index += 1
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            pending_key_points_list = False
            heading_text = line[4:].strip()
            sub_id = f"{current_section_id}-{slugify(heading_text)}"
            parts.append(f'<h3 id="{sub_id}">{format_inline(heading_text)}</h3>')
            index += 1
            continue

        if line.startswith("#### "):
            flush_paragraph()
            flush_list()
            pending_key_points_list = False
            heading_text = line[5:].strip()
            sub_id = f"{current_section_id}-{slugify(heading_text)}"
            parts.append(f'<h4 id="{sub_id}">{format_inline(heading_text)}</h4>')
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

            parts.append(
                '<figure class="report-figure" data-reveal>'
                f'<button class="figure-button" type="button" data-lightbox-src="../{mapped_source}" data-lightbox-alt="{html.escape(caption)}">'
                f'<img src="../{mapped_source}" alt="{html.escape(alt_text)}" loading="lazy" />'
                '<span class="figure-button__hint">Expand figure</span>'
                "</button>"
                f"<figcaption>{format_inline(caption)}</figcaption>"
                "</figure>"
            )
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
        parts.append(render_section_close())

    return "\n".join(parts)


def render_homepage(metadata: dict[str, str], figure_count: int) -> str:
    student_name = metadata.get("Student name", "Sukhjeet Singh Sekhon")
    submission_date = metadata.get("Submission date", "31 March 2026")

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>CMP-X305 Cyber Security Portfolio</title>
    <meta name="description" content="An academic GitHub Pages portfolio for CMP-X305, presenting four cyber security labs with structured evidence, analysis, reflection, and downloadable submission material." />
    <meta name="theme-color" content="#112338" />
    <link rel="stylesheet" href="assets/css/styles.css" />
  </head>
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
            <p class="section-kicker">University of Roehampton · 2026</p>
            <h1>CMP-X305 Cyber Security Coursework Portfolio</h1>
            <p class="hero__lede">
              A more professional, academic web presentation of the coursework portfolio, built for GitHub Pages while preserving the evidence, report structure, and submission-ready PDF.
            </p>
            <p>
              The site reframes the work as an editorial portfolio: an overview route for quick academic review, and a report route for the full narrative, figures, findings, reflections, and references.
            </p>
            <div class="hero__actions">
              <a class="button" href="report/">Read the full report</a>
              <a class="button button--secondary" href="assets/docs/cyb-report-fixed-v3.pdf">Open submission PDF</a>
            </div>
            <ul class="hero-stats">
              <li><strong>4</strong><span>practical lab strands</span></li>
              <li><strong>{figure_count}</strong><span>public figures</span></li>
              <li><strong>5</strong><span>core security tools</span></li>
              <li><strong>45</strong><span>page PDF submission</span></li>
            </ul>
          </div>
          <aside class="hero__aside">
            <article class="aside-card panel panel--navy">
              <p class="section-kicker">Portfolio dossier</p>
              <dl class="meta-list">
                <div><dt>Student</dt><dd>{html.escape(student_name)}</dd></div>
                <div><dt>Module</dt><dd>Cyber Security (CMP-X305)</dd></div>
                <div><dt>Submission date</dt><dd>{html.escape(submission_date)}</dd></div>
                <div><dt>Published format</dt><dd>Static GitHub Pages project site</dd></div>
              </dl>
            </article>
            <article class="aside-card panel panel--paper">
              <p class="section-kicker">Review lens</p>
              <p>
                The public site is deliberately evidence-rich: screenshots remain visible, tables stay intact, and the report language stays academically close to the written submission.
              </p>
            </article>
          </aside>
        </section>

        <section class="section-block">
          <div class="section-heading" data-reveal>
            <p class="section-kicker">Publishing logic</p>
            <h2>A portfolio site that still behaves like coursework</h2>
            <p>Instead of flattening the assignment into a generic personal site, the design keeps the academic tone, transparent evidence trail, and module framing visible from the first screen.</p>
          </div>
          <div class="dossier-grid">
            {render_dossier_cards()}
          </div>
        </section>

        <section class="section-block">
          <div class="section-heading" data-reveal>
            <p class="section-kicker">Lab sequence</p>
            <h2>Four linked investigations across web, network, and host security</h2>
            <p>Each week page segment preserves the original analysis while giving reviewers faster entry points into the most important evidence.</p>
          </div>
          <div class="week-grid">
            {render_week_cards()}
          </div>
        </section>

        <section class="section-block section-block--split">
          <div class="section-heading" data-reveal>
            <p class="section-kicker">Method matrix</p>
            <h2>How the tools map to academic value</h2>
            <p>The portfolio is strongest when the tooling is tied directly to evidence, interpretation, and module learning outcomes rather than treated as a tool list.</p>
          </div>
          <div class="panel panel--paper matrix-panel" data-reveal>
            <div class="table-wrap">
              <table class="report-table report-table--matrix">
                <thead>
                  <tr>
                    <th>Tool</th>
                    <th>Primary role</th>
                    <th>Evidence produced</th>
                    <th>Academic value</th>
                  </tr>
                </thead>
                <tbody>
                  {render_method_rows()}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <section class="section-block">
          <div class="section-heading" data-reveal>
            <p class="section-kicker">Learning outcomes</p>
            <h2>Direct alignment with the module brief</h2>
          </div>
          <div class="outcome-grid">
            {render_outcome_cards()}
          </div>
        </section>

        <section class="section-block">
          <div class="section-heading" data-reveal>
            <p class="section-kicker">Security toolkit</p>
            <h2>Tools used across the coursework</h2>
            <p>The methods span reconnaissance, exploitation, secure administration, and vulnerability management so the portfolio reads as a coherent security workflow rather than isolated tasks.</p>
          </div>
          <div class="tool-grid">
            {render_tool_cards()}
          </div>
        </section>

        <section class="section-block">
          <div class="cta-panel panel panel--navy" data-reveal>
            <div>
              <p class="section-kicker">Review options</p>
              <h2>Choose the report format that best fits the review</h2>
              <p>Use the site for structured navigation and figure expansion, or open the PDF for the formal submission version.</p>
            </div>
            <div class="cta-actions">
              <a class="button button--light" href="report/">Enter full report</a>
              <a class="button button--ghost-light" href="assets/docs/cyb-report-fixed-v3.pdf">Download PDF</a>
            </div>
          </div>
        </section>
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
    toc_items = [
        ("intro", "Introduction"),
        ("week-05", "Week 05"),
        ("week-07", "Week 07"),
        ("week-08", "Week 08"),
        ("week-09", "Week 09"),
        ("conclusion", "Conclusion"),
        ("ai-use", "AI use"),
        ("references", "References"),
    ]
    toc_html = "".join(
        f'<li><a href="#{section_id}">{label}</a></li>' for section_id, label in toc_items
    )
    shortcut_html = "".join(
        f'<a href="#{section_id}">{label}</a>' for section_id, label in toc_items
    )

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Full Report · CMP-X305 Cyber Security Portfolio</title>
    <meta name="description" content="The full CMP-X305 cybersecurity portfolio report, including evidence figures, findings tables, reflective analysis, and academic references." />
    <meta name="theme-color" content="#112338" />
    <link rel="stylesheet" href="../assets/css/styles.css" />
  </head>
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
            <a class="button button--light button--block" href="../assets/docs/cyb-report-fixed-v3.pdf">Open submission PDF</a>
          </div>
          <div class="panel panel--paper sidebar-card">
            <p class="section-kicker">Quick facts</p>
            <dl class="meta-list">
              <div><dt>Student</dt><dd>{html.escape(student_name)}</dd></div>
              <div><dt>Figures</dt><dd>{figure_count} public figures</dd></div>
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
              <p class="hero__lede">
                The full report keeps the wording academically close to the written submission while improving readability through anchored sections, refined tables, and expandable figures.
              </p>
              <div class="report-shortcuts">
                {shortcut_html}
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
    (SITE_ROOT / "assets" / "img").mkdir(parents=True, exist_ok=True)


def write_pages(homepage_html: str, report_html: str) -> None:
    (SITE_ROOT / "index.html").write_text(homepage_html, encoding="utf-8")
    (SITE_ROOT / "report" / "index.html").write_text(report_html, encoding="utf-8")


def main() -> None:
    ensure_directories()
    markdown_text, metadata = read_markdown()
    copy_pdf()
    image_map = copy_images(markdown_text)
    report_content = render_report_content(markdown_text, image_map)
    homepage_html = render_homepage(metadata, len(image_map))
    report_html = render_report_page(metadata, report_content, len(image_map))
    write_pages(homepage_html, report_html)
    print("GitHub Pages site generated in docs/")


if __name__ == "__main__":
    main()
