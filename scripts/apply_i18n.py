#!/usr/bin/env python3
"""Tag featured project blocks with data-i18n keys; merge TR project copy into tr.json."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
EN_JSON = ROOT / "i18n/en.json"
TR_JSON = ROOT / "i18n/tr.json"
TR_PROJ = Path(__file__).resolve().parent / "tr_projects.json"

PROJECT_IDS = [
    "analytics",
    "coach",
    "analyzer",
    "kpi",
    "skills",
    "gateway",
    "chatbot",
    "clustering",
]


def find_project_block(html: str, pid: str) -> tuple[int, int]:
    anchor = f'data-i18n="proj.{pid}.title"'
    pos = html.find(anchor)
    if pos < 0:
        raise ValueError(f"Project anchor not found: {pid}")
    start = html.rfind('<div class="ga-project"', 0, pos)
    if start < 0:
        raise ValueError(f"ga-project start not found: {pid}")
    depth = 0
    i = start
    while i < len(html):
        if html.startswith("<div", i):
            depth += 1
            i += 4
        elif html.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return start, i
        else:
            i += 1
    raise ValueError(f"Could not close ga-project block: {pid}")


def patch_block(block: str, pid: str, data: dict) -> str:
    p = f"proj.{pid}"

    block = re.sub(
        r'<span class="ga-badge"[^>]*>[^<]*</span>',
        f'<span class="ga-badge" data-i18n="{p}.badge">{data["badge"]}</span>',
        block,
        count=1,
    )

    block = re.sub(
        r'<p class="ga-desc"[^>]*>.*?</p>',
        f'<p class="ga-desc" data-i18n-html="{p}.desc">{data["desc"]}</p>',
        block,
        count=1,
        flags=re.S,
    )

    mi = [1]

    def metric_repl(m):
        n = mi[0]
        mi[0] += 1
        key = f"{p}.m{n}"
        val = data.get(f"m{n}", m.group(1))
        return f'<div class="ga-metric-lbl" data-i18n="{key}">{val}</div>'

    block = re.sub(
        r'<div class="ga-metric-lbl"[^>]*>([^<]*)</div>',
        metric_repl,
        block,
    )

    ci = [1]

    def contrib_repl(m):
        n = ci[0]
        ci[0] += 1
        c = data.get(f"c{n}", {})
        ck = f"{p}.c{n}"
        return (
            f'{m.group(1)}'
            f'<div class="ga-contrib-module" data-i18n="{ck}.module">{c.get("module", m.group(2))}</div>\n            '
            f'<div class="ga-contrib-title" data-i18n="{ck}.title">{c.get("title", m.group(3))}</div>\n            '
            f'<div class="ga-contrib-desc" data-i18n-html="{ck}.desc">{c.get("desc", m.group(4))}</div>'
        )

    block = re.sub(
        r'(<div class="ga-contrib">\s*)'
        r'<div class="ga-contrib-module"[^>]*>([^<]*)</div>\s*'
        r'<div class="ga-contrib-title"[^>]*>([^<]*)</div>\s*'
        r'<div class="ga-contrib-desc"[^>]*>(.*?)</div>',
        contrib_repl,
        block,
        flags=re.S,
    )

    block = re.sub(
        r'<div class="ga-highlight-title"[^>]*>[^<]*</div>',
        f'<div class="ga-highlight-title" data-i18n="{p}.highlightTitle">{data["highlightTitle"]}</div>',
        block,
        count=1,
    )
    block = re.sub(
        r'<div class="ga-highlight-desc"[^>]*>.*?</div>',
        f'<div class="ga-highlight-desc" data-i18n-html="{p}.highlightDesc">{data["highlightDesc"]}</div>',
        block,
        count=1,
        flags=re.S,
    )
    return block


def patch_html(html: str, proj: dict) -> str:
    for pid in PROJECT_IDS:
        start, end = find_project_block(html, pid)
        block = html[start:end]
        html = html[:start] + patch_block(block, pid, proj[pid]) + html[end:]
    return html


def main():
    en = json.loads(EN_JSON.read_text(encoding="utf-8"))
    tr = json.loads(TR_JSON.read_text(encoding="utf-8"))
    tr_proj = json.loads(TR_PROJ.read_text(encoding="utf-8"))

    for pid in PROJECT_IDS:
        merged = dict(en["proj"][pid])
        merged.update(tr_proj[pid])
        tr["proj"][pid] = merged

    html = HTML.read_text(encoding="utf-8")
    html = patch_html(html, en["proj"])
    HTML.write_text(html, encoding="utf-8")
    TR_JSON.write_text(json.dumps(tr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Done: index.html tagged, tr.json proj merged.")


if __name__ == "__main__":
    main()
