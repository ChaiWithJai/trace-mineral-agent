"""Main agent entry point for SkinIntelligenceAgent."""

import os

from deepagents import create_deep_agent

from ..observability import configure_langsmith, is_tracing_enabled, trace_research_query
from ..tools import (
    evidence_grade,
    literature_search,
    paradigm_mapper,
    synthesis_reporter,
)
from .prompts import SKINCARE_QUICK_QUESTIONS, SKINCARE_SYSTEM_PROMPT
from .subagents import (
    ingredient_analyst_subagent,
    routine_architect_subagent,
    trend_validator_subagent,
)
from .tools import (
    ingredient_analyzer,
    routine_builder,
    skin_profile_assessment,
    trend_evaluator,
)

# Configure LangSmith if API key is present
configure_langsmith(project_name="skin-intelligence-agent")


def create_skin_intelligence_agent(
    model: str = "anthropic:claude-sonnet-4-5-20250929",
    use_memory: bool = True,
):
    """
    Create the SkinIntelligenceAgent.

    This agent provides evidence-based skincare guidance for consumers who want
    science, not marketing. It serves the Skintellectual demographic with deep
    ingredient analysis, personalized routines, and trend validation.

    Target Demographics:
    - Skintellectuals (ingredient-obsessed, science-first)
    - Problem-Skin Sufferers (acne, rosacea, hyperpigmentation)
    - Preventive Agers (optimizing before damage)
    - Budget Hunters (finding effective alternatives)

    Args:
        model: Model identifier to use (default: Claude Sonnet 4.5)
        use_memory: Whether to enable memory/checkpointing

    Returns:
        Configured deep agent instance
    """
    running_in_langgraph_api = os.getenv("LANGGRAPH_API_URL") is not None

    return create_deep_agent(
        model=model,
        tools=[
            # Core research tools (from main agent)
            literature_search,
            evidence_grade,
            paradigm_mapper,
            synthesis_reporter,
            # Skincare-specific tools
            skin_profile_assessment,
            ingredient_analyzer,
            routine_builder,
            trend_evaluator,
        ],
        subagents=[
            ingredient_analyst_subagent,
            routine_architect_subagent,
            trend_validator_subagent,
        ],
        system_prompt=SKINCARE_SYSTEM_PROMPT,
        checkpointer=True if (use_memory and not running_in_langgraph_api) else None,
    )


# Create the default agent instance for LangGraph deployment
skin_intelligence_agent = create_skin_intelligence_agent()


def print_skincare_welcome() -> None:
    """Print welcome message for SkinIntelligenceAgent."""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║              🧴 SkinIntelligenceAgent                                 ║
║                                                                       ║
║     Evidence-Based Skincare Guidance for the Skintellectual          ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  I help you understand:                                               ║
║  • HOW ingredients work (mechanisms, not marketing)                   ║
║  • WHAT the research says (evidence grades)                           ║
║  • HOW to build routines (layering, scheduling)                       ║
║  • WHETHER trends are valid (science vs hype)                         ║
║                                                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  Try asking:                                                          ║
║  • "Analyze retinol vs tretinoin vs retinal"                         ║
║  • "Build me a routine for oily, acne-prone skin"                    ║
║  • "Is slugging actually backed by science?"                          ║
║  • "What's the best vitamin C form for sensitive skin?"               ║
║                                                                       ║
║  Type 'quit' or 'exit' to end the session                            ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")


def main() -> None:
    """Run the skincare agent in interactive mode."""
    print_skincare_welcome()

    # Show tracing status
    if is_tracing_enabled():
        print("  [LangSmith tracing enabled]\n")

    while True:
        try:
            user_input = input("\n You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n Goodbye! May your skin barrier be strong! 🧴")
                break

            # Handle quick picks
            if user_input == "help":
                print(SKINCARE_QUICK_QUESTIONS)
                continue

            # Process the question with optional tracing
            with trace_research_query(query=user_input):
                result = skin_intelligence_agent.invoke(
                    {"messages": [{"role": "user", "content": user_input}]}
                )

            print("\n SkinIntelligenceAgent:")
            print(result["messages"][-1].content)

        except KeyboardInterrupt:
            print("\n\n Interrupted. Goodbye!")
            break
        except Exception as e:
            error_msg = str(e)
            if "API" in error_msg or "key" in error_msg.lower():
                print("\n  API connection issue. Check your API keys.")
            elif "rate" in error_msg.lower():
                print("\n  Rate limited. Please wait a moment and try again.")
            else:
                print(f"\n  Something went wrong: {e}")


if __name__ == "__main__":
    main()
