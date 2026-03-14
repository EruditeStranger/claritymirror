# Clarity Mirror — Team Roles & Operating Guide

This document describes how each team member contributes to building Clarity Mirror from prototype to product. It includes a shared timeline, role definitions, and the operating agreements that keep the team aligned.

---

## First 30 Days — Critical Path

Before diving into individual roles, here's how the workstreams converge. Dependencies flow left to right — if something on the left slips, everything to its right is affected.

```
Week 1–2                    Week 3–4                     Week 5–6
────────                    ────────                     ────────

PM: User interviews (5–10)  PM: Define Phase 2 scope     PM: Write specs for
    Identify day-one value       based on interviews           broker parsers
    experience                   Lock "zero data" UX          Create GitHub milestones
         │                            │
         │                            ▼
         │                  Engineer: Build Google &      Engineer: Build Acxiom &
         │                      Meta export parsers           Experian parsers
         │                      + test harness                Replace hardcoded
         │                                                    profiles in index.html
         │                            │
         ▼                            ▼
Theologian: Audit current    Theologian: Deliver          Theologian: Co-author
    reflection prompts           vocabulary guide             LLM system prompt
    Review identity claim        Write reflection             draft with Engineer
                                 library (v1)
                                      │
DevOps: Package/distro            DevOps: Local backend    DevOps: IPC bridge
    research & decision               scaffold (Python         between frontend
    Fix repo structure                 + SQLite)               and backend
    Branch protection
```

The most important dependency: the PM's user interviews in weeks 1–2 determine what Phase 2 actually contains. Nobody should lock scope until those conversations happen.

---

## Product Manager

**Your north star:** Keep the team building toward a tool that genuinely helps people, not one that just looks good in a demo. This project sits at the intersection of privacy, psychology, and mindful technology — your job is to hold that vision and translate it into a prioritized, realistic roadmap.

### The single most important question you need to answer

What does the product do on day one, before any broker data arrives?

CCPA requests take 1–45 days. If someone downloads Clarity Mirror and can't get real value for a month, they won't come back. You need to decide — before anything else gets built — what the immediate-value experience looks like. The two most likely answers are: lean hard into Google and Meta data exports (which return in minutes to hours and contain rich ad targeting data), or design a meaningful self-assessment experience that provides value even with zero external data. This decision shapes everything the engineer builds first.

### Immediate priorities

**Conduct 5–10 user interviews before locking Phase 2 scope.** Talk to people who have some awareness of data privacy but haven't used tools like DeleteMe or Optery. Understand what they expect, what would keep them engaged during the waiting period, and whether the "mindfulness" framing resonates or feels abstract. Document findings in a shared doc the whole team reads.

**Define Phase 2 scope based on what you learn.** The README has a Phase 1–5 roadmap. Translate Phase 2 into a GitHub milestone with issues, owners, and acceptance criteria. Be specific about which brokers to support first, what a minimum viable parser looks like, and how to handle the CCPA wait time in the UX.

**Write user stories for the onboarding flow.** Currently the app asks users to self-select brokers from a grid. Map out the ideal first-time journey: how does someone go from "I heard about this" to "I have real insights about my data profile"? Pay special attention to the transition from simulated data to real data — that handoff needs to feel seamless, not jarring.

**Establish a feedback channel.** Set up GitHub Discussions or a simple form linked from the app. Identify the most common points of confusion from early users of the live prototype.

### Ongoing responsibilities

- Triage and prioritize GitHub issues
- Write clear specs before the engineer starts building — acceptance criteria, edge cases, open questions
- Decide what gets cut when scope creeps
- Protect the design principles in `README.md` — especially "awareness, not anxiety" — when feature pressure pushes toward more alarming or sensationalist framing
- Coordinate with the theologian to ensure the human framing of data is right before the engineer builds the analysis engine
- Own the "first 30 days" timeline above and update it as reality diverges from the plan

### Key files to read first

