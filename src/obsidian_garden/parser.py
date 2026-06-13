"""Parse Obsidian-flavoured markdown: frontmatter, wikilinks, tags, embeds."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
# [[target]], [[target|alias]], [[target#heading]], [[target#heading|alias]]
WIKILINK_RE = re.compile(r"(?<!\!)\[\[([^\[\]|#]+)(?:#[^\[\]|]*)?(?:\|([^\[\]]+))?\]\]")
EMBED_RE = re.compile(r"!\[\[([^\[\]|]+?)(?:\|[^\[\]]*)?\]\]")
TAG_RE = re.compile(r"(?:^|\s)#([\w一-鿿/-]+)", re.UNICODE)
CODE_BLOCK_RE = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp"}


@dataclass
class Note:
    """A single parsed vault note."""

    path: Path
    title: str
    slug: str
    meta: dict = field(default_factory=dict)
    body: str = ""
    links: list[tuple[str, str]] = field(default_factory=list)   # (target title, display text)
    embeds: list[str] = field(default_factory=list)              # embedded file names
    tags: list[str] = field(default_factory=list)
    backlinks: list["Note"] = field(default_factory=list)

    @property
    def date(self) -> str:
        for key in ("date", "created", "updated"):
            if key in self.meta:
                return str(self.meta[key])
        return ""


def slugify(name: str) -> str:
    """File-system and URL safe slug. Keeps CJK characters."""
    name = unicodedata.normalize("NFKC", name).strip().lower()
    name = re.sub(r"[\s_]+", "-", name)
    name = re.sub(r"[^\w一-鿿-]", "", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return name or "untitled"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from the body. Returns ({} , text) when absent."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
        if not isinstance(meta, dict):
            meta = {}
    except yaml.YAMLError:
        meta = {}
    return meta, text[m.end():]


def extract_wikilinks(body: str) -> list[tuple[str, str]]:
    """All [[wikilinks]] as (target, display) pairs, ignoring code blocks."""
    clean = CODE_BLOCK_RE.sub("", body)
    out = []
    for m in WIKILINK_RE.finditer(clean):
        target = m.group(1).strip()
        display = (m.group(2) or target).strip()
        out.append((target, display))
    return out


def extract_embeds(body: str) -> list[str]:
    """All ![[embedded]] file names."""
    clean = CODE_BLOCK_RE.sub("", body)
    return [m.group(1).strip() for m in EMBED_RE.finditer(clean)]


def extract_tags(body: str, meta: dict) -> list[str]:
    """Tags from frontmatter plus inline #tags (code blocks excluded)."""
    tags: list[str] = []
    fm = meta.get("tags") or meta.get("tag") or []
    if isinstance(fm, str):
        fm = [t.strip() for t in re.split(r"[,，]", fm) if t.strip()]
    tags.extend(str(t).lstrip("#") for t in fm)
    clean = CODE_BLOCK_RE.sub("", body)
    tags.extend(m.group(1) for m in TAG_RE.finditer(clean))
    seen, out = set(), []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def parse_note(path: Path) -> Note:
    """Parse one .md file into a Note."""
    text = path.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(text)
    title = str(meta.get("title") or path.stem)
    return Note(
        path=path,
        title=title,
        slug=slugify(title),
        meta=meta,
        body=body,
        links=extract_wikilinks(body),
        embeds=extract_embeds(body),
        tags=extract_tags(body, meta),
    )
