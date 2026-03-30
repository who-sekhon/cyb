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
        "summary": "Enumerated a lab WordPress instance, surfaced theme disclosure, directory listing exposure, XML-RPC attack surface, and patch lag indicators.",
        "tools": "WPScan, Kali Linux, WordPress",
        "outcomes": "LO1, LO3",
        "figures": "6 figures",
        "accent": "Enumeration and hardening",
    },
    "week-07": {
        "label": "Week 07",
        "title": "OWASP Juice Shop Lab",
        "topic": "Hands-on exploitation of low-difficulty web challenges",
        "summary": "Captured solved challenges covering DOM XSS, hidden routes, business logic abuse, weak authentication, and confidentiality failures in Juice Shop.",
        "tools": "OWASP Juice Shop, Browser Dev Workflow",
        "outcomes": "LO1, LO2, LO3",
        "figures": "9 figures",
        "accent": "Application misuse in practice",
    },
    "week-08": {
        "label": "Week 08",
        "title": "Vulnerability Assessment Lab",
        "topic": "Reconnaissance with Nmap and secure administration with SSH",
        "summary": "Mapped exposed services, compared scan techniques, then demonstrated password login, key deployment, local port forwarding, and connection control over SSH.",
        "tools": "Nmap, OpenSSH, Kali Linux",
        "outcomes": "LO1, LO2",
        "figures": "8 figures",
        "accent": "Discovery plus secure access",
    },
    "week-09": {
        "label": "Week 09",
        "title": "Vulnerability Scanning and Mitigation",
        "topic": "Nessus-driven vulnerability management and reporting",
        "summary": "Configured Nessus, ran two host scans, compared severity profiles, exported evidence, and highlighted the SSH Terrapin weakness on the WordPress host.",
        "tools": "Nessus Essentials, PDF Evidence Export",
        "outcomes": "LO1, LO2",
        "figures": "7 figures",
        "accent": "Risk comparison and mitigation",
    },
}

TOOL_CARDS = [
    ("WPScan", "WordPress reconnaissance, plugin/theme discovery, and XML-RPC attack-surface analysis."),
    ("OWASP Juice Shop", "Purpose-built vulnerable web app used to evidence authentication, XSS, business logic, and discovery issues."),
    ("Nmap", "Host discovery and service enumeration across the lab subnet."),
    ("SSH", "Encrypted remote administration, key-based access, tunnelling, and session control."),
    ("Nessus", "Structured vulnerability scanning, severity review, exportable evidence, and mitigation prioritisation."),
]

OUTCOME_CARDS = [
    ("LO1", "Investigate vulnerabilities and identify practical mitigations across web, network, and host services."),
    ("LO2", "Demonstrate confidentiality, integrity, and availability through secure remote administration and prioritised remediation."),
    ("LO3", "Evaluate privacy and anonymity risks created by information leakage, insecure browsing behaviour, and weak application design."),
]

IMAGE_PATTERN = re.compile(r"!\[(.*?)\]\(<(.*?)>\)")


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
    escaped = re.sub(
        r"(https?://[^\s<]+)",
        lambda match: f'<a href="{match.group(1)}" target="_blank" rel="noreferrer">{match.group(1)}</a>',
        escaped,
    )
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
        '<div class="table-wrap"><table class="report-table">'
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(body_html)}</tbody>"
        "</table></div>"
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


