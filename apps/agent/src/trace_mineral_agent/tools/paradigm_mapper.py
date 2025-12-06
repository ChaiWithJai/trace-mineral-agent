"""Paradigm mapper tool for cross-tradition concept mapping."""

from typing import Literal

from langchain_core.tools import tool

# Pre-defined mappings loaded from memories/paradigm_ontology.md
PARADIGM_MAPPINGS = {
    # TCM to Allopathy
    ("tcm", "allopathy"): {
        "kidney_yang": ["thyroid function", "adrenal function", "reproductive hormones"],
        "spleen_qi": ["digestive enzyme function", "metabolic rate", "immune function"],
        "liver_qi": ["hepatic detox", "autonomic regulation"],
        "phlegm_dampness": ["metabolic syndrome", "obesity", "dyslipidemia"],
        "blood_stasis": ["poor circulation", "thrombosis risk"],
        "yin_deficiency": ["dehydration", "hormonal imbalance"],
        "kidney_essence": ["bone marrow function", "reproductive health", "longevity"],
        "heart_fire": ["anxiety", "cardiovascular inflammation"],
    },
    # Ayurveda to Allopathy
    ("ayurveda", "allopathy"): {
        "kapha_imbalance": ["obesity", "fluid retention", "hypothyroidism"],
        "pitta_excess": ["inflammation", "hyperthyroidism", "acidosis"],
        "vata_aggravation": ["anxiety", "neurological dysfunction", "irregular metabolism"],
        "agni_dysfunction": ["metabolic rate", "enzyme deficiency"],
        "ama_accumulation": ["endotoxins", "advanced glycation end-products"],
        "dhatu_depletion": ["tissue wasting", "malnutrition"],
        "ojas_deficiency": ["immune weakness", "chronic fatigue"],
        "prameha": ["diabetes", "metabolic syndrome", "urinary disorders"],
    },
    # Naturopathy to Allopathy
    ("naturopathy", "allopathy"): {
        "vital_force": ["homeostatic mechanisms", "immune function"],
        "detoxification": ["hepatic phase I/II metabolism", "renal clearance"],
        "gut_health": ["microbiome balance", "intestinal permeability"],
        "adrenal_fatigue": ["HPA axis dysfunction", "cortisol dysregulation"],
        "leaky_gut": ["intestinal permeability", "food sensitivities"],
        "oxidative_stress": ["free radical damage", "antioxidant deficiency"],
    },
    # Bhasma to Trace Mineral
    ("ayurveda", "trace_mineral"): {
        "jasad_bhasma": ["zinc"],
        "lauha_bhasma": ["iron oxide nanoparticles"],
        "tamra_bhasma": ["copper"],
        "swarna_bhasma": ["gold nanoparticles"],
        "swarna_makshik_bhasma": ["copper-iron-sulfur complex"],
        "shankh_bhasma": ["calcium carbonate"],
        "mandur_bhasma": ["iron"],
        "rajata_bhasma": ["silver nanoparticles"],
        "vanga_bhasma": ["tin"],
        "naga_bhasma": ["lead (historically - now avoided)"],
    },
    # TCM to Trace Mineral (element correlations)
    ("tcm", "trace_mineral"): {
        "earth_element": ["zinc", "manganese", "silicon"],
        "metal_element": ["copper", "selenium"],
        "water_element": ["iodine", "molybdenum"],
        "wood_element": ["iron", "copper"],
        "fire_element": ["chromium", "vanadium"],
    },
}


@tool
def paradigm_mapper(
    concept: str,
    source_paradigm: Literal["allopathy", "naturopathy", "ayurveda", "tcm"],
    target_paradigm: Literal["allopathy", "naturopathy", "ayurveda", "tcm", "trace_mineral"],
) -> str:
    """
    Map a medical concept from one paradigm to another.

    Args:
        concept: The concept to map (e.g., "kidney_yang", "kapha_imbalance")
        source_paradigm: Source medical tradition
        target_paradigm: Target medical tradition

    Returns:
        Markdown-formatted mapping with confidence levels
    """
    # Normalize concept for lookup
    concept_key = concept.lower().replace(" ", "_").replace("-", "_")

    # Get mapping dictionary
    mapping_key = (source_paradigm, target_paradigm)
    reverse_key = (target_paradigm, source_paradigm)

    mappings = PARADIGM_MAPPINGS.get(mapping_key, {})
    reverse_mappings = PARADIGM_MAPPINGS.get(reverse_key, {})

    # Try direct mapping
    if concept_key in mappings:
        targets = mappings[concept_key]
        confidence = 0.85  # Pre-defined mappings have high confidence

        target_rows = "\n".join(f"| {target} | Primary mapping |" for target in targets)

        output = f"""## Paradigm Mapping Result

**Source:** {concept} ({source_paradigm.title()})
**Target Paradigm:** {target_paradigm.title()}
**Confidence:** {confidence:.0%}

### Mapped Concepts

| {target_paradigm.title()} Equivalent | Relationship |
|-------------------------------------|--------------|
{target_rows}

### Context

This mapping is based on established cross-paradigm ontology research.
The concepts share functional equivalence in their respective frameworks.

### Usage Notes

- Use {targets[0]} as the primary equivalent in {target_paradigm} research
- Consider all mapped concepts when doing comprehensive synthesis
"""
        return output

    # Try reverse mapping (find what maps TO this concept)
    for source_concept, target_list in reverse_mappings.items():
        if concept_key in [t.lower().replace(" ", "_") for t in target_list]:
            output = f"""## Paradigm Mapping Result

**Source:** {concept} ({source_paradigm.title()})
**Target Paradigm:** {target_paradigm.title()}
**Confidence:** 75%

### Reverse Mapped Concept

The concept "{concept}" in {source_paradigm} appears to correspond to:
- **{source_concept.replace('_', ' ').title()}** in {target_paradigm}

### Note

This is a reverse mapping (the ontology defines {target_paradigm} -> {source_paradigm}).
Confidence is lower for reverse mappings.
"""
            return output

    # No direct mapping found - return guidance
    available_concepts = _list_available_concepts(source_paradigm)
    return f"""## Paradigm Mapping Result

**Source:** {concept} ({source_paradigm.title()})
**Target Paradigm:** {target_paradigm.title()}
**Confidence:** Not mapped

### No Direct Mapping Found

The concept "{concept}" does not have a pre-defined mapping from {source_paradigm} to {target_paradigm}.

### Suggestions

1. Try searching for related concepts in each paradigm's literature
2. Consider functional equivalents based on:
   - Physiological systems affected
   - Therapeutic goals
   - Traditional indications
3. Consult domain experts for novel mappings

### Similar Concepts Available

{available_concepts}
"""


def _list_available_concepts(paradigm: str) -> str:
    """List concepts available for mapping from this paradigm."""
    concepts = []
    for (source, _), mapping in PARADIGM_MAPPINGS.items():
        if source == paradigm:
            concepts.extend(mapping.keys())

    if concepts:
        return "\n".join(f"- {c.replace('_', ' ').title()}" for c in sorted(set(concepts)))
    return "No concepts available for this paradigm"
