# obsidian-garden

[English](#english) | [中文](#中文)

Turn your Obsidian vault into a beautiful **digital garden** — a static site with working wikilinks, backlinks and tags. One command, zero config.

```
pip install obsidian-garden
obsidian-garden /path/to/vault -o site -n "My Garden"
```

---

## English

### Why

Obsidian notes link to each other with `[[wikilinks]]`. Most static site generators break them. obsidian-garden keeps your vault's link structure intact and publishes it as a clean, readable website — the way digital gardens are meant to work.

### Features

- **Wikilinks just work** — `[[note]]`, `[[note|alias]]`, `[[note#heading]]` all resolve to real links; unresolved links render as muted text instead of 404s
- **Backlinks** — every page lists the notes that link to it
- **Tags** — inline `#tags` and frontmatter tags collected into a tags page (CJK tags supported)
- **Image embeds** — `![[image.png]]` copied and rendered automatically
- **Selective publishing** — `--publish-only` builds only notes marked `publish: true`; `publish: false` always excludes a note
- **Chinese-friendly** — CJK titles, slugs, and tags are first-class
- **Zero config, zero JavaScript** — output is plain HTML + one CSS file, deployable anywhere (GitHub Pages, any static host)

### Usage

```bash
# build the whole vault
obsidian-garden ~/Documents/MyVault -o site -n "My Garden"

# only notes with `publish: true` in frontmatter
obsidian-garden ~/Documents/MyVault --publish-only -o site
```

Then deploy the `site/` folder to GitHub Pages or any static host.

### Frontmatter reference

```yaml
---
title: Custom Title    # optional, defaults to file name
date: 2026-06-13       # optional, shown in lists
tags: [garden, notes]  # optional
publish: true          # used by --publish-only; false always hides
---
```

### Related

- [obsidian-mcp](https://github.com/386522758/obsidian-mcp) — MCP server that lets AI agents read, write and search your Obsidian vault

---

## 中文

### 为什么做这个

Obsidian 的笔记之间用 `[[双向链接]]` 互相连接，但大多数静态网站生成器会弄断这些链接。obsidian-garden 完整保留笔记库的链接结构，把它发布成一个干净、可读的网站——这才是数字花园该有的样子。

### 功能

- **Wikilink 直接可用** — `[[笔记]]`、`[[笔记|别名]]`、`[[笔记#标题]]` 全部解析为真实链接；未发布的链接显示为灰色文本而不是 404
- **反向链接** — 每页底部列出链接到它的笔记
- **标签** — 正文 `#标签` 与 frontmatter 标签自动汇总成标签页（支持中文标签）
- **图片嵌入** — `![[图片.png]]` 自动复制并渲染
- **选择性发布** — `--publish-only` 只构建标记 `publish: true` 的笔记；`publish: false` 永远不发布
- **中文友好** — 中文标题、文件名、标签均为一等公民
- **零配置、零 JavaScript** — 输出纯 HTML + 一个 CSS 文件，可部署到任何静态托管（GitHub Pages 等）

### 使用

```bash
# 构建整个笔记库
obsidian-garden ~/Documents/我的笔记库 -o site -n "我的花园"

# 只发布 frontmatter 标记了 publish: true 的笔记
obsidian-garden ~/Documents/我的笔记库 --publish-only -o site
```

构建完成后，把 `site/` 文件夹部署到 GitHub Pages 或任意静态托管即可。

### 相关项目

- [obsidian-mcp](https://github.com/386522758/obsidian-mcp) — 让 AI 智能体读写、搜索 Obsidian 笔记库的 MCP 服务器

## License

MIT
