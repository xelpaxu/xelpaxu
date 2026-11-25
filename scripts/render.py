
    
  
"""Render original SVG cards for the GitHub profile README."""
from datetime import date, datetime, timedelta, timezone
from hashlib import sha256
from html import escape
import json
import os
import re
from pathlib import Path
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "dark"
NOW = datetime.now(timezone.utc).replace(microsecond=0)
TODAY = NOW.date()
INK = "#f1eefb"
BACKGROUND = "#16131e"
OUTLINE = "#716282"
SHADOW = "#0c0a12"
BLUE, GREEN, GOLD, LILAC, PINK, CYAN = (
    "#263b59", "#203f35", "#493824", "#3d3056", "#4a2e37", "#213f49"
)
COLORS = ["#272433", "#214736", "#2d6749", "#64cc92", "#a0efb4"]


def rect(x, y, w, h, fill, radius=12, stroke="none", sw=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def label(x, y, value, size=15, fill=INK, bold=False, anchor="start"):
    font = "Arial Rounded MT Bold, Trebuchet MS, sans-serif" if bold else "ui-monospace, Consolas, monospace"
    weight = 900 if bold else 400
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(str(value))}</text>'


def panel(x, y, w, h, color, radius=17):
    return rect(x+3, y+4, w, h, SHADOW, radius) + rect(x, y, w, h, color, radius, OUTLINE, 2)


def write(name, title, width, height, body, frame=True):
    pattern = '<defs><pattern id="dots" width="23" height="23" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.05" fill="#40374d" opacity=".7"/></pattern></defs>'
    base = rect(1, 1, width-2, height-2, BACKGROUND, 19, OUTLINE, 2)
    base += rect(2, 2, width-4, height-4, "url(#dots)", 18)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title>{pattern}{base if frame else ""}{body}</svg>'
    (ASSETS / f"{name}.svg").write_text(svg + "\n", encoding="utf-8")


def badge(name, title, color, width):
    write(name, title, width, 43, panel(2, 2, width-7, 34, color, 10)
          + label((width-3)/2, 24, title, 15, bold=True, anchor="middle"), False)


def render_static():
    badge("link-github", "@xelpaxu", PINK, 111)
    badge("link-linkedin", "LinkedIn", BLUE, 112)
    badge("link-portfolio", "xlpxu.vercel.app", "#221e2c", 170)
    badge("projects-heading", "What I ship", GOLD, 155)
    badge("exploring-heading", "Currently exploring", PINK, 202)
    body = panel(22, 20, 775, 239, "#202032")
    body += rect(23, 21, 773, 35, "#28283d", 13)
    for x, color in [(43, "#fb6947"), (61, GOLD), (79, "#49bf84")]:
        body += f'<circle cx="{x}" cy="39" r="4.8" fill="{color}"/>'
    body += label(410, 44, "axel@iloilo: ~", 13, "#b9b5d1", anchor="middle")
    lines = [
        (89, "$ whoami", "#ff947b"),
        (117, "Axel John Nuqui  ·  Full-stack developer  ·  Iloilo City, PH", "#f5f0ff"),
        (143, "Computer Science student majoring in AI at WVSU.", "#c6c1dc"),
        (180, "$ cat now.txt", "#ff947b"),
        (208, "→ Building web and mobile apps with AI and real-time features.", "#c6c1dc"),
        (234, "→ Exploring Rust, system design, and backend architecture.", "#c6c1dc"),
    ]
    body += "".join(label(45, y, line, 15, color) for y, line, color in lines)
    write("whoami", "Whoami — Axel John Nuqui, Computer Science student at WVSU", 820, 280, body)

    projects = [
        ("vecpro", "VEC-PRO", "01", "Mosquito surveillance", ["AI-powered reporting and classification", "for mosquito breeding sites."], ["Next.js", "React Native", "YOLOv8"], "#233249"),
        ("visaia", "VISAIA", "02", "Farm protection", ["Field scouting and pest detection", "for corn farmers."], ["Flutter", "Firebase", "YOLO"], "#213a42"),
        ("visaia-dashboard", "VISAIA Dashboard", "03", "Agricultural monitoring", ["Validate pest reports, monitor fields,", "and manage farm records."], ["Next.js", "Firestore", "Leaflet"], "#3b3027"),
        ("synt-ask", "SYNT-ASK", "04", "Multiplayer game", ["Find the impostor in a real-time game", "using semantic similarity."], ["React", "Socket.IO", "DistilBERT"], "#223c33"),
    ]
    glyphs = {
        "01": '<path d="M26 8C20 17 16 21 16 28a10 10 0 0 0 20 0c0-7-4-11-10-20z"/><path d="M22 31c1 3 3 5 6 5"/>',
        "02": '<path d="M26 41V23m0 7C11 30 10 16 10 16c11 0 16 7 16 14zm0-7c0-8 7-13 16-14 0 9-7 14-16 14z"/>',
        "03": '<path d="M11 12h30v27H11zM11 20h30m-23 12 6-5 5 4 6-7"/>',
        "04": '<path d="M15 19h22c4 0 7 13 5 16-2 4-6 0-10-4H20c-4 4-8 8-10 4-2-3 1-16 5-16zM17 24v8m-4-4h8m13-2h1m3 4h1"/>',
    }
    for slug, title, mark, kind, lines, tags, background in projects:
        body = panel(12, 12, 371, 218, background)
        body += panel(26, 29, 52, 52, "#272336", 12)
        body += f'<g transform="translate(26 29)" stroke="#f1dcff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none">{glyphs[mark]}</g>'
        body += label(92, 51, title, 24, bold=True)
        body += rect(92, 59, len(kind)*7+18, 21, "#62cb92", 10, INK, 1)
        body += label(101, 74, kind, 11, "#112a20")
        body += panel(343, 26, 23, 23, "#ff7044", 6)
        body += label(354, 43, "↗", 17, "#24121a", bold=True, anchor="middle")