"""Batch hypothesis processing for comprehensive mineral screening."""

import asyncio
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class Hypothesis(BaseModel):
    """A research hypothesis for batch processing."""

    mineral: str = Field(description="The trace mineral being studied")
    hypothesis: str = Field(description="The research hypothesis to investigate")
    target_outcomes: list[str] = Field(
        default_factory=list, description="Target outcome measures"
    )


class HypothesisResult(BaseModel):
    """Results from processing a single hypothesis."""

    mineral: str
    hypothesis: str
    consensus_score: float = Field(
        ge=0.0, le=1.0, description="Cross-paradigm consensus score (0-1)"
    )
    rank: int = Field(default=0, description="Ranking among all hypotheses")
    paradigm_grades: dict[str, str] = Field(
        default_factory=dict, description="Evidence grades by paradigm"
    )
    key_findings: dict[str, str] = Field(
        default_factory=dict, description="Key findings by paradigm"
    )
    target_outcomes: list[str] = Field(default_factory=list)
    research_gaps: list[str] = Field(default_factory=list)


class BatchResults(BaseModel):
    """Results from batch hypothesis processing."""

    results: list[HypothesisResult]
    summary: str = Field(description="Executive summary of all findings")
    processed_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp of processing",
    )
    total_hypotheses: int
    processing_time_seconds: float = 0.0


