"""Unit tests for the SkinIntelligence agent configuration."""

import pytest


class TestSkincareModuleExports:
    """Tests for skincare module exports."""

    def test_main_module_exports(self):
        """Test that main skincare module exports expected items."""
        from trace_mineral_agent.skincare import (
            SKINCARE_QUICK_QUESTIONS,
            SKINCARE_SYSTEM_PROMPT,
            create_skin_intelligence_agent,
            ingredient_analyst_subagent,
            ingredient_analyzer,
            routine_architect_subagent,
            routine_builder,
            skin_intelligence_agent,
            skin_profile_assessment,
            trend_evaluator,
            trend_validator_subagent,
        )

        # Just verify imports work
        assert skin_intelligence_agent is not None
        assert create_skin_intelligence_agent is not None
        assert SKINCARE_SYSTEM_PROMPT is not None

    def test_tools_module_exports(self):
        """Test that tools module exports expected items."""
        from trace_mineral_agent.skincare.tools import (
            ingredient_analyzer,
            routine_builder,
            skin_profile_assessment,
            trend_evaluator,
        )

        assert skin_profile_assessment is not None
        assert ingredient_analyzer is not None
        assert routine_builder is not None
        assert trend_evaluator is not None

    def test_subagents_module_exports(self):
        """Test that subagents module exports expected items."""
        from trace_mineral_agent.skincare.subagents import (
            ingredient_analyst_subagent,
            routine_architect_subagent,
            trend_validator_subagent,
        )

        assert ingredient_analyst_subagent is not None
        assert routine_architect_subagent is not None
        assert trend_validator_subagent is not None


class TestSkincareSystemPrompt:
    """Tests for the skincare system prompt."""

    def test_system_prompt_exists(self):
        """Test that system prompt is defined."""
        from trace_mineral_agent.skincare import SKINCARE_SYSTEM_PROMPT

        assert SKINCARE_SYSTEM_PROMPT is not None
        assert len(SKINCARE_SYSTEM_PROMPT) > 100  # Should be substantial

    def test_system_prompt_defines_agent_identity(self):
        """Test that system prompt defines agent identity."""
        from trace_mineral_agent.skincare import SKINCARE_SYSTEM_PROMPT

        prompt_lower = SKINCARE_SYSTEM_PROMPT.lower()

        assert "skinintelligence" in prompt_lower or "skin intelligence" in prompt_lower

    def test_system_prompt_targets_skintellectual(self):
        """Test that system prompt targets Skintellectual audience."""
        from trace_mineral_agent.skincare import SKINCARE_SYSTEM_PROMPT

        prompt_lower = SKINCARE_SYSTEM_PROMPT.lower()

        assert "skintellectual" in prompt_lower
        assert "science" in prompt_lower
        assert "evidence" in prompt_lower

    def test_system_prompt_lists_tools(self):
        """Test that system prompt references available tools."""
        from trace_mineral_agent.skincare import SKINCARE_SYSTEM_PROMPT

        prompt_lower = SKINCARE_SYSTEM_PROMPT.lower()

        # Should mention the tools
        assert "skin_profile_assessment" in prompt_lower or "profile" in prompt_lower
        assert "ingredient_analyzer" in prompt_lower or "ingredient" in prompt_lower
        assert "routine_builder" in prompt_lower or "routine" in prompt_lower
        assert "trend_evaluator" in prompt_lower or "trend" in prompt_lower

    def test_system_prompt_lists_subagents(self):
        """Test that system prompt references subagents."""
        from trace_mineral_agent.skincare import SKINCARE_SYSTEM_PROMPT

        prompt_lower = SKINCARE_SYSTEM_PROMPT.lower()

        # Should mention subagent specializations
        assert "ingredient analyst" in prompt_lower
        assert "routine architect" in prompt_lower
        assert "trend validator" in prompt_lower

    def test_system_prompt_includes_disclaimers(self):
        """Test that system prompt includes appropriate disclaimers."""
        from trace_mineral_agent.skincare import SKINCARE_SYSTEM_PROMPT

        prompt_lower = SKINCARE_SYSTEM_PROMPT.lower()

        # Should have some form of disclaimer
        assert "dermatologist" in prompt_lower or "medical advice" in prompt_lower

    def test_system_prompt_emphasizes_spf(self):
        """Test that system prompt emphasizes sun protection."""
        from trace_mineral_agent.skincare import SKINCARE_SYSTEM_PROMPT

        prompt_lower = SKINCARE_SYSTEM_PROMPT.lower()

        assert "spf" in prompt_lower or "sunscreen" in prompt_lower
        assert "non-negotiable" in prompt_lower or "essential" in prompt_lower