- `README.md` — especially Design Principles and Roadmap
- `PRIVACY-MODEL.md` — the privacy commitments you're building around
- `BROKER-CATALOG.md` — what data sources are in scope

---

## DevOps Engineer

**Your north star:** Make it possible for a non-technical person to install and run Clarity Mirror on their own machine. The current app is a single HTML file — your job is to build the scaffolding that supports a local Python backend, a browser frontend, and eventually a local LLM, all packaged into something someone's parent could set up.

### The single most important question you need to answer

How do you package a local Python backend + browser frontend + optional local LLM into something a non-technical user can install?

This is the existential infrastructure question. The options are a CLI tool (lowest effort, smallest audience), an Electron or Tauri wrapper (wider audience, significant packaging complexity), a Docker container (clean isolation, requires Docker knowledge), or an installable Python package with a `clarity-mirror` command that launches a local server and opens a browser. Research the tradeoffs, make a recommendation to the team by end of week 2, and prototype the chosen approach.

### Immediate priorities

**Research and recommend a packaging/distribution strategy.** This comes before everything else because it determines how the engineer structures the backend. Write a one-page decision doc covering the options, tradeoffs, and your recommendation. Include how each option handles the Phase 3 requirement of bundling Ollama for local LLM inference.

**Fix the repo structure.**
- The README footer references `assets/icon.svg` — confirm this path exists or update it
- Add a `vercel.json` for explicit routing and cache control on SVG assets
- Confirm Vercel is deploying from the correct directory

**Set up branch protection and minimal CI.** Protect `main` — require PR review before merging. Add a GitHub Actions workflow that validates HTML and any JSON/YAML config files on PRs. Keep this lightweight; don't over-engineer CI for a four-person team.

**Scaffold the local backend.** Once the packaging decision is made, create the initial project structure for the Python backend: a FastAPI server running on `localhost`, SQLite database initialization, and the IPC bridge that the frontend will use to request and display analysis results.

### Phase 3+ planning

- Evaluate bundling Ollama alongside the app for non-technical users — this is a hard packaging problem and should be researched early even though it's not needed until Phase 3
- Design the federated learning server infrastructure (lightweight FastAPI server — the only cloud component in the entire architecture)
- Set up environment separation for when the federated layer is built

### Key files to read first

- `README.md` — Tech Stack section
- `PRIVACY-MODEL.md` — the constraint that raw data never leaves the device shapes every infrastructure decision

---

## Application Engineer

**Your north star:** Replace every hardcoded data structure in `index.html` with a real, local-first data pipeline. Everything the user sees should come from their actual data, processed on their own machine.

### The single most important question you need to answer

How do you build parsers that survive upstream format changes?

Google, Meta, Acxiom, and every other data source will change their export formats without warning. Your first task — before writing any parser — is to build a test harness that validates parser output against a known schema. When Google renames `ads_interests.json` to `ad_interests.json` (this kind of thing happens), the team needs to know immediately, not when a user files a bug report.

### Immediate priorities

**Build the parser test harness first** (`src/normalization/tests/`). Define the canonical output schema — what a correctly parsed broker response looks like as structured data. Write validation tests against this schema. Every parser you build afterward gets tested against it automatically.

**Build Google and Meta export parsers** (`src/normalization/`). These are the fastest data sources (minutes, not weeks) and likely the PM's answer to the "day-one value" question.
- Google Takeout: parse `ads_interests.json`, `ads_information.json`, and the activity records that reveal behavioral patterns
- Meta: parse `your_topics.json` and `ads_interests.json` from the data export
- Store parsed output in local SQLite using the unified schema

**Build the CCPA request generator** (`src/retrieval/`). Start with Acxiom and Experian — the two highest-value traditional brokers. For each, implement the request mechanism (email template, portal link, or API call — see `BROKER-CATALOG.md`). Output a structured record of pending requests with expected response dates.

**Define the unified normalization schema** (`docs/DATA-SCHEMA.md`). The README sketches this (e.g., `clarity.financial.income_bracket` mapping from multiple broker-specific field names). Formalize it. This schema is the contract between the parsing layer and the analysis layer — it needs to be stable and well-documented.