def load_hypotheses(input_path: str | Path) -> list[Hypothesis]:
    """
    Load hypotheses from JSON or CSV file.

    Args:
        input_path: Path to input file (JSON or CSV)

    Returns:
        List of Hypothesis objects
    """
    path = Path(input_path)

    if path.suffix.lower() == ".json":
        with open(path) as f:
            data = json.load(f)
        # Handle both list format and dict with "hypotheses" key
        hypotheses_data = data if isinstance(data, list) else data.get("hypotheses", [])
        return [Hypothesis(**h) for h in hypotheses_data]

    elif path.suffix.lower() == ".csv":
        hypotheses = []
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse target_outcomes from comma-separated string
                outcomes = row.get("target_outcomes", "")
                if isinstance(outcomes, str):
                    outcomes = [o.strip() for o in outcomes.split(",") if o.strip()]

                hypotheses.append(
                    Hypothesis(
                        mineral=row["mineral"],
                        hypothesis=row["hypothesis"],
                        target_outcomes=outcomes,
                    )
                )
        return hypotheses

    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def save_results(results: BatchResults, output_path: str | Path) -> None:
    """
    Save batch results to JSON or CSV file.

    Args:
        results: BatchResults object
        output_path: Path to output file
    """
    path = Path(output_path)

    if path.suffix.lower() == ".json":
        with open(path, "w") as f:
            json.dump(results.model_dump(), f, indent=2)

    elif path.suffix.lower() == ".csv":
        with open(path, "w", newline="") as f:
            if results.results:
                fieldnames = [
                    "rank",
                    "mineral",
                    "hypothesis",
                    "consensus_score",
                    "allopathy_grade",
                    "naturopathy_grade",
                    "ayurveda_grade",
                    "tcm_grade",
                    "target_outcomes",
                    "research_gaps",
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in results.results:
                    writer.writerow(
                        {
                            "rank": r.rank,
                            "mineral": r.mineral,
                            "hypothesis": r.hypothesis,
                            "consensus_score": r.consensus_score,
                            "allopathy_grade": r.paradigm_grades.get("allopathy", "-"),
                            "naturopathy_grade": r.paradigm_grades.get(
                                "naturopathy", "-"
                            ),
                            "ayurveda_grade": r.paradigm_grades.get("ayurveda", "-"),
                            "tcm_grade": r.paradigm_grades.get("tcm", "-"),
                            "target_outcomes": ", ".join(r.target_outcomes),
                            "research_gaps": "; ".join(r.research_gaps),
                        }
                    )
    else:
        raise ValueError(f"Unsupported output format: {path.suffix}")


def _grade_to_score(grade: str) -> float:
    """Convert letter grade to numeric score."""
    grade_map = {"A": 1.0, "B": 0.75, "C": 0.5, "D": 0.25, "F": 0.0}
    return grade_map.get(grade.upper(), 0.5)


def _extract_grade_from_response(response: str) -> str:
    """Extract evidence grade from agent response."""
    response_upper = response.upper()
    for grade in ["A", "B", "C", "D"]:
        if f"GRADE {grade}" in response_upper or f"GRADE: {grade}" in response_upper:
            return grade
    # Default to C if no grade found
    return "C"


def _extract_key_finding(response: str, paradigm: str) -> str:
    """Extract key finding summary from response."""
    # Take first 200 chars as summary
    clean = response.strip()
    if len(clean) > 200:
        return clean[:197] + "..."
    return clean


async def process_hypothesis(
    agent: Any,
    hypothesis: Hypothesis,
    print_progress: bool = False,
) -> HypothesisResult:
    """
    Process a single hypothesis through the agent.

    Args:
        agent: The configured agent instance
        hypothesis: Hypothesis to process
        print_progress: Whether to print progress

    Returns:
        HypothesisResult with findings
    """
    if print_progress:
        print(f"  Processing: {hypothesis.mineral} - {hypothesis.hypothesis[:50]}...")

    # Build the research query
    query = f"""
    Research hypothesis: {hypothesis.hypothesis}
    Mineral: {hypothesis.mineral}
    Target outcomes: {', '.join(hypothesis.target_outcomes) or 'general efficacy'}

    Please investigate this hypothesis across all paradigms and provide:
    1. Evidence grade from each paradigm (A/B/C/D)
    2. Key findings from each paradigm
    3. Research gaps identified
    4. Overall assessment
    """

    # Run the agent
    result = await asyncio.to_thread(
        agent.invoke, {"messages": [{"role": "user", "content": query}]}
    )

    response = result["messages"][-1].content

    # Parse paradigm grades and findings from response
    paradigm_grades = {}
    key_findings = {}
    research_gaps = []

    paradigms = ["allopathy", "naturopathy", "ayurveda", "tcm"]

    # Simple parsing - look for paradigm mentions and grades
    response_lower = response.lower()
    for paradigm in paradigms:
        if paradigm in response_lower:
            paradigm_grades[paradigm] = _extract_grade_from_response(response)
            key_findings[paradigm] = _extract_key_finding(response, paradigm)
        else:
            paradigm_grades[paradigm] = "C"  # Default
            key_findings[paradigm] = "No specific findings"

    # Calculate consensus score
    scores = [_grade_to_score(g) for g in paradigm_grades.values()]
    consensus_score = sum(scores) / len(scores) if scores else 0.5

    # Extract research gaps
    if "gap" in response_lower or "further research" in response_lower:
        research_gaps.append("Further research recommended")
    if "limited" in response_lower:
        research_gaps.append("Limited evidence available")

    return HypothesisResult(
        mineral=hypothesis.mineral,
        hypothesis=hypothesis.hypothesis,
        consensus_score=consensus_score,
        paradigm_grades=paradigm_grades,
        key_findings=key_findings,
        target_outcomes=hypothesis.target_outcomes,
        research_gaps=research_gaps,
    )


async def run_batch(
    agent: Any,
    hypotheses: list[Hypothesis],
    max_concurrent: int = 3,
    print_progress: bool = True,
) -> BatchResults:
    """
    Process multiple hypotheses in batch mode.

    Args:
        agent: The configured agent instance
        hypotheses: List of hypotheses to process
        max_concurrent: Maximum concurrent processing tasks
        print_progress: Whether to print progress

    Returns:
        BatchResults with all findings
    """
    import time

    start_time = time.time()

    if print_progress:
        print(f"\nProcessing {len(hypotheses)} hypotheses...")
        print(f"Max concurrent: {max_concurrent}\n")

    # Process in batches to limit concurrency
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_with_limit(h: Hypothesis) -> HypothesisResult:
        async with semaphore:
            return await process_hypothesis(agent, h, print_progress)

    # Run all hypotheses
    tasks = [process_with_limit(h) for h in hypotheses]
    results = await asyncio.gather(*tasks)

    # Sort by consensus score and assign ranks
    sorted_results = sorted(results, key=lambda r: r.consensus_score, reverse=True)
    for i, result in enumerate(sorted_results, 1):
        result.rank = i

    # Generate summary
    if sorted_results:
        top_result = sorted_results[0]
        summary = (
            f"{top_result.mineral.title()} shows highest cross-paradigm consensus "
            f"(score: {top_result.consensus_score:.2f}) for '{top_result.hypothesis}'. "
            f"Processed {len(hypotheses)} hypotheses total."
        )
    else:
        summary = "No hypotheses processed."

    processing_time = time.time() - start_time

    if print_progress:
        print(f"\nBatch processing complete in {processing_time:.1f}s")
        print(f"Top result: {sorted_results[0].mineral if sorted_results else 'N/A'}")

    return BatchResults(
        results=sorted_results,
        summary=summary,
        total_hypotheses=len(hypotheses),
        processing_time_seconds=processing_time,
    )


def main_batch() -> None:
    """CLI entry point for batch processing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Batch process trace mineral research hypotheses"
    )
    parser.add_argument(
        "--input", "-i", required=True, help="Input file path (JSON or CSV)"
    )
    parser.add_argument(
        "--output", "-o", required=True, help="Output file path (JSON or CSV)"
    )
    parser.add_argument(
        "--max-concurrent",
        "-c",
        type=int,
        default=3,
        help="Maximum concurrent hypotheses to process",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress progress output"
    )

    args = parser.parse_args()

    # Load hypotheses
    print(f"Loading hypotheses from {args.input}...")
    hypotheses = load_hypotheses(args.input)
    print(f"Loaded {len(hypotheses)} hypotheses")

    # Create agent
    from .agent import create_trace_mineral_agent

    agent = create_trace_mineral_agent(use_memory=False)

    # Run batch processing
    results = asyncio.run(
        run_batch(
            agent,
            hypotheses,
            max_concurrent=args.max_concurrent,
            print_progress=not args.quiet,
        )
    )

    # Save results
    save_results(results, args.output)
    print(f"\nResults saved to {args.output}")

    # Print summary
    print(f"\n{'='*50}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'='*50}")
    print(f"Total hypotheses: {results.total_hypotheses}")
    print(f"Processing time: {results.processing_time_seconds:.1f}s")
    print("\nTop 3 by consensus score:")
    for r in results.results[:3]:
        print(f"  {r.rank}. {r.mineral} ({r.consensus_score:.2f})")
    print(f"\n{results.summary}")
