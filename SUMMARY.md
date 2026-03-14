# Clarity Mirror — Project Summary

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Data Normalization Flow](#data-normalization-flow)
- [Data Retrieval Sources](#data-retrieval-sources)
- [Tech Stack](#tech-stack)
- [Roadmap](#roadmap)
- [Design Principles](#design-principles)

---

## Overview

**Clarity Mirror** is a privacy-first tool that shows people what data brokers know about them and how advertisers exploit that data. It reframes surveillance profiles as prompts for self-awareness — turning "what they know about you" into "what you can notice about yourself."

All analysis runs locally. Raw data never leaves the device.

## Core Features

```mermaid
mindmap
  root((Clarity Mirror))
    Vulnerability Mirror
      Surfaces psychological pressure points
      Reframes as mindfulness prompts
      Maps broker segments to vulnerabilities
    Attention Audit
      Maps attention economy allocation
      Shows which categories target you
      Reveals exploitation mechanisms
    Intention Conflicts
      User sets personal intentions
      Flags targeting that conflicts with goals
      Bridges awareness and action
```

## System Architecture

```mermaid
flowchart TB
    subgraph device["YOUR DEVICE"]
        direction TB
        A["Data Broker Retrieval\n(CCPA / GDPR requests)"] --> B["Normalizer &\nSchema Mapping"]
        B --> C["Clarity Engine\n(Analysis)"]
        D["Intention Store\n(User goals)"] --> E["Conflict Detection"]
        C --> E
        E --> F["Reflection Surface\n(UI Output)"]
    end

    subgraph fed["FEDERATED SERVER (optional, opt-in)"]
        G["Federated Aggregation\n(model weights only)"]
    end

    device -. "model weight deltas only\n(never raw data)" .-> fed

    style device fill:#f9f9f0,stroke:#333,stroke-width:2px
    style fed fill:#eef6ee,stroke:#666,stroke-dasharray:5 5
```

## Data Normalization Flow

```mermaid
flowchart LR
    A1["Acxiom\nP$Income_Discretionary_Amount"] --> U["clarity.financial\n.income_bracket"]
    A2["Experian\nEstimated Household Income"] --> U
    A3["Oracle\nHH_INCOME_RANGE"] --> U

    U --> R["Rule Engine +\nLocal LLM"]
    R --> V["Vulnerability\nCategories"]
    R --> AT["Attention\nTargets"]

    style U fill:#e8f0fe,stroke:#4285f4
    style R fill:#fef7e0,stroke:#f9ab00
```

## Data Retrieval Sources

```mermaid
flowchart LR
    subgraph sources["Data Sources"]
        DB["Data Brokers\n(Acxiom, Experian, LexisNexis)"]
        AP["Ad Platforms\n(Google, Meta, TikTok, Amazon)"]
        IR["Identity Resolution\n(LiveRamp, The Trade Desk)"]
        PS["People Search\n(Spokeo, BeenVerified)"]
    end

    subgraph methods["Access Methods"]
        CCPA["CCPA/GDPR Request\n1-45 days"]
        EXP["Platform Export Tools\nMinutes-hours"]
        OPT["Opt-out Portals\n1-14 days"]
    end

    DB --> CCPA
    AP --> EXP
    IR --> CCPA
    PS --> OPT

    CCPA --> N["Normalization Layer"]
    EXP --> N
    OPT --> N

    style sources fill:#fff5f5,stroke:#999
    style methods fill:#f5fff5,stroke:#999
```

## Tech Stack

```mermaid
flowchart TB
    subgraph current["Phase 1 (Current)"]
        HTML["Vanilla HTML/CSS/JS\nSingle file, zero deps"]
    end

    subgraph planned["Phase 2+ (Planned)"]
        PY["Python\nRetrieval + Normalization"]
        SQL["SQLite\nLocal storage"]
        LLM["Ollama (Llama/Mistral)\nLocal LLM reflections"]
        FL["PyTorch + Flower\nFederated learning"]
        SK["SvelteKit\nFrontend v2"]
    end

    HTML -.-> SK
    PY --> SQL
    PY --> LLM
    FL -.-> LLM

    style current fill:#e8f5e9,stroke:#4caf50
    style planned fill:#fff3e0,stroke:#ff9800,stroke-dasharray:5 5
```

## Roadmap

```mermaid
gantt
    title Clarity Mirror Roadmap
    dateFormat YYYY
    axisFormat %Y

    section Phase 1
    Prototype (complete)          :done, p1, 2024, 2025

    section Phase 2
    Real Data Retrieval           :active, p2, 2025, 2026

    section Phase 3
    Local Analysis Engine         : p3, 2026, 2027

    section Phase 4
    Community & Federated Learning: p4, 2027, 2028

    section Phase 5
    Platform Expansion            : p5, 2028, 2029
```

### Phase Details

```mermaid
flowchart LR
    P1["Phase 1\nPrototype"] -->|done| P2["Phase 2\nReal Data Retrieval"]
    P2 --> P3["Phase 3\nLocal Analysis Engine"]
    P3 --> P4["Phase 4\nFederated Learning"]
    P4 --> P5["Phase 5\nPlatform Expansion"]

    P1a["Interactive Mirror\nAttention Audit\nIntention Setting"] -.-> P1
    P2a["CCPA automation\nGoogle/Meta parsers\nUnified schema"] -.-> P2
    P3a["Rule-based mapping\nIAB taxonomy\nLocal LLM"] -.-> P3
    P4a["FedAvg infra\nCommunity intel\nExposure benchmarks"] -.-> P4
    P5a["Mobile app\nBrowser extension\nPrivacy tool integrations"] -.-> P5

    style P1 fill:#4caf50,color:#fff
    style P2 fill:#ff9800,color:#fff
    style P3 fill:#9e9e9e,color:#fff
    style P4 fill:#9e9e9e,color:#fff
    style P5 fill:#9e9e9e,color:#fff
```

## Design Principles

```mermaid
mindmap
  root((Design\nPrinciples))
    Awareness not anxiety
      "Notice" and "pause" language
      Breathing exercises built in
      Mirror, not alarm
    Local-first always
      Data never leaves device
      Federated layer is opt-in
      Model updates only
    Honest about limitations
      Shows inferences not certainties
      Broker data is incomplete
      The mirror is imperfect
    Non-judgmental
      Patterns not character flaws
      Industries exploit everyone
      Seeing clearly is the goal
    Calm technology
      Periodic reflections
      Journal not feed
      No constant notifications
```
