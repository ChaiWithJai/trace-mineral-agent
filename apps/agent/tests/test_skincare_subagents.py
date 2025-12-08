"""Unit tests for skincare subagents."""

import pytest

from trace_mineral_agent.skincare.subagents import (
    ingredient_analyst_subagent,
    routine_architect_subagent,
    trend_validator_subagent,
)


class TestIngredientAnalystSubagent:
    """Tests for the Ingredient Analyst subagent configuration."""

    def test_subagent_structure(self):
        """Test that subagent has required structure."""
        assert "name" in ingredient_analyst_subagent
        assert "description" in ingredient_analyst_subagent
        assert "system_prompt" in ingredient_analyst_subagent
        assert "tools" in ingredient_analyst_subagent

    def test_subagent_name(self):
        """Test subagent name format."""
        assert ingredient_analyst_subagent["name"] == "ingredient-analyst-agent"

    def test_subagent_description_content(self):
        """Test that description covers key capabilities."""
        desc = ingredient_analyst_subagent["description"].lower()

        assert "ingredient" in desc
        assert "mechanism" in desc or "analysis" in desc
        assert "evidence" in desc or "interaction" in desc

    def test_subagent_tools_assigned(self):
        """Test that appropriate tools are assigned."""
        tools = ingredient_analyst_subagent["tools"]
        tool_names = [t.name for t in tools]

        assert "ingredient_analyzer" in tool_names
        assert "literature_search" in tool_names
        assert "evidence_grade" in tool_names

    def test_system_prompt_content(self):
        """Test that system prompt covers key aspects."""
        prompt = ingredient_analyst_subagent["system_prompt"].lower()

        # Should mention key ingredient categories
        assert "retinoid" in prompt or "vitamin c" in prompt
        assert "mechanism" in prompt
        assert "evidence" in prompt
        assert "interaction" in prompt or "compatible" in prompt

    def test_system_prompt_skintellectual_focus(self):
        """Test that system prompt targets Skintellectual audience."""
        prompt = ingredient_analyst_subagent["system_prompt"].lower()

        # Should reference science-focused approach
        assert "science" in prompt or "scientific" in prompt
        assert "mechanism" in prompt or "how" in prompt


class TestRoutineArchitectSubagent:
    """Tests for the Routine Architect subagent configuration."""

    def test_subagent_structure(self):
        """Test that subagent has required structure."""
        assert "name" in routine_architect_subagent
        assert "description" in routine_architect_subagent
        assert "system_prompt" in routine_architect_subagent
        assert "tools" in routine_architect_subagent

    def test_subagent_name(self):
        """Test subagent name format."""
        assert routine_architect_subagent["name"] == "routine-architect-agent"

    def test_subagent_description_content(self):
        """Test that description covers key capabilities."""
        desc = routine_architect_subagent["description"].lower()

        assert "routine" in desc
        assert "am" in desc or "pm" in desc or "layering" in desc
        assert "personalized" in desc or "recommendation" in desc

    def test_subagent_tools_assigned(self):
        """Test that appropriate tools are assigned."""
        tools = routine_architect_subagent["tools"]
        tool_names = [t.name for t in tools]

        assert "routine_builder" in tool_names
        assert "skin_profile_assessment" in tool_names

    def test_system_prompt_layering_rules(self):
        """Test that system prompt covers layering rules."""
        prompt = routine_architect_subagent["system_prompt"].lower()

        assert "layering" in prompt or "layer" in prompt or "order" in prompt
        assert "sunscreen" in prompt or "spf" in prompt

    def test_system_prompt_scheduling_guidance(self):
        """Test that system prompt covers active scheduling."""
        prompt = routine_architect_subagent["system_prompt"].lower()

        # Should mention active scheduling concepts
        assert "retinoid" in prompt or "acid" in prompt
        assert "schedule" in prompt or "rotation" in prompt or "alternating" in prompt

    def test_system_prompt_sustainability_focus(self):
        """Test that system prompt emphasizes sustainability."""
        prompt = routine_architect_subagent["system_prompt"].lower()

        assert "sustainable" in prompt or "consistency" in prompt


