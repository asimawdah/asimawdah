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

REQUIRED_PROFILE_METADATA_KEYS = [
    "location",
    "education",
    "focus",
    "status",
    "languages",
]

SENSITIVE_METADATA_KEYS = {
    "address",
    "api_key",
    "apikey",
    "email",
    "password",
    "phone",
    "secret",
    "token",
}

REQUIRED_PROJECT_LINKS = {
    "MahamKit": "https://github.com/asimawdah/maham-app",
    "maham-api": "https://github.com/asimawdah/maham-api",
    "PyPrivate": "https://github.com/asimawdah/passgen",
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

FORBIDDEN_PLACEHOLDERS = (
    "todo",
    "tbd",
    "coming soon",
    "lorem ipsum",
    "your project",
    "example.com",
)

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TABLE_SEPARATOR_RE = re.compile(r"^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$")
YAML_BLOCK_RE = re.compile(r"```yaml\n(?P<body>.*?)\n```", re.DOTALL)


def fail(message: str) -> None:
    print(f"README validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalize_cell(value: str) -> str:
    return value.strip().replace("`", "")


def table_cells(row: str) -> list[str]:
    if not row.startswith("|"):
        fail(f"malformed markdown table row: {row}")
    return [normalize_cell(cell) for cell in row.strip().strip("|").split("|")]


def extract_table_after_heading(content: str, heading: str) -> list[str]:
    lines = content.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        fail(f"missing heading: {heading}")

    table: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("## ") and table:
            break
        if line.startswith("|"):
            table.append(line)
        elif table and line.strip():
            break

    if len(table) < 3:
        fail(f"{heading} table must include a header, separator, and at least one data row")
    if not TABLE_SEPARATOR_RE.match(table[1]):
        fail(f"{heading} table separator is malformed")
    return table


def validate_table_shape(table: list[str], expected_header: list[str], heading: str) -> list[list[str]]:
    header = table_cells(table[0])
    if header != expected_header:
        fail(f"{heading} table header must be: {' | '.join(expected_header)}")

    rows = [table_cells(row) for row in table[2:]]
    for row in rows:
        if len(row) != len(expected_header):
            fail(f"{heading} row has {len(row)} cells, expected {len(expected_header)}: {row}")
        if any(not cell for cell in row):
            fail(f"{heading} row contains an empty cell: {row}")
    return rows


def parse_inline_list(value: str, key: str) -> list[str]:
    if not (value.startswith("[") and value.endswith("]")):
        fail(f"profile metadata `{key}` must use an inline list")
    items = [item.strip() for item in value[1:-1].split(",")]
    if not items or any(not item for item in items):
        fail(f"profile metadata `{key}` contains an empty list item")
    if len(items) != len(set(items)):
        fail(f"profile metadata `{key}` contains duplicate items")
    return items


def validate_profile_metadata(content: str) -> None:
    blocks = YAML_BLOCK_RE.findall(content)
    if len(blocks) != 1:
        fail("profile README must contain exactly one yaml metadata block")

    metadata: dict[str, str] = {}
    for line in blocks[0].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"profile metadata line must use `key: value`: {line}")
        key, value = [part.strip() for part in line.split(":", 1)]
        if not key or not value:
            fail(f"profile metadata line must include a non-empty key and value: {line}")
        if key in metadata:
            fail(f"duplicate profile metadata key: {key}")
        if key in SENSITIVE_METADATA_KEYS:
            fail(f"sensitive profile metadata key is not allowed: {key}")
        metadata[key] = value

    expected_keys = set(REQUIRED_PROFILE_METADATA_KEYS)
    actual_keys = set(metadata)
    missing = sorted(expected_keys - actual_keys)
    if missing:
        fail(f"missing profile metadata keys: {', '.join(missing)}")
    unknown = sorted(actual_keys - expected_keys)
    if unknown:
        fail(f"unexpected profile metadata keys: {', '.join(unknown)}")

    if "Yemen" not in metadata["location"]:
        fail("profile metadata location should stay general and include Yemen")
    if len(metadata["status"]) > 110:
        fail("profile metadata status should stay concise")

    focus = parse_inline_list(metadata["focus"], "focus")
    if not 3 <= len(focus) <= 7:
        fail("profile metadata focus should include three to seven concise items")
    if any(len(item) > 24 for item in focus):
        fail("profile metadata focus items should stay concise")

    languages = parse_inline_list(metadata["languages"], "languages")
    if set(languages) != {"English", "العربية"}:
        fail("profile metadata languages must be exactly English and العربية")


def validate_featured_projects(content: str) -> None:
    table = extract_table_after_heading(content, "## Featured projects")
    rows = validate_table_shape(table, ["Project", "What it is", "Current focus"], "Featured projects")

    if len(rows) < 5:
        fail("Featured projects table should include at least five active projects")

    project_names: set[str] = set()
    project_urls: set[str] = set()
    for project, description, current_focus in rows:
        link_match = LINK_RE.fullmatch(project)
        if not link_match:
            fail(f"featured project must be a markdown link: {project}")

        project_name, project_url = link_match.groups()
        if project_name in project_names:
            fail(f"duplicate featured project row: {project_name}")
        project_names.add(project_name)

        if project_url in project_urls:
            fail(f"duplicate featured project URL: {project_url}")
        project_urls.add(project_url)

        if not project_url.startswith("https://github.com/asimawdah/"):
            fail(f"featured project must link to an asimawdah repository: {project_url}")
        if len(description) > 180:
            fail(f"featured project description is too long: {project_name}")
        if len(current_focus) > 180:
            fail(f"featured project current focus is too long: {project_name}")

    missing_projects = sorted(set(REQUIRED_PROJECT_LINKS) - project_names)
    if missing_projects:
        fail(f"missing required featured projects: {', '.join(missing_projects)}")

    for required_name, required_url in REQUIRED_PROJECT_LINKS.items():
        if required_url not in project_urls:
            fail(f"missing required featured project URL for {required_name}: {required_url}")


def validate_roadmap(content: str) -> None:
    table = extract_table_after_heading(content, "## Current roadmap")
    rows = validate_table_shape(table, ["Now", "Next", "Later"], "Current roadmap")

    if len(rows) < 2:
        fail("Current roadmap should include at least two concise rows")
    if len(rows) > 4:
        fail("Current roadmap should stay concise with no more than four rows")

    for row in rows:
        for cell in row:
            if len(cell) > 170:
                fail(f"roadmap cell is too long: {cell}")


def validate_placeholder_content(content: str) -> None:
    lowered = content.lower()
    for placeholder in FORBIDDEN_PLACEHOLDERS:
        if placeholder in lowered:
            fail(f"placeholder content found: {placeholder}")


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

    validate_profile_metadata(content)
    validate_featured_projects(content)
    validate_roadmap(content)
    validate_placeholder_content(content)

    print("README validation passed")


if __name__ == "__main__":
    main()
