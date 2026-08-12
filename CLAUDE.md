# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Documentation source for the **Adobe Firefly Services — Photoshop API** developer site. There is no application code: the repo holds Markdown content, OpenAPI specs, and assets that are built and deployed by Adobe's shared **ADP devsite** tooling (`github:AdobeDocs/adp-devsite-utils`, a Gatsby-based platform). The published site lives under the path prefix `/firefly-services/docs/photoshop/` (see `src/pages/config.md`).

## Repository layout

- `src/pages/` — all site content as Markdown (`.md`). Every page starts with YAML frontmatter (`title`, `description`, `keywords`, etc.). Folders map to URL routes; each section has an `index.md`.
  - `getting-started/`, `guides/`, `api/` are the three top-level content areas.
  - The site has two API versions: **v2** (current, recommended) and **v1** (deprecated/EOL). Much of `guides/photoshop-v2/v1-to-v2/` is v1→v2 migration content.
- `src/pages/config.md` — site navigation/TOC, header buttons, and `pathPrefix`. Edit this to change the nav tree or add/remove pages from the sidebar.
- `static/` — OpenAPI JSON specs: `photoshop_api.json` (v1) and `photoshopv2-api.json` (v2). These render as the API Reference.
- `redirects.json` — URL redirect map for the deployed site.
- `src/pages/adp-site-metadata.json`, `contributors.json` — auto-generated; do not hand-edit.
- `.cursor/` is a symlink to a shared `ff-services-docs/.cursor` directory containing rules and skills (see below).

## Commands

All build/lint tooling runs through `adp-devsite-utils` via `npx` (no local install). Node `^24.11.0`.

- `npm run dev` — run the local dev server.
- `npm run lint` — lint Markdown content (`src/pages/`) verbose; `npm run lint:errorOnly` for errors only. This is what CI runs on PRs touching `src/pages/`.
- `npm run link:checkAllLinks` — validate internal + external links; `npm run link:externalLinkOnly` for external only.
- `npm run buildNavigation` / `buildRedirections` / `buildSiteMetadata` / `buildContributors` — regenerate auto-generated artifacts.
- `npm run redirectCheck:stage` / `redirectCheck:prod` — verify redirects against an environment.

There is no test suite. Validation = lint + link checking. CI workflows: `lint.yml` (runs `runLint` when `src/pages/` changes and comments the report on the PR), `deploy.yml`, `stage.yml`, `build-auto-generated-files.yml`.

## OpenAPI specs (`static/*.json`)

When editing or reviewing the JSON specs, use the agent skills under `.cursor/skills/` rather than ad-hoc edits:

- **`/api-eval`** — audit/findings only, no edits.
- **`/api-review`** — produce description catalog tables for manual review, no edits.
- **`/api-fix`** — apply Redocly lint + structural fixes (edits the file).

Resolve the spec path explicitly (`static/photoshop_api.json` or `static/photoshopv2-api.json`); there is **no** `petstore.json` default. Key structural rules (`.cursor/rules/api-ref-*.mdc`):

- Top-level key order: `openapi`, `info`, `servers`, `security`, `tags`, `paths`, `components`.
- HTTP response status `description` → Title Case, **no** trailing period. All other descriptions → full sentences **with** periods.
- All `$ref`s must resolve; no duplicate schema names.

## Conventions enforced by Cursor rules

These `.cursor/rules/*.mdc` are `alwaysApply: true` and apply to Claude too. They are the single source of truth and imported directly below (don't paraphrase them here — edit the rule files):

- **Commit messages** — subject, body wrapping, and the 📖 / ✏️ / 🆕 / 🗑️ markers:

  @.cursor/rules/commit-rules.mdc

- **Pull requests** — Jira derivation, `{type}/{JIRA-ID}- {desc}` titles, required `# Summary` / `# Changes` / `# Context` body sections:

  @.cursor/rules/pr-rules.mdc

**New Cursor rules** go in `.cursor/rules/`, kebab-case, `.mdc` extension, with `description`/`globs`/`alwaysApply` frontmatter.

## Notes

- `linter-report.txt` is a generated lint artifact (gitignored) — don't edit.
- `.cursor/rules/security-global/` and `security-lang/` are vendored security rule sets tracked by `manifest.json`; treat as managed/external.