class TestTrendValidatorSubagent:
    """Tests for the Trend Validator subagent configuration."""

    def test_subagent_structure(self):
        """Test that subagent has required structure."""
        assert "name" in trend_validator_subagent
        assert "description" in trend_validator_subagent
        assert "system_prompt" in trend_validator_subagent
        assert "tools" in trend_validator_subagent

    def test_subagent_name(self):
        """Test subagent name format."""
        assert trend_validator_subagent["name"] == "trend-validator-agent"

    def test_subagent_description_content(self):
        """Test that description covers key capabilities."""
        desc = trend_validator_subagent["description"].lower()

        assert "trend" in desc
        assert "tiktok" in desc or "viral" in desc or "social" in desc
        assert "evidence" in desc or "science" in desc or "valid" in desc

    def test_subagent_tools_assigned(self):
        """Test that appropriate tools are assigned."""
        tools = trend_validator_subagent["tools"]
        tool_names = [t.name for t in tools]

        assert "trend_evaluator" in tool_names
        assert "literature_search" in tool_names
        assert "evidence_grade" in tool_names

    def test_system_prompt_verdict_categories(self):
        """Test that system prompt defines verdict categories."""
        prompt = trend_validator_subagent["system_prompt"]

        # Should define verdict types
        assert "VALIDATED" in prompt or "validated" in prompt.lower()
        assert "HARMFUL" in prompt or "harmful" in prompt.lower()
        assert "MIXED" in prompt or "mixed" in prompt.lower()

    def test_system_prompt_red_flags(self):
        """Test that system prompt identifies red flags."""
        prompt = trend_validator_subagent["system_prompt"].lower()

        assert "red flag" in prompt or "warning" in prompt
        assert "detox" in prompt or "natural" in prompt  # Common false claims

    def test_system_prompt_evidence_focus(self):
        """Test that system prompt emphasizes evidence."""
        prompt = trend_validator_subagent["system_prompt"].lower()

        assert "evidence" in prompt
        assert "peer-reviewed" in prompt or "study" in prompt or "research" in prompt


class TestSubagentConsistency:
    """Tests for consistency across all subagents."""

    def test_all_subagents_have_same_structure(self):
        """Test that all subagents have consistent structure."""
        subagents = [
            ingredient_analyst_subagent,
            routine_architect_subagent,
            trend_validator_subagent,
        ]

        required_keys = {"name", "description", "system_prompt", "tools"}

        for subagent in subagents:
            assert set(subagent.keys()) >= required_keys

    def test_all_subagent_names_follow_pattern(self):
        """Test that all subagent names follow naming convention."""
        subagents = [
            ingredient_analyst_subagent,
            routine_architect_subagent,
            trend_validator_subagent,
        ]

        for subagent in subagents:
            name = subagent["name"]
            assert "-agent" in name
            assert name.islower() or "-" in name

    def test_all_subagents_have_tools(self):
        """Test that all subagents have at least one tool."""
        subagents = [
            ingredient_analyst_subagent,
            routine_architect_subagent,
            trend_validator_subagent,
        ]

        for subagent in subagents:
            assert len(subagent["tools"]) >= 1

    def test_no_duplicate_subagent_names(self):
        """Test that subagent names are unique."""
        names = [
            ingredient_analyst_subagent["name"],
            routine_architect_subagent["name"],
            trend_validator_subagent["name"],
        ]

        assert len(names) == len(set(names))


class TestSubagentToolCompatibility:
    """Tests for tool-subagent compatibility."""

    def test_ingredient_analyst_has_analysis_tool(self):
        """Test that Ingredient Analyst has ingredient analysis capability."""
        tools = ingredient_analyst_subagent["tools"]
        tool_names = [t.name for t in tools]

        assert "ingredient_analyzer" in tool_names

    def test_routine_architect_has_builder_tool(self):
        """Test that Routine Architect has routine building capability."""
        tools = routine_architect_subagent["tools"]
        tool_names = [t.name for t in tools]

        assert "routine_builder" in tool_names

    def test_trend_validator_has_evaluator_tool(self):
        """Test that Trend Validator has trend evaluation capability."""
        tools = trend_validator_subagent["tools"]
        tool_names = [t.name for t in tools]

        assert "trend_evaluator" in tool_names

    def test_research_tools_shared_appropriately(self):
        """Test that research tools are shared where needed."""
        # Both analyst and validator need research capabilities
        analyst_tools = [t.name for t in ingredient_analyst_subagent["tools"]]
        validator_tools = [t.name for t in trend_validator_subagent["tools"]]

        # Both should have literature search for evidence
        assert "literature_search" in analyst_tools
        assert "literature_search" in validator_tools

        # Both should have evidence grading
        assert "evidence_grade" in analyst_tools
        assert "evidence_grade" in validator_tools