class TestSkincareQuickQuestions:
    """Tests for quick questions."""

    def test_quick_questions_exist(self):
        """Test that quick questions are defined."""
        from trace_mineral_agent.skincare import SKINCARE_QUICK_QUESTIONS

        assert SKINCARE_QUICK_QUESTIONS is not None
        assert len(SKINCARE_QUICK_QUESTIONS) > 50  # Should have content

    def test_quick_questions_cover_categories(self):
        """Test that quick questions cover main categories."""
        from trace_mineral_agent.skincare import SKINCARE_QUICK_QUESTIONS

        questions_lower = SKINCARE_QUICK_QUESTIONS.lower()

        # Should cover main agent capabilities
        assert "ingredient" in questions_lower
        assert "routine" in questions_lower
        assert "trend" in questions_lower


class TestAgentFactoryFunction:
    """Tests for the agent factory function."""

    def test_factory_function_exists(self):
        """Test that factory function is defined."""
        from trace_mineral_agent.skincare import create_skin_intelligence_agent

        assert callable(create_skin_intelligence_agent)

    def test_factory_function_docstring(self):
        """Test that factory function has documentation."""
        from trace_mineral_agent.skincare import create_skin_intelligence_agent

        assert create_skin_intelligence_agent.__doc__ is not None
        assert len(create_skin_intelligence_agent.__doc__) > 50

    def test_factory_function_mentions_demographics(self):
        """Test that factory function mentions target demographics."""
        from trace_mineral_agent.skincare import create_skin_intelligence_agent

        doc = create_skin_intelligence_agent.__doc__.lower()

        # Should mention target demographics
        assert "skintellectual" in doc or "skin" in doc


class TestAgentInstance:
    """Tests for the default agent instance."""

    def test_default_agent_exists(self):
        """Test that default agent instance is created."""
        from trace_mineral_agent.skincare import skin_intelligence_agent

        assert skin_intelligence_agent is not None

    def test_agent_is_invocable(self):
        """Test that agent has invoke method."""
        from trace_mineral_agent.skincare import skin_intelligence_agent

        assert hasattr(skin_intelligence_agent, "invoke")


class TestLangGraphConfiguration:
    """Tests for LangGraph deployment configuration."""

    def test_langgraph_json_has_skincare_endpoint(self):
        """Test that langgraph.json includes skin-intelligence endpoint."""
        import json
        from pathlib import Path

        langgraph_path = Path(__file__).parent.parent.parent.parent / "langgraph.json"

        with open(langgraph_path) as f:
            config = json.load(f)

        assert "graphs" in config
        assert "skin-intelligence" in config["graphs"]
        assert "trace_mineral_agent.skincare.agent:skin_intelligence_agent" in config["graphs"]["skin-intelligence"]


class TestCLIEntryPoint:
    """Tests for CLI entry point configuration."""

    def test_cli_entry_point_defined(self):
        """Test that CLI entry point is defined in pyproject.toml."""
        import tomllib
        from pathlib import Path

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)

        assert "project" in config
        assert "scripts" in config["project"]
        assert "skin-intelligence-agent" in config["project"]["scripts"]

    def test_main_function_exists(self):
        """Test that main function exists for CLI."""
        from trace_mineral_agent.skincare.agent import main

        assert callable(main)
