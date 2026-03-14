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

## Data Retention

- **On device**: User controls all retention; can delete at any time
- **Federated server**: Only aggregated model weights are stored; no individual updates are retained after aggregation
- **Logs**: The federated server logs participation counts only (no device identifiers)
