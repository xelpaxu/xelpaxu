"""Render original SVG cards for the GitHub profile README."""
from datetime import date, datetime, timedelta, timezone
from hashlib import sha256
from html import escape
import json
import os
import re
from pathlib import Path
import sys
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
        for index, line in enumerate(lines):
            body += label(28, 119+22*index, line, 16, bold=True)
        x = 28
        for tag, color in zip(tags, [BLUE, CYAN, LILAC]):
            width = len(tag)*7+15
            body += rect(x, 170, width, 23, color, 5, INK, 1)
            body += label(x+7, 186, tag, 11)
            x += width+7
        write(slug, title, 400, 246, body)

    body = ""
    for i, (title, subtitle, color) in enumerate([
        ("Rust", "Terminal tools", GOLD),
        ("System design", "Scalable services", BLUE),
        ("Backend", "APIs & real-time apps", GREEN),
    ]):
        x = 22+i*261
        body += panel(x, 21, 249, 99, color)
        body += label(x+15, 61, title, 23, bold=True)
        body += label(x+15, 88, subtitle, 13)
    write("exploring", "Currently exploring Rust, system design, and backend architecture", 820, 144, body)


def days_between(start, end):
    return [start+timedelta(days=i) for i in range((end-start).days+1)]


def query(token, statement, **variables):
    request = Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": statement, "variables": variables}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "xelpaxu-profile-readme"},
    )
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError(result["errors"][0]["message"])
    return result["data"]["user"]


