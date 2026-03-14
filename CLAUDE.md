# Clarity Mirror — Claude Code Guide

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Running the Project](#running-the-project)
- [Architecture](#architecture)
  - [Core JS Data & Functions](#core-js-data--functions)
- [Design Principles](#design-principles)
- [Development Conventions](#development-conventions)
- [Deployment](#deployment)
- [Active Work](#active-work)
- [Related Documentation](#related-documentation)

---

## Project Overview

**Clarity Mirror** — A privacy-first tool that shows people what data brokers know about them and how advertisers use that data, framed as self-awareness rather than threat.

*"See what data brokers see when they look at you. Then choose who you actually are."*

Live prototype: https://claritymirror.vercel.app

## Tech Stack

- **Frontend:** Single self-contained HTML file (`index.html`) with inline CSS + JS. Zero dependencies, no build step.
- **Backend:** Python serverless function (`api/reflect.py`) on Vercel, calling OpenAI GPT-5-nano for LLM reflections.
- **Dependencies:** `openai>=1.0.0` (see `requirements.txt`)

**Planned (Phase 2+):** SQLite, Ollama, PyTorch + Flower (federated learning), SvelteKit

## Running the Project

```bash
# Frontend — works offline, no install
open index.html

# Backend (local dev) — requires .env with OPENAI_API_KEY
pip install -r requirements.txt
# The /api/reflect endpoint runs as a Vercel serverless function in production
```

## Architecture

`index.html` (~1227 lines) is the entire frontend:
- **Lines 8–666:** CSS design system using variables (`--ink`, `--paper`, `--accent`, `--calm`, `--caution`). Fonts: Cormorant Garamond (headings), DM Sans (body). Includes grain overlay and fadeUp/breathing animations.
- **Lines 668–776:** HTML — 3-step UI flow: select data sources → set intentions → generate analysis
- **Lines 777–1224:** JavaScript — all application logic including LLM reflection call

`api/reflect.py` — Vercel serverless function that:
1. Receives intentions, vulnerabilities, and broker names from the frontend
2. Loads the system prompt from `docs/system-prompt.md`
3. Calls OpenAI GPT-5-nano with `store=False` (zero data retention)
4. Returns a structured reflection (plain prose, 150–250 words)

### Core JS Data & Functions

| Symbol | Line | Purpose |
|---|---|---|
| `brokers[]` | ~927 | 10 major data brokers/platforms |
| `intentions[]` | ~940 | 6 personal intention types |
| `vulnerabilityProfiles[]` | ~982 | 6 vulnerability categories mapped to broker combinations |
| `attentionCategories[]` | ~1033 | 6 attention economy sectors |
| `getMatchingVulnerabilities()` | ~1042 | Filters profiles by selected brokers |
| `generateReflection()` | ~1052 | Calls `/api/reflect` for LLM-generated reflection |
| `generateMirror()` | ~1064 | Orchestrates analysis with loading animation + API call via `Promise.all` |
| `renderResults()` | ~1117 | Renders vulnerability cards, attention audit bars, and reflection panel |

## Design Principles

Non-negotiable — raise conflicts explicitly before proceeding:

- **Awareness, not anxiety** — language is "notice" and "pause," never "danger" or "warning"
- **Local-first, always** — user data stays on device; LLM receives only intentions + vulnerability labels, never raw broker data
- **Honest about limitations** — the profile is incomplete and sometimes wrong; say so
- **Non-judgmental** — vulnerability categories are not character flaws
- **Calm technology** — no urgency, no notifications, no feeds

## Development Conventions

- **No build tooling.** Do not introduce a build step, package manager, or bundler without a team decision.
- **Prefer editing `index.html`** over creating new frontend files.
- **Backend files** go in `api/` (Vercel serverless) or `src/` (local backend).
- **Never commit** API keys, `.env` files, broker response data, or personal data exports.
- `docs/system-prompt.md` requires theologian (Ryan) sign-off to modify.
- User-facing copy — including error messages and empty states — should follow the project's non-judgmental, calm tone.

## Deployment

Hosted on Vercel at https://claritymirror.vercel.app

- Auto-deploys from `main`
- `vercel.json` handles routing and SVG cache headers
- Serverless functions in `api/` (Python runtime)
- Environment variable: `OPENAI_API_KEY` (set in Vercel project settings, never in repo)

## Active Work

| Task | Status | Owner | Reference |
|---|---|---|---|
| LLM reflection integration | **Implemented** | Engineer + Theologian | `docs/LLM-INTEGRATION.md` |
| System prompt | **Finalized** | Theologian (Ryan) | `docs/system-prompt.md` |
| Persona-based simulation | Scoped, not started | PM + Theologian + Engineer | `PERSONAS.md` |
| Real broker data parsers | Not started | Engineer | `BROKER-CATALOG.md` |
| `docs/ETHICS.md` | Not started | Theologian | — |
| `docs/DATA-SCHEMA.md` | Not started | Engineer | — |

## Related Documentation

| File | Description | When to consult |
|---|---|---|
| `README.md` | Full project overview, architecture diagrams, roadmap | First read; any product or design decision |
| `ROLES.md` | Team roles, 30-day critical path, decision ownership | Before changes affecting copy, ethics, or team scope |
| `PERSONAS.md` | Persona simulation scope and definitions | Starting persona feature work |
| `PRIVACY-MODEL.md` | Privacy guarantees and threat model | Any architectural decision involving data flow |
| `BROKER-CATALOG.md` | Data broker reference (access methods, formats) | Building parsers or adding broker support |
| `CONTRIBUTING.md` | Contribution guidelines by skill area | Onboarding new contributors |
| `SUMMARY.md` | Project summary with mermaid architecture diagrams | Quick visual overview of system design |
| `docs/LLM-INTEGRATION.md` | Full LLM integration guide (API, privacy, testing) | Modifying reflection pipeline or `api/reflect.py` |
| `docs/system-prompt.md` | Finalized LLM system prompt | Reviewing or revising reflection output quality |
| `docs/SYSTEM-PROMPT-BRIEF.md` | Theologian's brief for system prompt authoring | Understanding the ethical rationale behind the prompt |
