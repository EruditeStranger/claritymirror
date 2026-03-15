# DataVault Integration

## What DataVault is

[DataVault](https://github.com/mindfulmakers/datavault) is a local-first personal data gateway built by a separate team (mindfulmakers). It runs as a FastAPI server on the user's machine and acts as a controlled intermediary between personal data sources and the applications that want to use them.

**Core idea:** apps register with DataVault, request specific data types, and the user explicitly approves each request before any data is shared. No data leaves the device. The approval workflow is the product — it's a consent layer for personal data, not just a storage system.

**Current data types supported:**
- Location (iOS, Garmin)
- Messages (demo provider)

**Tech stack:** Python, FastAPI, SQLite, Pydantic, LangChain (for approval summaries), `uv` package manager. Runs at `http://127.0.0.1:8787` by default.

---

## Why this is relevant to Clarity Mirror

DataVault and Clarity Mirror solve adjacent problems for the same user:

```
DataVault:        Raw data → Normalized records → Gated access
Clarity Mirror:   Normalized data → Vulnerability analysis → Reflection
```

DataVault could replace the entire planned `src/retrieval/` and `src/normalization/` layers, plus the `claude -p` normalization step. Instead of running a command-line tool to parse exports, Clarity Mirror would register as a DataVault consumer, request ad profile data types, and receive normalized records through the approval-gated API.

This is architecturally cleaner and more privacy-sound than building our own ingestion pipeline — the consent model is explicit and auditable rather than implicit.

---

## DataVault's data model

All data follows a `NormalizedRecord` structure:

```json
{
  "record_id": "unique identifier",
  "type_id": "location | messages | ...",
  "provider_id": "source provider",
  "source_reference": "ID from original source",
  "occurred_at": "ISO 8601",
  "captured_at": "ISO 8601",
  "ingested_at": "ISO 8601",
  "payload": {}
}
```

The `payload` is type-specific JSON. For a future `ad-profile` type, this is where interests, segments, and behavioral signals would live.

**Query results** return:
```json
{
  "results": [],
  "summary": "optional LangChain-generated summary",
  "cursor": "optional pagination cursor"
}
```

---

## DataVault's API (relevant endpoints)

| Endpoint | Method | Purpose |
|---|---|---|
| `/v1/apps/register` | POST | Register Clarity Mirror as a consumer |
| `/v1/oauth/token` | POST | Get bearer token |
| `/v1/types` | GET | List available data types |
| `/v1/types/{type_id}/records` | GET | Fetch normalized records |
| `/v1/types/{type_id}/queries/{query_name}` | POST | Run parameterized queries |
| `/v1/approvals/{approval_id}/decision` | POST | User approves or rejects a data request |

Authentication is Bearer token. Apps register once with a `consumer_id` and secret, then exchange for a token.

---

## What integration would look like

### Step 1 — Clarity Mirror registers as a DataVault consumer

On first run, Clarity Mirror calls `/v1/apps/register` with its `consumer_id` and stores the returned credentials locally. This is a one-time setup step.

```python
# src/datavault/client.py
import httpx

DATAVAULT_BASE = "http://127.0.0.1:8787"

async def register():
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{DATAVAULT_BASE}/v1/apps/register", json={
            "consumer_id": "clarity-mirror",
            "secret": "<generated locally>",
            "display_name": "Clarity Mirror"
        })
        return r.json()

async def get_token(consumer_id, secret):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{DATAVAULT_BASE}/v1/oauth/token", json={
            "consumer_id": consumer_id,
            "secret": secret
        })
        return r.json()["access_token"]
```

### Step 2 — A new DataVault data type plugin: `ad-profile`

This is the core contribution. Someone needs to build `datavault-type-ad-profile` as a DataVault plugin — a new package that defines the ad profile data type and its queries.

**Plugin interface (DataVault SDK):**
```python
class AdProfileDataType(DataTypePlugin):
    type_id = "ad-profile"
    display_name = "Ad & Data Broker Profile"
    record_schema = {
        "type": "object",
        "properties": {
            "interests": {"type": "array", "items": {"type": "string"}},
            "segments": {"type": "array", "items": {"type": "string"}},
            "behavioral_signals": {"type": "array", "items": {"type": "string"}},
            "inferred_demographics": {"type": "object"},
            "vulnerability_scores": {"type": "object"},
            "attention_allocation": {"type": "object"},
            "source_platform": {"type": "string"}
        }
    }

    def execute_query(self, name, params, records):
        if name == "vulnerability-summary":
            return self._summarize_vulnerabilities(records)
        if name == "attention-breakdown":
            return self._attention_breakdown(records)
```

### Step 3 — Provider plugins for Google, Meta, etc.

Each platform export becomes a DataVault provider plugin:

```python
class GoogleAdProfileProvider(DataProviderPlugin):
    provider_id = "google-ad-profile"
    display_name = "Google Ad Profile (Takeout)"
    normalized_type_ids = ["ad-profile"]

    def normalize_payload(self, payload: dict) -> list[NormalizedRecord]:
        # Parse Google Takeout ads_interests.json format
        # Return normalized NormalizedRecord objects
        ...
```

This is where the parsing work lives — but it's contributed to DataVault as a shared plugin, not owned solely by Clarity Mirror.

### Step 4 — Clarity Mirror requests data through the approval gate

```python
async def fetch_ad_profile(token):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{DATAVAULT_BASE}/v1/types/ad-profile/records",
            headers={"Authorization": f"Bearer {token}"}
        )
        # DataVault triggers approval workflow for the user
        # Returns records once approved
        return r.json()["results"]
```

The user sees a DataVault approval prompt: "Clarity Mirror is requesting your ad profile data. Approve?" — explicit, auditable consent.

### Step 5 — Map DataVault records to Clarity Mirror's schema

The normalized records from DataVault map directly to our existing `vulnerability_scores` and `attention_allocation` schema — the same structure the `claude -p` normalization step produces. The rendering layer in `index.html` doesn't change.

---

## What doesn't exist yet

| Missing piece | Owner |
|---|---|
| `datavault-type-ad-profile` plugin | Needs to be built — could be a joint contribution with the DataVault team |
| `datavault-provider-google-ad-profile` | Same |
| `datavault-provider-meta-ad-profile` | Same |
| Clarity Mirror local backend (to call DataVault API) | Our engineer |
| DataVault running on user's machine | User setup step — same friction point as the `claude -p` approach |

---

## Relationship to the current `claude -p` approach

The `claude -p` normalization skill (see `SKILLS.md`) and DataVault integration are **not in conflict** — they produce the same output schema and both feed the same upload/load flow in `index.html`. The `claude -p` approach is:

- Lower friction for a demo (no local server required)
- Already built and working
- The right path for v1

DataVault integration is:
- Architecturally cleaner for a real product
- Adds explicit user consent and audit trail
- Requires a local backend and plugin development
- The right path for Phase 2+

Use `claude -p` to ship the demo. Plan DataVault as the Phase 2 ingestion layer.

---

## Before integrating

Two things to resolve before writing code against DataVault:

**1. License** — The DataVault repo has no open-source license specified. Default copyright law applies, meaning no permission to use, modify, or distribute without explicit permission from the author. Reach out to Gabriel Montague (mindfulmakers) before building against it.

**2. Plugin contribution model** — The ad profile data type is generically useful — it's not Clarity Mirror-specific. The right move is to propose contributing `datavault-type-ad-profile` upstream rather than forking or maintaining it separately. This also gets us DataVault's approval workflow for free.