def get_data(token):
    login = os.environ.get("GITHUB_REPOSITORY_OWNER", "xelpaxu")
    user = query(token, """query($login:String!) {
      user(login:$login) {
        createdAt followers { totalCount }
        repositories(first:1, privacy:PUBLIC, ownerAffiliations:[OWNER]) { totalCount }
      }
    }""", login=login)
    start_year = int(user["createdAt"][:4])
    counts = {}
    for year in range(start_year, TODAY.year+1):
        end = NOW.isoformat() if year == TODAY.year else f"{year}-12-31T23:59:59Z"
        year_data = query(token, """query($login:String!, $from:DateTime!, $to:DateTime!) {
          user(login:$login) { contributionsCollection(from:$from,to:$to) {
            contributionCalendar { weeks { contributionDays { date contributionCount } } }
          } }
        }""", login=login, **{"from": f"{year}-01-01T00:00:00Z", "to": end})
        for week in year_data["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for day in week["contributionDays"]:
                parsed = date.fromisoformat(day["date"])
                if parsed.year == year and parsed <= TODAY:
                    counts[parsed] = day["contributionCount"]
    stars = 0
    cursor = None
    while True:
        page = query(token, """query($login:String!, $cursor:String) {
          user(login:$login) { repositories(first:100, after:$cursor, privacy:PUBLIC, ownerAffiliations:[OWNER]) {
            nodes { stargazerCount } pageInfo { endCursor hasNextPage }
          } }
        }""", login=login, cursor=cursor)["repositories"]
        stars += sum(repo["stargazerCount"] for repo in page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return counts, start_year, user["repositories"]["totalCount"], stars, user["followers"]["totalCount"]


def render_stats(stats):
    counts, year, repos, stars, followers = stats if stats else ({}, None, None, None, None)
    recent = days_between(TODAY-timedelta(days=364), TODAY)
    longest = current = running = 0
    if stats:
        for day in days_between(date(year, 1, 1), TODAY):
            running = running+1 if counts.get(day, 0) else 0
            longest = max(longest, running)
            if day == TODAY-timedelta(days=1):
                current = running
        if counts.get(TODAY, 0):
            current = running

    def value(number):
        return "—" if number is None else f"{number:,}"

    body = label(29, 49, "On GitHub", 29, bold=True)
    body += label(787, 47, f"redrawn nightly · {TODAY:%d %b %Y}" if stats else "awaiting first refresh", 13, "#bfb5ce", anchor="end")
    cards = [
        (value(sum(counts.get(day, 0) for day in recent) if stats else None), "contributions in", "the last year", BLUE, "▦"),
        (f"{current} days" if stats else "—", "current streak", "", GREEN, "◆"),
        (f"{longest} days" if stats else "—", "longest streak", "on record", GOLD, "★"),
        (value(sum(counts.values()) if stats else None), "contributions", f"since {year}" if stats else "on record", LILAC, "▥"),
    ]
    for i, (number, first, second, color, icon) in enumerate(cards):
        x = 29+i*194
        body += f'<g transform="rotate({[-1, 1, -0.8, 1][i]} {x+89} 136)">'
        body += panel(x, 74, 177, 128, color)
        body += label(x+146, 106, icon, 22, "#ff9b83", True)
        body += label(x+14, 139, number, 30, bold=True)
        body += label(x+14, 163, first, 13)
        body += label(x+14, 182, second, 13)
        body += "</g>"
    for x, width, number, caption, color in [
        (29, 224, repos, "public repos", CYAN),
        (272, 224, stars, "stars earned", PINK),
        (515, 273, followers, "followers", GREEN),
    ]:
        body += panel(x, 220, width, 60, color)
        body += label(x+17, 258, value(number), 27, bold=True)
        body += label(x+97, 256, caption, 13)
    write("github", "GitHub contribution stats", 820, 313, body)


def heatmap(name, caption, days, counts, numbered=False, ready=True):
    first = days[0]-timedelta(days=(days[0].weekday()+1)%7)
    weeks = (days[-1]-first).days//7+1
    step = min(28, 744/weeks)
    cell = step-2
    maximum = max((counts.get(day, 0) for day in days), default=0)
    total = sum(counts.get(day, 0) for day in days)
    body = panel(25, 23, 767, 321, "#221e2c")
    title = f"{total:,} contributions {caption}" if ready else f"Contribution calendar {caption}"
    body += label(40, 61, title, 20, bold=True)
    if not ready:
        body += label(410, 192, "The calendar appears after the first successful refresh.", 15, "#bfb5ce", anchor="middle")
    else:
        for day in days:
            column, row = divmod((day-first).days, 7)
            x, y = 40+column*step, 96+row*29
            count = counts.get(day, 0)
            level = min(4, 1+(4*(count-1)//max(1, maximum))) if count else 0
            body += rect(x, y, cell, 25, COLORS[level], 5)
            if day == days[0] or (day.day == 1 and column > 1):
                body += label(x, 87, day.strftime("%b"), 11, "#bfb5ce")
            if numbered:
                body += label(x+cell/2, y+17, count, 11, "#122a1d" if level >= 3 else INK, anchor="middle")
        body += label(40, 324, "contributions per day", 13, "#bfb5ce")
        body += label(615, 324, "Less", 12, "#bfb5ce")
        for index, color in enumerate(COLORS):
            body += rect(651+17*index, 313, 14, 14, color, 2)
        body += label(739, 324, "More", 12, "#bfb5ce")
    write(name, title, 820, 369, body)


def chart(counts, ready):
    days = days_between(TODAY-timedelta(days=29), TODAY)
    values = [counts.get(day, 0) for day in days]
    maximum = max(4, max(values))
    body = panel(25, 24, 767, 318, "#221e2c")
    title = f"{sum(values):,} contributions in the last 30 days" if ready else "Contributions in the last 30 days"
    body += label(42, 62, title, 20, bold=True)
    if ready:
        points = [(76+i*24, 281-190*count/maximum) for i, count in enumerate(values)]
        for i in range(5):
            y = 281-i*47.5
            body += f'<path d="M76 {y}H772" stroke="#50475e" stroke-dasharray="4 5"/>'
            body += label(67, y+4, round(maximum*i/4), 11, "#bfb5ce", anchor="end")
        path = " ".join(f"{x},{y:.2f}" for x, y in points)
        body += f'<polygon points="76,281 {path} 772,281" fill="#432839"/>'
        body += f'<polyline points="{path}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
        body += f'<polyline points="{path}" fill="none" stroke="#f66545" stroke-width="3" stroke-linejoin="round"/>'
        for (x, y), day in zip(points, days):
            body += f'<circle cx="{x}" cy="{y:.2f}" r="4" fill="#ff7654" stroke="{INK}" stroke-width="1.5"/>'
            body += label(x, 301, day.day, 11, "#bfb5ce", anchor="middle")
            if day == days[0] or day.day == 1:
                body += label(x, 319, day.strftime("%b"), 11, "#bfb5ce", anchor="middle")
    else:
        body += label(410, 192, "The chart appears after the first successful refresh.", 15, "#bfb5ce", anchor="middle")
    write("activity-30d", title, 820, 368, body)


def main():
    preview = "--initial" in sys.argv
    ASSETS.mkdir(parents=True, exist_ok=True)
    if preview:
        stats = None
    else:
        token = os.environ.get("PROFILE_STATS_TOKEN")
        if not token:
            raise SystemExit("Set the PROFILE_STATS_TOKEN repository secret before running the refresh.")
        stats = get_data(token)
    render_static()
    render_stats(stats)
    counts = stats[0] if stats else {}
    heatmap("activity-6mo", "in the last 6 months", days_between(TODAY-timedelta(days=181), TODAY),
            counts, numbered=True, ready=bool(stats))
    recent = days_between(TODAY-timedelta(days=364), TODAY)
    heatmap("activity-12mo", "in the last 12 months", recent, counts, ready=bool(stats))
    chart(counts, bool(stats))
    readme = ROOT / "README.md"
    source = readme.read_text(encoding="utf-8")
    start, end = "<!-- activity:start -->", "<!-- activity:end -->"
    contents = ["<details>", f"<summary>Last 12 months{f' · {sum(counts.get(day, 0) for day in recent):,} contributions' if stats else ''}</summary>",
                "", "![Last 12 months of contributions](assets/dark/activity-12mo.svg)", "", "</details>"]
    if stats:
        for year in range(TODAY.year, stats[1]-1, -1):
            days = days_between(date(year, 1, 1), min(TODAY, date(year, 12, 31)))
            heatmap(f"activity-{year}", f"in {year}", days, counts)
            contents.extend(["", "<details>",
                             f"<summary>{year} · {sum(counts.get(day, 0) for day in days):,} contributions</summary>",
                             "", f"![Contributions in {year}](assets/dark/activity-{year}.svg)", "", "</details>"])
    before, after = source.split(start, 1)
    trailing = after.split(end, 1)[1]
    updated = before+start+"\n\n"+"\n".join(contents)+"\n\n"+end+trailing

    def versioned_asset(match):
        path = match[1]
        digest = sha256((ROOT / path).read_bytes()).hexdigest()[:12]
        return f"{path}?v={digest}"

    updated = re.sub(r"(assets/dark/[\w-]+\.svg)(?:\?v=[0-9a-f]+)?", versioned_asset, updated)
    readme.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
