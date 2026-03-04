#!/usr/bin/env python3
"""Export Advent instruction HTML files to readable Markdown copies.

This utility scans `advent20XX/DayN/dN_instructions.html` files and writes
`dN_instructions.md` next to each source file. The converter focuses on AoC's
`article.day-desc` content to keep output concise for GitHub browsing.
"""

from __future__ import annotations

import argparse
import html
import re
from html.parser import HTMLParser
from pathlib import Path


class AoCArticleMarkdownParser(HTMLParser):
    """Convert AoC article HTML fragments into readable Markdown text."""

    BLOCK_TAGS = {"p", "div", "section", "article", "blockquote"}
    HEADING_TAGS = {"h1", "h2", "h3", "h4"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.parts: list[str] = []
        self.capture_depth = 0
        self.skip_depth = 0
        self.in_pre = False
        self.in_code = False
        self.in_em = False
        self.in_li = False
        self.heading_level: int | None = None

    def _emit(self, text: str) -> None:
        if self.capture_depth > 0 and self.skip_depth == 0:
            self.parts.append(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if self.skip_depth > 0:
            self.skip_depth += 1
            return

        if tag in {"script", "style"}:
            self.skip_depth = 1
            return

        classes = set((attrs_dict.get("class") or "").split())
        if tag == "article" and "day-desc" in classes:
            self.capture_depth += 1
            if self.parts and not self.parts[-1].endswith("\n\n"):
                self.parts.append("\n\n")
            return

        if self.capture_depth == 0:
            return

        if tag in self.HEADING_TAGS:
            level = int(tag[1])
            self.heading_level = min(max(level, 1), 6)
            self._emit("\n\n" + "#" * self.heading_level + " ")
            return

        if tag in self.BLOCK_TAGS:
            self._emit("\n\n")
            return

        if tag in {"ul", "ol"}:
            self._emit("\n")
            return

        if tag == "li":
            self.in_li = True
            self._emit("\n- ")
            return

        if tag == "br":
            self._emit("\n")
            return

        if tag == "pre":
            self.in_pre = True
            self._emit("\n\n```text\n")
            return

        if tag == "code":
            self.in_code = True
            if not self.in_pre:
                self._emit("`")
            return

        if tag in {"em", "i"}:
            self.in_em = True
            self._emit("*")
            return

        if tag in {"strong", "b"}:
            self._emit("**")
            return

        if tag == "a":
            # Keep anchor text only for readability.
            return

    def handle_endtag(self, tag: str) -> None:
        if self.skip_depth > 0:
            self.skip_depth -= 1
            return

        if tag == "article" and self.capture_depth > 0:
            self.capture_depth -= 1
            self._emit("\n\n")
            return

        if self.capture_depth == 0:
            return

        if tag in self.HEADING_TAGS:
            self.heading_level = None
            self._emit("\n")
            return

        if tag == "li":
            self.in_li = False
            return

        if tag == "pre":
            self.in_pre = False
            self._emit("\n```\n\n")
            return

        if tag == "code":
            if not self.in_pre:
                self._emit("`")
            self.in_code = False
            return

        if tag in {"em", "i"}:
            self.in_em = False
            self._emit("*")
            return

        if tag in {"strong", "b"}:
            self._emit("**")
            return

    def handle_data(self, data: str) -> None:
        if self.capture_depth == 0 or self.skip_depth > 0:
            return

        if self.in_pre:
            self._emit(html.unescape(data))
            return

        text = html.unescape(data)
        text = re.sub(r"\s+", " ", text)
        if text.strip():
            self._emit(text)

    def handle_entityref(self, name: str) -> None:
        if self.capture_depth > 0 and self.skip_depth == 0:
            self._emit(html.unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        if self.capture_depth > 0 and self.skip_depth == 0:
            self._emit(html.unescape(f"&#{name};"))

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n[ \t]+", "\n", text)
        return text.strip() + "\n"


def convert_file(html_path: Path, overwrite: bool) -> bool:
    """Convert one HTML instructions file into a Markdown sibling file."""
    md_path = html_path.with_suffix(".md")
    if md_path.exists() and not overwrite:
        return False

    parser = AoCArticleMarkdownParser()
    parser.feed(html_path.read_text(encoding="utf-8", errors="ignore"))
    body = parser.markdown()

    rel = html_path.relative_to(Path.cwd())
    header = (
        f"# {rel.parent.name} Instructions\n\n"
        f"Source: `{rel.as_posix()}`\n\n"
    )
    md_path.write_text(header + body, encoding="utf-8")
    return True


def find_instruction_html(root: Path) -> list[Path]:
    """Return all known AoC instruction HTML files in stable sorted order."""
    return sorted(root.glob("advent20*/Day*/d*_instructions.html"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overwrite", action="store_true", help="Rewrite existing .md files")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path.cwd()
    files = find_instruction_html(root)
    created = 0
    for html_file in files:
        if convert_file(html_file, overwrite=args.overwrite):
            created += 1
    print(f"html_files={len(files)} markdown_written={created}")


if __name__ == "__main__":
    main()
