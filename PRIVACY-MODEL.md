# Privacy & Threat Model

Clarity Mirror exists to protect people's relationship with their own data. Our privacy model must be exemplary.

## Core Guarantee

**Your raw personal data never leaves your device.** This is not a preference or a default setting — it is an architectural constraint enforced at the code level.

## Threat Model

### What we protect against

| Threat | Mitigation |
|---|---|
| Data exfiltration to our servers | No server component for personal data; all analysis runs locally |
| Data leakage through federated learning | Differential privacy (DP-SGD) on all model updates; secure aggregation |
| Interception of federated model updates | TLS for all network communication; encrypted payloads |
| Broker data stored insecurely on device | Encrypted local storage; OS-level file protection |
| Identity verification data exposure | Verification docs processed locally, never transmitted |

### What we do NOT protect against

- A compromised device (malware with root access)
- A user voluntarily sharing their Clarity Mirror output
- Brokers correlating data access requests to build richer profiles (a known risk of exercising CCPA/GDPR rights)

## Federated Learning Privacy

The optional federated layer uses:

1. **Local differential privacy**: Noise is added to model updates before they leave the device
2. **Secure aggregation**: The server only sees the aggregate of all participants' updates, never individual contributions
3. **Minimum participation threshold**: Aggregation only occurs when enough participants contribute to prevent individual identification

## LLM Reflection API Exception

The reflection panel uses OpenAI's GPT-5-nano model via a serverless API call. This is a deliberate, limited exception to the local-first principle.

### What is sent
- Self-reported intention labels (e.g., "Spend more mindfully")
- Vulnerability category labels and exposure levels (e.g., "Financial Anxiety — high")
- Broker-voice descriptions (the "whatTheySee" text)
- Selected broker names (e.g., "Experian, Google Ad Profile")

### What is NOT sent
- Actual broker export files or CCPA response data
- Location data, purchase history, or behavioral records
- Device identifiers, IP addresses (beyond what HTTPS requires), or session data
- Any data from the local SQLite database (future phase)

### Data retention
- OpenAI API calls use `store: false`, which prevents OpenAI from storing the request or response
- The Vercel serverless function is stateless; no request data is logged or persisted
- No request data is stored on any server controlled by Clarity Mirror

### API key scoping
- The OpenAI API key uses Restricted permissions: only Chat completions (`/v1/chat/completions`) Write access is enabled
- All other API surfaces (Assistants, Embeddings, Files, Fine-tuning, etc.) are set to None

### User disclosure
- Users are informed before generation that reflection uses AI and what data is sent

## Data Retention

- **On device**: User controls all retention; can delete at any time
- **Federated server**: Only aggregated model weights are stored; no individual updates are retained after aggregation
- **Logs**: The federated server logs participation counts only (no device identifiers)
