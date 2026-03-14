# Clarity Mirror — Persona-Based Simulation

## What this is

Right now, Clarity Mirror shows every user the same six vulnerability profiles filtered by a simple broker checkbox. The simulation isn't personalized — it's the same portrait for everyone.

This document scopes the work to replace that with **pre-built user personas**: realistic, research-grounded profiles that produce meaningfully different mirrors for different kinds of people. This is the primary way users will experience the product until real broker data ingestion is built.

A persona is a complete, self-consistent data profile — a person with a recognizable life situation, a specific set of data broker footprints, a distinct vulnerability signature, and tailored reflection language. When a user selects a persona (or is matched to one), they see a mirror that feels like it was made for them, not generated at random.

---

## Why personas before real data

Real broker data ingestion (Phase 2) requires CCPA requests, parsers, and a local backend. Personas require none of that — they run entirely in the existing single HTML file. They let us:

- Ship a meaningfully improved product to real users now
- Test whether the reflection language actually lands with different audiences
- Gather feedback that informs which broker integrations to prioritize
- Give the theologian real content to audit before the LLM is involved

---

## Scope of work

### 1. Persona definitions (Theologian + PM)

Define 5–6 personas. Each persona needs:

**Demographic & life situation**
A short, specific description of who this person is — not a stereotype, but a recognizable situation. Avoid naming them (no "Meet Sarah"). Describe their life context, their relationship to technology, and what they're generally trying to do with their time and money.

**Data broker footprint**
Which brokers realistically hold data on this person, and why. What specific behaviors created that footprint? This should feel grounded — not "they use Google" but "they've searched for mortgage refinancing twice, use Google Maps heavily for commuting, and have location history going back three years."

**Vulnerability profile**
Which of the six vulnerability categories apply, at what intensity, and in what order of prominence. Each persona should have a distinct signature — not just "high on everything" but a specific shape. Include what the broker data would actually say about them.

**Attention allocation**
Realistic percentage breakdowns across the six attention categories. These should reflect the persona's life, not just be reshuffled versions of the defaults. A new parent's attention profile looks completely different from a recent graduate's.

**Reflection tone**
Notes on how the reflection language should shift for this persona. The Financial Anxiety reflection for someone in their 50s approaching retirement hits differently than the same underlying insight for someone in their 20s with student debt. The theologian should flag which framings need adjustment per persona.

**Intention conflicts**
Which of the default intentions are most live for this persona, and what a meaningful intention conflict actually looks like in their specific context.

---

### 2. Implementation (Application Engineer)

The existing rendering machinery in `index.html` (`renderResults()`, `vulnerabilityProfiles`, `attentionCategories`) stays unchanged. Personas are a data layer that feeds it.

**What needs to be built:**

**Persona selector UI** — A new step before the broker grid (or replacing it). Could be a card-based selector with a brief description of each persona's life situation. Should feel like recognition, not categorization — the user picks the profile that most resembles their own situation, not a label.

**Persona data objects** — Each persona is a JavaScript object containing:
- Pre-selected broker IDs
- A custom `vulnerabilityProfiles` array (can reuse existing profiles or define new ones with persona-specific `whatTheySee` and `reflection` text)
- Custom attention percentage weights per category
- Pre-selected or pre-suggested intentions
- A persona-specific reflection panel text

**Broker grid behavior** — When a persona is selected, the broker grid should pre-populate with that persona's footprint. The user can still modify selections. This keeps the existing interaction model intact while making the defaults meaningful.

**"Build your own" option** — The current behavior (manually selecting brokers with no persona) should remain available. Personas are a shortcut, not a requirement.

---

### 3. Content per persona (Theologian)

For each persona, the theologian writes or reviews:

- The `whatTheySee` text for each active vulnerability card — the italicized broker-voice description of what the data says
- The `reflection` text — the mindful reframe
- The reflection panel prompt and moments
- Any persona-specific intention language

This is the most important content work in the project right now. The quality of these reflections determines whether the product is genuinely useful or just interesting-looking. See the vocabulary guide (once written) for tone and language guidelines.

---

## Suggested personas

These are starting points. The PM and theologian should pressure-test them against real user interviews before the engineer builds anything.

| # | Working title | Core tension |
|---|---|---|
| 1 | Early-career urban professional | Aspirational spending vs. financial insecurity |
| 2 | Mid-career parent | Attention scarcity, health anxiety, time pressure |
| 3 | Late-career pre-retiree | Financial anxiety, health monitoring, legacy concerns |
| 4 | College student / recent graduate | Status comparison, debt, identity formation |
| 5 | Small business owner / freelancer | Financial stress, productivity culture, risk tolerance |
| 6 | Caregiver (parent, elder care) | Emotional exhaustion, health research, guilt targeting |

These six cover distinct vulnerability signatures and attention profiles. They are not exhaustive — they are a starting set that can be expanded based on user feedback.

---

## Who does what

| Task | Owner | Input needed from |
|---|---|---|
| Finalize persona list | PM | Theologian |
| Write persona life situations | PM | — |
| Define broker footprints per persona | PM + Engineer | BROKER-CATALOG.md |
| Write vulnerability & reflection text | Theologian | Vocabulary guide |
| Review reflection text for accuracy | PM | — |
| Build persona selector UI | Engineer | PM (design direction) |
| Build persona data objects in JS | Engineer | Theologian (content) |
| Write attention weights per persona | Engineer | PM (research) |
| User test persona selection flow | PM | All |

---

## Definition of done

A persona is complete when:

- [ ] Life situation description written and reviewed
- [ ] Broker footprint defined with specific behavioral rationale
- [ ] All active vulnerability cards have persona-specific `whatTheySee` and `reflection` text
- [ ] Attention percentages set and justified
- [ ] Reflection panel text written
- [ ] Theologian has reviewed all user-facing copy
- [ ] Engineer has implemented the persona in the selector
- [ ] At least one person outside the team has selected the persona and said "this feels like me"

---

## What this is not

This is not a segmentation or targeting system. Personas are not user accounts, they don't store data, and they don't follow anyone anywhere. They are simulation scaffolding — a way to make the prototype feel real while the actual data pipeline is being built. The moment real broker data ingestion works, personas become optional context rather than the primary experience.
