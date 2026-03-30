from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from PIL import Image, ImageDraw, ImageFont


REPORT_PATH = Path("CMP-X305_coursework_report.md")
OUTPUT_ROOT = Path("labelled")

IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\(<(?P<path>[^>]+)>\)")
CAPTION_RE = re.compile(r"^\*Figure\s+(?P<number>\d+)\.\s*(?P<caption>.+?)\*$")


@dataclass
class Figure:
    number: int
    path: Path


@dataclass
class Mark:
    bbox: tuple[float, float, float, float]
    label: str | None = None
    label_xy: tuple[float, float] | None = None
    shape: str = "box"


MARKS: dict[int, list[Mark]] = {
    1: [Mark((0.19, 0.18, 0.53, 0.24), "Admin dashboard", (0.03, -0.06))],
    2: [Mark((0.08, 0.47, 0.46, 0.82), "WPScan sign-up", (0.03, -0.06)), Mark((0.80, 0.22, 0.95, 0.31), "Login", (0.76, -0.06))],
    3: [Mark((0.46, 0.46, 0.61, 0.53), "WPScan update", (0.50, -0.06))],
    4: [Mark((0.47, 0.24, 0.80, 0.81), "Enumeration output", (0.52, -0.06))],
    5: [Mark((0.01, 0.13, 0.55, 0.54), "Akismet advisory", (0.03, -0.06))],
    6: [Mark((0.01, 0.11, 0.26, 0.17), "Directory listing", (0.03, -0.06))],
    7: [Mark((0.04, 0.39, 0.52, 0.44), "Admin login solved", (0.04, -0.06))],
    8: [Mark((0.04, 0.39, 0.56, 0.44), "Chatbot solved", (0.04, -0.06))],
    9: [Mark((0.04, 0.39, 0.66, 0.44), "Allowlist solved", (0.04, -0.06))],
    10: [Mark((0.04, 0.39, 0.94, 0.46), "Bonus payload solved", (0.04, -0.06))],
    11: [Mark((0.72, 0.21, 0.87, 0.28), "Injected payload", (0.64, -0.06)), Mark((0.34, 0.54, 0.66, 0.70), "Alert box", (0.46, 0.73))],
    12: [Mark((0.04, 0.39, 0.62, 0.44), "Privacy Policy solved", (0.04, -0.06))],
    13: [Mark((0.04, 0.39, 0.60, 0.44), "Mass Dispel solved", (0.04, -0.06))],
    14: [Mark((0.04, 0.39, 0.72, 0.44), "Error Handling solved", (0.04, -0.06))],
    15: [Mark((0.31, 0.12, 0.48, 0.18), "Hidden route", (0.56, -0.06)), Mark((0.03, 0.29, 0.28, 0.37), "Score Board", (0.03, -0.06))],
    16: [Mark((0.05, 0.68, 0.49, 0.74), "Target IP", (0.03, -0.06))],
    17: [Mark((0.01, 0.87, 0.43, 0.95), "Live hosts", (0.03, -0.06))],
    18: [Mark((0.01, 0.12, 0.22, 0.22), "Open MySQL port", (0.03, -0.06))],
    19: [Mark((0.01, 0.39, 0.19, 0.55), "TCP connect scan", (0.03, -0.06)), Mark((0.01, 0.63, 0.22, 0.82), "SYN scan", (0.25, -0.06))],
    20: [Mark((0.01, 0.12, 0.55, 0.35), "Host key check", (0.03, -0.06)), Mark((0.01, 0.37, 0.31, 0.64), "SSH session", (0.30, -0.06))],
    21: [Mark((0.12, 0.52, 0.54, 0.76), "ssh-copy-id", (0.03, -0.06)), Mark((0.16, 0.80, 0.34, 0.86), "Key added", (0.33, -0.06))],
    22: [Mark((0.01, 0.24, 0.37, 0.30), "Port forwarding", (0.03, -0.06))],
    23: [Mark((0.02, 0.79, 0.60, 0.85), "SSH control option", (0.03, -0.06))],
    24: [Mark((0.41, 0.43, 0.60, 0.77), "Nessus login", (0.43, -0.06))],
    25: [Mark((0.57, 0.39, 0.70, 0.43), "New scan", (0.55, -0.06)), Mark((0.79, 0.27, 0.98, 0.40), "Plugin notice", (0.77, -0.06))],
    26: [Mark((0.29, 0.43, 0.46, 0.58), "Two scans", (0.30, -0.06))],
    27: [Mark((0.30, 0.53, 0.77, 0.61), "Severity row", (0.30, -0.06)), Mark((0.41, 0.53, 0.46, 0.61), "Auth failed", (0.56, -0.06))],
    28: [Mark((0.75, 0.38, 0.98, 0.58), "Completed scans", (0.70, -0.06))],
    29: [Mark((0.28, 0.43, 0.55, 0.57), "Exported PDFs", (0.30, -0.06))],
    30: [Mark((0.12, 0.19, 0.83, 0.45), "WordPress medium issue", (0.48, -0.06)), Mark((0.12, 0.56, 0.66, 0.83), "Mostly informational", (0.03, -0.06))],
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = current + " " + word
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def parse_figures(report_path: Path) -> list[Figure]:
    lines = report_path.read_text(encoding="utf-8").splitlines()
    figures: list[Figure] = []

    for idx, line in enumerate(lines):
        image_match = IMAGE_RE.search(line)
        if not image_match:
            continue

        rel_path = Path(unquote(image_match.group("path").strip()))
        for look_ahead in range(idx + 1, min(idx + 10, len(lines))):
            caption_match = CAPTION_RE.match(lines[look_ahead].strip())
            if caption_match:
                figures.append(Figure(number=int(caption_match.group("number")), path=rel_path))
                break

    return figures


def annotate_image(figure: Figure, source: Path, dest: Path) -> None:
    image = Image.open(source).convert("RGBA")
    width, height = image.size
    pad_left = max(18, width // 45)
    pad_right = max(18, width // 45)
    pad_bottom = max(12, height // 70)
    pad_top = max(48, height // 10)
    canvas_w = width + pad_left + pad_right
    canvas_h = height + pad_top + pad_bottom

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (250, 252, 255, 255))
    canvas.paste(image, (pad_left, pad_top))

    overlay = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    outline = (229, 57, 53, 255)
    fill = (229, 57, 53, 0)
    label_fill = (255, 248, 225, 245)
    label_text = (33, 33, 33, 255)
    stroke = max(2, width // 650)
    radius = max(6, width // 220)
    font = load_font(max(14, width // 70), bold=True)

    for mark in MARKS.get(figure.number, []):
        x1 = pad_left + int(mark.bbox[0] * width)
        y1 = pad_top + int(mark.bbox[1] * height)
        x2 = pad_left + int(mark.bbox[2] * width)
        y2 = pad_top + int(mark.bbox[3] * height)
        if mark.shape == "circle":
            draw.ellipse((x1, y1, x2, y2), outline=outline, fill=fill, width=stroke)
        else:
            draw.rounded_rectangle((x1, y1, x2, y2), radius=radius, outline=outline, fill=fill, width=stroke)

        if mark.label:
            lx = pad_left + int((mark.label_xy[0] if mark.label_xy else mark.bbox[0]) * width)
            ly = pad_top + int((mark.label_xy[1] if mark.label_xy else mark.bbox[1] - 0.08) * height)
            max_label_w = max(120, int(width * 0.20))
            lines = wrap_text(draw, mark.label, font, max_label_w - 16)
            line_h = draw.textbbox((0, 0), "Ag", font=font)[3]
            label_w = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines) + 16
            label_h = len(lines) * (line_h + 4) + 12
            lx = max(8, min(lx, canvas_w - label_w - 8))
            ly = max(8, min(ly, canvas_h - label_h - 8))
            draw.rounded_rectangle((lx, ly, lx + label_w, ly + label_h), radius=max(6, width // 260), outline=outline, fill=label_fill, width=stroke)
            ty = ly + 6
            for line in lines:
                draw.text((lx + 8, ty), line, font=font, fill=label_text)
                ty += line_h + 4

    combined = Image.alpha_composite(canvas, overlay).convert("RGB")
    dest.parent.mkdir(parents=True, exist_ok=True)
    combined.save(dest, quality=95)


def main() -> int:
    for figure in parse_figures(REPORT_PATH):
        if not figure.path.exists():
            print(f"Skipping missing image: {figure.path}")
            continue
        annotate_image(figure, figure.path, OUTPUT_ROOT / figure.path)
        print((OUTPUT_ROOT / figure.path).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