**Replace the hardcoded vulnerability profiles in `index.html`** with a rule engine (`src/analysis/`) that reads from the normalized schema and generates vulnerability categories, exposure levels, supporting evidence from real data, and intention conflict detection.

**Handle the unhappy paths.** Broker responses are messy by design. Build explicit handling for: PDFs instead of structured data (use `pdfplumber` or similar to extract what you can), partial or incomplete responses, outright rejections (and what to tell the user), and unexpected formats that don't match any known parser.

### Phase 3 (Analysis Engine)

- Co-author the LLM system prompt with the theologian — this is a shared deliverable, not a handoff
- Integrate Ollama for personalized reflection generation
- Implement IAB Content Taxonomy mapping
- Build the Persuasion Weather Report

### Architecture notes

- Everything runs locally. No user data goes to a server.
- The frontend and Python backend communicate via a local HTTP server (FastAPI on `localhost`) — coordinate with DevOps on the IPC approach
- Write tests for all parsing logic, and expect to maintain them as upstream formats change

### Key files to read first

- `README.md` — Architecture section
- `BROKER-CATALOG.md` — primary reference for data sources and access methods
- `index.html` — search for `vulnerabilityProfiles` and `attentionCategories` to see the hardcoded structures you're replacing

---

## Theologian

**Your north star:** This project makes a claim that seeing yourself through the lens of a data profile can be liberating rather than reductive. That claim needs to be rigorously examined, carefully framed, and honestly communicated. Your role is not peripheral — the product's entire thesis rests on philosophical and ethical ground that you are uniquely equipped to evaluate and strengthen.

### The single most important question you need to answer

Does knowing your vulnerability profile make you more free, or does it create a new kind of self-surveillance?

Every contemplative tradition distinguishes between self-knowledge that liberates and self-knowledge that becomes its own trap — the Desert Fathers warned against scrupulosity, Buddhist teachers distinguish between mindfulness and metacognitive attachment. Clarity Mirror risks becoming the thing it critiques: another system demanding your attention, another voice telling you what you are. Your job is to help the team navigate that tension honestly, and to build it into the product's design at every level.

### Immediate priorities

**Audit the current reflection prompts in `index.html`.** The prototype contains hand-written reflections for each vulnerability category (Financial Anxiety, Health Vulnerability, Status Comparison, etc.). Read each one critically and produce a short document with your assessment and suggested rewrites. Evaluate whether the framing respects human dignity and agency, whether it avoids shaming or pathologizing normal behavior, whether it's honest about the limits of what the data actually tells us, and whether the "pause and notice" language aligns with contemplative traditions that have thought carefully about attention and desire.

**Develop a vocabulary guide.** The product uses words like "vulnerability," "exploitation," "manipulation," "anxiety," and "impulse." These are loaded terms. Write a brief style guide — informed by theological and philosophical anthropology — that defines how the project should and shouldn't use this language. The goal is precision and compassion, not clinical detachment or moral alarm. This guide will be used by every team member who writes user-facing copy, including the engineer writing error messages and empty states.

**Examine the identity claim.** The tagline is "See what data brokers see. Then choose who you actually are." This implies there is a "who you actually are" that is distinct from and more authoritative than the data profile. Write a brief reflection (1–2 pages) on what that claim implies, where it holds up, and where it needs nuance. This directly informs how the product talks about itself and will shape the README, onboarding copy, and marketing language.

### The shared deliverable with the Engineer

In Phase 3, the local LLM generates personalized reflections. The system prompt that governs this generation is the single most important piece of text in the product — it determines the voice, ethics, and depth of every reflection a user sees. **You and the engineer co-author this prompt together.** Your vocabulary guide and ethical framing need to be embedded directly in it, not handed off as a document for the engineer to interpret. Plan to pair on this starting around week 5–6.

### Ongoing responsibilities

