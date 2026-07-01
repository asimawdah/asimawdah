#!/usr/bin/env python3
"""Regression tests for the profile README validator."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_profile_readme.py"
README_PATH = ROOT / "README.md"

spec = importlib.util.spec_from_file_location("validate_profile_readme", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


@contextmanager
def patched_readme(content: str) -> Iterator[None]:
    original_readme = validator.README
    with tempfile.TemporaryDirectory() as tmpdir:
        readme_path = Path(tmpdir) / "README.md"
        readme_path.write_text(content, encoding="utf-8")
        validator.README = readme_path
        try:
            yield
        finally:
            validator.README = original_readme


class ProfileReadmeValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.valid_content = README_PATH.read_text(encoding="utf-8")

    def assert_validation_fails(self, content: str) -> None:
        with patched_readme(content):
            with self.assertRaises(SystemExit) as context:
                validator.main()
        self.assertEqual(context.exception.code, 1)

    def test_current_readme_matches_contract(self) -> None:
        with patched_readme(self.valid_content):
            validator.main()

    def test_rejects_duplicate_featured_project_names(self) -> None:
        duplicate_row = (
            "| [MahamKit](https://github.com/asimawdah/maham-app) | "
            "Duplicate project row. | Duplicate focus. |"
        )
        mutated = self.valid_content.replace(
            "## Current roadmap",
            f"{duplicate_row}\n\n## Current roadmap",
            1,
        )

        self.assert_validation_fails(mutated)

    def test_rejects_duplicate_featured_project_urls(self) -> None:
        duplicate_url_row = (
            "| [MahamKit mobile](https://github.com/asimawdah/maham-app) | "
            "Duplicate repository row. | Duplicate focus. |"
        )
        mutated = self.valid_content.replace(
            "## Current roadmap",
            f"{duplicate_url_row}\n\n## Current roadmap",
            1,
        )

        self.assert_validation_fails(mutated)

    def test_rejects_missing_required_featured_project(self) -> None:
        mutated = self.valid_content.replace(
            "[PyPrivate](https://github.com/asimawdah/passgen)",
            "[Passgen](https://github.com/asimawdah/passgen)",
            1,
        )

        self.assert_validation_fails(mutated)

    def test_rejects_untrusted_external_links(self) -> None:
        mutated = self.valid_content.replace(
            "[Python](https://python.org)",
            "[Python](https://example.org)",
            1,
        )

        self.assert_validation_fails(mutated)

    def test_rejects_overlong_roadmap_cells(self) -> None:
        overlong_cell = "Improve " + "release validation " * 12
        mutated = self.valid_content.replace(
            "Improve product websites, screenshots, onboarding, and pricing/feature explanations.",
            overlong_cell,
            1,
        )

        self.assert_validation_fails(mutated)


if __name__ == "__main__":
    unittest.main()
