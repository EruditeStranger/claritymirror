# Broker Catalog

A living catalog of data brokers, their data access mechanisms, and known response formats.

> **Status:** Research in progress. Contributions welcome.

## Tier 1 — Major Data Brokers

| Broker | Access Method | Response Format | Typical Timeline | Notes |
|---|---|---|---|---|
| Acxiom | [aboutthedata.com](https://aboutthedata.com) | Web portal, CSV | Immediate–7 days | Self-service portal; limited categories shown |
| Experian | Written request / online portal | PDF report | 15–30 days | Consumer disclosure report; credit-oriented |
| LexisNexis | [consumer.risk.lexisnexis.com](https://consumer.risk.lexisnexis.com) | PDF | 15–30 days | Full file disclosure available |
| Oracle Data Cloud | CCPA request via email | Varies | 30–45 days | Exited third-party data business in 2024; residual data may still exist |
| LiveRamp | Privacy portal | JSON/CSV | 15–45 days | Identity resolution graph data |
| Epsilon | CCPA request via email | PDF/CSV | 30–45 days | Marketing segments and household data |

## Tier 2 — Ad Platforms (First-Party)

| Platform | Access Method | Response Format | Timeline |
|---|---|---|---|
| Google | [takeout.google.com](https://takeout.google.com) | JSON/HTML archive | Minutes–hours |
| Meta | Settings → Download Your Information | JSON/HTML archive | Minutes–hours |
| Amazon | Request My Data | CSV/JSON | Days |
| TikTok | Settings → Download Your Data | JSON | Minutes–hours |

## Tier 3 — People Search / Public Records

| Broker | Opt-Out Method | Notes |
|---|---|---|
| Spokeo | Online form | Requires email verification |
| BeenVerified | Online form | May require identity verification |
| Whitepages | Online form | Premium data requires separate request |
| Intelius | Online form | Shares data infrastructure with other brokers |

## Adding a New Broker

Please include:
1. Broker name and parent company
2. What data they hold (categories)
3. How to request your data (with links)
4. Expected response format and timeline
5. Any known quirks or difficulties
