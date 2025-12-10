"""Streaming support for real-time research feedback."""

import asyncio
from collections.abc import AsyncIterator
from typing import Any

from .observability import is_tracing_enabled, trace_research_query

# Progress event types
PROGRESS_EVENTS = {
    "research_started": "Starting research query...",
    "paradigm_research_started": "Researching {paradigm} perspective...",
    "paradigm_research_completed": "{paradigm} research complete (Grade: {grade})",
    "tool_started": "Using {tool_name}...",
    "tool_completed": "{tool_name} complete",
    "synthesis_started": "Synthesizing cross-paradigm findings...",
    "report_generated": "Report generated",
}

# Paradigm emoji mapping
PARADIGM_ICONS = {
    "allopathy": "🔬",
    "naturopathy": "🌿",
    "ayurveda": "🕉️",
    "tcm": "☯️",
    "unani": "🏛️",
    "siddha": "🔱",
    "synthesis": "🔄",
}


def get_paradigm_icon(paradigm: str) -> str:
    """Get emoji icon for a paradigm."""
    return PARADIGM_ICONS.get(paradigm.lower(), "📋")


async def stream_research(
    agent: Any,
    query: str,
    print_output: bool = True,
) -> AsyncIterator[dict]:
    """
    Stream research progress with real-time feedback.

    Args:
        agent: The configured agent instance
        query: Research query to process
        print_output: Whether to print progress to stdout

    Yields:
        Progress events as dictionaries
    """
    # Wrap in trace context if enabled
    with trace_research_query(query=query):
        yield {"event": "research_started", "data": {"query": query}}
        if print_output:
            print(f"\n🔍 {PROGRESS_EVENTS['research_started']}")
            print(f"   Query: {query}\n")

        async for event in agent.astream_events(
            {"messages": [{"role": "user", "content": query}]},
            version="v2",
        ):
            event_type = event.get("event", "")
            event_name = event.get("name", "")
            event_data = event.get("data", {})

            # Handle tool/subagent start events
            if event_type == "on_tool_start":
                tool_name = event_name

                # Check if this is a paradigm-specific subagent
                for paradigm in PARADIGM_ICONS:
                    if paradigm in tool_name.lower():
                        yield {
                            "event": "paradigm_research_started",
                            "data": {"paradigm": paradigm},
                        }
                        if print_output:
                            icon = get_paradigm_icon(paradigm)
                            print(f"  {icon} Researching {paradigm.title()}...")
                        break
                else:
                    yield {
                        "event": "tool_started",
                        "data": {"tool_name": tool_name},
                    }
                    if print_output:
                        print(f"  🔧 Using {tool_name}...")

            # Handle tool/subagent end events
            elif event_type == "on_tool_end":
                tool_name = event_name
                output = event_data.get("output", "")

                # Check for paradigm completion
                for paradigm in PARADIGM_ICONS:
                    if paradigm in tool_name.lower():
                        # Try to extract grade from output
                        grade = "—"
                        if "Grade" in str(output):
                            for letter in ["A", "B", "C", "D"]:
                                if f"Grade {letter}" in str(output) or f"Grade: {letter}" in str(output):
                                    grade = letter
                                    break

                        yield {
                            "event": "paradigm_research_completed",
                            "data": {"paradigm": paradigm, "grade": grade},
                        }
                        if print_output:
                            icon = get_paradigm_icon(paradigm)
                            print(f"  {icon} {paradigm.title()} complete (Grade: {grade})")
                        break
                else:
                    yield {
                        "event": "tool_completed",
                        "data": {"tool_name": tool_name},
                    }

            # Handle LLM streaming for real-time text output
            elif event_type == "on_llm_stream":
                chunk = event_data.get("chunk", {})
                content = getattr(chunk, "content", "") if hasattr(chunk, "content") else ""

                if content and print_output:
                    print(content, end="", flush=True)

                if content:
                    yield {
                        "event": "llm_chunk",
                        "data": {"content": content},
                    }

            # Handle chain end (synthesis complete)
            elif event_type == "on_chain_end" and "synthesis" in event_name.lower():
                yield {"event": "synthesis_started", "data": {}}
                if print_output:
                    print("\n  🔄 Synthesizing findings...")

        yield {"event": "report_generated", "data": {}}
        if print_output:
            print("\n\n✅ Research complete!")


async def run_streaming_cli(agent: Any) -> None:
    """
    Run the CLI in streaming mode.

    Args:
        agent: The configured agent instance
    """
    from .prompts import QUICK_QUESTIONS, print_welcome

    print_welcome()
    print("  [Streaming mode enabled]\n")

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

            # Stream the research
            print("\n TraceMineralDiscoveryAgent:")
            async for _ in stream_research(agent, user_input, print_output=True):
                pass  # Events are printed by stream_research

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


def main_streaming() -> None:
    """Entry point for streaming CLI mode."""
    from .agent import create_trace_mineral_agent

    agent = create_trace_mineral_agent()
    asyncio.run(run_streaming_cli(agent))
