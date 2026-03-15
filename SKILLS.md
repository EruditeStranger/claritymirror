# Clarity Mirror — Data Normalization Skill

## What this does

This skill uses `claude -p` (Claude Code in headless mode) to read a raw data file — either a simulated persona file or a real data export from a broker or platform — and produce a normalized JSON object that Clarity Mirror can consume directly.

This replaces the hand-written parser layer. Instead of maintaining separate parsers for Google Takeout, Meta exports, Acxiom responses, and every other format, Claude reads whatever format the data arrives in and maps it to the unified schema.

---

## Prerequisites

1. **Claude Code installed**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Authenticated**
   ```bash
   claude
   # Follow the login prompt on first run
   ```

3. **A data file to process** — either a real export or one of the persona simulation files in `data/`

---

## The command

```bash
claude -p "
You are a data normalization tool for Clarity Mirror, a privacy tool that helps
people understand their advertising and data broker profiles.

Read the JSON file at the path I give you and produce a single normalized JSON
object using ONLY the schema below. Do not infer, fabricate, or add fields that
are not supported by evidence in the file. Where data is absent or unclear,
omit the field rather than guess.

OUTPUT SCHEMA:
{
  \"persona_label\": \"string — one of: early-career-professional, mid-career-parent, pre-retiree, college-student, freelancer, caregiver, or unknown\",
  \"data_sources\": [\"list of platforms or brokers this data came from\"],
  \"ad_interests\": [\"list of interest/topic categories inferred from the data\"],
  \"inferred_demographics\": {
    \"age_range\": \"string\",
    \"income_bracket\": \"string\",
    \"life_stage\": \"string\",
    \"location_type\": \"string — urban / suburban / rural / unknown\"
  },
  \"behavioral_signals\": [\"specific behaviors observed in the data\"],
  \"broker_segments\": [\"any named psychographic or audience segments present in the data\"],
  \"vulnerability_scores\": {
    \"financial_anxiety\": \"integer 1-10\",
    \"health_vulnerability\": \"integer 1-10\",
    \"status_comparison\": \"integer 1-10\",
    \"impulse_susceptibility\": \"integer 1-10\",
    \"attention_fragmentation\": \"integer 1-10\",
    \"emotional_targeting\": \"integer 1-10\"
  },
  \"attention_allocation\": {
    \"financial_products\": \"integer percent\",
    \"wellness_supplements\": \"integer percent\",
    \"lifestyle_aspiration\": \"integer percent\",
    \"productivity_tools\": \"integer percent\",
    \"news_outrage\": \"integer percent\",
    \"entertainment_escapism\": \"integer percent\"
  },
  \"top_intention_conflicts\": [\"up to 3 of: Spend more mindfully | Reduce anxiety-driven decisions | Protect my focus | Make health choices from evidence | Resist status comparison | Be present with people I love\"]
}

The attention_allocation percentages must sum to 100.
Vulnerability scores should reflect the intensity of targeting signals in the data, not a moral judgment about the person.

FILE TO PROCESS: data/persona-1-early-career-professional.json

Return only the JSON object. No explanation, no markdown, no commentary.
" > data/persona-1-early-career-professional.out.json
```

---

## Running all six personas

Replace the filename at the end of the command for each persona:

```bash
# Persona 1 — Early-career professional
claude -p "$(cat .claude-normalize-prompt.txt)" --file data/persona-1-early-career-professional.json > data/persona-1.out.json

# Persona 2 — Mid-career parent
claude -p "$(cat .claude-normalize-prompt.txt)" --file data/persona-2-mid-career-parent.json > data/persona-2.out.json

# Persona 3 — Pre-retiree
claude -p "$(cat .claude-normalize-prompt.txt)" --file data/persona-3-late-career-pre-retiree.json > data/persona-3.out.json

# Persona 4 — College student
claude -p "$(cat .claude-normalize-prompt.txt)" --file data/persona-4-college-student-recent-grad.json > data/persona-4.out.json

# Persona 5 — Freelancer
claude -p "$(cat .claude-normalize-prompt.txt)" --file data/persona-5-small-business-owner-freelancer.json > data/persona-5.out.json

# Persona 6 — Caregiver
claude -p "$(cat .claude-normalize-prompt.txt)" --file data/persona-6-caregiver.json > data/persona-6.out.json
```

