# Team Roles — Clarity Mirror

This document describes how each team member can contribute meaningfully to building out Clarity Mirror from its current prototype state into a fully functional product.

---

## Product Manager

**Your north star:** Keep the team building toward a tool that genuinely helps people, not one that just looks good. This project sits at the intersection of privacy, psychology, and mindful technology — the PM role is to hold that vision and translate it into a prioritized, realistic roadmap.

### Immediate priorities

- **Define Phase 2 scope.** The prototype is live at [claritymirror.vercel.app](https://claritymirror.vercel.app). Decide what "real data" means for the first real release — which brokers to support first, what a minimum viable parser looks like, and how to handle the 1–45 day wait time for CCPA responses in the user experience.
- **Write user stories for the onboarding flow.** Currently the app asks users to self-report which brokers have their data. That's a friction point. Map out the ideal first-time user journey: how does someone go from "I heard about this" to "I have real insights about my data profile"?
- **Establish a feedback loop.** Set up a simple channel (GitHub Discussions, a form, or a Discord) to collect feedback from early users of the live prototype. Identify the most common points of confusion.
- **Own the roadmap document.** The README has a Phase 1–5 roadmap. Translate each phase into a GitHub milestone with issues, owners, and acceptance criteria.

### Ongoing responsibilities

- Triage and prioritize GitHub issues
- Write clear specs before the engineer starts building (acceptance criteria, edge cases, open questions)
- Decide what gets cut when scope creeps
- Protect the design principles in `README.md` — especially "awareness, not anxiety" — when feature pressure pushes toward more alarming or sensationalist framing
- Coordinate CCPA/GDPR research with the theologian (see below) to ensure the human framing of data is right before the engineer builds the analysis engine

### Key files to read first
- `README.md` — especially the Design Principles and Roadmap sections
- `PRIVACY-MODEL.md` — understand the privacy commitments you're building the product around
- `BROKER-CATALOG.md` — understand what data sources are in scope

---

## DevOps Engineer

**Your north star:** Make deployment, infrastructure, and development workflow invisible to the rest of the team so they can ship without friction. The current app is a single HTML file on Vercel — your job is to build the scaffolding that supports what comes next without over-engineering for phases that haven't started yet.

### Immediate priorities

- **Stabilize the Vercel deployment.**
  - The live site is at [claritymirror.vercel.app](https://claritymirror.vercel.app). Confirm it is deploying from the correct directory (`claritymirror/` subdirectory, not the repo root).
  - Add a `vercel.json` for explicit routing and cache control on the SVG assets.
  - Set up automatic deployments on push to `main`.

- **Set up branch protection and CI basics.**
  - Protect `main` — require PR review before merging.
  - Add a GitHub Actions workflow that at minimum lints the HTML and validates any future JSON/YAML config files on every PR.

- **Fix the README icon path.** The footer of `README.md` still references `assets/icon.svg` (line 269) — that path doesn't exist. Either move the SVGs into an `assets/` folder or update the path to match the actual file location.

- **Plan the local-first architecture for Phase 2.** When the Python data retrieval layer arrives, it runs on the user's machine, not on a server. You need to think about:
  - Packaging and distribution (a CLI tool? a local Electron/Tauri wrapper? an installable Python package?)
  - How the locally-running Python backend will communicate with the browser frontend
  - SQLite database location and migration strategy

### Phase 3+ planning

- Evaluate how to bundle Ollama (local LLM) alongside the app for non-technical users
- Design the optional federated learning server infrastructure (likely a lightweight Python/FastAPI server — this is the only cloud component in the whole architecture)
- Set up environment separation (local dev vs. staging vs. production) for when the federated layer is built

### Key files to read first
- `README.md` — Tech Stack section for planned technologies
- `PRIVACY-MODEL.md` — the constraint that raw data never leaves the device shapes every infrastructure decision you make

---

## Application Engineer

**Your north star:** Build the real data pipeline that replaces the simulated vulnerability profiles in the current prototype. Everything currently hardcoded in `index.html` needs to become a real, local-first system.

### Immediate priorities (Phase 2)

- **Build the CCPA request generator** (`src/retrieval/`).
  - Start with the top 3 brokers: Acxiom, Experian, and Google.
  - For each, implement the request mechanism (email template generator, portal link, or API call — see `BROKER-CATALOG.md` for details).
  - Output a structured record of pending requests with expected response dates.

- **Build the data parsers** (`src/normalization/`).
  - Google Takeout: parse `ads_interests.json` and `ads_information.json`
  - Meta: parse `your_topics.json` and `ads_interests.json` from the Meta data export
  - Define a unified normalization schema (the README sketches this — e.g., `clarity.financial.income_bracket` as a canonical field that maps from Acxiom's `P$Income_Discretionary_Amount`, Experian's `Estimated Household Income`, etc.)
  - Store parsed output in local SQLite

- **Replace the hardcoded vulnerability profiles in `index.html`** with a real rule engine (`src/analysis/`) that reads from the normalized schema and outputs:
  - Vulnerability category + exposure level
  - Supporting evidence from real broker data
  - Conflict detection against user-set intentions

### Phase 3 (Analysis Engine)

- Integrate Ollama (local LLM via `ollama` Python library) to generate personalized reflection prompts instead of the current hand-written ones
- Implement the IAB Content Taxonomy mapping so broker segments map to standardized attention categories
- Build the "Persuasion Weather Report" — a periodic summary of targeting patterns over time

### Architecture notes

- **Everything runs locally.** No user data goes to a server. Design accordingly.
- The frontend (`index.html`) and the Python backend will need an IPC bridge — a local HTTP server (Flask/FastAPI on `localhost`) is the simplest approach
- Write tests for all parsing logic — broker response formats change without notice

### Key files to read first
- `README.md` — Architecture section for the full data flow diagram
- `BROKER-CATALOG.md` — your primary reference for what data each broker holds and how to access it
- `index.html` — understand the hardcoded data structures you'll be replacing (search for `vulnerabilityProfiles` and `attentionCategories` in the JavaScript)

---

## Theologian

**Your north star:** This project is fundamentally about human dignity, self-knowledge, and the conditions for free choice. Your role is not peripheral — the entire product thesis rests on a claim that seeing yourself through the lens of a data profile can be liberating rather than reductive. That claim needs to be rigorously examined, carefully framed, and honestly communicated.

This is a rare opportunity to do applied philosophical and ethical work that directly shapes a product used by real people.

### Immediate priorities

- **Audit the current reflection prompts in `index.html`.**
  The prototype contains hand-written "reflection" text for each vulnerability category (Financial Anxiety, Health Vulnerability, Status Comparison, etc.). Read each one critically:
  - Does the framing respect human dignity and agency?
  - Does it avoid shaming or pathologizing normal human behavior?
  - Is it honest about the limits of what the data actually tells us?
  - Does "pause and notice" language align with contemplative traditions that have thought carefully about attention and desire?
  Produce a short document with your assessment and suggested rewrites.

- **Develop a vocabulary guide.**
  The product uses words like "vulnerability," "exploitation," "manipulation," "anxiety," and "impulse." These are loaded terms. Write a brief style guide — informed by theological and philosophical anthropology — that defines how the project should and shouldn't use this language. The goal is precision and compassion, not clinical detachment or moral alarm.

- **Think through the identity question.**
  The tagline is "See what data brokers see. Then choose who you actually are." This makes a strong implicit claim: that there is a "who you actually are" that is distinct from and more authoritative than the data profile. That claim is philosophically interesting and worth examining. Write a brief reflection (1–2 pages) on what that claim implies, where it holds up, and where it needs nuance. This will directly inform how the product talks about itself.

### Ongoing responsibilities

- **Review all user-facing copy** before it ships, especially reflection prompts generated by the LLM in Phase 3. The LLM will need a system prompt that embeds the project's ethical commitments — you should write the first draft of that prompt.
- **Consult on the "Intention" feature.** The app asks users to set intentions ("spend more mindfully," "reduce anxiety-driven decisions"). This is an invitation to a kind of examined life. Think about what that invitation should look and feel like, what it should not claim to do, and how it avoids becoming prescriptive or paternalistic.
- **Engage the federated learning ethics question.** Phase 4 introduces community intelligence — the system learns which reflections help people most. This raises genuine questions: Who defines "helped"? What counts as a reflection being effective? Is there a risk that optimizing for engagement subtly distorts the project's values? Flag these concerns early, before they're baked into architecture.
- **Document your thinking.** Create `docs/ETHICS.md` as a living document. This will be valuable for contributors, for users who want to understand the project's values, and for any future grant or partnership conversations.

### Key files to read first
- `README.md` — especially the Design Principles section and the "Why Clarity Mirror?" section at the bottom
- `PRIVACY-MODEL.md` — understanding the technical privacy model will help you engage meaningfully with the ethical one
- `index.html` — search for `reflection` in the JavaScript to find the current hand-written prompts you'll be reviewing

---

## How the Team Works Together

| Decision | Owner | Consulted |
|---|---|---|
| What to build next | PM | All |
| How it gets deployed | DevOps | Engineer |
| How it gets built | Engineer | DevOps |
| What it says to users | Theologian | PM |
| Privacy architecture | Engineer + DevOps | All |
| Ethical framing | Theologian | PM |
| Roadmap priorities | PM | All |

The most important shared constraint: **the design principles in `README.md` are not negotiable on a feature-by-feature basis.** "Awareness, not anxiety," "local-first, always," and "calm technology" are commitments, not suggestions. Any proposed feature that violates them needs to be explicitly discussed as a team before proceeding.
