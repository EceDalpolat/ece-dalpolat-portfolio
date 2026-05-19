#!/usr/bin/env python3
"""Extract project copy from index.html, merge TR translations, tag data-i18n attributes."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"

MARKERS = [
    ("analytics", "ANALYTICS"),
    ("coach", "COACH"),
    ("analyzer", "ANALYZER"),
    ("kpi", "KPI ADVISOR"),
    ("skills", "SKILLS ADVISOR"),
    ("gateway", "AGENT GATEWAY"),
    ("chatbot", "QKARE CHATBOT"),
    ("clustering", "CLUSTERING"),
]

COMMON = {
    "badgeProd": {"en": "Production · B2B SaaS", "tr": "Üretim · B2B SaaS"},
    "badgeWeb": {"en": "Production · Web", "tr": "Üretim · Web"},
    "badgePlatform": {"en": "Production · Platform", "tr": "Üretim · Platform"},
    "badgeRd": {"en": "R&D · Research", "tr": "Ar-Ge · Araştırma"},
}


def extract_block(html: str, marker: str) -> str:
    pat = rf"<!-- {re.escape(marker)}[^>]* -->\s*(<div class=\"ga-project\".*?</div>\s*</motion.div>\s*</div>)"
    m = re.search(pat, html, re.S)
    if not m:
        pat2 = rf"<!-- {re.escape(marker)}[^>]* -->\s*(<motion.div class=\"ga-project\".*?</div>\s*</div>)"
        m = re.search(pat2, html, re.S)
    if not m:
        raise ValueError(f"Block not found: {marker}")
    return m.group(1).replace("motion.div", "motion.div")  # noop


def extract_fields(block: str) -> dict:
    badge = re.search(r'class="ga-badge">([^<]*)</', block)
    desc = re.search(r'class="ga-desc">(.*?)</p>', block, re.S)
    metrics = re.findall(r'class="ga-metric-lbl">([^<]*)</', block)
    ht = re.search(r'class="ga-highlight-title">([^<]*)</', block)
    hd = re.search(r'class="ga-highlight-desc">(.*?)</div>', block, re.S)
    contribs = []
    for mod, title, cdesc in re.findall(
        r'class="ga-contrib-module">([^<]*)</div>\s*'
        r'<div class="ga-contrib-title">([^<]*)</div>\s*'
        r'<motion.div class="ga-contrib-desc">(.*?)</div>',
        block,
        re.S,
    ):
        contribs.append(
            {
                "module": mod.strip(),
                "title": title.strip(),
                "desc": cdesc.strip(),
            }
        )
    block = block.replace("motion.div", "motion.div")
    contribs = []
    for mod, title, cdesc in re.findall(
        r'class="ga-contrib-module">([^<]*)</motion.div>\s*'
        r'<motion.div class="ga-contrib-title">([^<]*)</motion.div>\s*'
        r'<motion.div class="ga-contrib-desc">(.*?)</motion.div>',
        block,
        re.S,
    ):
        contribs.append({"module": mod.strip(), "title": title.strip(), "desc": cdesc.strip()})
    if not contribs:
        for mod, title, cdesc in re.findall(
            r'class="ga-contrib-module">([^<]*)</div>\s*'
            r'<div class="ga-contrib-title">([^<]*)</motion.div>\s*'
            r'<motion.div class="ga-contrib-desc">(.*?)</motion.div>',
            block,
            re.S,
        ):
            contribs.append({"module": mod.strip(), "title": title.strip(), "desc": cdesc.strip()})
    if not contribs:
        for mod, title, cdesc in re.findall(
            r'class="ga-contrib-module">([^<]*)</motion.div>\s*'
            r'<motion.div class="ga-contrib-title">([^<]*)</div>\s*'
            r'<motion.div class="ga-contrib-desc">(.*?)</div>',
            block,
            re.S,
        ):
            contribs.append({"module": mod.strip(), "title": title.strip(), "desc": cdesc.strip()})

    return {
        "badge": badge.group(1).strip() if badge else "",
        "desc": desc.group(1).strip() if desc else "",
        "metrics": [m.strip() for m in metrics],
        "contribs": contribs,
        "highlightTitle": ht.group(1).strip() if ht else "",
        "highlightDesc": hd.group(1).strip() if hd else "",
    }


def fix_contrib_regex(block: str) -> list:
    contribs = []
    for part in re.split(r'<motion.div class="ga-contrib">|<div class="ga-contrib">', block)[1:]:
        mod = re.search(r'class="ga-contrib-module">([^<]*)</', part)
        title = re.search(r'class="ga-contrib-title">([^<]*)</', part)
        desc = re.search(r'class="ga-contrib-desc">(.*?)</motion.div>', part, re.S)
        if not desc:
            desc = re.search(r'class="ga-contrib-desc">(.*?)</motion.div>', part, re.S)
        if mod and title and desc:
            contribs.append(
                {
                    "module": mod.group(1).strip(),
                    "title": title.group(1).strip(),
                    "desc": desc.group(1).strip(),
                }
            )
    return contribs


def extract_fields_v2(block: str) -> dict:
    badge = re.search(r'class="ga-badge">([^<]*)</', block)
    desc = re.search(r'class="ga-desc">(.*?)</p>', block, re.S)
    metrics = re.findall(r'class="ga-metric-lbl">([^<]*)</', block)
    ht = re.search(r'class="ga-highlight-title">([^<]*)</', block)
    hd = re.search(r'class="ga-highlight-desc">(.*?)</motion.div>', block, re.S)
    if not hd:
        hd = re.search(r'class="ga-highlight-desc">(.*?)</div>', block, re.S)
    return {
        "badge": badge.group(1).strip() if badge else "",
        "desc": desc.group(1).strip() if desc else "",
        "metrics": [m.strip() for m in metrics],
        "contribs": fix_contrib_regex(block),
        "highlightTitle": ht.group(1).strip() if ht else "",
        "highlightDesc": hd.group(1).strip() if hd else "",
    }


# Turkish translations keyed same as English extracted text (by project id + field path)
TR: dict = {}
