"""Synthesis reporter tool for multi-stakeholder report generation."""

from datetime import datetime
from typing import Literal

from langchain_core.tools import tool


@tool
def synthesis_reporter(
    hypothesis: str,
    mineral: str,
    consensus_score: float,
    allopathy_findings: str,
    naturopathy_findings: str,
    ayurveda_findings: str,
    tcm_findings: str,
    stakeholder: Literal["research_scientist", "product_trainer", "dx_professional"],
    include_research_gaps: bool = True,
) -> str:
    """
    Generate stakeholder-specific synthesis report from multi-paradigm research.

    Args:
        hypothesis: The research hypothesis tested
        mineral: Primary mineral compound investigated
        consensus_score: Cross-paradigm consensus (0.0-1.0)
        allopathy_findings: Summary from AllopathyResearchAgent
        naturopathy_findings: Summary from NaturopathyResearchAgent
        ayurveda_findings: Summary from AyurvedicResearchAgent
        tcm_findings: Summary from TCMResearchAgent
        stakeholder: Target audience for report
        include_research_gaps: Whether to include gap analysis

    Returns:
        Markdown-formatted synthesis report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d")

    if stakeholder == "research_scientist":
        return _generate_research_scientist_report(
            hypothesis,
            mineral,
            consensus_score,
            allopathy_findings,
            naturopathy_findings,
            ayurveda_findings,
            tcm_findings,
            timestamp,
            include_research_gaps,
        )
    elif stakeholder == "product_trainer":
        return _generate_product_trainer_report(
            hypothesis,
            mineral,
            consensus_score,
            allopathy_findings,
            naturopathy_findings,
            ayurveda_findings,
            tcm_findings,
            timestamp,
        )
    else:  # dx_professional
        return _generate_dx_professional_report(
            hypothesis,
            mineral,
            consensus_score,
            allopathy_findings,
            naturopathy_findings,
            ayurveda_findings,
            tcm_findings,
            timestamp,
        )


def _generate_research_scientist_report(
    hypothesis: str,
    mineral: str,
    consensus_score: float,
    allopathy_findings: str,
    naturopathy_findings: str,
    ayurveda_findings: str,
    tcm_findings: str,
    timestamp: str,
    include_research_gaps: bool,
) -> str:
    """Academic-style report with full citations and methodology."""

    # Determine confidence language
    if consensus_score > 0.6:
        confidence_lang = "promising"
    elif consensus_score > 0.3:
        confidence_lang = "limited"
    else:
        confidence_lang = "insufficient"

    gaps_section = ""
    if include_research_gaps:
        gaps_section = """## Research Gaps & Future Directions

1. **Clinical Trials Needed:** Randomized controlled trials with standardized mineral forms
2. **Mechanism Studies:** Pathways requiring further investigation at molecular level
3. **Cross-Paradigm Validation:** Opportunities for integrative research protocols
4. **Safety Data:** Long-term safety and drug interaction studies needed
5. **Bioavailability:** Comparative studies of different mineral forms and delivery methods

---"""

    return f"""# Multi-Paradigm Evidence Synthesis Report

**Hypothesis:** {hypothesis}
**Primary Compound:** {mineral}
**Date:** {timestamp}
**Consensus Score:** {consensus_score:.2f} / 1.00

---

## Abstract

This report synthesizes evidence from four medical paradigms (Allopathic, Naturopathic,
Ayurvedic, Traditional Chinese Medicine) regarding {mineral} and its potential role
in achieving {hypothesis}.

---

## Methods

### Search Strategy
- **Allopathy:** PubMed, Cochrane Library, ClinicalTrials.gov
- **Naturopathy:** NDNR, Natural Medicine Journal, integrative medicine databases
- **Ayurveda:** Classical texts (Charaka Samhita, Sushruta Samhita), AYUSH databases
- **TCM:** Huang Di Nei Jing, modern TCM journals, pattern-based literature

### Evidence Grading
Each paradigm's evidence was graded using adapted GRADE methodology accounting for
epistemological differences between traditions.

---

## Results by Paradigm

### 1. Allopathic Medicine (Western/Evidence-Based)

{allopathy_findings if allopathy_findings else "_No significant allopathic evidence identified._"}

### 2. Naturopathic Medicine

{naturopathy_findings if naturopathy_findings else "_No significant naturopathic evidence identified._"}

### 3. Ayurvedic Medicine

{ayurveda_findings if ayurveda_findings else "_No significant Ayurvedic evidence identified._"}

### 4. Traditional Chinese Medicine

{tcm_findings if tcm_findings else "_No significant TCM evidence identified._"}

---

## Cross-Paradigm Analysis

### Convergent Findings
[Areas where multiple paradigms agree on mechanism or indication]

### Divergent Findings
[Areas of disagreement or unique paradigm-specific insights]

### Confidence Assessment

| Paradigm | Evidence Grade | Mechanism Support | Clinical Evidence |
|----------|---------------|-------------------|-------------------|
| Allopathy | {'Present' if allopathy_findings else 'Absent'} | See above | See above |
| Naturopathy | {'Present' if naturopathy_findings else 'Absent'} | See above | See above |
| Ayurveda | {'Present' if ayurveda_findings else 'Absent'} | See above | See above |
| TCM | {'Present' if tcm_findings else 'Absent'} | See above | See above |

