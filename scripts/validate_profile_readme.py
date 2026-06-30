#!/usr/bin/env python3
"""Validate the profile README structure and links.

The profile repository is mostly documentation, so this script keeps the
README useful by checking that the important visitor-facing sections exist,
that project links use expected GitHub URLs, and that markdown links are not
empty or malformed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

REQUIRED_SECTIONS = [
    "# Asim Awdah",
    "## What I build",
    "## Featured projects",
    "## Current roadmap",
    "## Working style",
    "## Tech stack",
    "## Quick links",
]

REQUIRED_PROJECT_LINKS = {
    "MahamKit": "https://github.com/asimawdah/maham-app",
    "maham-api": "https://github.com/asimawdah/maham-api",
    "Vaultlet": "https://github.com/asimawdah/vaultlet",
    "SkillMint": "https://github.com/asimawdah/SkillMint",
    "main_cluster": "https://github.com/asimawdah/main_cluster",
}

ALLOWED_URL_PREFIXES = (
    "https://github.com/asimawdah/",
    "https://github.com/asimawdah",
    "https://python.org",
    "https://dart.dev",
    "https://developer.mozilla.org/",
    "https://typescriptlang.org",
    "https://www.gnu.org/",
    "https://flutter.dev",
    "https://react.dev",
    "https://fastapi.tiangolo.com",
    "https://flask.palletsprojects.com",
    "https://docker.com",
    "https://kubernetes.io",
    "https://git-scm.com",
    "https://mongodb.com",
    "https://redis.io",
    "https://sqlite.org",
    "https://nginx.org",
)

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def fail(message: str) -> None:
    print(f"README validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not README.exists():
        fail("README.md is missing")

    content = README.read_text(encoding="utf-8")

    for section in REQUIRED_SECTIONS:
        if section not in content:
            fail(f"missing section: {section}")

    if content.count("## Featured projects") != 1:
        fail("Featured projects section must appear exactly once")

    if content.count("## Current roadmap") != 1:
        fail("Current roadmap section must appear exactly once")

    for name, url in REQUIRED_PROJECT_LINKS.items():
        expected = f"[{name}]({url})"
        if expected not in content:
            fail(f"missing featured project link: {expected}")

    links = LINK_RE.findall(content)
    if len(links) < 10:
        fail("expected at least 10 markdown links")

    seen_labels: set[str] = set()
    for label, url in links:
        if not label.strip():
            fail("empty markdown link label")
        if not url.startswith("https://"):
            fail(f"non-https link found: {url}")
        if not any(url.startswith(prefix) for prefix in ALLOWED_URL_PREFIXES):
            fail(f"unexpected external link: {url}")
        if label in seen_labels and label in REQUIRED_PROJECT_LINKS:
            fail(f"duplicate featured project link label: {label}")
        seen_labels.add(label)

    if "skillicons.dev" in content:
        fail("profile should avoid heavy badge/icon sections and stay concise")

    if "Current roadmap" not in content or "Now | Next | Later" not in content:
        fail("roadmap table is missing or malformed")

    print("README validation passed")


if __name__ == "__main__":
    main()
