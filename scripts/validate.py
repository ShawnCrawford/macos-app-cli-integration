#!/usr/bin/env python3
"""Dependency-free structural checks for this Agent Skill repository."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    ROOT / "SKILL.md",
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "references/cli-interface.md",
    ROOT / "references/macos-integration.md",
    ROOT / "references/distribution-validation.md",
    ROOT / "references/example-projects.md",
]
errors: list[str] = []

for path in REQUIRED:
    if not path.is_file():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

skill_path = ROOT / "SKILL.md"
if skill_path.is_file():
    source = skill_path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", source, re.S)
    if not match:
        errors.append("SKILL.md: missing YAML frontmatter delimiters")
    else:
        frontmatter = match.group(1)
        for key in ("name", "description"):
            if not re.search(rf"(?m)^{re.escape(key)}:\s*\S", frontmatter):
                errors.append(f"SKILL.md: missing non-empty {key} frontmatter")
        name = re.search(r"(?m)^name:\s*([^\s#]+)\s*$", frontmatter)
        if name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1)):
            errors.append("SKILL.md: name must be lowercase kebab-case")
        if name and name.group(1) != ROOT.name:
            errors.append("SKILL.md: name must match the repository directory")

    placeholders = ("TODO", "REPLACE ME", "<skill-name>")
    for token in placeholders:
        if token in source:
            errors.append(f"SKILL.md: unresolved scaffold marker {token!r}")

link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for md in ROOT.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    for target in link_pattern.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        local = target.split("#", 1)[0]
        if not local:
            continue
        if not (md.parent / local).resolve().exists():
            errors.append(f"{md.relative_to(ROOT)}: broken local link {target!r}")

if errors:
    print("Validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("Skill repository structure, frontmatter, and local Markdown links are valid.")
