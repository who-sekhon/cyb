from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
from pypdf import PdfReader


SEVERITY_ORDER = ["Critical", "High", "Medium", "Low", "Info"]
COLORS = {
    "Critical": "#d7263d",
    "High": "#f46036",
    "Medium": "#f6ae2d",
    "Low": "#5bc0eb",
    "Info": "#6c7a89",
}


def extract_counts(pdf_path: Path) -> tuple[str, dict[str, int]]:
    text = "\n".join((page.extract_text() or "") for page in PdfReader(str(pdf_path)).pages)
    pattern = re.compile(
        r"Vulnerabilities by Host\s+"
        r"(?P<host>\d+\.\d+\.\d+\.\d+)\s+"
        r"(?P<critical>\d+)\s+"
        r"(?P<high>\d+)\s+"
        r"(?P<medium>\d+)\s+"
        r"(?P<low>\d+)\s+"
        r"(?P<info>\d+)\s+CRITICAL\s+HIGH\s+MEDIUM\s+LOW\s+INFO",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"Could not find severity summary in {pdf_path}")

    counts = {
        "Critical": int(match.group("critical")),
        "High": int(match.group("high")),
        "Medium": int(match.group("medium")),
        "Low": int(match.group("low")),
        "Info": int(match.group("info")),
    }
    return match.group("host"), counts


def build_chart(output_path: Path, sources: list[Path]) -> None:
    data = []
    for source in sources:
        host, counts = extract_counts(source)
        label = "Ubuntu scan" if "ubunto" in source.name.lower() else "WordPress scan"
        data.append((label, host, counts, source.name))

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(11, 6.4))

    y_positions = list(range(len(data)))
    left = [0] * len(data)

    for severity in SEVERITY_ORDER:
        values = [item[2][severity] for item in data]
        ax.barh(
            y_positions,
            values,
            left=left,
            color=COLORS[severity],
            edgecolor="white",
            height=0.55,
            label=severity,
        )
        for idx, value in enumerate(values):
            if value > 0:
                ax.text(
                    left[idx] + value / 2,
                    y_positions[idx],
                    str(value),
                    ha="center",
                    va="center",
                    color="white" if severity in {"Critical", "High", "Info"} else "#13202b",
                    fontsize=10,
                    fontweight="bold",
                )
        left = [left[idx] + values[idx] for idx in range(len(values))]

    labels = [f"{name}\n{host}" for name, host, _, _ in data]
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=11)
    ax.set_xlabel("Number of findings", fontsize=11)
    ax.set_title("Week 9 Nessus Severity Comparison from Exported Scan PDFs", fontsize=15, fontweight="bold", pad=14)
    ax.legend(ncols=5, loc="upper center", bbox_to_anchor=(0.5, 1.06), frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)

    max_total = max(sum(item[2].values()) for item in data)
    ax.set_xlim(0, max_total + 8)

    fig.text(
        0.01,
        0.01,
        "Source PDFs: " + ", ".join(item[3] for item in data),
        fontsize=9,
        color="#4f5d75",
    )

    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    base = Path.cwd()
    sources = [
        base / "Week 9" / "ubunto_rpb70j.pdf",
        base / "Week 9" / "wordpress_9dsnz3.pdf",
    ]
    output = base / "Week 9" / "week9_nessus_severity_chart.png"
    build_chart(output, sources)
    print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
