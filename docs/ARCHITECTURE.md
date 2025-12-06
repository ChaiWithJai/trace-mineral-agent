# Architecture

## Overview

TraceMineralDiscoveryAgent is a multi-agent system built on LangChain DeepAgents for cross-paradigm medical research synthesis.

## System Architecture

```mermaid
graph TB
    subgraph "User Interface"
        CLI[CLI Entry Point]
        API[LangGraph API]
    end

    subgraph "Orchestration"
        MA[Main Agent<br/>TraceMineralDiscoveryAgent]
        WT[write_todos]
    end

    subgraph "Paradigm Research Subagents"
        AR[AllopathyResearchAgent<br/>PubMed, Cochrane]
        NR[NaturopathyResearchAgent<br/>Integrative Medicine]
        AYR[AyurvedicResearchAgent<br/>Rasa Shastra, Bhasmas]
        TCR[TCMResearchAgent<br/>Five Elements, Meridians]
    end

    subgraph "Synthesis"
        SA[SynthesisAgent<br/>Cross-Paradigm Integration]
        SR[synthesis_reporter<br/>Multi-Stakeholder Output]
    end

    subgraph "Tools"
        LS[literature_search]
        EG[evidence_grade]
        PM[paradigm_mapper]
    end

    CLI --> MA
    API --> MA
    MA --> WT
    MA --> AR
    MA --> NR
    MA --> AYR
    MA --> TCR
    AR --> LS
    NR --> LS
    AYR --> LS
    TCR --> LS
    AR --> EG
    NR --> EG
    AYR --> EG
    TCR --> EG
    AR --> SA
    NR --> SA
    AYR --> SA
    TCR --> SA
    SA --> PM
    SA --> SR
```

## Data Model

```mermaid
erDiagram
    HYPOTHESIS {
        string hypothesis_id PK "UUID"
        string mineral "e.g., chromium"
        string target_pathway "e.g., GLP-1"
        string target_outcomes "weight, insulin"
        datetime created_at
        string status "draft|validated|synthesized"
    }

    PARADIGM_RESEARCH {
        string research_id PK
        string hypothesis_id FK
        string paradigm "allopathy|naturopathy|ayurveda|tcm"
        json literature_results
        string evidence_grade "A|B|C|D"
        json citations
        datetime completed_at
    }

    CROSS_PARADIGM_MAPPING {
        string mapping_id PK
        string hypothesis_id FK
        string source_paradigm
        string target_paradigm
        string source_concept
        string target_concept
        float confidence_score
    }

    SYNTHESIS_REPORT {
        string report_id PK
        string hypothesis_id FK
        string stakeholder_type "researcher|trainer|dx"
        float consensus_score
        json paradigm_breakdown
        json recommendations
        json research_gaps
        datetime generated_at
    }

    HYPOTHESIS ||--o{ PARADIGM_RESEARCH : "researched by"
    HYPOTHESIS ||--o{ CROSS_PARADIGM_MAPPING : "mapped across"
    HYPOTHESIS ||--|| SYNTHESIS_REPORT : "synthesized into"
```

## Component Details

### Main Agent

The main TraceMineralDiscoveryAgent orchestrates the research workflow:

1. Receives user research query
2. Creates investigation plan
3. Dispatches to paradigm-specific subagents in parallel
4. Collects findings
5. Triggers synthesis

### Subagents

Each subagent has:

- **System Prompt**: Paradigm-specific research methodology
- **Tools**: Appropriate subset of available tools
- **Output Format**: Standardized markdown structure

#### Allopathy Research Agent

- Searches PubMed via E-utilities API
- Grades evidence using GRADE methodology
- Prioritizes RCTs and meta-analyses

#### Naturopathy Research Agent

- Searches integrative medicine databases
- Emphasizes food-first approaches
- Considers synergistic combinations

#### Ayurveda Research Agent

- Searches Ayurvedic literature and AYUSH databases
- Maps bhasma preparations to trace minerals
- Considers dosha theory and Agni

#### TCM Research Agent

- Searches TCM literature
- Maps Five Element correspondences
- Considers pattern diagnosis relevance

#### Synthesis Agent

- Integrates findings across paradigms
- Calculates consensus scores
- Generates stakeholder-specific reports

### Tools

#### literature_search

Routes to appropriate database based on paradigm:

- Allopathy → PubMed E-utilities
- Others → Tavily web search with domain filtering

#### evidence_grade

Implements adapted GRADE methodology:

- Paradigm-aware study type weighting
- Sample size, effect size, CI width assessment
- Peer review and replication bonuses

#### paradigm_mapper

Provides concept translations:

- Pre-defined mappings (85% confidence)
- Reverse mapping lookup
- Suggestions for unmapped concepts

#### synthesis_reporter

Generates three report types:

- **Research Scientist**: Full citations, methods, limitations
- **Product Trainer**: Talking points, positioning
- **DX Professional**: Clinical protocols, contraindications

## Deployment

### Local Development

```bash
# CLI mode
trace-mineral-agent

# LangGraph dev server
langgraph dev
```

### LangGraph Cloud

Configuration in `langgraph.json`:

```json
{
  "python_version": "3.11",
  "dependencies": ["./apps/agent"],
  "graphs": {
    "trace-mineral-discovery": "./apps/agent/src/trace_mineral_agent/agent.py:agent"
  }
}
```

## Security Considerations

- No hardcoded API keys
- Rate limiting for external APIs
- Input sanitization for search queries
- Medical disclaimer on all outputs

## Performance

- Parallel subagent execution for research queries
- Caching for repeated literature searches (planned)
- Streaming responses for long operations (planned)

## Testing Strategy

- Unit tests for tools and subagent configs
- Integration tests with mocked APIs
- End-to-end tests with LangSmith traces
