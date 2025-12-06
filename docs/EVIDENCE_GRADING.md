# Evidence Grading Methodology

## Introduction

TraceMineralDiscoveryAgent uses an adapted GRADE (Grading of Recommendations, Assessment, Development and Evaluations) methodology to assess evidence quality across multiple medical paradigms.

### Why Multi-Paradigm Grading Matters

Traditional GRADE was designed for allopathic medicine, where randomized controlled trials (RCTs) are the gold standard. However, when researching trace minerals across Ayurveda, Traditional Chinese Medicine (TCM), and Naturopathy, we must account for:

- Different epistemological frameworks
- Varying evidence types (classical texts vs. clinical trials)
- Paradigm-specific validation methods
- Long-term observational evidence from traditional practice

## GRADE Framework Components

### 1. Risk of Bias

Assessment of systematic errors in study design:

| Level | Description | Examples |
|-------|-------------|----------|
| Low | Rigorous methodology, proper blinding | Double-blind RCT, allocation concealment |
| Some concerns | Minor methodological issues | Single-blind, unclear randomization |
| High | Significant methodological flaws | No blinding, selection bias |

### 2. Inconsistency

Heterogeneity across studies:

| Level | Description | When Applied |
|-------|-------------|--------------|
| None | Consistent results across studies | I² < 25%, similar effect directions |
| Serious | Moderate heterogeneity | I² 25-75%, some conflicting results |
| Very serious | High heterogeneity | I² > 75%, contradictory findings |

### 3. Imprecision

Statistical precision of estimates:

| Level | CI Width | Interpretation |
|-------|----------|----------------|
| None | < 0.2 | Narrow confidence interval, precise estimate |
| Serious | 0.2 - 0.5 | Moderate uncertainty |
| Very serious | > 0.5 | Wide interval, imprecise estimate |

### 4. Study Type Weighting

Different paradigms weight study types differently:

#### Allopathy Weights

| Study Type | Weight | Rationale |
|------------|--------|-----------|
| Meta-analysis | 30% | Highest evidence synthesis |
| RCT | 25% | Gold standard for intervention |
| Cohort | 15% | Observational, temporal relationship |
| Case-control | 10% | Observational, retrospective |
| Case series | 5% | Descriptive only |
| Expert opinion | 2% | Lowest tier |
| Traditional text | 0% | Not recognized as evidence |

#### Traditional Medicine Weights (Ayurveda, TCM)

| Study Type | Weight | Rationale |
|------------|--------|-----------|
| Meta-analysis | 20% | Valued but not dominant |
| RCT | 20% | Important for validation |
| Cohort | 15% | Observational support |
| Case-control | 10% | Supporting evidence |
| Case series | 10% | Clinical observation valued |
| Expert opinion | 10% | Lineage knowledge important |
| Traditional text | 15% | Classical source authority |

#### Naturopathy Weights (Hybrid)

| Study Type | Weight | Rationale |
|------------|--------|-----------|
| Meta-analysis | 25% | Evidence synthesis valued |
| RCT | 22% | Important but not sole standard |
| Cohort | 15% | Clinical practice evidence |
| Case-control | 10% | Supporting evidence |
| Case series | 8% | Practitioner observations |
| Expert opinion | 10% | Clinical wisdom |
| Traditional text | 10% | Naturopathic heritage |

## Scoring Algorithm

```python
credibility = 0.0

# Study type contribution (paradigm-specific)
credibility += study_weights[paradigm][study_type]

# Sample size contribution
if sample_size > 1000:
    credibility += 0.25
elif sample_size > 400:
    credibility += 0.20
elif sample_size > 100:
    credibility += 0.10
elif sample_size > 30:
    credibility += 0.05

# Effect size contribution
if abs(effect_size) > 0.8:  # Large (Cohen's d)
    credibility += 0.15
elif abs(effect_size) > 0.5:  # Medium
    credibility += 0.10
elif abs(effect_size) > 0.2:  # Small
    credibility += 0.05

# Precision contribution
if ci_width < 0.2:
    credibility += 0.10
elif ci_width < 0.5:
    credibility += 0.05

# Peer review bonus
if peer_reviewed:
    credibility += 0.10

# Replication bonus
if replications >= 3:
    credibility += 0.10
elif replications == 2:
    credibility += 0.05
```

## Grade Assignments

| Grade | Score Range | Interpretation |
|-------|-------------|----------------|
| **A (High)** | ≥ 0.70 | Further research is unlikely to change confidence in the effect estimate |
| **B (Moderate)** | 0.50 - 0.69 | Further research is likely to have an important impact and may change the estimate |
| **C (Low)** | 0.30 - 0.49 | Further research is very likely to have an important impact and is likely to change the estimate |
| **D (Very Low)** | < 0.30 | Any estimate of effect is very uncertain |