def render_report_content(markdown_text: str, image_map: dict[str, str]) -> str:
    lines = markdown_text.splitlines()
    first_section = next(index for index, line in enumerate(lines) if line.startswith("## "))
    body_lines = lines[first_section:]
    parts: list[str] = []
    paragraph_lines: list[str] = []
    list_items: list[str] = []
    open_section = False
    current_section_id = ""
    index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            text = " ".join(line.strip() for line in paragraph_lines)
            parts.append(f"<p>{format_inline(text)}</p>")
            paragraph_lines = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            items_html = "".join(f"<li>{format_inline(item)}</li>" for item in list_items)
            parts.append(f"<ul>{items_html}</ul>")
            list_items = []

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
            index += 1
            continue
        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            if open_section:
                parts.append("</section>")
            heading_text = line[3:].strip()
            current_section_id = SECTION_ID_MAP.get(heading_text, slugify(heading_text))
            parts.append(
                f'<section class="panel report-section" id="{current_section_id}" data-section="{current_section_id}">'
                f'<div class="section-kicker">Portfolio section</div><h2>{format_inline(heading_text)}</h2>'
            )
            open_section = True
            index += 1
            continue
        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            heading_text = line[4:].strip()
            sub_id = f"{current_section_id}-{slugify(heading_text)}"
            parts.append(f'<h3 id="{sub_id}">{format_inline(heading_text)}</h3>')
            index += 1
            continue
        if line.startswith("#### "):
            flush_paragraph()
            flush_list()
            heading_text = line[5:].strip()
            sub_id = f"{current_section_id}-{slugify(heading_text)}"
            parts.append(f'<h4 id="{sub_id}">{format_inline(heading_text)}</h4>')
            index += 1
            continue
        image_match = IMAGE_PATTERN.match(stripped)
        if image_match:
            flush_paragraph()
            flush_list()
            alt_text, source_text = image_match.groups()
            mapped_source = image_map[source_text]
            caption = ""
            look_ahead = index + 1
            while look_ahead < len(body_lines) and not body_lines[look_ahead].strip():
                look_ahead += 1
            if look_ahead < len(body_lines) and body_lines[look_ahead].strip().startswith("*Figure"):
                caption = body_lines[look_ahead].strip().strip("*")
                index = look_ahead
            parts.append(
                '<figure class="report-figure">'
                f'<img src="../{mapped_source}" alt="{html.escape(alt_text)}" loading="lazy" />'
                f"<figcaption>{format_inline(caption or alt_text)}</figcaption></figure>"
            )
            index += 1
            continue
        if stripped.startswith("|"):
            flush_paragraph()
            flush_list()
            table_lines = []
            while index < len(body_lines) and body_lines[index].strip().startswith("|"):
                table_lines.append(body_lines[index])
                index += 1
            parts.append(render_table(table_lines))
            continue
        if re.match(r"\[\d+\]\s+", stripped) and current_section_id == "references":
            flush_paragraph()
            flush_list()
            reference_lines = []
            while index < len(body_lines) and re.match(r"\[\d+\]\s+", body_lines[index].strip()):
                reference_lines.append(body_lines[index].strip())
                index += 1
            parts.append(render_reference_list(reference_lines))
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            list_items.append(stripped[2:].strip())
            index += 1
            continue
        if stripped.startswith("**Key points shown in Figure"):
            flush_paragraph()
            flush_list()
            parts.append(f'<p class="key-points-label">{format_inline(stripped)}</p>')
            index += 1
            continue
        paragraph_lines.append(stripped)
        index += 1

    flush_paragraph()
    flush_list()
    if open_section:
        parts.append("</section>")
    return "\n".join(parts)


def render_week_cards() -> str:
    cards = []
    for week_id in ("week-05", "week-07", "week-08", "week-09"):
        details = WEEK_DETAILS[week_id]
        cards.append(
            f"""
            <article class="week-card panel" data-reveal>
              <p class="card-kicker">{details["label"]}</p>
              <h3>{details["title"]}</h3>
              <p class="card-topic">{details["topic"]}</p>
              <p>{details["summary"]}</p>
              <ul class="chip-list">
                <li>{details["tools"]}</li>
                <li>{details["outcomes"]}</li>
                <li>{details["figures"]}</li>
              </ul>
              <div class="card-footer">
                <span>{details["accent"]}</span>
                <a class="text-link" href="report/#{week_id}">Open section</a>
              </div>
            </article>
            """
        )
    return "\n".join(cards)


def render_tool_cards() -> str:
    cards = []
    for name, description in TOOL_CARDS:
        cards.append(
            f"""
            <article class="mini-card panel panel--soft" data-reveal>
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
            <article class="outcome-card panel panel--soft" data-reveal>
              <p class="card-kicker">{code}</p>
              <p>{text}</p>
            </article>
            """
        )
    return "\n".join(cards)