**Review all user-facing copy before it ships.** This includes reflection prompts, but also error messages, empty states, loading messages, and failure states. When a broker rejects a CCPA request, the message the user sees is as much a "what it says to users" moment as the reflection prompts. Work with the engineer to establish a shared set of principles for how the app communicates failure, uncertainty, and incompleteness.

**Consult on the Intention feature.** The app invites users to set intentions ("spend more mindfully," "reduce anxiety-driven decisions"). This is an invitation to a kind of examined life. Think about what that invitation should feel like, what it should not claim to do, and how it avoids becoming prescriptive or paternalistic.

**Engage the federated learning ethics questions early.** Phase 4 introduces community intelligence — the system learns which reflections help people most. This raises real questions: Who defines "helped"? What counts as a reflection being effective? Is there a risk that optimizing reflections for engagement subtly distorts the project's contemplative values? Is "most people found this helpful" an appropriate metric for something that's supposed to be personal and sometimes uncomfortable? Flag these concerns before they're baked into architecture.

**Create and maintain `docs/ETHICS.md`.** This is a living document capturing your thinking on the project's ethical foundations, tensions, and unresolved questions. It will be valuable for contributors, for users who want to understand the project's values, and for any future grant or partnership conversations.

### Key files to read first

- `README.md` — especially Design Principles and the "Why Clarity Mirror?" section
- `PRIVACY-MODEL.md` — understanding the technical privacy model helps you engage with the ethical one
- `index.html` — search for `reflection` in the JavaScript to find the prompts you'll review

---

## How the Team Works Together

### Decision Ownership

| Decision | Owner | Consulted |
|---|---|---|
| What to build next | PM | All |
| Phase 2 scope and priorities | PM | All |
| Packaging and distribution approach | DevOps | Engineer, PM |
| How features get built | Engineer | DevOps |
| What the product says to users (all copy) | Theologian | PM, Engineer |
| Error states, empty states, failure messages | Engineer | Theologian |
| Privacy architecture | Engineer + DevOps | All |
| Ethical framing and reflection content | Theologian | PM |
| LLM system prompt for reflections | Engineer + Theologian (co-owned) | PM |
| Roadmap and timeline | PM | All |

### Shared Constraint

The design principles in `README.md` are durable commitments, not suggestions:

- **Awareness, not anxiety**
- **Local-first, always**
- **Honest about limitations**
- **Non-judgmental**
- **Calm technology**

These are not negotiable on a feature-by-feature basis. Any proposed feature that conflicts with them requires an explicit team discussion before proceeding.

That said, the principles themselves may evolve as the team learns from real users. The PM has the authority to propose revisiting a principle, but the decision to change one requires consensus from the full team and a documented rationale in `docs/ETHICS.md`.

### Communication Norms

- **Async by default.** Use GitHub issues and PRs for decisions that need a record. Use a shared chat (Slack, Discord) for quick coordination.
- **Weekly sync.** One 30-minute meeting per week to review the critical path, surface blockers, and adjust priorities. The PM runs this.
- **Pair when it matters.** The theologian and engineer should pair on the LLM system prompt. The PM and theologian should pair on onboarding copy. The engineer and DevOps should pair on the IPC bridge design. Don't formalize pairing beyond these known intersections.

---

## Appendix: Key Files Reference

| File | What it contains | Who should read it |
|---|---|---|
| `README.md` | Project vision, architecture, roadmap, design principles | Everyone |
| `PRIVACY-MODEL.md` | Privacy guarantees and threat model | Everyone |
| `BROKER-CATALOG.md` | Known data brokers, access methods, response formats | PM, Engineer |
| `CONTRIBUTING.md` | Contribution guidelines | Everyone |
| `index.html` | Current prototype with hardcoded data | Engineer, Theologian |
| `docs/ETHICS.md` (to be created) | Ethical foundations and open questions | Everyone |
| `docs/DATA-SCHEMA.md` (to be created) | Unified normalization schema | Engineer, DevOps |