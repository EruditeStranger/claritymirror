<p align="center">
  <img src="assets/banner.svg" alt="Clarity Mirror" width="100%">
</p>

<p align="center">
  <strong>See what data brokers see when they look at you. Then choose who you actually are.</strong>
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a> · <a href="#the-problem">The Problem</a> · <a href="#how-it-works">How It Works</a> · <a href="#architecture">Architecture</a> · <a href="#roadmap">Roadmap</a> · <a href="#contributing">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/status-prototype-orange.svg" alt="Status: Prototype">
  <img src="https://img.shields.io/badge/data-stays%20local-green.svg" alt="Data stays local">
</p>

---

## The Problem

Hundreds of data brokers — Acxiom, Experian, Oracle Data Cloud, LexisNexis, LiveRamp, Epsilon, and many others — hold detailed profiles about you. These profiles map your psychological pressure points: financial anxiety, health fears, status aspirations, impulse patterns. Advertisers use these profiles to target you with messages designed to bypass your judgment.

You have a legal right to see this data (CCPA, GDPR, state privacy laws). But even when you get it, it arrives as incomprehensible category codes and opaque segment IDs.

**Clarity Mirror** turns that data into a tool for self-awareness instead of manipulation.

## What It Does

Clarity Mirror combines two core features:

### 🪞 Vulnerability Mirror

Surfaces the psychological pressure points your data profile reveals — the levers advertisers pull — and reframes them as prompts for mindfulness:

> **What they see:** *Credit-monitoring behavior pattern. Classified as financially anxious, responsive to urgency-based financial products.*
>
> **Your reflection:** *You're being shown a version of financial reality designed to keep you slightly afraid. Pause before any financial decision that arrives with a countdown timer. The urgency is manufactured.*

### 📡 Attention Audit

Maps where the attention economy is allocating effort against you — which categories of content and products are competing for your attention, and what psychological mechanisms they're exploiting:

| Category | Share | Mechanism |
|---|---|---|
| Financial Products | 28% | Targeting financial anxiety signals |
| Wellness & Supplements | 22% | Leveraging health search patterns |
| Lifestyle & Aspiration | 18% | Feeding the comparison engine |

### 🧘 Intention Conflicts

You set personal intentions ("spend more mindfully," "reduce anxiety-driven decisions"), and the system flags when your data profile is being targeted in ways that conflict with those intentions.

## How It Works

```
┌─────────────────────────────────────────────────────┐
│                    YOUR DEVICE                       │
│                                                      │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────┐ │
│  │ Data Broker  │──▸│ Normalizer & │──▸│ Clarity  │ │
│  │  Retrieval   │   │   Schema     │   │  Engine  │ │
│  │  (CCPA/GDPR) │   │   Mapping    │   │          │ │
│  └─────────────┘   └──────────────┘   └────┬─────┘ │
│                                             │       │
│  ┌─────────────┐   ┌──────────────┐        │       │
│  │  Intention   │──▸│  Conflict    │◂───────┘       │
│  │   Store      │   │  Detection   │                │
│  └─────────────┘   └──────┬───────┘                 │
│                            │                         │
│                     ┌──────▾───────┐                 │
│                     │  Reflection  │                 │
│                     │   Surface    │                 │
│                     └──────────────┘                 │
│                                                      │
│  ⚠ Raw data NEVER leaves this boundary               │
└─────────────────────────────────────────────────────┘
          │ (optional, model updates only)
          ▾
  ┌───────────────┐
  │   Federated   │  Shared model learns which
  │   Aggregation │  reflections help people most
  │   Server      │  — without seeing anyone's data
  └───────────────┘
```

**Everything runs locally.** Your broker data, ad platform exports, intentions, and analysis never leave your device. The optional federated learning layer only transmits model weight updates — never raw data.

## Quickstart

### Run the Prototype

The current prototype demonstrates the Vulnerability Mirror and Attention Audit with simulated broker data:

```bash
git clone https://github.com/your-org/clarity-mirror.git
cd clarity-mirror

# Open the prototype directly in your browser
open app/clarity-mirror.html
```

No build step, no dependencies, no server. It's a single HTML file.

### Project Structure

```
clarity-mirror/
├── app/
│   └── clarity-mirror.html    # Interactive prototype (self-contained)
├── assets/
│   ├── logo.svg               # Logo mark
│   ├── icon.svg               # Favicon / app icon
│   └── banner.svg             # Social / README banner
├── docs/
│   ├── ARCHITECTURE.md        # Detailed system architecture
│   ├── BROKER-CATALOG.md      # Known data brokers & access methods
│   ├── DATA-SCHEMA.md         # Unified attribute schema
│   └── PRIVACY-MODEL.md       # Privacy & threat model
├── src/                       # (coming soon)
│   ├── retrieval/             # Broker data request automation
│   ├── normalization/         # Format parsing & schema mapping
│   ├── analysis/              # Vulnerability & attention profiling
│   ├── reflection/            # LLM-powered reflection generation
│   └── federated/             # Optional FL aggregation layer
├── LICENSE
└── README.md
```

## Architecture

### Data Retrieval Layer

Automates exercising your data rights across brokers and platforms:

