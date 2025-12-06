# Contributing to TraceMineralDiscoveryAgent

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- GitHub CLI (`gh`)

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/ChaiWithJai/trace-mineral-agent.git
cd trace-mineral-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install with dev dependencies
pip install -e "apps/agent[dev]"
```

### Configure Environment

```bash
cp apps/agent/.env.example apps/agent/.env
# Edit .env with your API keys
```

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

### Creating a Feature

```bash
# Create feature branch from develop
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# Make changes...

# Run tests
pytest apps/agent/tests/ -v

# Run linting
ruff check apps/agent/src/
ruff format apps/agent/src/

# Commit with conventional commit format
git add .
git commit -m "feat: add new tool for mineral bioavailability"
```

### Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Formatting, no code change
- `refactor:` - Code change that neither fixes a bug nor adds a feature
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:

```
feat: add selenium tool for thyroid research
fix: handle empty PubMed results gracefully
docs: update README with new quick picks
test: add integration tests for synthesis_reporter
```

### Pull Request Process

1. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create PR via GitHub CLI:
   ```bash
   gh pr create --title "feat: your feature" --body "Description of changes"
   ```

3. Ensure CI passes
4. Request review
5. Address feedback
6. Merge when approved

## Code Standards

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use Ruff for linting and formatting

### Documentation

- Docstrings for all public functions (Google style)
- Update README for new features
- Update ARCHITECTURE.md for structural changes

### Testing

- Write tests for new functionality
- Maintain >70% coverage
- Use meaningful test names

Example test:

```python
def test_evidence_grade_returns_valid_grade_for_rct():
    """High-quality RCT should receive grade A or B."""
    result = evidence_grade.invoke({
        "study_type": "rct",
        "sample_size": 500,
        ...
    })
    assert "**Overall Grade:** A" in result or "**Overall Grade:** B" in result
```

## Adding New Tools

1. Create file in `apps/agent/src/trace_mineral_agent/tools/`
2. Implement using `@tool` decorator from LangChain
3. Return markdown-formatted string
4. Add to `tools/__init__.py`
5. Write tests in `tests/test_tools.py`

Example:

```python
from langchain_core.tools import tool

@tool
def new_tool(param: str) -> str:
    """Tool description for the LLM.

    Args:
        param: Description of parameter

    Returns:
        Markdown-formatted result
    """
    # Implementation
    return f"## Result\n\n{result}"
```

## Adding New Subagents

1. Create file in `apps/agent/src/trace_mineral_agent/subagents/`
2. Define system prompt with:
   - Role description
   - Research methodology
   - Output format
   - Safety guidelines
3. Configure with appropriate tools
4. Add to `subagents/__init__.py`
5. Write tests in `tests/test_subagents.py`

## Running CI Locally

```bash
# Run full CI suite
ruff check apps/agent/src/
ruff format --check apps/agent/src/
pyright apps/agent/src/
pytest apps/agent/tests/ -v --cov=trace_mineral_agent
```

## Getting Help

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Tag `@ChaiWithJai` for urgent items

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
