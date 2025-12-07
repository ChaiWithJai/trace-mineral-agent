"""Integration tests with real API calls.

These tests require real API keys and make actual network requests.
Run with: pytest -m integration --no-cov
Skip with: pytest -m "not integration"
"""

import os

import pytest

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


def requires_api_key(key_name: str):
    """Skip test if API key is not available."""
    return pytest.mark.skipif(
        os.getenv(key_name) is None or os.getenv(key_name, "").startswith("test-"),
        reason=f"{key_name} not configured",
    )


class TestLiteratureSearchIntegration:
    """Integration tests for literature search with real PubMed API."""

    @requires_api_key("TAVILY_API_KEY")
    def test_pubmed_search_returns_results(self):
        """Test that PubMed search returns actual results."""
        from trace_mineral_agent.tools import literature_search

        result = literature_search.invoke(
            {"mineral": "zinc", "condition": "immune function", "max_results": 3}
        )

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 100
        # Should contain some research-related content
        assert any(
            term in result.lower()
            for term in ["study", "research", "evidence", "zinc", "immune"]
        )

    @requires_api_key("TAVILY_API_KEY")
    def test_literature_search_chromium_diabetes(self):
        """Test chromium-diabetes search returns relevant results."""
        from trace_mineral_agent.tools import literature_search

        result = literature_search.invoke(
            {"mineral": "chromium", "condition": "diabetes", "max_results": 5}
        )

        assert result is not None
        assert "chromium" in result.lower() or "diabetes" in result.lower()


class TestDrugInteractionsIntegration:
    """Integration tests for drug interaction checking."""

    def test_check_drug_interactions_real_data(self):
        """Test drug interaction check with real mineral/drug combinations."""
        from trace_mineral_agent.tools import check_drug_interactions

        result = check_drug_interactions.invoke(
            {"mineral": "zinc", "medications": ["penicillamine", "quinolones"]}
        )

        assert result is not None
        assert isinstance(result, str)
        # Should identify known interactions
        assert "interaction" in result.lower() or "warning" in result.lower()

    def test_list_mineral_interactions(self):
        """Test listing known interactions for a mineral."""
        from trace_mineral_agent.tools import list_mineral_interactions

        result = list_mineral_interactions.invoke({"mineral": "iron"})

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 50


class TestEvidenceGradeIntegration:
    """Integration tests for evidence grading."""

    def test_grade_strong_evidence(self):
        """Test grading research with strong evidence indicators."""
        from trace_mineral_agent.tools import evidence_grade

        findings = """
        A systematic review and meta-analysis of 15 RCTs (n=1,200) found
        that zinc supplementation reduced cold duration by 33% (95% CI: 25-40%,
        p<0.001). Heterogeneity was low (I²=15%). GRADE assessment: HIGH quality.
        """

        result = evidence_grade.invoke({"findings": findings})

        assert result is not None
        assert isinstance(result, str)
        # Should recognize high-quality evidence
        assert any(
            grade in result.upper() for grade in ["A", "HIGH", "STRONG", "GRADE"]
        )

    def test_grade_weak_evidence(self):
        """Test grading research with weak evidence indicators."""
        from trace_mineral_agent.tools import evidence_grade

        findings = """
        A case report from 1985 suggested that selenium might help with
        fatigue in one patient. No controlled studies available.
        """

        result = evidence_grade.invoke({"findings": findings})

        assert result is not None
        # Should recognize weak evidence
        assert any(
            indicator in result.upper()
            for indicator in ["C", "D", "LOW", "WEAK", "LIMITED", "PRELIMINARY"]
        )


class TestParadigmMapperIntegration:
    """Integration tests for paradigm mapping."""

    def test_map_zinc_across_paradigms(self):
        """Test mapping zinc to different healing paradigms."""
        from trace_mineral_agent.tools import paradigm_mapper

        result = paradigm_mapper.invoke({"mineral": "zinc"})

        assert result is not None
        assert isinstance(result, str)
        # Should include multiple paradigm perspectives
        assert len(result) > 200

    def test_map_selenium_paradigms(self):
        """Test mapping selenium across paradigms."""
        from trace_mineral_agent.tools import paradigm_mapper

        result = paradigm_mapper.invoke({"mineral": "selenium"})

        assert result is not None


class TestSynthesisReporterIntegration:
    """Integration tests for synthesis report generation."""

    def test_generate_synthesis_report(self):
        """Test generating a synthesis report from paradigm findings."""
        from trace_mineral_agent.tools import synthesis_reporter

        findings = {
            "allopathy": "3 RCTs show zinc reduces cold duration by 33%",
            "naturopathy": "Commonly used in immune support protocols",
            "ayurveda": "Associated with Vata dosha and nervous system",
            "tcm": "Metal element; supports Lung Qi",
        }

        result = synthesis_reporter.invoke(
            {"mineral": "zinc", "paradigm_findings": findings}
        )

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 100


