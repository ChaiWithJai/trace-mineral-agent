"""Tests for the concierge subagent configurations."""


from trace_mineral_agent.concierge.subagents import (
    care_coordinator_subagent,
    patient_advisor_subagent,
    wellness_researcher_subagent,
)


class TestConciergeSubagentConfiguration:
    """Tests for concierge subagent structure and configuration."""

    def test_patient_advisor_subagent_has_required_fields(self):
        """Patient advisor subagent should have all required fields."""
        assert "name" in patient_advisor_subagent
        assert "description" in patient_advisor_subagent
        assert "system_prompt" in patient_advisor_subagent
        assert "tools" in patient_advisor_subagent

    def test_wellness_researcher_subagent_has_required_fields(self):
        """Wellness researcher subagent should have all required fields."""
        assert "name" in wellness_researcher_subagent
        assert "description" in wellness_researcher_subagent
        assert "system_prompt" in wellness_researcher_subagent
        assert "tools" in wellness_researcher_subagent

    def test_care_coordinator_subagent_has_required_fields(self):
        """Care coordinator subagent should have all required fields."""
        assert "name" in care_coordinator_subagent
        assert "description" in care_coordinator_subagent
        assert "system_prompt" in care_coordinator_subagent
        assert "tools" in care_coordinator_subagent

    def test_patient_advisor_has_literature_search(self):
        """Patient advisor should have literature_search tool."""
        tool_names = [t.name for t in patient_advisor_subagent["tools"]]
        assert "literature_search" in tool_names

    def test_patient_advisor_has_drug_interactions(self):
        """Patient advisor should have check_drug_interactions tool."""
        tool_names = [t.name for t in patient_advisor_subagent["tools"]]
        assert "check_drug_interactions" in tool_names

    def test_wellness_researcher_has_literature_search(self):
        """Wellness researcher should have literature_search tool."""
        tool_names = [t.name for t in wellness_researcher_subagent["tools"]]
        assert "literature_search" in tool_names

    def test_wellness_researcher_has_paradigm_mapper(self):
        """Wellness researcher should have paradigm_mapper tool."""
        tool_names = [t.name for t in wellness_researcher_subagent["tools"]]
        assert "paradigm_mapper" in tool_names

    def test_care_coordinator_has_synthesis_reporter(self):
        """Care coordinator should have synthesis_reporter tool."""
        tool_names = [t.name for t in care_coordinator_subagent["tools"]]
        assert "synthesis_reporter" in tool_names

    def test_concierge_subagent_names_are_unique(self):
        """All concierge subagent names should be unique."""
        all_agents = [
            patient_advisor_subagent,
            wellness_researcher_subagent,
            care_coordinator_subagent,
        ]

        names = [agent["name"] for agent in all_agents]
        assert len(names) == len(set(names))


class TestConciergeSubagentPrompts:
    """Tests for concierge subagent system prompts."""

    def test_patient_advisor_prompt_mentions_personalization(self):
        """Patient advisor prompt should emphasize personalization."""
        prompt = patient_advisor_subagent["system_prompt"]
        assert "personalized" in prompt.lower() or "individual" in prompt.lower()

    def test_patient_advisor_prompt_mentions_safety(self):
        """Patient advisor prompt should mention safety considerations."""
        prompt = patient_advisor_subagent["system_prompt"]
        assert "safety" in prompt.lower() or "contraindication" in prompt.lower()

    def test_wellness_researcher_prompt_mentions_multi_paradigm(self):
        """Wellness researcher prompt should mention multi-paradigm approach."""
        prompt = wellness_researcher_subagent["system_prompt"]
        assert "paradigm" in prompt.lower()
        assert "allopathy" in prompt.lower() or "western" in prompt.lower()

    def test_wellness_researcher_prompt_mentions_evidence_grading(self):
        """Wellness researcher prompt should mention evidence grading."""
        prompt = wellness_researcher_subagent["system_prompt"]
        assert "grade" in prompt.lower() or "evidence" in prompt.lower()

    def test_care_coordinator_prompt_mentions_care_plan(self):
        """Care coordinator prompt should mention care plan development."""
        prompt = care_coordinator_subagent["system_prompt"]
        assert "care plan" in prompt.lower() or "protocol" in prompt.lower()

    def test_care_coordinator_prompt_mentions_monitoring(self):
        """Care coordinator prompt should mention monitoring protocols."""
        prompt = care_coordinator_subagent["system_prompt"]
        assert "monitor" in prompt.lower()

    def test_all_concierge_prompts_have_output_format(self):
        """All concierge prompts should specify output format."""
        all_agents = [
            patient_advisor_subagent,
            wellness_researcher_subagent,
            care_coordinator_subagent,
        ]

        for agent in all_agents:
            assert "output" in agent["system_prompt"].lower()

    def test_all_concierge_prompts_have_safety_guidelines(self):
        """All concierge prompts should have safety guidelines."""
        all_agents = [
            patient_advisor_subagent,
            wellness_researcher_subagent,
            care_coordinator_subagent,
        ]

        for agent in all_agents:
            prompt = agent["system_prompt"].lower()
            assert "not to do" in prompt or "don't" in prompt or "what not" in prompt
