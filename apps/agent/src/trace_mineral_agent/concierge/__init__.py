"""ConciergeHealthAgent - Personalized health research for concierge medicine.

This module provides a specialized agent for concierge medicine practices,
offering personalized health research, evidence-based recommendations,
and comprehensive care planning.

Key Features:
- Multi-paradigm health research (Western, Traditional, Naturopathic)
- Personalized wellness assessments
- Evidence-graded recommendations
- Comprehensive care plan generation
- Drug-supplement interaction checking

Usage:
    from trace_mineral_agent.concierge import concierge_agent

    # Use via LangGraph API
    result = concierge_agent.invoke({
        "messages": [{"role": "user", "content": "Your health question"}]
    })

    # Or run in CLI mode
    from trace_mineral_agent.concierge.agent import main
    main()
"""

from .agent import concierge_agent, create_concierge_agent
from .prompts import CONCIERGE_QUICK_QUESTIONS, CONCIERGE_SYSTEM_PROMPT
from .subagents import (
    care_coordinator_subagent,
    patient_advisor_subagent,
    wellness_researcher_subagent,
)
from .tools import care_plan_generator, wellness_assessment

__all__ = [
    # Main agent
    "concierge_agent",
    "create_concierge_agent",
    # Prompts
    "CONCIERGE_SYSTEM_PROMPT",
    "CONCIERGE_QUICK_QUESTIONS",
    # Subagents
    "patient_advisor_subagent",
    "wellness_researcher_subagent",
    "care_coordinator_subagent",
    # Tools
    "wellness_assessment",
    "care_plan_generator",
]