Or run the full batch in one go:

```bash
for i in 1 2 3 4 5 6; do
  files=(data/persona-$i-*.json)
  claude -p "$(cat docs/normalize-prompt.txt) FILE TO PROCESS: ${files[0]}" > data/persona-$i.out.json
  echo "Done: persona $i"
done
```

---

## Storing the prompt separately

To avoid repeating the full prompt inline, save it to `docs/normalize-prompt.txt` (this file is gitignored via `data/` — move it to `docs/` if you want it tracked):

```bash
# Save the normalization prompt once
cat > docs/normalize-prompt.txt << 'EOF'
You are a data normalization tool for Clarity Mirror...
[paste the full prompt text here]
EOF
```

Then reference it in the command with `$(cat docs/normalize-prompt.txt)`.

---

## What the output looks like

A correctly normalized file (`data/persona-1.out.json`) will look like:

```json
{
  "persona_label": "early-career-professional",
  "data_sources": ["google_ad_settings", "meta_ad_preferences", "acxiom"],
  "ad_interests": ["Personal finance", "Luxury goods", "Travel", "Career development"],
  "inferred_demographics": {
    "age_range": "25-34",
    "income_bracket": "$65,000-$95,000",
    "life_stage": "early career",
    "location_type": "urban"
  },
  "behavioral_signals": [
    "Frequent late-night browsing sessions",
    "Aspirational brand affinity above income level",
    "Active credit account opening",
    "Salary negotiation and savings comparison searches"
  ],
  "broker_segments": ["HENRY", "Urban Achiever", "Aspirational Spender"],
  "vulnerability_scores": {
    "financial_anxiety": 7,
    "health_vulnerability": 3,
    "status_comparison": 8,
    "impulse_susceptibility": 7,
    "attention_fragmentation": 6,
    "emotional_targeting": 5
  },
  "attention_allocation": {
    "financial_products": 30,
    "wellness_supplements": 10,
    "lifestyle_aspiration": 28,
    "productivity_tools": 12,
    "news_outrage": 8,
    "entertainment_escapism": 12
  },
  "top_intention_conflicts": [
    "Spend more mindfully",
    "Resist status comparison"
  ]
}
```

---

## How this connects to the app

The `.out.json` files feed directly into Clarity Mirror. Once the persona selector and LLM integration are built (see `PERSONAS.md` and `docs/LLM-INTEGRATION.md`), the app will:

1. Load the normalized JSON for the selected persona
2. Use `vulnerability_scores` to populate the vulnerability cards
3. Use `attention_allocation` to drive the attention audit bars
4. Pass `behavioral_signals`, `top_intention_conflicts`, and `broker_segments` as context to the LLM reflection call

The rendering layer in `index.html` does not need to change — the normalized JSON is a drop-in replacement for the hardcoded `vulnerabilityProfiles` and `attentionCategories` arrays.

---

## Using with real data exports

This same command works on real data. Download your exports from:

- **Google:** myaccount.google.com → Data & privacy → Download your data → select "Ads"
- **Meta:** facebook.com/settings → Your Facebook information → Download your information → select "Ads"
- **Amazon:** amazon.com → Account & Lists → Request my data

Then run:

```bash
claude -p "$(cat docs/normalize-prompt.txt) FILE TO PROCESS: ~/Downloads/google-ads-data.json" > data/my-profile.out.json
```

The output schema is identical regardless of the input format. Claude handles the format variation so the app doesn't have to.

---

## What this is not

This normalization step does not send your raw data anywhere. `claude -p` runs locally using your own Claude Code installation. The raw file stays on your machine. Only the normalized summary — with no raw behavioral data — is what eventually gets passed to the hosted LLM reflection endpoint (and only the `top_intention_conflicts` and vulnerability category labels, not the full profile).

See `PRIVACY-MODEL.md` for the full data flow and privacy guarantees.
