"""Tests for the subagent configurations."""

import pytest

from trace_mineral_agent.subagents import (
    allopathy_subagent,
    ayurveda_subagent,
    naturopathy_subagent,
    synthesis_subagent,
    tcm_subagent,
)


class TestSubagentConfiguration:
    """Tests for subagent structure and configuration."""

    def test_allopathy_subagent_has_required_fields(self):
        """Allopathy subagent should have all required fields."""
        assert "name" in allopathy_subagent
        assert "description" in allopathy_subagent
        assert "system_prompt" in allopathy_subagent
        assert "tools" in allopathy_subagent

    def test_naturopathy_subagent_has_required_fields(self):
        """Naturopathy subagent should have all required fields."""
        assert "name" in naturopathy_subagent
        assert "description" in naturopathy_subagent
        assert "system_prompt" in naturopathy_subagent
        assert "tools" in naturopathy_subagent

    def test_ayurveda_subagent_has_required_fields(self):
        """Ayurveda subagent should have all required fields."""
        assert "name" in ayurveda_subagent
        assert "description" in ayurveda_subagent
        assert "system_prompt" in ayurveda_subagent
        assert "tools" in ayurveda_subagent

    def test_tcm_subagent_has_required_fields(self):
        """TCM subagent should have all required fields."""
        assert "name" in tcm_subagent
        assert "description" in tcm_subagent
        assert "system_prompt" in tcm_subagent
        assert "tools" in tcm_subagent

    def test_synthesis_subagent_has_required_fields(self):
        """Synthesis subagent should have all required fields."""
        assert "name" in synthesis_subagent
        assert "description" in synthesis_subagent
        assert "system_prompt" in synthesis_subagent
        assert "tools" in synthesis_subagent

    def test_research_subagents_have_literature_search(self):
        """Research subagents should have literature_search tool."""
        research_agents = [
            allopathy_subagent,
            naturopathy_subagent,
            ayurveda_subagent,
            tcm_subagent,
        ]

        for agent in research_agents:
            tool_names = [t.name for t in agent["tools"]]
            assert "literature_search" in tool_names

    def test_research_subagents_have_evidence_grade(self):
        """Research subagents should have evidence_grade tool."""
        research_agents = [
            allopathy_subagent,
            naturopathy_subagent,
            ayurveda_subagent,
            tcm_subagent,
        ]

        for agent in research_agents:
            tool_names = [t.name for t in agent["tools"]]
            assert "evidence_grade" in tool_names

    def test_traditional_subagents_have_paradigm_mapper(self):
        """Ayurveda and TCM subagents should have paradigm_mapper."""
        traditional_agents = [ayurveda_subagent, tcm_subagent]

        for agent in traditional_agents:
            tool_names = [t.name for t in agent["tools"]]
            assert "paradigm_mapper" in tool_names

    def test_synthesis_subagent_has_synthesis_reporter(self):
        """Synthesis subagent should have synthesis_reporter tool."""
        tool_names = [t.name for t in synthesis_subagent["tools"]]
        assert "synthesis_reporter" in tool_names

    def test_subagent_names_are_unique(self):
        """All subagent names should be unique."""
        all_agents = [
            allopathy_subagent,
            naturopathy_subagent,
            ayurveda_subagent,
            tcm_subagent,
            synthesis_subagent,
        ]

        names = [agent["name"] for agent in all_agents]
        assert len(names) == len(set(names))


class TestSubagentPrompts:
    """Tests for subagent system prompts."""

    def test_allopathy_prompt_mentions_evidence(self):
        """Allopathy prompt should emphasize evidence-based approach."""
        prompt = allopathy_subagent["system_prompt"]
        assert "evidence" in prompt.lower()
        assert "rct" in prompt.lower() or "randomized" in prompt.lower()

    def test_naturopathy_prompt_mentions_principles(self):
        """Naturopathy prompt should mention core principles."""
        prompt = naturopathy_subagent["system_prompt"]
        assert "vis medicatrix" in prompt.lower() or "healing power" in prompt.lower()

    def test_ayurveda_prompt_mentions_dosha(self):
        """Ayurveda prompt should mention dosha theory."""
        prompt = ayurveda_subagent["system_prompt"]
        assert "dosha" in prompt.lower()
        assert "vata" in prompt.lower() or "pitta" in prompt.lower() or "kapha" in prompt.lower()

    def test_ayurveda_prompt_mentions_bhasma(self):
        """Ayurveda prompt should mention bhasma preparations."""
        prompt = ayurveda_subagent["system_prompt"]
        assert "bhasma" in prompt.lower()

    def test_tcm_prompt_mentions_five_elements(self):
        """TCM prompt should mention Five Element theory."""
        prompt = tcm_subagent["system_prompt"]
        assert "five element" in prompt.lower() or "wu xing" in prompt.lower()

    def test_tcm_prompt_mentions_patterns(self):
        """TCM prompt should mention pattern diagnosis."""
        prompt = tcm_subagent["system_prompt"]
        assert "spleen" in prompt.lower() or "kidney" in prompt.lower()

    def test_synthesis_prompt_mentions_consensus(self):
        """Synthesis prompt should mention consensus scoring."""
        prompt = synthesis_subagent["system_prompt"]
        assert "consensus" in prompt.lower()

    def test_all_prompts_have_output_format(self):
        """All prompts should specify output format."""
        all_agents = [
            allopathy_subagent,
            naturopathy_subagent,
            ayurveda_subagent,
            tcm_subagent,
            synthesis_subagent,
        ]

        for agent in all_agents:
            assert "output" in agent["system_prompt"].lower()

    def test_all_prompts_have_what_not_to_do(self):
        """All prompts should have safety guidelines."""
        all_agents = [
            allopathy_subagent,
            naturopathy_subagent,
            ayurveda_subagent,
            tcm_subagent,
            synthesis_subagent,
        ]

        for agent in all_agents:
            assert "not to do" in agent["system_prompt"].lower() or "don't" in agent["system_prompt"].lower()
