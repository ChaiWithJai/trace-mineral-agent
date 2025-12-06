# TraceMineralDiscoveryAgent

Multi-paradigm research agent for trace mineral therapeutics discovery. Finds the "trace mineral equivalent of GLP-1" by backtesting hypotheses against four medical paradigms.

## Overview

TraceMineralDiscoveryAgent is a LangChain Deep Agent that conducts research across:

- **Allopathy** (Western Medicine) - PubMed, clinical trials, RCTs
- **Naturopathy** - Integrative medicine, food-first approaches
- **Ayurveda** - Rasa Shastra, bhasma preparations, dosha theory
- **Traditional Chinese Medicine** - Five Elements, Zang-Fu, pattern diagnosis

## Installation

```bash
# Clone the repository
git clone https://github.com/ChaiWithJai/trace-mineral-agent.git
cd trace-mineral-agent

# Install the agent package
pip install -e apps/agent

# Or install with development dependencies
pip install -e "apps/agent[dev]"
```

## Configuration

Create a `.env` file in `apps/agent/`:

```bash
cp apps/agent/.env.example apps/agent/.env
```

Required API keys:

- `ANTHROPIC_API_KEY` - Claude API access
- `TAVILY_API_KEY` - Web search for traditional medicine sources

Optional:

- `NCBI_API_KEY` - PubMed E-utilities (rate limited without)
- `LANGSMITH_API_KEY` - Observability

## Quick Start

### CLI Mode

```bash
# Run the interactive CLI
trace-mineral-agent
```

### Quick Picks

Type a number for pre-configured research queries:

```
1. Magnesium as GLP-1 equivalent
2. Chromium for glucose regulation
3. Zinc-copper-selenium synergy
4. Best minerals for insulin sensitivity
5. Compare berberine + chromium to GLP-1
```

### LangGraph Deployment

```bash
# Start LangGraph server
langgraph dev

# Or deploy to LangGraph Cloud
langgraph build
langgraph deploy
```

## Architecture

```
trace-mineral-agent/
├── apps/
│   └── agent/
│       ├── src/trace_mineral_agent/
│       │   ├── agent.py          # Main agent entry point
│       │   ├── prompts.py        # System prompts
│       │   ├── tools/            # Core tools
│       │   │   ├── literature_search.py
│       │   │   ├── evidence_grade.py
│       │   │   ├── paradigm_mapper.py
│       │   │   └── synthesis_reporter.py
│       │   ├── subagents/        # Specialized research agents
│       │   │   ├── allopathy.py
│       │   │   ├── naturopathy.py
│       │   │   ├── ayurveda.py
│       │   │   ├── tcm.py
│       │   │   └── synthesis.py
│       │   └── memories/         # Domain knowledge base
│       └── tests/
├── langgraph.json                # LangGraph deployment config
└── docs/
```

## Tools

### literature_search

Search medical literature by paradigm:

```python
literature_search(
    query="chromium insulin sensitivity",
    paradigm="allopathy",  # or naturopathy, ayurveda, tcm
    max_results=10
)
```

### evidence_grade

Grade evidence quality using adapted GRADE methodology:

```python
evidence_grade(
    study_type="rct",
    sample_size=500,
    effect_size=0.6,
    confidence_interval_width=0.15,
    paradigm="allopathy"
)
```

### paradigm_mapper

Map concepts between medical traditions:

```python
paradigm_mapper(
    concept="kidney_yang",
    source_paradigm="tcm",
    target_paradigm="allopathy"
)
```

### synthesis_reporter

Generate stakeholder-specific reports:

```python
synthesis_reporter(
    hypothesis="Chromium improves insulin sensitivity",
    mineral="chromium",
    consensus_score=0.65,
    stakeholder="research_scientist"  # or product_trainer, dx_professional
)
```

## Subagents

| Agent | Focus | Tools |
|-------|-------|-------|
| AllopathyResearchAgent | Western medicine, RCTs | literature_search, evidence_grade |
| NaturopathyResearchAgent | Holistic protocols | literature_search, evidence_grade |
| AyurvedicResearchAgent | Bhasmas, doshas | literature_search, evidence_grade, paradigm_mapper |
| TCMResearchAgent | Five Elements, patterns | literature_search, evidence_grade, paradigm_mapper |
| SynthesisAgent | Cross-paradigm integration | paradigm_mapper, synthesis_reporter |

## Development

### Running Tests

```bash
cd apps/agent
pytest tests/ -v
```

### Linting

```bash
ruff check apps/agent/src/
ruff format apps/agent/src/
```

### Type Checking

```bash
pyright apps/agent/src/
```

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Disclaimer

This is a research tool, not medical advice. Always consult qualified healthcare practitioners for medical decisions.
