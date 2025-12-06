"""Main agent entry point for TraceMineralDiscoveryAgent."""

import os

from deepagents import create_deep_agent

from .observability import configure_langsmith, is_tracing_enabled, trace_research_query
from .prompts import QUICK_QUESTIONS, TRACE_MINERAL_SYSTEM_PROMPT, print_welcome
from .subagents import (
    allopathy_subagent,
    ayurveda_subagent,
    naturopathy_subagent,
    synthesis_subagent,
    tcm_subagent,
)
from .tools import (
    check_drug_interactions,
    evidence_grade,
    list_mineral_interactions,
    literature_search,
    paradigm_mapper,
    synthesis_reporter,
)

# Configure LangSmith if API key is present
configure_langsmith()


def create_trace_mineral_agent(
    model: str = "anthropic:claude-sonnet-4-5-20250929",
    use_memory: bool = True,
):
    """
    Create the TraceMineralDiscoveryAgent.

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
            literature_search,
            evidence_grade,
            paradigm_mapper,
            synthesis_reporter,
            check_drug_interactions,
            list_mineral_interactions,
        ],
        subagents=[
            allopathy_subagent,
            naturopathy_subagent,
            ayurveda_subagent,
            tcm_subagent,
            synthesis_subagent,
        ],
        system_prompt=TRACE_MINERAL_SYSTEM_PROMPT,
        checkpointer=True if (use_memory and not running_in_langgraph_api) else None,
    )


# Create the default agent instance for LangGraph deployment
agent = create_trace_mineral_agent()


def main() -> None:
    """Run the agent in interactive mode."""
    print_welcome()

    # Show tracing status
    if is_tracing_enabled():
        print("  [LangSmith tracing enabled]\n")

    while True:
        try:
            user_input = input("\n You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n Goodbye! Keep researching!")
                break

            # Handle quick picks
            if user_input in QUICK_QUESTIONS:
                user_input = QUICK_QUESTIONS[user_input]
                print(f" Quick pick: {user_input}\n")

            # Process the question with optional tracing
            with trace_research_query(query=user_input):
                result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

            print("\n TraceMineralDiscoveryAgent:")
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