| Source Type | Examples | Access Method | Response Time |
|---|---|---|---|
| Data brokers | Acxiom, Experian, LexisNexis | CCPA/GDPR request (email, API, portal) | 1–45 days |
| Ad platforms | Google, Meta, TikTok, Amazon | Platform data export tools | Minutes–hours |
| Identity resolution | LiveRamp, The Trade Desk | CCPA request | 15–45 days |
| People search | Spokeo, BeenVerified, Whitepages | Opt-out portals | 1–14 days |

### Normalization Layer

Maps broker-specific attributes to a unified schema:

```
Acxiom "P$Income_Discretionary_Amount"  ──┐
Experian "Estimated Household Income"    ──┼──▸ clarity.financial.income_bracket
Oracle "HH_INCOME_RANGE"                ──┘
```

### Analysis Engine

Classifies normalized data into vulnerability categories and attention targets using a combination of rule-based mapping (broker segments → IAB taxonomy → vulnerability categories) and an optional local LLM for generating personalized reflections.

### Federated Learning Layer (Optional)

If a community of users opts in, Federated Averaging trains a shared model that improves over time:

- Learns which reflection framings actually help people become more mindful
- Identifies emerging broker practices across the population
- Benchmarks individual data exposure against anonymized population statistics
- **No raw data ever leaves any device** — only model weight deltas are transmitted

## Design Principles

**1. Awareness, not anxiety.** The language is "notice" and "pause," never "danger" and "warning." The interface includes breathing exercises and grounding elements. We're building a mirror, not an alarm.

**2. Local-first, always.** Your data is the most sensitive thing about you. It never leaves your device. Period. The federated layer is opt-in and transmits only model updates.

**3. Honest about limitations.** We show you what we can infer, not what we're certain about. Broker data is incomplete, sometimes wrong, and always a simplification. The mirror is imperfect — and that's worth reflecting on too.

**4. Non-judgmental.** Being tagged as "impulse buyer" or "status-seeking" isn't a character flaw. These are patterns that entire industries have spent billions learning to exploit. Seeing them clearly is the goal, not fixing them.

**5. Calm technology.** Periodic reflections, not constant notifications. The system should feel like a journal, not a feed.

## Roadmap

### Phase 1: Prototype ✅
- [x] Interactive Vulnerability Mirror with simulated data
- [x] Attention Audit visualization
- [x] Intention setting and conflict detection
- [x] Brand identity and open-source setup

### Phase 2: Real Data Retrieval
- [ ] Automated CCPA request generation for top 10 brokers
- [ ] Google Takeout ad profile parser
- [ ] Meta data export ad interest parser
- [ ] Unified normalization schema (v1)
- [ ] Identity verification flow

### Phase 3: Local Analysis Engine
- [ ] Rule-based broker segment → vulnerability mapping
- [ ] IAB Content Taxonomy integration
- [ ] Local LLM integration for personalized reflections
- [ ] Persuasion Weather Report (periodic summary)

### Phase 4: Community & Federated Learning
- [ ] Federated Averaging infrastructure
- [ ] Opt-in community intelligence
- [ ] Reflection effectiveness model
- [ ] Population-level exposure benchmarking

### Phase 5: Platform Expansion
- [ ] Mobile app (local-first, no cloud sync)
- [ ] Browser extension for real-time ad targeting awareness
- [ ] Integration with existing privacy tools (DeleteMe, Optery)

## Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Prototype | Vanilla HTML/CSS/JS | Zero dependencies, runs anywhere |
| Data retrieval | Python | Best library ecosystem for web scraping, email automation, PDF parsing |
| Normalization | Python + SQLite | Local-only structured storage |
| Analysis | Rule engine + local LLM (Llama/Mistral via Ollama) | No data leaves the device |
| Federated learning | PyTorch + Flower | Mature FL framework |
| Frontend (v2) | SvelteKit | Lightweight, local-first friendly |
| Mobile | React Native or Capacitor | Cross-platform with local storage |

## Team & Contributing

We need people with experience in:

- **Privacy law & data rights** — CCPA/GDPR compliance, broker request mechanics
- **Data engineering** — Parsing broker response formats (PDF, CSV, XML, JSON), schema normalization
- **Platform integration** — Google, Meta, Amazon, TikTok data export APIs
- **ML/Federated learning** — FedAvg implementation, differential privacy
- **UX/Product design** — Translating opaque data attributes into meaningful human reflections
- **Security** — Identity verification flows, secure local storage, threat modeling

### How to Contribute

1. **Fork** the repository
2. **Pick an issue** from the [Issues](../../issues) tab, or open a new one
3. **Discuss** your approach in the issue before writing code
4. **Submit a PR** with a clear description of what it does and why

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting.

### Code of Conduct

This project exists to help people see clearly and choose freely. We expect all contributors to treat each other with the same respect and non-judgment we bring to the product itself. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Why "Clarity Mirror"?

Data brokers build a model of you optimized for one purpose: getting you to act in ways that benefit advertisers. That model — your impulses, vulnerabilities, habits, aspirations — is a portrait painted by people who don't care about you.

But the same portrait, if you can see it clearly, becomes a tool for self-knowledge. The shift is simple:

> From **"here's what they know about you so they can push your buttons"**
> to **"here's what they know about you so you can notice your own patterns."**

The mirror doesn't change what it reflects. But looking in it changes you.

## License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <img src="assets/icon.svg" alt="Clarity Mirror" width="32" height="32">
  <br>
  <sub>This is information, not identity. Breathe. Notice. Choose.</sub>
</p>