## Grade Examples

### Grade A Example: Chromium for Glucose Control

```markdown
**Study:** Meta-analysis of 25 RCTs (n=1,422)
**Effect:** HbA1c reduction -0.55% (95% CI: -0.65 to -0.45)
**Paradigm:** Allopathy

Scoring:
- Study type (meta_analysis): +0.30
- Sample size (>1000): +0.25
- Effect size (0.55, medium): +0.10
- CI width (0.20): +0.10
- Peer reviewed: +0.10
- Replicated 5+ times: +0.10

Total: 0.95 → Grade A
```

### Grade B Example: Magnesium for Metabolic Function

```markdown
**Study:** 3 RCTs (n=350 total)
**Effect:** Fasting glucose -8 mg/dL (95% CI: -12 to -4)
**Paradigm:** Allopathy

Scoring:
- Study type (rct): +0.25
- Sample size (350): +0.20
- Effect size (0.4, small-medium): +0.05
- CI width (0.3): +0.05
- Peer reviewed: +0.10
- Replicated 3 times: +0.10

Total: 0.65 → Grade B
```

### Grade C Example: Jasad Bhasma (Zinc) for Prameha

```markdown
**Study:** Classical text reference + 2 modern case series
**Effect:** Clinical improvement reported, no standardized measure
**Paradigm:** Ayurveda

Scoring:
- Study type (traditional_text): +0.15
- Study type (case_series): +0.10
- Sample size (50): +0.05
- Effect size (not quantified): +0.00
- CI width (not applicable): +0.00
- Expert opinion support: +0.10

Total: 0.40 → Grade C
```

### Grade D Example: Novel Mineral Hypothesis

```markdown
**Study:** Single animal study, no human data
**Effect:** Proposed mechanism only
**Paradigm:** Allopathy

Scoring:
- Study type (expert_opinion): +0.02
- Sample size (0 human): +0.00
- Effect size (unknown): +0.00
- Not peer reviewed: +0.00
- Not replicated: +0.00

Total: 0.02 → Grade D
```

## Paradigm-Specific Considerations

### Allopathy

- Requires statistical significance (p < 0.05)
- Effect sizes must be clinically meaningful
- Publication in indexed journals preferred
- Pre-registration valued

### Ayurveda

- Classical text citations carry weight (Charaka, Sushruta)
- Rasa Shastra preparation methods matter
- Dosha-specific outcomes considered
- Safety data from traditional use valued

### TCM

- Pattern diagnosis relevance assessed
- Five Element correspondence considered
- Long-term observational evidence valued
- Integration with acupuncture/herbal data

### Naturopathy

- Whole-food sources prioritized
- Synergistic combinations considered
- Root-cause approach valued
- Clinical practice consensus weighted

## Limitations

### Incommensurability

Different paradigms measure different things:
- Allopathy: Biomarkers, statistical outcomes
- Ayurveda: Dosha balance, Agni strength
- TCM: Pattern resolution, Qi flow
- Naturopathy: Vitality, constitutional improvement

These cannot be directly compared, only synthesized.

### Translation Uncertainty

When mapping concepts across paradigms (e.g., "Kidney Yang" → "thyroid function"), some meaning is inevitably lost. The mapping confidence scores attempt to quantify this uncertainty.

### Publication Bias

- Allopathic literature may over-represent positive findings
- Traditional medicine literature may lack negative results
- Grey literature and unpublished studies may be missed

### Temporal Context

- Traditional texts reflect historical understanding
- Modern validation may differ from traditional claims
- Evidence quality improves over time

## Epistemic Humility

The grading system is a tool for synthesis, not a truth oracle. Users should:

1. **Consider paradigm context** - A Grade B in Ayurveda means something different than Grade B in Allopathy
2. **Read underlying evidence** - Grades summarize, they don't replace primary sources
3. **Acknowledge uncertainty** - Even Grade A evidence has limitations
4. **Consult experts** - Especially for clinical application

## References

1. Guyatt GH, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008.
2. Patwardhan B, et al. Ayurveda and Traditional Chinese Medicine: A Comparative Overview. Evid Based Complement Alternat Med. 2005.
3. Traditional Medicine Strategy 2014-2023. World Health Organization.
4. Balshem H, et al. GRADE guidelines: 3. Rating the quality of evidence. J Clin Epidemiol. 2011.
