"""Build the public website (site/) from the Markdown files in this repo.

Run: python3 scripts/build_site.py   (needs: pip install markdown)
"""
import html, pathlib, re, shutil
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
REPO = "https://github.com/rowechcag-byte/constitution-for-human-creation"

PAGES = [  # (source, output, nav label, lang)
    ("README.md", "index.html", "Home", "en"),
    ("docs/foundational-principles.md", "principles.html", "The Eight Principles", "en"),
    ("docs/constitution.md", "constitution.html", "Full Constitution", "en"),
    ("docs/principios-fundamentales.md", "principios.html", "En español", "es"),
    ("docs/research-brief-frameworks.md", "research-brief.html", "Research brief", "en"),
    ("docs/pilot-sheets.md", "pilot-sheets.html", "Pilots", "en"),
]
LINKS = {pathlib.PurePosixPath(src).name: out for src, out, _, _ in PAGES}
LINKS["LICENSE"] = "https://creativecommons.org/licenses/by/4.0/"

CSS = """
:root{--ink:#1d2430;--muted:#5b6575;--accent:#1f4e79;--bg:#fbfaf7;--line:#e3e0d8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.65 Georgia,'Times New Roman',serif}
header{background:var(--accent);color:#fff;padding:18px 20px}
header a.brand{color:#fff;text-decoration:none;font-weight:bold;font-size:1.15em}
nav{margin-top:8px;font:15px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
nav a{color:#dfe9f5;margin-right:14px;text-decoration:none;white-space:nowrap}
nav a.on,nav a:hover{color:#fff;text-decoration:underline}
main{max-width:760px;margin:0 auto;padding:28px 20px 48px}
h1,h2,h3{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.25;color:var(--accent)}
h1{font-size:1.9em;margin-top:.2em}
a{color:var(--accent)}
table{border-collapse:collapse;width:100%;font-size:.9em;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
code{background:#efece4;padding:1px 4px;border-radius:3px;font-size:.9em}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
blockquote{border-left:4px solid var(--line);margin:1em 0;padding:.2em 1em;color:var(--muted)}
footer{border-top:1px solid var(--line);color:var(--muted);font:14px/1.6 system-ui,sans-serif;text-align:center;padding:20px}
footer a{color:var(--muted)}
"""

def fix_links(m):
    target = m.group(1)
    if target.startswith(("http", "#", "mailto:")):
        return m.group(0)
    path, _, frag = target.partition("#")
    name = pathlib.PurePosixPath(path).name
    new = LINKS.get(name)
    if not new:
        return m.group(0)
    return 'href="%s%s"' % (new, "#" + frag if frag else "")

LIST_RE = re.compile(r"^\s*([-*+]|\d+\.)\s")

def loosen_lists(text):
    """Python-Markdown needs a blank line before a list; GitHub doesn't."""
    out, prev = [], ""
    for line in text.splitlines():
        if LIST_RE.match(line) and prev.strip() and not LIST_RE.match(prev) and not prev.startswith(("|", "    ")):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out) + "\n"

def render(src, out, label, lang):
    text = (ROOT / src).read_text(encoding="utf-8")
    text = loosen_lists(text)
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "toc"])
    body = re.sub(r'href="([^"]+)"', fix_links, body)
    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    title = title_m.group(1).strip() if title_m else label
    nav = "".join('<a href="%s"%s>%s</a>' % (o, ' class="on"' if o == out else "", html.escape(l))
                  for _, o, l, _ in PAGES)
    page = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | Constitution for Human Creation</title>
<meta name="description" content="Constitution for Human Creation: eight plain foundational principles for AI, a living constitution open for public feedback.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header><a class="brand" href="index.html">Constitution for Human Creation</a><nav>{nav}</nav></header>
<main>
{body}
</main>
<footer>Text licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Copy, translate, and adapt it freely with credit to Constitution for Human Creation.<br>
Source and feedback: <a href="{REPO}">GitHub</a> · <a href="{REPO}/issues">open an issue</a></footer>
</body>
</html>
"""
    (OUT / out).write_text(page, encoding="utf-8")

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    for p in PAGES:
        render(*p)
    print("built", len(PAGES), "pages into", OUT)

if __name__ == "__main__":
    main()
