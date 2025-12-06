"""LangSmith integration for observability and tracing."""

import os
from collections.abc import Callable
from contextlib import contextmanager
from functools import wraps
from typing import Any

# Check if LangSmith is available
LANGSMITH_AVAILABLE = False
try:
    from langsmith import traceable as langsmith_traceable
    from langsmith.run_helpers import get_current_run_tree

    LANGSMITH_AVAILABLE = True
except ImportError:
    pass


def is_tracing_enabled() -> bool:
    """Check if LangSmith tracing is enabled."""
    return (
        LANGSMITH_AVAILABLE
        and os.getenv("LANGCHAIN_TRACING_V2", "").lower() == "true"
        and os.getenv("LANGSMITH_API_KEY") is not None
    )


def configure_langsmith(
    project_name: str = "trace-mineral-agent",
    enable_tracing: bool = True,
) -> None:
    """
    Configure LangSmith for the agent.

    Args:
        project_name: LangSmith project name
        enable_tracing: Whether to enable tracing
    """
    if not LANGSMITH_AVAILABLE:
        return

    if enable_tracing:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = project_name
    else:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"


def traceable(
    name: str | None = None,
    run_type: str = "chain",
    metadata: dict | None = None,
) -> Callable:
    """
    Decorator to trace function execution in LangSmith.

    Falls back to no-op if LangSmith is not available or tracing is disabled.

    Args:
        name: Name for the trace (defaults to function name)
        run_type: Type of run (chain, tool, llm, retriever, etc.)
        metadata: Additional metadata to include in trace

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        if not LANGSMITH_AVAILABLE:
            return func

        trace_name = name or func.__name__
        trace_metadata = metadata or {}

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not is_tracing_enabled():
                return func(*args, **kwargs)

            # Use LangSmith traceable
            traced_func = langsmith_traceable(
                name=trace_name,
                run_type=run_type,
                metadata=trace_metadata,
            )(func)

            return traced_func(*args, **kwargs)

        return wrapper

    return decorator


@contextmanager
def trace_research_query(
    query: str,
    mineral: str | None = None,
    paradigms: list[str] | None = None,
    stakeholder: str | None = None,
):
    """
    Context manager for tracing a complete research query.

    Args:
        query: The research query
        mineral: Primary mineral being researched
        paradigms: List of paradigms to search
        stakeholder: Target stakeholder type

    Yields:
        Trace context with metadata
    """
    metadata = {
        "query": query,
        "mineral": mineral,
        "paradigms": paradigms or ["allopathy", "naturopathy", "ayurveda", "tcm"],
        "stakeholder": stakeholder,
    }

    if not is_tracing_enabled():
        yield metadata
        return

    try:
        from langsmith.run_helpers import traceable as context_traceable

        @context_traceable(
            name="research_query",
            run_type="chain",
            metadata=metadata,
        )
        def _traced_context():
            return metadata

        yield _traced_context()
    except Exception:
        yield metadata


def log_tool_call(
    tool_name: str,
    inputs: dict,
    output: str,
    paradigm: str | None = None,
) -> None:
    """
    Log a tool call to LangSmith.

    Args:
        tool_name: Name of the tool called
        inputs: Input parameters to the tool
        output: Output from the tool
        paradigm: Paradigm context if applicable
    """
    if not is_tracing_enabled():
        return

    try:
        run_tree = get_current_run_tree()
        if run_tree:
            run_tree.add_metadata(
                {
                    f"tool_{tool_name}_inputs": inputs,
                    f"tool_{tool_name}_paradigm": paradigm,
                }
            )
    except Exception:
        pass  # Don't fail on tracing errors


def log_evidence_grade(
    mineral: str,
    paradigm: str,
    grade: str,
    confidence: float,
) -> None:
    """
    Log an evidence grade assignment to LangSmith.

    Args:
        mineral: Mineral being graded
        paradigm: Paradigm context
        grade: Assigned grade (A/B/C/D)
        confidence: Confidence score
    """
    if not is_tracing_enabled():
        return

    try:
        run_tree = get_current_run_tree()
        if run_tree:
            run_tree.add_metadata(
                {
                    "evidence_grade": {
                        "mineral": mineral,
                        "paradigm": paradigm,
                        "grade": grade,
                        "confidence": confidence,
                    }
                }
            )
    except Exception:
        pass


def log_consensus_score(
    hypothesis: str,
    mineral: str,
    consensus_score: float,
    paradigm_scores: dict[str, str],
) -> None:
    """
    Log a consensus score calculation to LangSmith.

    Args:
        hypothesis: Research hypothesis
        mineral: Primary mineral
        consensus_score: Calculated consensus score
        paradigm_scores: Individual paradigm grades
    """
    if not is_tracing_enabled():
        return

    try:
        run_tree = get_current_run_tree()
        if run_tree:
            run_tree.add_metadata(
                {
                    "synthesis": {
                        "hypothesis": hypothesis,
                        "mineral": mineral,
                        "consensus_score": consensus_score,
                        "paradigm_grades": paradigm_scores,
                    }
                }
            )
    except Exception:
        pass


# Evaluation helpers for LangSmith datasets


def create_evaluation_example(
    query: str,
    expected_mineral: str,
    expected_min_consensus: float,
    expected_paradigms_present: list[str],
) -> dict:
    """
    Create an evaluation example for LangSmith dataset.

    Args:
        query: Input research query
        expected_mineral: Expected mineral in response
        expected_min_consensus: Minimum expected consensus score
        expected_paradigms_present: Paradigms that should have findings

    Returns:
        Evaluation example dict
    """
    return {
        "inputs": {"query": query},
        "expected_outputs": {
            "mineral": expected_mineral,
            "min_consensus": expected_min_consensus,
            "paradigms_present": expected_paradigms_present,
        },
    }


EVALUATION_EXAMPLES = [
    create_evaluation_example(
        query="Research chromium for insulin sensitivity",
        expected_mineral="chromium",
        expected_min_consensus=0.5,
        expected_paradigms_present=["allopathy", "naturopathy"],
    ),
    create_evaluation_example(
        query="Investigate magnesium for metabolic health",
        expected_mineral="magnesium",
        expected_min_consensus=0.6,
        expected_paradigms_present=["allopathy", "naturopathy", "ayurveda", "tcm"],
    ),
    create_evaluation_example(
        query="Analyze zinc's role in immune function",
        expected_mineral="zinc",
        expected_min_consensus=0.5,
        expected_paradigms_present=["allopathy", "ayurveda"],
    ),
    create_evaluation_example(
        query="Research selenium for thyroid function",
        expected_mineral="selenium",
        expected_min_consensus=0.6,
        expected_paradigms_present=["allopathy", "tcm"],
    ),
]
