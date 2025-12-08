"""SkinIntelligence Agent module for evidence-based skincare guidance.

This module provides a specialized agent for personalized skincare recommendations,
ingredient analysis, routine building, and trend validation - designed for consumers
who want science-backed skincare guidance beyond generic TikTok advice.

Target Demographics:
- Skintellectuals (ingredient-obsessed, science-first)
- Problem-Skin Sufferers (acne, rosacea, hyperpigmentation)
- Preventive Agers (optimizing before damage)
- Budget Hunters (finding effective alternatives)
"""

from trace_mineral_agent.skincare.agent import (
    create_skin_intelligence_agent,
    skin_intelligence_agent,
)
from trace_mineral_agent.skincare.prompts import (
    SKINCARE_QUICK_QUESTIONS,
    SKINCARE_SYSTEM_PROMPT,
)
from trace_mineral_agent.skincare.subagents import (
    ingredient_analyst_subagent,
    routine_architect_subagent,
    trend_validator_subagent,
)
from trace_mineral_agent.skincare.tools import (
    ingredient_analyzer,
    routine_builder,
    skin_profile_assessment,
    trend_evaluator,
)

__all__ = [
    # Agent
    "skin_intelligence_agent",
    "create_skin_intelligence_agent",
    # Prompts
    "SKINCARE_SYSTEM_PROMPT",
    "SKINCARE_QUICK_QUESTIONS",
    # Subagents
    "ingredient_analyst_subagent",
    "routine_architect_subagent",
    "trend_validator_subagent",
    # Tools
    "skin_profile_assessment",
    "ingredient_analyzer",
    "routine_builder",
    "trend_evaluator",
]
