"""Evidence grading tool using adapted GRADE methodology."""

from typing import Literal

from langchain_core.tools import tool


@tool
def evidence_grade(
    study_type: Literal[
        "meta_analysis",
        "rct",
        "cohort",
        "case_control",
        "case_series",
        "expert_opinion",
        "traditional_text",
    ],
    sample_size: int,
    effect_size: float,
    confidence_interval_width: float,
    peer_reviewed: bool = True,
    replication_count: int = 1,
    paradigm: Literal["allopathy", "naturopathy", "ayurveda", "tcm"] = "allopathy",
) -> str:
    """
    Grade evidence quality using GRADE methodology adapted for multi-paradigm research.

    Args:
        study_type: Type of study (meta_analysis, rct, cohort, etc.)
        sample_size: Total participants across studies
        effect_size: Standardized effect size (Cohen's d or similar)
        confidence_interval_width: Width of 95% CI
        peer_reviewed: Whether published in peer-reviewed source
        replication_count: Number of independent replications
        paradigm: Medical paradigm context for grading

    Returns:
        Markdown-formatted evidence grade assessment
    """
    # Calculate component scores
    credibility = 0.0

    # Study type weight (paradigm-aware)
    if paradigm == "allopathy":
        study_weights = {
            "meta_analysis": 0.30,
            "rct": 0.25,
            "cohort": 0.15,
            "case_control": 0.10,
            "case_series": 0.05,
            "expert_opinion": 0.02,
            "traditional_text": 0.00,  # Not recognized in allopathy
        }
    elif paradigm in ["ayurveda", "tcm"]:
        study_weights = {
            "meta_analysis": 0.20,
            "rct": 0.20,
            "cohort": 0.15,
            "case_control": 0.10,
            "case_series": 0.10,
            "expert_opinion": 0.10,
            "traditional_text": 0.15,  # Valued in traditional systems
        }
    else:  # naturopathy - hybrid
        study_weights = {
            "meta_analysis": 0.25,
            "rct": 0.22,
            "cohort": 0.15,
            "case_control": 0.10,
            "case_series": 0.08,
            "expert_opinion": 0.10,
            "traditional_text": 0.10,
        }

    credibility += study_weights.get(study_type, 0)

    # Sample size weight
    if sample_size > 1000:
        credibility += 0.25
    elif sample_size > 400:
        credibility += 0.20
    elif sample_size > 100:
        credibility += 0.10
    elif sample_size > 30:
        credibility += 0.05

    # Effect size weight
    if abs(effect_size) > 0.8:
        credibility += 0.15  # Large effect
    elif abs(effect_size) > 0.5:
        credibility += 0.10  # Medium effect
    elif abs(effect_size) > 0.2:
        credibility += 0.05  # Small effect

    # Precision weight (narrower CI = more precise)
    if confidence_interval_width < 0.2:
        credibility += 0.10
        imprecision = "None"
    elif confidence_interval_width < 0.5:
        credibility += 0.05
        imprecision = "Serious"
    else:
        imprecision = "Very serious"

    # Peer review bonus
    if peer_reviewed:
        credibility += 0.10

    # Replication bonus
    if replication_count >= 3:
        credibility += 0.10
        inconsistency = "None"
    elif replication_count == 2:
        credibility += 0.05
        inconsistency = "None"
    else:
        inconsistency = "Serious" if sample_size < 100 else "None"

    # Determine overall grade
    if credibility >= 0.70:
        grade = "A"
        risk_of_bias = "Low"
    elif credibility >= 0.50:
        grade = "B"
        risk_of_bias = "Some concerns"
    elif credibility >= 0.30:
        grade = "C"
        risk_of_bias = "Some concerns"
    else:
        grade = "D"
        risk_of_bias = "High"

    # Build rationale
    rationale_parts = []
    rationale_parts.append(
        f"Study type ({study_type}) contributes {study_weights.get(study_type, 0):.0%}"
    )
    rationale_parts.append(
        f"Sample size ({sample_size}) indicates {'adequate' if sample_size > 100 else 'limited'} power"
    )

    effect_desc = "large" if abs(effect_size) > 0.8 else "moderate" if abs(effect_size) > 0.5 else "small"
    rationale_parts.append(f"Effect size ({effect_size:.2f}) is {effect_desc}")

    if replication_count > 1:
        rationale_parts.append(f"Replicated {replication_count} times")

    # Format output as markdown
    rationale_list = "\n".join("- " + r for r in rationale_parts)

    output = f"""## Evidence Grade Assessment

**Overall Grade:** {grade}
**Confidence Score:** {credibility:.2f}
**Paradigm Context:** {paradigm.title()}

### GRADE Domains

| Domain | Assessment |
|--------|------------|
| Risk of Bias | {risk_of_bias} |
| Inconsistency | {inconsistency} |
| Imprecision | {imprecision} |
| Study Type | {study_type.replace('_', ' ').title()} |

### Rationale

{rationale_list}

### Grade Scale Reference

- **A (High):** Further research unlikely to change confidence
- **B (Moderate):** Further research may change confidence
- **C (Low):** Further research likely to change confidence
- **D (Very Low):** Any estimate is uncertain
"""

    return output