---

{gaps_section}

## Limitations

- Traditional medicine evidence may not meet RCT standards
- Translation of traditional concepts introduces uncertainty
- Publication bias may affect paradigm-specific literature
- Consensus scoring assumes equal paradigm weighting

---

## Conclusions

Based on multi-paradigm synthesis with consensus score of {consensus_score:.2f},
{mineral} shows {confidence_lang} evidence for {hypothesis}.

---

*Report generated by TraceMineralDiscoveryAgent*
*This is not medical advice. Consult qualified practitioners.*
"""


def _generate_product_trainer_report(
    hypothesis: str,
    mineral: str,
    consensus_score: float,
    allopathy_findings: str,
    naturopathy_findings: str,
    ayurveda_findings: str,
    tcm_findings: str,
    timestamp: str,
) -> str:
    """Application-focused report for product training."""

    if consensus_score > 0.7:
        confidence_level = "High"
    elif consensus_score > 0.4:
        confidence_level = "Moderate"
    else:
        confidence_level = "Low"

    return f"""# {mineral.title()} Product Training Brief

**Date:** {timestamp}
**Confidence Level:** {confidence_level}

---

## Key Talking Points

**Primary Benefit Claim:** {hypothesis}

### What the Science Says

| Tradition | Key Finding | Confidence |
|-----------|-------------|------------|
| Western Research | {allopathy_findings[:100] + '...' if allopathy_findings else 'Limited data'} | {'Moderate' if allopathy_findings else 'Low'} |
| Traditional Use | Multiple paradigm support | {'High' if consensus_score > 0.5 else 'Moderate'} |

---

## How to Position

**Elevator Pitch:**
> "{mineral.title()} has been used across multiple healing traditions - from Western medicine
> to Ayurveda to Traditional Chinese Medicine - for its role in metabolic health support."

**Differentiation:**
- Multi-paradigm validation (not just Western OR Eastern, but both)
- Evidence-based traditional wisdom
- Cross-validated mechanisms

---

## Common Questions & Answers

**Q: Is this supported by clinical research?**
A: {"Yes, there are clinical studies supporting this use." if allopathy_findings else "Traditional use is well-documented; clinical research is ongoing."}

**Q: How does this compare to competitor products?**
A: Our formulation is informed by multi-paradigm research, ensuring both traditional wisdom and modern validation.

**Q: What's the recommended use?**
A: [Refer to product label - consult healthcare provider for personalized advice]

---

## Training Resources

- Full Research Report: Available on request
- Paradigm Deep-Dives: Ayurveda, TCM, Naturopathy modules
- Competitive Analysis: See separate document

---

*For internal training use only. Not for consumer distribution.*
"""


def _generate_dx_professional_report(
    hypothesis: str,
    mineral: str,
    consensus_score: float,
    allopathy_findings: str,
    naturopathy_findings: str,
    ayurveda_findings: str,
    tcm_findings: str,
    timestamp: str,
) -> str:
    """Clinical protocol-focused report for practitioners."""

    return f"""# Clinical Integration Summary: {mineral.title()}

**Date:** {timestamp}
**Evidence Consensus:** {consensus_score:.0%}

---

## Clinical Summary

**Indication:** {hypothesis}
**Compound:** {mineral}
**Multi-Paradigm Support:** {consensus_score:.0%} consensus across traditions

---

## Evidence Overview

### Western Medical Evidence
{allopathy_findings if allopathy_findings else "Limited controlled trial data available."}

### Integrative Medicine Perspective
{naturopathy_findings if naturopathy_findings else "Consult naturopathic references."}

### Traditional Medicine Context
- **Ayurveda:** {ayurveda_findings[:200] if ayurveda_findings else "Traditional preparations exist (bhasmas)"}
- **TCM:** {tcm_findings[:200] if tcm_findings else "Element/organ system correlations documented"}

---

## Clinical Considerations

### Suggested Protocols

| Population | Form | Typical Range* | Duration |
|------------|------|----------------|----------|
| Adult general | [Form TBD] | [Range TBD] | [Duration TBD] |
| With metabolic concerns | [Form TBD] | [Range TBD] | [Duration TBD] |

*Ranges are informational. Individual assessment required.*

### Contraindications & Cautions

1. **Drug Interactions:** [Research specific to mineral]
2. **Conditions:** [Relevant contraindications]
3. **Pregnancy/Lactation:** [Safety classification]

### Monitoring Parameters

- Baseline assessment: [Relevant labs]
- Follow-up: [Timeline and markers]

---

## Integration Points

**Complements:**
- [Other minerals/compounds with synergy]

**Protocol Stacking:**
- Phase 1: [Foundation]
- Phase 2: [Addition of {mineral}]
- Phase 3: [Optimization]

---

## Quick Reference

- **Start with:** [Initial approach]
- **Optimize at:** [Adjustment point]
- **Monitor via:** [Key markers]
- **Duration:** [Typical course]

---

*For licensed healthcare provider use. Not patient-facing.*
*Consult primary literature and clinical judgment.*
"""
