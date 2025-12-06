"""Tests for the core tools."""

from unittest.mock import MagicMock, patch

import pytest

from trace_mineral_agent.tools.evidence_grade import evidence_grade
from trace_mineral_agent.tools.literature_search import literature_search
from trace_mineral_agent.tools.paradigm_mapper import paradigm_mapper
from trace_mineral_agent.tools.synthesis_reporter import synthesis_reporter


class TestLiteratureSearch:
    """Tests for the literature_search tool."""

    @patch("trace_mineral_agent.tools.literature_search.httpx.get")
    def test_pubmed_search_returns_markdown(self, mock_get):
        """Should return markdown-formatted results."""
        # Mock the search response
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"esearchresult": {"idlist": []}},
        )

        result = literature_search.invoke(
            {
                "query": "chromium insulin",
                "paradigm": "allopathy",
                "max_results": 5,
            }
        )

        # Should return no results message for empty results
        assert "No results found" in result or "Allopathy" in result

    def test_unknown_paradigm_raises_validation_error(self):
        """Should raise validation error for unknown paradigms (Pydantic validates input)."""
        import pydantic

        with pytest.raises(pydantic.ValidationError):
            literature_search.invoke(
                {
                    "query": "test",
                    "paradigm": "unknown",
                    "max_results": 1,
                }
            )

    @patch("trace_mineral_agent.tools.literature_search.httpx.get")
    def test_pubmed_api_error_handling(self, mock_get):
        """Should handle API errors gracefully."""
        mock_get.side_effect = Exception("API Error")

        result = literature_search.invoke(
            {
                "query": "test query",
                "paradigm": "allopathy",
                "max_results": 5,
            }
        )

        assert "error" in result.lower() or "Search error" in result


class TestEvidenceGrade:
    """Tests for the evidence_grade tool."""

    def test_high_quality_rct_gets_good_grade(self):
        """High-quality RCT with large sample should get A or B."""
        result = evidence_grade.invoke(
            {
                "study_type": "rct",
                "sample_size": 500,
                "effect_size": 0.6,
                "confidence_interval_width": 0.15,
                "peer_reviewed": True,
                "replication_count": 3,
                "paradigm": "allopathy",
            }
        )

        assert "**Overall Grade:** A" in result or "**Overall Grade:** B" in result
        assert "Evidence Grade Assessment" in result

    def test_case_series_gets_lower_grade(self):
        """Case series with small sample should get C or D."""
        result = evidence_grade.invoke(
            {
                "study_type": "case_series",
                "sample_size": 20,
                "effect_size": 0.3,
                "confidence_interval_width": 0.8,
                "peer_reviewed": True,
                "replication_count": 1,
                "paradigm": "allopathy",
            }
        )

        assert "**Overall Grade:** C" in result or "**Overall Grade:** D" in result

    def test_traditional_text_valued_in_ayurveda(self):
        """Traditional texts should get more weight in Ayurveda paradigm."""
        result = evidence_grade.invoke(
            {
                "study_type": "traditional_text",
                "sample_size": 0,
                "effect_size": 0,
                "confidence_interval_width": 1.0,
                "peer_reviewed": False,
                "replication_count": 1,
                "paradigm": "ayurveda",
            }
        )

        # Should produce valid assessment even for traditional texts in Ayurveda
        assert "Evidence Grade Assessment" in result
        # Check for paradigm context in output (format may vary)
        assert "Ayurveda" in result
        assert "Paradigm Context" in result

    def test_meta_analysis_high_weight(self):
        """Meta-analysis should receive high weight."""
        result = evidence_grade.invoke(
            {
                "study_type": "meta_analysis",
                "sample_size": 2000,
                "effect_size": 0.5,
                "confidence_interval_width": 0.1,
                "peer_reviewed": True,
                "replication_count": 5,
                "paradigm": "allopathy",
            }
        )

        assert "**Overall Grade:** A" in result

    def test_grade_scale_reference_included(self):
        """Should include grade scale reference."""
        result = evidence_grade.invoke(
            {
                "study_type": "rct",
                "sample_size": 100,
                "effect_size": 0.4,
                "confidence_interval_width": 0.3,
                "peer_reviewed": True,
                "replication_count": 1,
                "paradigm": "allopathy",
            }
        )

        assert "Grade Scale Reference" in result
        assert "A (High)" in result
        assert "D (Very Low)" in result


