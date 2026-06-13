"""Default theme: a clean, light 'digital garden' look."""

CSS = """
:root{
  --ink:#23263a;--dim:#6a7188;--vio:#6c4cf5;
  --line:rgba(120,110,220,.16);--card:rgba(255,255,255,.66);
  --mono:"JetBrains Mono","SF Mono",Consolas,monospace;
  --sans:-apple-system,"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
body{
  font-family:var(--sans);color:var(--ink);line-height:1.9;
  background:
    radial-gradient(55% 60% at 12% 10%, rgba(124,92,255,.18), transparent),
    radial-gradient(45% 55% at 90% 20%, rgba(64,210,255,.16), transparent),
    radial-gradient(50% 55% at 50% 100%, rgba(255,122,217,.10), transparent),
    #f2f3fb;
  background-attachment:fixed;
  min-height:100vh;padding:48px 20px 80px;
}
a{color:var(--vio);text-decoration:none}
a:hover{text-decoration:underline}
.container{max-width:760px;margin:0 auto}
.site-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:36px}
.site-head .name{font-weight:700;font-size:18px;color:var(--ink)}
.site-head .name:hover{text-decoration:none;color:var(--vio)}
.site-head .sub{font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.15em}
.card{
  background:var(--card);border:1px solid rgba(255,255,255,.8);border-radius:20px;
  padding:40px 44px;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.95),0 14px 40px rgba(96,84,200,.12);
}
h1{font-size:30px;line-height:1.4;margin-bottom:6px}
h2{font-size:21px;margin:1.6em 0 .6em}
h3{font-size:17px;margin:1.4em 0 .5em}
p{margin-bottom:1.1em}
ul,ol{margin:0 0 1.1em 1.4em}
blockquote{border-left:3px solid var(--vio);padding:8px 18px;margin:1.4em 0;color:#4d5470;background:rgba(108,76,245,.05);border-radius:0 10px 10px 0}
code{font-family:var(--mono);font-size:.88em;background:rgba(108,76,245,.08);padding:2px 6px;border-radius:6px}
pre{background:#1d1f2e;color:#dfe3f2;padding:18px 20px;border-radius:14px;overflow-x:auto;margin:1.4em 0}
pre code{background:none;padding:0;color:inherit}
img{max-width:100%;border-radius:12px}
hr{border:none;border-top:1px solid var(--line);margin:2em 0}
table{border-collapse:collapse;margin:1.4em 0;width:100%}
th,td{border:1px solid var(--line);padding:8px 12px;text-align:left}
.meta{font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.12em;margin-bottom:26px}
.tags{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 22px}
.tag{font-family:var(--mono);font-size:11px;color:var(--dim);border:1px solid var(--line);border-radius:999px;padding:2px 12px}
a.tag:hover{color:var(--vio);border-color:var(--vio);text-decoration:none}
a.wikilink{border-bottom:1px dashed rgba(108,76,245,.5)}
a.wikilink:hover{text-decoration:none;border-bottom-style:solid}
span.broken{color:var(--dim);border-bottom:1px dashed var(--line);cursor:default}
.backlinks{margin-top:42px;padding-top:24px;border-top:1px solid var(--line)}
.backlinks h4{font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.2em;margin-bottom:12px}
.backlinks li{list-style:none;margin-bottom:6px}
.note-list{list-style:none}
.note-list li{display:flex;justify-content:space-between;gap:16px;padding:13px 4px;border-bottom:1px solid var(--line);align-items:baseline}
.note-list li:last-child{border-bottom:none}
.note-list .d{font-family:var(--mono);font-size:11px;color:var(--dim);white-space:nowrap}
.footer{text-align:center;margin-top:40px;font-family:var(--mono);font-size:10px;color:#9aa0b8;letter-spacing:.15em}
@media(max-width:600px){.card{padding:28px 22px}}
"""

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {site_name}</title>
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<div class="container">
  <div class="site-head">
    <a class="name" href="{root}index.html">{site_name}</a>
    <span class="sub">DIGITAL GARDEN</span>
  </div>
  <div class="card">
{content}
  </div>
  <div class="footer">PLANTED WITH OBSIDIAN-GARDEN</div>
</div>
</body>
</html>
"""


def render_page(title: str, content: str, site_name: str, root: str = "") -> str:
    return PAGE.format(title=title, content=content, site_name=site_name, root=root)
