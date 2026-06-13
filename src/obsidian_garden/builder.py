"""Build a static site from a parsed Obsidian vault."""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

import markdown

from .parser import IMAGE_EXTS, Note, WIKILINK_RE, EMBED_RE, parse_note, slugify
from .theme import CSS, render_page

SKIP_DIRS = {".obsidian", ".trash", ".git", "node_modules", "templates", "Templates"}

MD = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"])


def collect_notes(vault: Path, publish_only: bool = False) -> list[Note]:
    """Scan the vault for publishable .md notes."""
    notes = []
    for p in sorted(vault.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.relative_to(vault).parts):
            continue
        note = parse_note(p)
        if publish_only and not note.meta.get("publish"):
            continue
        if note.meta.get("publish") is False:
            continue
        notes.append(note)
    return notes


def link_notes(notes: list[Note]) -> dict[str, Note]:
    """Index notes by title/filename and wire up backlinks."""
    index: dict[str, Note] = {}
    for n in notes:
        index[n.title.lower()] = n
        index[n.path.stem.lower()] = n
    for n in notes:
        for target, _ in n.links:
            t = index.get(target.lower())
            if t and t is not n and n not in t.backlinks:
                t.backlinks.append(n)
    return index


def _find_attachment(vault: Path, name: str) -> Path | None:
    """Locate an embedded file anywhere in the vault."""
    cand = vault / name
    if cand.exists():
        return cand
    for p in vault.rglob(name):
        return p
    return None


def render_body(note: Note, index: dict[str, Note], vault: Path, out: Path) -> str:
    """Convert wikilinks/embeds, then markdown -> HTML."""
    body = note.body

    def embed_repl(m: re.Match) -> str:
        name = m.group(1).strip()
        src = _find_attachment(vault, name)
        if src and src.suffix.lower() in IMAGE_EXTS:
            assets = out / "assets"
            assets.mkdir(parents=True, exist_ok=True)
            dest = assets / src.name
            if not dest.exists():
                shutil.copy2(src, dest)
            return f"![{src.stem}](assets/{src.name})"
        target = index.get(Path(name).stem.lower())
        if target:
            return f"[{target.title}]({target.slug}.html)"
        return ""

    def link_repl(m: re.Match) -> str:
        target_name = m.group(1).strip()
        display = (m.group(2) or target_name).strip()
        target = index.get(target_name.lower())
        if target:
            return f'<a class="wikilink" href="{target.slug}.html">{html.escape(display)}</a>'
        return f'<span class="broken" title="未发布或不存在">{html.escape(display)}</span>'

    body = EMBED_RE.sub(embed_repl, body)
    body = WIKILINK_RE.sub(link_repl, body)
    MD.reset()
    return MD.convert(body)


def render_note_page(note: Note, index: dict[str, Note], vault: Path, out: Path, site_name: str) -> str:
    parts = [f"<h1>{html.escape(note.title)}</h1>"]
    meta_bits = []
    if note.date:
        meta_bits.append(html.escape(note.date))
    if meta_bits:
        parts.append(f'<div class="meta">{" · ".join(meta_bits)}</div>')
    if note.tags:
        chips = "".join(f'<a class="tag" href="tags.html#{slugify(t)}">#{html.escape(t)}</a>' for t in note.tags)
        parts.append(f'<div class="tags">{chips}</div>')
    parts.append(render_body(note, index, vault, out))
    if note.backlinks:
        items = "".join(
            f'<li><a class="wikilink" href="{b.slug}.html">{html.escape(b.title)}</a></li>'
            for b in sorted(note.backlinks, key=lambda x: x.title)
        )
        parts.append(f'<div class="backlinks"><h4>← LINKED FROM / 反向链接</h4><ul>{items}</ul></div>')
    return render_page(note.title, "\n".join(parts), site_name)


def render_index_page(notes: list[Note], site_name: str) -> str:
    items = []
    for n in sorted(notes, key=lambda x: (x.date, x.title), reverse=True):
        date = f'<span class="d">{html.escape(n.date)}</span>' if n.date else ""
        items.append(f'<li><a class="wikilink" href="{n.slug}.html">{html.escape(n.title)}</a>{date}</li>')
    content = (
        f"<h1>{html.escape(site_name)}</h1>"
        f'<div class="meta">{len(notes)} NOTES · <a href="tags.html">TAGS</a></div>'
        f'<ul class="note-list">{"".join(items)}</ul>'
    )
    return render_page("首页", content, site_name)


def render_tags_page(notes: list[Note], site_name: str) -> str:
    by_tag: dict[str, list[Note]] = {}
    for n in notes:
        for t in n.tags:
            by_tag.setdefault(t, []).append(n)
    sections = ["<h1>标签 TAGS</h1>"]
    for tag in sorted(by_tag):
        links = "".join(
            f'<li><a class="wikilink" href="{n.slug}.html">{html.escape(n.title)}</a></li>'
            for n in sorted(by_tag[tag], key=lambda x: x.title)
        )
        sections.append(f'<h3 id="{slugify(tag)}">#{html.escape(tag)}</h3><ul class="note-list">{links}</ul>')
    return render_page("标签", "\n".join(sections), site_name)


def build(vault: Path, out: Path, site_name: str = "My Garden", publish_only: bool = False) -> int:
    """Build the site. Returns the number of pages generated."""
    vault, out = Path(vault), Path(out)
    if not vault.is_dir():
        raise FileNotFoundError(f"vault not found: {vault}")
    notes = collect_notes(vault, publish_only)
    if not notes:
        raise ValueError("no publishable notes found")
    # 保证 slug 唯一，且不与站点保留页冲突
    seen = {"index", "tags", "style"}
    for n in notes:
        s, i = n.slug, 2
        while s in seen:
            s = f"{n.slug}-{i}"
            i += 1
        n.slug = s
        seen.add(s)
    index = link_notes(notes)
    out.mkdir(parents=True, exist_ok=True)
    (out / "style.css").write_text(CSS, encoding="utf-8")
    for n in notes:
        (out / f"{n.slug}.html").write_text(
            render_note_page(n, index, vault, out, site_name), encoding="utf-8"
        )
    (out / "index.html").write_text(render_index_page(notes, site_name), encoding="utf-8")
    (out / "tags.html").write_text(render_tags_page(notes, site_name), encoding="utf-8")
    return len(notes) + 2