class TestCitationExportIntegration:
    """Integration tests for citation export."""

    def test_export_bibtex(self):
        """Test BibTeX export format."""
        from trace_mineral_agent.tools import export_citations

        citations = [
            {
                "title": "Effects of zinc on immune function",
                "authors": ["Smith, John", "Doe, Jane"],
                "year": "2023",
                "journal": "Journal of Nutrition",
                "volume": "153",
                "pages": "100-110",
                "doi": "10.1234/jn.2023.001",
            }
        ]

        result = export_citations.invoke({"citations": citations, "format": "bibtex"})

        assert result is not None
        assert "@article" in result
        assert "Smith" in result
        assert "2023" in result

    def test_export_ris(self):
        """Test RIS export format."""
        from trace_mineral_agent.tools import export_citations

        citations = [
            {
                "title": "Selenium and thyroid function",
                "authors": ["Brown, Alice"],
                "year": "2022",
                "journal": "Thyroid Research",
            }
        ]

        result = export_citations.invoke({"citations": citations, "format": "ris"})

        assert result is not None
        assert "TY  - JOUR" in result
        assert "AU  - Brown, Alice" in result

    def test_export_endnote(self):
        """Test EndNote XML export format."""
        from trace_mineral_agent.tools import export_citations

        citations = [
            {
                "title": "Chromium and glucose metabolism",
                "authors": ["Wilson, Mark"],
                "year": "2021",
                "journal": "Diabetes Care",
            }
        ]

        result = export_citations.invoke({"citations": citations, "format": "endnote"})

        assert result is not None
        assert "<?xml" in result
        assert "<record>" in result

    def test_format_citation_for_report(self):
        """Test Vancouver-style citation formatting."""
        from trace_mineral_agent.tools import format_citation_for_report

        result = format_citation_for_report.invoke(
            {
                "title": "Zinc supplementation in elderly",
                "authors": "Smith J, Doe J, Brown A, Wilson M",
                "year": "2023",
                "journal": "Geriatric Nutrition",
                "doi": "10.1234/gn.2023",
            }
        )

        assert result is not None
        assert "Smith J, et al." in result
        assert "2023" in result
        assert "doi:" in result


class TestAgentEndToEndIntegration:
    """End-to-end integration tests for the full agent."""

    @requires_api_key("ANTHROPIC_API_KEY")
    @pytest.mark.slow
    def test_simple_query(self):
        """Test a simple query through the full agent."""
        from trace_mineral_agent.agent import create_trace_mineral_agent

        agent = create_trace_mineral_agent(use_memory=False)

        result = agent.invoke(
            {"messages": [{"role": "user", "content": "What are the main trace minerals?"}]}
        )

        assert result is not None
        assert "messages" in result
        assert len(result["messages"]) > 0
        response = result["messages"][-1].content
        assert len(response) > 50

    @requires_api_key("ANTHROPIC_API_KEY")
    @requires_api_key("TAVILY_API_KEY")
    @pytest.mark.slow
    def test_research_query(self):
        """Test a research query that uses tools."""
        from trace_mineral_agent.agent import create_trace_mineral_agent

        agent = create_trace_mineral_agent(use_memory=False)

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "What does the research say about zinc and immune function? Keep it brief.",
                    }
                ]
            }
        )

        assert result is not None
        assert "messages" in result
        response = result["messages"][-1].content
        # Should include zinc-related content
        assert "zinc" in response.lower() or "immune" in response.lower()

    @requires_api_key("ANTHROPIC_API_KEY")
    @pytest.mark.slow
    def test_drug_interaction_query(self):
        """Test a drug interaction query."""
        from trace_mineral_agent.agent import create_trace_mineral_agent

        agent = create_trace_mineral_agent(use_memory=False)

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Does zinc interact with any medications?",
                    }
                ]
            }
        )

        assert result is not None
        response = result["messages"][-1].content
        assert len(response) > 50


class TestStreamingIntegration:
    """Integration tests for streaming functionality."""

    @requires_api_key("ANTHROPIC_API_KEY")
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_streaming_query(self):
        """Test streaming query execution."""
        from trace_mineral_agent.agent import create_trace_mineral_agent
        from trace_mineral_agent.streaming import stream_research

        agent = create_trace_mineral_agent(use_memory=False)

        events = []
        async for event in stream_research(
            agent, "What is selenium?", print_output=False
        ):
            events.append(event)

        assert len(events) > 0
        # Should have start and end events
        event_types = [e["event"] for e in events]
        assert "research_started" in event_types
        assert "report_generated" in event_types
