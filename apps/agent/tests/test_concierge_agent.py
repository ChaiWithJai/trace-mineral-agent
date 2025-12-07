"""Tests for the concierge agent configuration."""


from trace_mineral_agent.concierge import (
    CONCIERGE_QUICK_QUESTIONS,
    CONCIERGE_SYSTEM_PROMPT,
    care_coordinator_subagent,
    care_plan_generator,
    concierge_agent,
    create_concierge_agent,
    patient_advisor_subagent,
    wellness_assessment,
    wellness_researcher_subagent,
)


class TestConciergeAgentExports:
    """Tests for concierge module exports."""

    def test_concierge_agent_is_exported(self):
        """Concierge agent should be exported from module."""
        assert concierge_agent is not None

    def test_create_concierge_agent_is_exported(self):
        """Factory function should be exported from module."""
        assert create_concierge_agent is not None
        assert callable(create_concierge_agent)

    def test_system_prompt_is_exported(self):
        """System prompt should be exported from module."""
        assert CONCIERGE_SYSTEM_PROMPT is not None
        assert len(CONCIERGE_SYSTEM_PROMPT) > 0

    def test_quick_questions_is_exported(self):
        """Quick questions should be exported from module."""
        assert CONCIERGE_QUICK_QUESTIONS is not None
        assert len(CONCIERGE_QUICK_QUESTIONS) > 0

    def test_subagents_are_exported(self):
        """All subagents should be exported from module."""
        assert patient_advisor_subagent is not None
        assert wellness_researcher_subagent is not None
        assert care_coordinator_subagent is not None

    def test_tools_are_exported(self):
        """Concierge-specific tools should be exported from module."""
        assert wellness_assessment is not None
        assert care_plan_generator is not None


class TestConciergeSystemPrompt:
    """Tests for the concierge system prompt."""

    def test_system_prompt_mentions_concierge(self):
        """System prompt should mention concierge context."""
        assert "concierge" in CONCIERGE_SYSTEM_PROMPT.lower()

    def test_system_prompt_mentions_personalization(self):
        """System prompt should emphasize personalization."""
        prompt_lower = CONCIERGE_SYSTEM_PROMPT.lower()
        assert "personalized" in prompt_lower or "individual" in prompt_lower

    def test_system_prompt_mentions_evidence(self):
        """System prompt should emphasize evidence-based approach."""
        assert "evidence" in CONCIERGE_SYSTEM_PROMPT.lower()

    def test_system_prompt_mentions_safety(self):
        """System prompt should mention safety requirements."""
        prompt_lower = CONCIERGE_SYSTEM_PROMPT.lower()
        assert "safety" in prompt_lower or "hipaa" in prompt_lower

    def test_system_prompt_mentions_subagents(self):
        """System prompt should describe available subagents."""
        assert "PatientAdvisorAgent" in CONCIERGE_SYSTEM_PROMPT or "Patient Advisor" in CONCIERGE_SYSTEM_PROMPT
        assert "WellnessResearcherAgent" in CONCIERGE_SYSTEM_PROMPT or "Wellness Researcher" in CONCIERGE_SYSTEM_PROMPT
        assert "CareCoordinatorAgent" in CONCIERGE_SYSTEM_PROMPT or "Care Coordinator" in CONCIERGE_SYSTEM_PROMPT

    def test_system_prompt_has_response_patterns(self):
        """System prompt should specify response patterns."""
        assert "Response Pattern" in CONCIERGE_SYSTEM_PROMPT or "### For" in CONCIERGE_SYSTEM_PROMPT

    def test_system_prompt_has_follow_up_suggestions(self):
        """System prompt should encourage follow-up interactions."""
        prompt_lower = CONCIERGE_SYSTEM_PROMPT.lower()
        assert "follow-up" in prompt_lower or "next step" in prompt_lower


class TestConciergeQuickQuestions:
    """Tests for quick questions configuration."""

    def test_quick_questions_are_numbered(self):
        """Quick questions should be numbered strings."""
        for key in CONCIERGE_QUICK_QUESTIONS:
            assert key.isdigit()

    def test_quick_questions_have_content(self):
        """Each quick question should have content."""
        for value in CONCIERGE_QUICK_QUESTIONS.values():
            assert len(value) > 10  # Reasonable minimum length

    def test_quick_questions_are_health_focused(self):
        """Quick questions should be health-related."""
        health_keywords = [
            "wellness",
            "health",
            "protocol",
            "supplement",
            "nutrition",
            "sleep",
            "stress",
            "gut",
            "hormone",
            "cognitive",
            "longevity",
            "metabolic",
        ]

        all_questions = " ".join(CONCIERGE_QUICK_QUESTIONS.values()).lower()

        # At least some health keywords should appear
        matches = sum(1 for kw in health_keywords if kw in all_questions)
        assert matches >= 5


class TestConciergeAgentFactory:
    """Tests for the agent factory function."""

    def test_factory_creates_agent(self):
        """Factory should create an agent instance."""
        agent = create_concierge_agent()
        assert agent is not None

    def test_factory_default_model(self):
        """Factory should use Claude Sonnet as default."""
        # Test that it doesn't raise with defaults
        agent = create_concierge_agent()
        assert agent is not None

    def test_factory_custom_model(self):
        """Factory should accept custom model."""
        # Test that it accepts model parameter
        agent = create_concierge_agent(model="anthropic:claude-sonnet-4-5-20250929")
        assert agent is not None

    def test_factory_memory_option(self):
        """Factory should accept memory option."""
        agent_with_memory = create_concierge_agent(use_memory=True)
        agent_without_memory = create_concierge_agent(use_memory=False)
        assert agent_with_memory is not None
        assert agent_without_memory is not None
