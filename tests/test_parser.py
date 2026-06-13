from pathlib import Path

from obsidian_garden.parser import (
    extract_embeds,
    extract_tags,
    extract_wikilinks,
    parse_frontmatter,
    parse_note,
    slugify,
)


def test_slugify():
    assert slugify("Hello World") == "hello-world"
    assert slugify("数字花园 与 自留地") == "数字花园-与-自留地"
    assert slugify("  Weird///Name!!  ") == "weirdname"
    assert slugify("***") == "untitled"


def test_frontmatter():
    meta, body = parse_frontmatter("---\ntitle: Test\ntags: [a, b]\n---\nbody here")
    assert meta["title"] == "Test"
    assert meta["tags"] == ["a", "b"]
    assert body == "body here"


def test_frontmatter_absent():
    meta, body = parse_frontmatter("just text")
    assert meta == {}
    assert body == "just text"


def test_wikilinks():
    body = "See [[Note A]] and [[note-b|alias]] plus [[C#heading|see C]]. `[[in code]]`"
    links = extract_wikilinks(body)
    assert ("Note A", "Note A") in links
    assert ("note-b", "alias") in links
    assert ("C", "see C") in links
    assert all(t != "in code" for t, _ in links)


def test_embeds_not_links():
    body = "![[image.png]] and [[Real Link]]"
    assert extract_embeds(body) == ["image.png"]
    assert extract_wikilinks(body) == [("Real Link", "Real Link")]


def test_tags():
    meta = {"tags": "x, y"}
    body = "Inline #garden and #中文标签 but not `#code`"
    tags = extract_tags(body, meta)
    assert tags[:2] == ["x", "y"]
    assert "garden" in tags and "中文标签" in tags
    assert "code" not in tags


def test_parse_note(tmp_path: Path):
    f = tmp_path / "My Note.md"
    f.write_text("---\ntags: [t1]\n---\nHello [[Other]]", encoding="utf-8")
    n = parse_note(f)
    assert n.title == "My Note"
    assert n.slug == "my-note"
    assert n.links == [("Other", "Other")]
    assert n.tags == ["t1"]
