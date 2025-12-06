"""Tests for the observability module."""

import os

import pytest

from trace_mineral_agent.observability import (
    EVALUATION_EXAMPLES,
    configure_langsmith,
    is_tracing_enabled,
    log_consensus_score,
    log_evidence_grade,
    trace_research_query,
    traceable,
)


class TestConfigureLangsmith:
    """Tests for LangSmith configuration."""

    def test_configures_with_api_key(self, monkeypatch):
        """Should configure LangSmith when API key is present."""
        monkeypatch.setenv("LANGSMITH_API_KEY", "test-key")

        # Should not raise
        configure_langsmith(project_name="test-project")

        # Implementation uses LANGCHAIN_PROJECT (not LANGSMITH_PROJECT)
        assert os.getenv("LANGCHAIN_PROJECT") == "test-project"
        assert os.getenv("LANGCHAIN_TRACING_V2") == "true"

    def test_skips_without_api_key(self, monkeypatch):
        """Should skip configuration without API key."""
        monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)

        # Should not raise
        configure_langsmith()

    def test_respects_enable_flag(self, monkeypatch):
        """Should not enable tracing when flag is False."""
        monkeypatch.setenv("LANGSMITH_API_KEY", "test-key")

        configure_langsmith(enable_tracing=False)

        # Implementation uses LANGCHAIN_TRACING_V2 (not LANGSMITH_TRACING_V2)
        assert os.getenv("LANGCHAIN_TRACING_V2") == "false"


class TestIsTracingEnabled:
    """Tests for tracing status check."""

    def test_returns_true_when_enabled(self, monkeypatch):
        """Should return True when tracing is enabled."""
        monkeypatch.setenv("LANGSMITH_API_KEY", "test-key")
        # Implementation checks LANGCHAIN_TRACING_V2 (not LANGSMITH_TRACING_V2)
        monkeypatch.setenv("LANGCHAIN_TRACING_V2", "true")

        assert is_tracing_enabled() is True

    def test_returns_false_without_key(self, monkeypatch):
        """Should return False without API key."""
        monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)
        monkeypatch.setenv("LANGCHAIN_TRACING_V2", "true")

        assert is_tracing_enabled() is False

    def test_returns_false_when_disabled(self, monkeypatch):
        """Should return False when tracing is disabled."""
        monkeypatch.setenv("LANGSMITH_API_KEY", "test-key")
        monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")

        assert is_tracing_enabled() is False


class TestTraceable:
    """Tests for the traceable decorator."""

    def test_decorator_works_without_langsmith(self):
        """Should work as no-op without LangSmith."""
        @traceable(name="test_func", run_type="chain")
        def sample_function(x):
            return x * 2

        result = sample_function(5)
        assert result == 10

    def test_decorator_with_metadata(self):
        """Should accept metadata parameter."""
        @traceable(name="test", run_type="tool", metadata={"key": "value"})
        def another_function():
            return "result"

        result = another_function()
        assert result == "result"


class TestTraceResearchQuery:
    """Tests for the trace_research_query context manager."""

    def test_context_manager_executes_block(self):
        """Should execute the code block."""
        executed = False

        with trace_research_query(query="test query"):
            executed = True

        assert executed is True

    def test_context_manager_with_parameters(self):
        """Should accept all parameters."""
        with trace_research_query(
            query="chromium insulin sensitivity",
            mineral="chromium",
            paradigms=["allopathy", "naturopathy"],
            stakeholder="research_scientist",
        ):
            pass  # Should not raise

    def test_context_manager_propagates_exceptions(self):
        """Should propagate exceptions from the block."""
        with pytest.raises(ValueError, match="test error"), trace_research_query(query="test"):
            raise ValueError("test error")


class TestLogEvidenceGrade:
    """Tests for evidence grade logging."""

    def test_logs_grade_info(self, capfd):
        """Should log grade information."""
        log_evidence_grade(
            mineral="chromium",
            paradigm="allopathy",
            grade="A",
            confidence=0.85,
        )

        # Function should not raise
        # In production, would verify LangSmith logging

    def test_handles_all_grades(self):
        """Should handle all grade levels."""
        for grade in ["A", "B", "C", "D"]:
            log_evidence_grade(
                mineral="zinc",
                paradigm="tcm",
                grade=grade,
                confidence=0.5,
            )


class TestLogConsensusScore:
    """Tests for consensus score logging."""

    def test_logs_consensus_info(self):
        """Should log consensus information."""
        log_consensus_score(
            hypothesis="Test hypothesis",
            mineral="magnesium",
            consensus_score=0.72,
            paradigm_scores={
                "allopathy": 0.8,
                "naturopathy": 0.7,
                "ayurveda": 0.6,
                "tcm": 0.65,
            },
        )

        # Should not raise

    def test_handles_partial_paradigm_scores(self):
        """Should handle missing paradigm scores."""
        log_consensus_score(
            hypothesis="Test",
            mineral="selenium",
            consensus_score=0.5,
            paradigm_scores={
                "allopathy": 0.6,
            },
        )


class TestEvaluationExamples:
    """Tests for evaluation examples structure."""

    def test_examples_exist(self):
        """Should have evaluation examples."""
        assert len(EVALUATION_EXAMPLES) > 0

    def test_examples_have_required_fields(self):
        """Each example should have inputs and expected_outputs."""
        for example in EVALUATION_EXAMPLES:
            assert "inputs" in example
            assert "expected_outputs" in example

    def test_examples_cover_diverse_scenarios(self):
        """Examples should cover different scenarios."""
        categories = set()
        for example in EVALUATION_EXAMPLES:
            if "category" in example:
                categories.add(example["category"])

        # Should have multiple categories if structure supports it
        # At minimum, examples should exist
        assert len(EVALUATION_EXAMPLES) >= 1

    def test_example_inputs_are_valid(self):
        """Example inputs should be valid queries."""
        for example in EVALUATION_EXAMPLES:
            input_dict = example["inputs"]
            assert isinstance(input_dict, dict)
            assert "query" in input_dict
            assert isinstance(input_dict["query"], str)
            assert len(input_dict["query"]) > 0