def render_homepage(metadata: dict[str, str]) -> str:
    student_name = metadata.get("Student name", "Sukhjeet Singh Sekhon")
    submission_date = metadata.get("Submission date", "31 March 2026")
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>CMP-X305 Cyber Security Portfolio</title>
    <meta name="description" content="Cyber security coursework portfolio site covering WPScan, OWASP Juice Shop, Nmap, SSH, and Nessus labs." />
    <link rel="stylesheet" href="assets/css/styles.css" />
  </head>
  <body class="home-page">
    <div class="site-shell">
      <header class="site-header">
        <a class="brand" href="./"><span class="brand-mark">CYB</span><span class="brand-text">Portfolio Site</span></a>
        <nav class="site-nav" aria-label="Primary">
          <a href="./" aria-current="page">Home</a>
          <a href="report/">Full report</a>
          <a href="assets/docs/cyb-report-fixed-v3.pdf">PDF</a>
        </nav>
      </header>
      <main>
        <section class="hero-grid">
          <div class="hero-copy panel" data-reveal>
            <p class="eyebrow">University of Roehampton · 2026</p>
            <h1>CMP-X305 Cyber Security Coursework Portfolio</h1>
            <p class="lede">A GitHub Pages version of the coursework portfolio, turning the written submission into a cleaner public-facing site without losing the evidence trail.</p>
            <p>The site keeps the full report public, adds direct navigation by week, and preserves the screenshots, chart, and downloadable PDF submission artifact.</p>
            <div class="hero-actions">
              <a class="button" href="report/">Read the full report</a>
              <a class="button button--ghost" href="assets/docs/cyb-report-fixed-v3.pdf">Download PDF</a>
            </div>
            <ul class="stat-list">
              <li><strong>4</strong><span>lab strands</span></li>
              <li><strong>30</strong><span>public figures</span></li>
              <li><strong>5</strong><span>core tools</span></li>
              <li><strong>45</strong><span>page submission PDF</span></li>
            </ul>
          </div>
          <aside class="hero-aside panel panel--soft" data-reveal>
            <p class="eyebrow">Portfolio details</p>
            <dl class="meta-list">
              <div><dt>Student</dt><dd>{html.escape(student_name)}</dd></div>
              <div><dt>Module</dt><dd>Cyber Security (CMP-X305)</dd></div>
              <div><dt>Submission</dt><dd>{html.escape(submission_date)}</dd></div>
              <div><dt>Published as</dt><dd>Static GitHub Pages project site</dd></div>
            </dl>
            <p class="aside-note">The public site is intentionally evidence-rich: screenshots, analysis tables, and the submission PDF are all included.</p>
          </aside>
        </section>
        <section class="section-block">
          <div class="section-heading" data-reveal>
            <p class="eyebrow">Week-by-week</p>
            <h2>Four labs, one coherent evidence trail</h2>
            <p>Each week section keeps the academic findings intact while making navigation faster than a single document alone.</p>
          </div>
          <div class="week-grid">{render_week_cards()}</div>
        </section>
        <section class="section-block section-block--alt">
          <div class="section-heading" data-reveal>
            <p class="eyebrow">Learning outcomes</p>
            <h2>How the portfolio maps back to the module brief</h2>
          </div>
          <div class="outcome-grid">{render_outcome_cards()}</div>
        </section>
        <section class="section-block">
          <div class="section-heading" data-reveal>
            <p class="eyebrow">Tooling</p>
            <h2>Security tools used across the labs</h2>
            <p>The coursework combines scanner output, exploitation evidence, reconnaissance, tunnelling, and formal vulnerability reporting.</p>
          </div>
          <div class="tool-grid">{render_tool_cards()}</div>
        </section>
        <section class="section-block">
          <div class="download-panel panel" data-reveal>
            <div>
              <p class="eyebrow">Evidence access</p>
              <h2>Prefer the original submission format?</h2>
              <p>The fixed PDF remains available alongside the web version so the portfolio can be reviewed either as a formal report or as a navigable project site.</p>
            </div>
            <div class="download-actions">
              <a class="button" href="assets/docs/cyb-report-fixed-v3.pdf">Open PDF</a>
              <a class="button button--ghost" href="report/#references">Jump to references</a>
            </div>
          </div>
        </section>
      </main>
      <footer class="site-footer">
        <p>Built from the coursework markdown source and repackaged for GitHub Pages deployment.</p>
        <p>Project routes: <a href="./">Home</a> · <a href="report/">Full report</a> · <a href="assets/docs/cyb-report-fixed-v3.pdf">PDF</a></p>
      </footer>
    </div>
    <script src="assets/js/site.js" defer></script>
  </body>
</html>
"""


def render_report_page(metadata: dict[str, str], report_content: str) -> str:
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
    toc_html = "".join(f'<li><a href="#{section_id}">{label}</a></li>' for section_id, label in toc_items)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Full Report · CMP-X305 Cyber Security Portfolio</title>
    <meta name="description" content="Full report page for the CMP-X305 cyber security coursework portfolio, including screenshots, tables, reflections, and references." />
    <link rel="stylesheet" href="../assets/css/styles.css" />
  </head>
  <body class="report-page">
    <div class="site-shell">
      <header class="site-header">
        <a class="brand" href="../"><span class="brand-mark">CYB</span><span class="brand-text">Portfolio Site</span></a>
        <nav class="site-nav" aria-label="Primary">
          <a href="../">Home</a>
          <a href="./" aria-current="page">Full report</a>
          <a href="../assets/docs/cyb-report-fixed-v3.pdf">PDF</a>
        </nav>
      </header>
      <main class="report-layout">
        <aside class="report-sidebar">
          <div class="panel toc-panel">
            <p class="eyebrow">On this page</p>
            <h2>Report navigation</h2>
            <ol class="toc-list">{toc_html}</ol>
            <a class="button button--ghost button--block" href="../assets/docs/cyb-report-fixed-v3.pdf">Download submission PDF</a>
          </div>
        </aside>
        <div class="report-main">
          <section class="panel report-hero" data-reveal>
            <p class="eyebrow">Evidence-rich portfolio</p>
            <h1>CMP-X305 Cyber Security Coursework Portfolio</h1>
            <p class="lede">This page keeps the wording of the written report largely intact while adding section anchors, responsive figure layouts, and faster navigation.</p>
            <ul class="chip-list">
              <li>{html.escape(student_name)}</li>
              <li>Cyber Security (CMP-X305)</li>
              <li>{html.escape(submission_date)}</li>
            </ul>
          </section>
          {report_content}
        </div>
      </main>
      <footer class="site-footer">
        <p>Static report route prepared for GitHub Pages project-site deployment.</p>
        <p><a href="../">Back to homepage</a></p>
      </footer>
    </div>
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
    homepage_html = render_homepage(metadata)
    report_html = render_report_page(metadata, report_content)
    write_pages(homepage_html, report_html)
    print("GitHub Pages site generated in docs/")


if __name__ == "__main__":
    main()
