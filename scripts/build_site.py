"""Build the shutdown notice site (project ended 2026-10-06)."""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
REPO = "https://github.com/rowechcag-byte/constitution-for-human-creation"
CSS = """
:root{--ink:#1d2430;--muted:#5b6575;--accent:#1f4e79;--bg:#fbfaf7}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.65 Georgia,'Times New Roman',serif}
main{max-width:640px;margin:0 auto;padding:48px 20px}
h1{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--accent);font-size:1.7em;line-height:1.25}
p{margin:1em 0}a{color:var(--accent)}
.muted{color:var(--muted);font-size:.95em}
"""
PAGES = ["index.html","principles.html","constitution.html","principios.html","research-brief.html","pilot-sheets.html"]

def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.iterdir():
        if old.is_file():
            old.unlink()
    (OUT / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Constitution for Human Creation — ended</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
<h1>This project has ended</h1>
<p>Constitution for Human Creation is closed as of October 6, 2026. This website is offline.</p>
<p>A read-only archive of the text remains on GitHub:</p>
<p><a href="{REPO}">{REPO}</a></p>
<p class="muted">No further outreach or updates are planned.</p>
</main>
</body>
</html>
"""
    for name in PAGES:
        (OUT / name).write_text(html, encoding="utf-8")
    print(f"Wrote shutdown pages to {OUT}")

if __name__ == "__main__":
    main()
