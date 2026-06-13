from pathlib import Path

import pytest

from obsidian_garden.builder import build, collect_notes, link_notes


@pytest.fixture
def vault(tmp_path: Path) -> Path:
    v = tmp_path / "vault"
    v.mkdir()
    (v / "Home.md").write_text(
        "---\ndate: 2026-06-01\ntags: [home]\n---\n# Hi\nGo to [[Second Note]] and [[Missing]].",
        encoding="utf-8",
    )
    (v / "Second Note.md").write_text("Back to [[Home]]. #demo", encoding="utf-8")
    (v / "Secret.md").write_text("---\npublish: false\n---\nhidden", encoding="utf-8")
    (v / ".obsidian").mkdir()
    (v / ".obsidian" / "app.md").write_text("config", encoding="utf-8")
    return v


def test_collect_skips_config_and_unpublished(vault: Path):
    notes = collect_notes(vault)
    assert {n.title for n in notes} == {"Home", "Second Note"}


def test_publish_only(vault: Path):
    (vault / "Pub.md").write_text("---\npublish: true\n---\nyes", encoding="utf-8")
    notes = collect_notes(vault, publish_only=True)
    assert [n.title for n in notes] == ["Pub"]


def test_backlinks(vault: Path):
    notes = collect_notes(vault)
    link_notes(notes)
    home = next(n for n in notes if n.title == "Home")
    second = next(n for n in notes if n.title == "Second Note")
    assert home in second.backlinks
    assert second in home.backlinks


def test_build_outputs(vault: Path, tmp_path: Path):
    out = tmp_path / "site"
    count = build(vault, out, site_name="Test Garden")
    assert count == 4  # 2 notes + index + tags
    assert (out / "index.html").exists()
    assert (out / "tags.html").exists()
    assert (out / "style.css").exists()
    second = (out / "second-note.html").read_text(encoding="utf-8")
    assert 'href="home.html"' in second      # resolved wikilink
    assert "反向链接" in second               # backlinks section
    home = (out / "home.html").read_text(encoding="utf-8")
    assert 'class="broken"' in home          # unresolved [[Missing]]
    idx = (out / "index.html").read_text(encoding="utf-8")
    assert "Test Garden" in idx and "2026-06-01" in idx


def test_reserved_slug_collision(tmp_path: Path):
    v = tmp_path / "v"
    v.mkdir()
    (v / "Index.md").write_text("I clash with the homepage", encoding="utf-8")
    out = tmp_path / "site"
    build(v, out, site_name="G")
    # 笔记被重命名为 index-2.html，站点首页未被覆盖
    assert (out / "index-2.html").exists()
    idx = (out / "index.html").read_text(encoding="utf-8")
    assert "index-2.html" in idx


def test_empty_vault_raises(tmp_path: Path):
    v = tmp_path / "v"
    v.mkdir()
    with pytest.raises(ValueError):
        build(v, tmp_path / "o")
