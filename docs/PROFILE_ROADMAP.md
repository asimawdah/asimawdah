# Profile roadmap maintenance

This document keeps the GitHub profile README practical and easy to refresh.

## What the profile should communicate

- Who Asim is and what he builds.
- Which projects are currently active.
- Which repositories are useful starting points for visitors.
- What is being built now, next, and later.

## Featured project selection rules

Use the featured table for projects that are active, useful, or important to the public story.

A project is a strong candidate when it has at least one of these qualities:

- It represents a real product or app.
- It demonstrates a core skill such as Flutter, backend APIs, DevOps, or developer tooling.
- It has documentation, examples, or a clear README.
- It is part of a larger project family such as MahamKit.

Avoid adding every repository to the featured table. Use the repository map for broader grouping.

## Update checklist

Run this checklist before merging future profile updates:

1. Keep the README concise.
2. Make active projects obvious near the top.
3. Keep project descriptions factual and current.
4. Verify every repository link points to an existing repository.
5. Update the roadmap if priorities change.
6. Run:

```bash
node scripts/validate-profile-readme.mjs
```

## Roadmap format

Use three short groups:

- `Now`: active work currently receiving updates.
- `Next`: near-term improvements that support current projects.
- `Later`: larger polish, release, deployment, or public-demo goals.

This keeps the profile easy to scan and avoids a long backlog inside the README.
