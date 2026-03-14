# LLM Integration — Clarity Mirror

## Why we're doing this

The reflection panel is currently the weakest part of the product. It shows the same three hardcoded sentences to every user, regardless of what intentions they selected, which brokers they chose, or what vulnerabilities surfaced. A user who selects "Protect my focus" and a user who selects "Spend more mindfully" see identical text.

LLM integration replaces that with a reflection that is actually responsive to the user's specific profile — their stated intentions, their matched vulnerability categories, and their broker footprint. This is the feature that makes the product feel like a mirror rather than a pamphlet.

It also unlocks the persona system: each persona produces a distinct vulnerability signature and broker context, and the LLM generates a reflection tailored to that specific combination rather than one the team had to pre-write.

---

## What gets sent to the model

The LLM receives three inputs assembled at generation time:

**1. The user's stated intentions**
Everything in `selectedIntentions` plus any custom intention text. Example:
```
"Spend more mindfully", "Protect my focus", "I want to stop comparing myself to people online"
```

**2. The matched vulnerability profiles**
The categories, exposure levels, and broker-voice descriptions for the profiles that matched the user's broker selection. Example:
```
- Financial Anxiety (high): "Credit-monitoring behavior pattern. Classified as financially anxious, responsive to urgency-based financial products."
- Attention Fragmentation (medium): "Multi-platform engagement, high scroll velocity. Attention span profiled as snackable content optimized."
```

**3. The selected brokers**
Which data sources are in the profile. This provides context about the type of data involved.

These inputs are assembled into a user message. The system prompt (see `docs/SYSTEM-PROMPT-BRIEF.md`) governs how the model responds to them.

---

## What the model returns

A structured reflection containing:

- **A framing sentence** — one sentence that acknowledges the specific tension between the user's intentions and their vulnerability profile
- **2–3 reflection moments** — short paragraphs, each grounding an abstract insight in a specific, recognizable situation the user might encounter
- **A closing line** — a single quiet sentence that returns the user to agency

The model should not return lists, headers, or markdown formatting. The output is prose, rendered directly into the existing reflection panel UI.

---

## Privacy considerations

Sending data to a hosted API means intention data leaves the device. This is a deliberate, limited exception to the local-first principle:

- **What is sent:** Self-reported intentions and vulnerability category labels. No raw broker data, no personal identifiers, no behavioral records.
- **What is not sent:** Actual broker export files, CCPA response data, location data, purchase history, or anything from the local SQLite database.
- **API configuration:** Use zero data retention mode where available (Anthropic supports this via API header). Confirm this is configured before shipping.
- **User disclosure:** The UI must tell the user before they generate that reflection generation uses an AI model and what is sent. This should be a one-time acknowledgment, not a modal on every generation.

Update `PRIVACY-MODEL.md` to document this exception explicitly once the integration is live.

---

## Implementation

### Where it plugs in

In `index.html`, the reflection panel is rendered in the `renderResults()` function starting around line 851. Currently:

```javascript
// This entire block gets replaced
const reflectionText = document.getElementById('reflection-text');
const reflectionMoments = document.getElementById('reflection-moments');

if (allIntentions.length > 0) {
  reflectionText.textContent = `You said you want to...`;
  // hardcoded moments rendered here
}
```

Replace this block with an async call to the reflection endpoint, then populate the same DOM elements with the response.

### Architecture

The API key must never be in the frontend. The call goes through a thin backend endpoint:

```
Browser (index.html)
    │
    ▼
/api/reflect  (Vercel serverless function — Python or Node)
    │  Assembles system prompt + user message
    │  Calls hosted LLM API
    │  Returns structured reflection
    ▼
Browser renders reflection into existing DOM
```

For the Vercel deployment, this is a serverless function in `api/reflect.py` (Python) or `api/reflect.js` (Node). The API key is stored as a Vercel environment variable, never in the repo.

### Vercel serverless function (Python)

Create `api/reflect.py`:

```python
import anthropic
import json
from http.server import BaseHTTPRequestHandler

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

SYSTEM_PROMPT = open("docs/system-prompt.md").read()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        intentions = body.get("intentions", [])
        vulnerabilities = body.get("vulnerabilities", [])
        brokers = body.get("brokers", [])

        user_message = build_user_message(intentions, vulnerabilities, brokers)

        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "reflection": message.content[0].text
        }).encode())


def build_user_message(intentions, vulnerabilities, brokers):
    lines = []

    if intentions:
        lines.append("The user's stated intentions:")
        for i in intentions:
            lines.append(f"  - {i}")

    if vulnerabilities:
        lines.append("\nVulnerability profile:")
        for v in vulnerabilities:
            lines.append(f"  - {v['category']} ({v['level']}): {v['whatTheySee']}")

    if brokers:
        lines.append(f"\nData sources in profile: {', '.join(brokers)}")

    return "\n".join(lines)
```

### Frontend call (in index.html)

Replace the hardcoded reflection block with:

```javascript
async function generateReflection(intentions, vulnerabilities, brokers) {
  const response = await fetch('/api/reflect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ intentions, vulnerabilities, brokers })
  });
  const data = await response.json();
  return data.reflection;
}
```

Then in `renderResults()`, collect the matched vulnerability data and call this function. Render the returned text into `#reflection-text` and `#reflection-moments`.

Handle the loading state: the existing loading indicator and messages can cover the API call duration. Expect 2–5 seconds for response time.

Handle errors gracefully: if the API call fails, fall back to the existing hardcoded reflection. Never show a raw error to the user.

### Loading state during API call

The existing `generateMirror()` function already has a loading state with cycling messages. Extend the loading duration to cover the API call, or trigger the API call during the fake loading period and render results when both the timer and the API call have resolved (use `Promise.all`).

---

## Environment setup

Add to Vercel project settings (never to the repo):
```
ANTHROPIC_API_KEY=sk-ant-...
```

For local development, create a `.env` file (already in `.gitignore`) with the same variable. Use `python-dotenv` to load it locally.

---

## The system prompt

The system prompt is the most important configuration in this integration. It is maintained in `docs/system-prompt.md` and co-owned by the engineer and the theologian. **Do not modify it without theologian review.**

See `docs/SYSTEM-PROMPT-BRIEF.md` for the full rationale, constraints, and review process.

---

## Testing before shipping

Before this goes live, run every persona through the integration and review the outputs with the theologian. Specific things to check:

- Does the model ever use shame-adjacent language ("you have a problem with", "you struggle with")?
- Does it ever overstate certainty ("you are an impulse buyer" vs. "your profile suggests")?
- Does it ever give advice rather than prompts for awareness?
- Does the reflection feel responsive to the specific intentions, or generic?
- Does the closing line return the user to agency?

If any output fails these checks, revise the system prompt before shipping. Do not patch individual bad outputs — fix the prompt.
