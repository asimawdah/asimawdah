# Profile maintenance guide

Use this checklist when updating the profile README.

## Goals

- Keep the profile focused on active projects and current engineering direction.
- Make important repositories easy to find from the featured projects table.
- Keep the roadmap short enough to update during regular project work.
- Avoid noisy badge sections that hide the main content on mobile.

## Update checklist

Before opening or merging a README change:

1. Confirm every featured project link points to an existing `asimawdah/*` repository or a trusted official technology site.
2. Keep project descriptions short and visitor-focused.
3. Update the `Current roadmap` table when active work changes.
4. Avoid adding private contact details or credentials.
5. Check the profile on a narrow/mobile viewport after editing long table text.
6. Run:

   ```bash
   python3 scripts/validate_profile_readme.py
   ```

## Featured project rules

Each featured project should include:

- repository link;
- one-line value proposition;
- current focus that reflects active work;
- no claims that depend on unreleased production features unless clearly framed as current focus.

The automated validator also protects the table contract:

- the table must use exactly three columns: `Project`, `What it is`, and `Current focus`;
- every project cell must be a Markdown link to an `asimawdah/*` repository;
- every row must have non-empty cells;
- project names cannot be duplicated;
- descriptions and current-focus cells must stay concise enough for mobile readability;
- placeholder content such as `TBD`, `TODO`, or `coming soon` is not allowed.

## Roadmap rules

Use three columns only:

- `Now`: active implementation and stabilization work;
- `Next`: near-term polish, docs, releases, or integration work;
- `Later`: broader platform or automation direction.

The roadmap should include at least two concise rows and no more than four rows. This keeps it easy to scan and prevents the profile from becoming a long backlog.

## Link and content safety

- Use HTTPS links only.
- Prefer GitHub repository links for project references.
- Avoid badge-heavy sections that slow scanning on mobile.
- Do not add phone numbers, credentials, private infrastructure details, or temporary contact links.
- Keep roadmap language current and practical instead of promising unreleased production status.
