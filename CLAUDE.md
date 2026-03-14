# Clarity Mirror — Claude Code Guide

## What this project is

Clarity Mirror is a privacy-first tool that shows users the psychological and behavioral profiles that data brokers and ad platforms have built about them, framed as self-awareness rather than threat. The tagline: *"See what data brokers see when they look at you. Then choose who you actually are."*

Live prototype: https://claritymirror.vercel.app

---

## Current state

The entire working app is a single file: `index.html`. No build step, no dependencies, no server. It runs in the browser.

All data is currently simulated. The vulnerability profiles, attention percentages, and reflections are hardcoded. The next major work is:
1. Persona-based simulation (see `PERSONAS.md`)
2. LLM integration for the reflection panel (see `docs/LLM-INTEGRATION.md`)
3. Real data ingestion via CCPA requests and platform export parsers (Phase 2, not yet started)

---

## Repo structure

```
claritymirror/
├── index.html                  # The entire frontend app
├── banner.svg                  # README banner (also rendered on the live site)
├── icon.svg                    # App icon / favicon
├── logo.svg                    # Logo mark
├── vercel.json                 # Vercel deployment config
├── CLAUDE.md                   # This file
├── README.md                   # Project overview, architecture, roadmap
├── ROLES.md                    # Team roles and operating guide
├── PERSONAS.md                 # Persona simulation scope
├── CONTRIBUTING.md             # Contribution guidelines
├── BROKER-CATALOG.md           # Data broker reference
├── PRIVACY-MODEL.md            # Privacy guarantees and threat model
└── docs/
    ├── LLM-INTEGRATION.md      # How to integrate the reflection API
    └── SYSTEM-PROMPT-BRIEF.md  # Theologian's brief for the LLM system prompt
```

Planned but not yet created:
```
├── api/
│   └── reflect.py              # Vercel serverless function for LLM reflection
├── src/
│   ├── retrieval/              # CCPA request automation
│   ├── normalization/          # Broker export parsers + unified schema
│   └── analysis/              # Rule engine replacing hardcoded profiles
└── docs/
    ├── system-prompt.md        # Finalized LLM system prompt (theologian-approved)
    ├── ETHICS.md               # Ethical foundations (theologian maintains)
    └── DATA-SCHEMA.md          # Unified normalization schema
```

---

## Key files to understand before editing

**`index.html`** — Read this before touching anything. The important JavaScript sections:
- `brokers` array (line ~629) — data broker definitions
- `intentions` array (line ~642) — hardcoded intention options
- `vulnerabilityProfiles` array (line ~684) — the 6 hardcoded vulnerability profiles. Each has `category`, `level`, `brokers[]`, `whatTheySee`, `reflection`, and `intentionConflict`.
- `attentionCategories` array (line ~735) — the 6 attention categories with base percentages
- `generateMirror()` (line ~754) — handles button click, loading state, and triggers `renderResults()`
- `renderResults()` (line ~788) — renders vulnerability cards, attention bars, and the reflection panel. **The reflection panel block (line ~851) is what LLM integration replaces.**

**`PRIVACY-MODEL.md`** — Read before making any architectural decision. The core constraint: raw broker data never leaves the device. LLM integration is a deliberate, documented exception for intention data only — not broker data.

**`ROLES.md`** — Understand who owns what before making changes that affect copy, system prompt, or ethical framing.

---

## Design principles — non-negotiable

These are in `README.md` and apply to every code and content decision:

- **Awareness, not anxiety** — language is "notice" and "pause," never "danger" or "warning"
- **Local-first, always** — user data stays on device; LLM exception is intentions only, disclosed to user
- **Honest about limitations** — the profile is incomplete and sometimes wrong; say so
- **Non-judgmental** — vulnerability categories are not character flaws
- **Calm technology** — no urgency, no notifications, no feeds

If a proposed change conflicts with these, raise it explicitly before proceeding.

---

## Development conventions

### No build tooling (yet)
The prototype has zero dependencies. Do not introduce a build step, package manager, or bundler without a team decision. If adding a `src/` Python backend, use standard Python conventions (`requirements.txt`, `venv`).

### File editing
- Prefer editing `index.html` directly over creating new files
- New backend files go in `api/` (Vercel serverless) or `src/` (local backend)
- Documentation goes in `docs/`

### Sensitive content
- Never commit API keys. Use Vercel environment variables for `ANTHROPIC_API_KEY`.
- Never commit broker response data, personal data exports, or `.env` files.
- `docs/system-prompt.md` (once created) requires theologian sign-off to modify.

### Copy and language
- Any user-facing text — including error messages, loading states, and empty states — should be reviewed against the vocabulary guide (once the theologian writes it)
- The theologian co-owns the LLM system prompt. Do not modify `docs/system-prompt.md` without their review.

---

## Deployment

Hosted on Vercel at https://claritymirror.vercel.app

- Deploys automatically from `main`
- Root directory: `claritymirror/` (the inner folder — set in Vercel project settings)
- `vercel.json` handles routing and SVG cache headers
- Future serverless functions go in `api/` within the `claritymirror/` directory

---

## Active work

| Task | Status | Owner | Reference |
|---|---|---|---|
| Persona-based simulation | Scoped, not started | PM + Theologian + Engineer | `PERSONAS.md` |
| LLM reflection integration | Scoped, not started | Engineer + Theologian | `docs/LLM-INTEGRATION.md` |
| System prompt draft | In progress | Theologian (Ryan) | `docs/SYSTEM-PROMPT-BRIEF.md` |
| Real broker data parsers | Not started | Engineer | `BROKER-CATALOG.md` |
| `docs/ETHICS.md` | Not started | Theologian | — |
| `docs/DATA-SCHEMA.md` | Not started | Engineer | — |

---

## Team

Four people. See `ROLES.md` for full role definitions and the 30-day critical path.

| Role | Responsibilities |
|---|---|
| Product Manager | Roadmap, specs, user interviews, GitHub milestones |
| Application Engineer | Frontend, backend, parsers, LLM integration, some DevOps |
| DevOps Engineer | Packaging, CI, Vercel, local backend scaffold |
| Theologian (Ryan) | System prompt, reflection copy, vocabulary guide, `ETHICS.md` |