class TestParadigmMapper:
    """Tests for the paradigm_mapper tool."""

    def test_tcm_to_allopathy_mapping(self):
        """Should map TCM kidney_yang to allopathic equivalents."""
        result = paradigm_mapper.invoke(
            {
                "concept": "kidney_yang",
                "source_paradigm": "tcm",
                "target_paradigm": "allopathy",
            }
        )

        assert "thyroid" in result.lower() or "adrenal" in result.lower()
        assert "Paradigm Mapping Result" in result

    def test_unknown_concept_suggests_alternatives(self):
        """Should provide guidance for unmapped concepts."""
        result = paradigm_mapper.invoke(
            {
                "concept": "made_up_concept",
                "source_paradigm": "tcm",
                "target_paradigm": "allopathy",
            }
        )

        assert "No Direct Mapping Found" in result or "Suggestions" in result

    def test_bhasma_to_mineral_mapping(self):
        """Should map Ayurvedic bhasmas to trace minerals."""
        result = paradigm_mapper.invoke(
            {
                "concept": "jasad_bhasma",
                "source_paradigm": "ayurveda",
                "target_paradigm": "trace_mineral",
            }
        )

        assert "zinc" in result.lower()

    def test_ayurveda_to_allopathy_mapping(self):
        """Should map Ayurvedic concepts to Western equivalents."""
        result = paradigm_mapper.invoke(
            {
                "concept": "kapha_imbalance",
                "source_paradigm": "ayurveda",
                "target_paradigm": "allopathy",
            }
        )

        assert "obesity" in result.lower() or "hypothyroidism" in result.lower()

    def test_confidence_score_included(self):
        """Should include confidence score for valid mappings."""
        result = paradigm_mapper.invoke(
            {
                "concept": "spleen_qi",
                "source_paradigm": "tcm",
                "target_paradigm": "allopathy",
            }
        )

        assert "Confidence" in result


class TestSynthesisReporter:
    """Tests for the synthesis_reporter tool."""

    def test_research_scientist_report_has_methods(self):
        """Research scientist report should include methods section."""
        result = synthesis_reporter.invoke(
            {
                "hypothesis": "Chromium improves insulin sensitivity",
                "mineral": "chromium",
                "consensus_score": 0.65,
                "allopathy_findings": "3 RCTs show modest HbA1c reduction",
                "naturopathy_findings": "Common protocol for blood sugar support",
                "ayurveda_findings": "No direct bhasma equivalent",
                "tcm_findings": "Earth element, Spleen support",
                "stakeholder": "research_scientist",
                "include_research_gaps": True,
            }
        )

        assert "Methods" in result
        assert "Search Strategy" in result
        assert "Limitations" in result

    def test_research_scientist_report_has_gaps(self):
        """Research scientist report should include research gaps when requested."""
        result = synthesis_reporter.invoke(
            {
                "hypothesis": "Chromium improves insulin sensitivity",
                "mineral": "chromium",
                "consensus_score": 0.65,
                "allopathy_findings": "Evidence present",
                "naturopathy_findings": "Protocols exist",
                "ayurveda_findings": "",
                "tcm_findings": "",
                "stakeholder": "research_scientist",
                "include_research_gaps": True,
            }
        )

        assert "Research Gaps" in result or "Future Directions" in result

    def test_product_trainer_report_has_talking_points(self):
        """Product trainer report should include key talking points."""
        result = synthesis_reporter.invoke(
            {
                "hypothesis": "Chromium improves insulin sensitivity",
                "mineral": "chromium",
                "consensus_score": 0.65,
                "allopathy_findings": "3 RCTs show modest benefit",
                "naturopathy_findings": "Common protocol",
                "ayurveda_findings": "",
                "tcm_findings": "Earth element",
                "stakeholder": "product_trainer",
                "include_research_gaps": False,
            }
        )

        assert "Talking Points" in result or "Key" in result
        assert "Position" in result or "Differentiation" in result

    def test_dx_professional_report_has_protocols(self):
        """DX professional report should include clinical protocols."""
        result = synthesis_reporter.invoke(
            {
                "hypothesis": "Chromium improves insulin sensitivity",
                "mineral": "chromium",
                "consensus_score": 0.65,
                "allopathy_findings": "Evidence supports use",
                "naturopathy_findings": "Standard protocol",
                "ayurveda_findings": "",
                "tcm_findings": "",
                "stakeholder": "dx_professional",
                "include_research_gaps": False,
            }
        )

        assert "Protocol" in result or "Clinical" in result

    def test_consensus_score_affects_language(self):
        """High consensus should use 'promising' language."""
        high_consensus = synthesis_reporter.invoke(
            {
                "hypothesis": "Test hypothesis",
                "mineral": "test",
                "consensus_score": 0.75,
                "allopathy_findings": "Strong evidence",
                "naturopathy_findings": "Supported",
                "ayurveda_findings": "Traditional use",
                "tcm_findings": "Pattern match",
                "stakeholder": "research_scientist",
                "include_research_gaps": False,
            }
        )

        low_consensus = synthesis_reporter.invoke(
            {
                "hypothesis": "Test hypothesis",
                "mineral": "test",
                "consensus_score": 0.25,
                "allopathy_findings": "",
                "naturopathy_findings": "",
                "ayurveda_findings": "",
                "tcm_findings": "",
                "stakeholder": "research_scientist",
                "include_research_gaps": False,
            }
        )

        assert "promising" in high_consensus.lower()
        assert "insufficient" in low_consensus.lower() or "limited" in low_consensus.lower()

    def test_disclaimer_included(self):
        """All reports should include medical disclaimer."""
        result = synthesis_reporter.invoke(
            {
                "hypothesis": "Test",
                "mineral": "test",
                "consensus_score": 0.5,
                "allopathy_findings": "Test",
                "naturopathy_findings": "Test",
                "ayurveda_findings": "Test",
                "tcm_findings": "Test",
                "stakeholder": "research_scientist",
                "include_research_gaps": False,
            }
        )

        assert "not medical advice" in result.lower() or "consult" in result.lower()
