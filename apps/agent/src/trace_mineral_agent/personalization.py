"""Personalization based on user constitutional type."""

from typing import Literal

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User constitutional profile for personalized recommendations."""

    dosha_primary: Literal["vata", "pitta", "kapha"] = Field(
        description="Primary Ayurvedic dosha type"
    )
    dosha_secondary: str | None = Field(
        default=None, description="Secondary dosha influence"
    )
    tcm_pattern: str | None = Field(
        default=None,
        description="Traditional Chinese Medicine pattern (e.g., 'spleen_qi_deficiency')",
    )
    mizaj: Literal["damawi", "balghami", "safrawi", "saudawi"] | None = Field(
        default=None, description="Unani temperament type"
    )
    health_goals: list[str] = Field(
        default_factory=list, description="User's health goals"
    )
    current_medications: list[str] = Field(
        default_factory=list, description="Current medications"
    )
    allergies: list[str] = Field(default_factory=list, description="Known allergies")


# Mineral-Constitution compatibility matrix
MINERAL_DOSHA_EFFECTS = {
    "zinc": {
        "vata": {"effect": "balancing", "notes": "Supports nervous system, calms anxiety"},
        "pitta": {"effect": "cooling", "notes": "Supports immune function, reduces inflammation"},
        "kapha": {"effect": "stimulating", "notes": "Supports metabolism, reduces congestion"},
    },
    "magnesium": {
        "vata": {"effect": "very_beneficial", "notes": "Calms nervous system, supports sleep"},
        "pitta": {"effect": "cooling", "notes": "Reduces heat, supports relaxation"},
        "kapha": {"effect": "neutral", "notes": "May increase heaviness in excess"},
    },
    "iron": {
        "vata": {"effect": "grounding", "notes": "Builds blood, reduces fatigue"},
        "pitta": {"effect": "caution", "notes": "May increase heat, use carefully"},
        "kapha": {"effect": "stimulating", "notes": "Improves circulation, reduces lethargy"},
    },
    "selenium": {
        "vata": {"effect": "neutral", "notes": "Supports thyroid function"},
        "pitta": {"effect": "cooling", "notes": "Antioxidant, reduces oxidative stress"},
        "kapha": {"effect": "beneficial", "notes": "Supports metabolism, thyroid function"},
    },
    "chromium": {
        "vata": {"effect": "grounding", "notes": "Stabilizes blood sugar"},
        "pitta": {"effect": "neutral", "notes": "Supports metabolism"},
        "kapha": {"effect": "very_beneficial", "notes": "Excellent for blood sugar, reduces cravings"},
    },
    "copper": {
        "vata": {"effect": "warming", "notes": "Supports circulation"},
        "pitta": {"effect": "caution", "notes": "May increase heat"},
        "kapha": {"effect": "stimulating", "notes": "Supports metabolism, reduces congestion"},
    },
    "manganese": {
        "vata": {"effect": "grounding", "notes": "Supports bone health"},
        "pitta": {"effect": "neutral", "notes": "Antioxidant support"},
        "kapha": {"effect": "neutral", "notes": "Supports metabolism"},
    },
    "molybdenum": {
        "vata": {"effect": "neutral", "notes": "Supports detoxification"},
        "pitta": {"effect": "cooling", "notes": "Aids sulfite metabolism"},
        "kapha": {"effect": "neutral", "notes": "Supports enzyme function"},
    },
    "iodine": {
        "vata": {"effect": "caution", "notes": "May increase anxiety in excess"},
        "pitta": {"effect": "caution", "notes": "May increase heat"},
        "kapha": {"effect": "very_beneficial", "notes": "Excellent for sluggish metabolism"},
    },
}

# TCM pattern mineral recommendations
TCM_MINERAL_PATTERNS = {
    "spleen_qi_deficiency": {
        "recommended": ["zinc", "chromium", "manganese"],
        "caution": ["iron"],
        "notes": "Focus on minerals that support digestion and metabolism",
    },
    "kidney_yang_deficiency": {
        "recommended": ["selenium", "zinc", "iodine"],
        "caution": [],
        "notes": "Warming minerals to support kidney function",
    },
    "liver_qi_stagnation": {
        "recommended": ["magnesium", "zinc"],
        "caution": ["iron", "copper"],
        "notes": "Minerals that support smooth energy flow",
    },
    "blood_deficiency": {
        "recommended": ["iron", "copper", "zinc"],
        "caution": [],
        "notes": "Blood-building minerals essential",
    },
    "yin_deficiency": {
        "recommended": ["magnesium", "selenium"],
        "caution": ["iodine"],
        "notes": "Cooling, nourishing minerals preferred",
    },
    "phlegm_dampness": {
        "recommended": ["chromium", "selenium", "iodine"],
        "caution": ["magnesium"],
        "notes": "Minerals that transform dampness and support metabolism",
    },
}

# Unani temperament mineral recommendations
UNANI_MINERAL_MIZAJ = {
    "damawi": {  # Sanguine - Hot/Moist
        "recommended": ["zinc", "selenium"],
        "caution": ["iron", "copper"],
        "notes": "Cooling minerals preferred, avoid heating",
    },
    "balghami": {  # Phlegmatic - Cold/Moist
        "recommended": ["iodine", "chromium", "copper"],
        "caution": ["magnesium"],
        "notes": "Warming, drying minerals beneficial",
    },
    "safrawi": {  # Choleric - Hot/Dry
        "recommended": ["magnesium", "zinc"],
        "caution": ["iron", "copper", "iodine"],
        "notes": "Cooling, moistening minerals needed",
    },
    "saudawi": {  # Melancholic - Cold/Dry
        "recommended": ["iron", "copper", "zinc"],
        "caution": [],
        "notes": "Warming, moistening minerals beneficial",
    },
}


def _get_effect_emoji(effect: str) -> str:
    """Get emoji for effect type."""
    emoji_map = {
        "very_beneficial": "✅",
        "beneficial": "👍",
        "balancing": "⚖️",
        "cooling": "❄️",
        "warming": "🔥",
        "grounding": "🌍",
        "stimulating": "⚡",
        "neutral": "➖",
        "caution": "⚠️",
    }
    return emoji_map.get(effect, "•")


@tool
def assess_constitution(
    body_type: Literal["thin", "medium", "heavy"],
    digestion: Literal["irregular", "strong", "slow"],
    temperature: Literal["cold", "hot", "balanced"],
    energy: Literal["variable", "intense", "steady"],
    sleep: Literal["light", "moderate", "heavy"],
) -> str:
    """
    Assess Ayurvedic constitution based on physical and lifestyle factors.

    Args:
        body_type: Physical body type (thin=Vata, medium=Pitta, heavy=Kapha)
        digestion: Digestive pattern (irregular=Vata, strong=Pitta, slow=Kapha)
        temperature: Temperature preference (cold=Vata, hot=Pitta, balanced=Kapha)
        energy: Energy pattern (variable=Vata, intense=Pitta, steady=Kapha)
        sleep: Sleep pattern (light=Vata, moderate=Pitta, heavy=Kapha)

    Returns:
        Constitutional assessment with primary and secondary dosha
    """
    # Score each dosha
    scores = {"vata": 0, "pitta": 0, "kapha": 0}

    # Body type
    if body_type == "thin":
        scores["vata"] += 2
    elif body_type == "medium":
        scores["pitta"] += 2
    else:
        scores["kapha"] += 2

    # Digestion
    if digestion == "irregular":
        scores["vata"] += 2
    elif digestion == "strong":
        scores["pitta"] += 2
    else:
        scores["kapha"] += 2

    # Temperature
    if temperature == "cold":
        scores["vata"] += 1
    elif temperature == "hot":
        scores["pitta"] += 1
    else:
        scores["kapha"] += 1

    # Energy
    if energy == "variable":
        scores["vata"] += 2
    elif energy == "intense":
        scores["pitta"] += 2
    else:
        scores["kapha"] += 2

    # Sleep
    if sleep == "light":
        scores["vata"] += 1
    elif sleep == "moderate":
        scores["pitta"] += 1
    else:
        scores["kapha"] += 1

    # Determine primary and secondary
    sorted_doshas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_doshas[0][0]
    secondary = sorted_doshas[1][0] if sorted_doshas[1][1] > 3 else None

    # Build result
    result = f"""## Constitutional Assessment

**Primary Dosha:** {primary.title()} (Score: {sorted_doshas[0][1]}/10)
**Secondary Dosha:** {secondary.title() if secondary else 'None'}{f' (Score: {sorted_doshas[1][1]}/10)' if secondary else ''}

### Dosha Profile

"""

    dosha_descriptions = {
        "vata": "Air + Space element. Governs movement, creativity, flexibility. When imbalanced: anxiety, insomnia, irregular digestion.",
        "pitta": "Fire + Water element. Governs metabolism, transformation, intellect. When imbalanced: inflammation, irritability, acid reflux.",
        "kapha": "Earth + Water element. Governs structure, stability, immunity. When imbalanced: weight gain, sluggishness, congestion.",
    }

    result += f"**{primary.title()}:** {dosha_descriptions[primary]}\n\n"
    if secondary:
        result += f"**{secondary.title()} influence:** {dosha_descriptions[secondary]}\n\n"

    result += "### General Mineral Recommendations\n\n"
    result += "Based on your constitution, here are general guidelines:\n\n"

    if primary == "vata":
        result += "- **Focus on:** Grounding, calming minerals (Magnesium, Zinc)\n"
        result += "- **Timing:** Take with warm water, with meals\n"
        result += "- **Caution:** Avoid stimulating minerals in excess\n"
    elif primary == "pitta":
        result += "- **Focus on:** Cooling, anti-inflammatory minerals (Zinc, Selenium)\n"
        result += "- **Timing:** Take with cool water, between meals\n"
        result += "- **Caution:** Use iron and copper carefully\n"
    else:  # kapha
        result += "- **Focus on:** Metabolism-supporting minerals (Chromium, Selenium, Iodine)\n"
        result += "- **Timing:** Take with warm water, before meals\n"
        result += "- **Caution:** Avoid heavy supplementation\n"

    return result


@tool
def personalize_mineral_recommendation(
    mineral: str,
    dosha_primary: Literal["vata", "pitta", "kapha"],
    dosha_secondary: str | None = None,
    tcm_pattern: str | None = None,
    mizaj: str | None = None,
) -> str:
    """
    Get personalized mineral recommendation based on constitutional type.

    Args:
        mineral: The trace mineral being evaluated
        dosha_primary: Primary Ayurvedic dosha (vata/pitta/kapha)
        dosha_secondary: Secondary dosha influence (optional)
        tcm_pattern: TCM pattern diagnosis (optional)
        mizaj: Unani temperament (optional)

    Returns:
        Personalized recommendation for the mineral
    """
    mineral_lower = mineral.lower()
    result = f"""## Personalized Analysis: {mineral.title()}

### For {dosha_primary.title()}{f'-{dosha_secondary.title()}' if dosha_secondary else ''} Constitution

"""

    # Ayurvedic analysis
    if mineral_lower in MINERAL_DOSHA_EFFECTS:
        effects = MINERAL_DOSHA_EFFECTS[mineral_lower]
        primary_effect = effects.get(dosha_primary, {"effect": "unknown", "notes": ""})

        emoji = _get_effect_emoji(primary_effect["effect"])
        result += f"**Ayurvedic Assessment:** {emoji} {primary_effect['effect'].replace('_', ' ').title()}\n"
        result += f"- {primary_effect['notes']}\n\n"

        if dosha_secondary and dosha_secondary in effects:
            secondary_effect = effects[dosha_secondary]
            emoji2 = _get_effect_emoji(secondary_effect["effect"])
            result += f"**Secondary Dosha ({dosha_secondary.title()}):** {emoji2} {secondary_effect['effect'].replace('_', ' ').title()}\n"
            result += f"- {secondary_effect['notes']}\n\n"
    else:
        result += f"No specific Ayurvedic data for {mineral}.\n\n"

    # TCM analysis
    if tcm_pattern:
        result += f"### TCM Pattern: {tcm_pattern.replace('_', ' ').title()}\n\n"
        pattern_data = TCM_MINERAL_PATTERNS.get(tcm_pattern)
        if pattern_data:
            if mineral_lower in pattern_data["recommended"]:
                result += "✅ **Recommended** for this pattern\n"
            elif mineral_lower in pattern_data["caution"]:
                result += "⚠️ **Use with caution** for this pattern\n"
            else:
                result += "➖ **Neutral** for this pattern\n"
            result += f"- {pattern_data['notes']}\n\n"

    # Unani analysis
    if mizaj:
        result += f"### Unani Temperament: {mizaj.title()}\n\n"
        mizaj_data = UNANI_MINERAL_MIZAJ.get(mizaj.lower())
        if mizaj_data:
            if mineral_lower in mizaj_data["recommended"]:
                result += "✅ **Recommended** for your temperament\n"
            elif mineral_lower in mizaj_data["caution"]:
                result += "⚠️ **Use with caution** for your temperament\n"
            else:
                result += "➖ **Neutral** for your temperament\n"
            result += f"- {mizaj_data['notes']}\n\n"

    # Timing recommendations
    result += "### Timing & Dosage Considerations\n\n"
    if dosha_primary == "vata":
        result += "- Take with warm water or warm milk\n"
        result += "- Best with meals for better absorption\n"
        result += "- Evening dosing may support sleep\n"
    elif dosha_primary == "pitta":
        result += "- Take with cool or room temperature water\n"
        result += "- Between meals or with cooling foods\n"
        result += "- Avoid taking with spicy foods\n"
    else:  # kapha
        result += "- Take with warm water, add honey if appropriate\n"
        result += "- Before meals to support digestion\n"
        result += "- Morning dosing preferred for energy\n"

    return result


@tool
def get_constitutional_mineral_overview(
    dosha_primary: Literal["vata", "pitta", "kapha"],
    dosha_secondary: str | None = None,
) -> str:
    """
    Get overview of all trace minerals for a constitutional type.

    Args:
        dosha_primary: Primary Ayurvedic dosha
        dosha_secondary: Secondary dosha influence (optional)

    Returns:
        Overview of all minerals ranked by suitability
    """
    result = f"""## Trace Mineral Overview for {dosha_primary.title()}{f'-{dosha_secondary.title()}' if dosha_secondary else ''} Constitution

### Highly Recommended

"""

    very_beneficial = []
    beneficial = []
    neutral = []
    caution = []

    for mineral, effects in MINERAL_DOSHA_EFFECTS.items():
        effect = effects.get(dosha_primary, {}).get("effect", "neutral")
        notes = effects.get(dosha_primary, {}).get("notes", "")

        if effect == "very_beneficial":
            very_beneficial.append((mineral, notes))
        elif effect in ["beneficial", "balancing", "cooling", "warming", "grounding", "stimulating"]:
            beneficial.append((mineral, notes, effect))
        elif effect == "neutral":
            neutral.append((mineral, notes))
        else:  # caution
            caution.append((mineral, notes))

    if very_beneficial:
        for mineral, notes in very_beneficial:
            result += f"✅ **{mineral.title()}**\n   - {notes}\n\n"
    else:
        result += "_No minerals marked as highly beneficial._\n\n"

    result += "### Beneficial\n\n"
    if beneficial:
        for mineral, notes, effect in beneficial:
            emoji = _get_effect_emoji(effect)
            result += f"{emoji} **{mineral.title()}** ({effect})\n   - {notes}\n\n"
    else:
        result += "_No minerals in this category._\n\n"

    result += "### Neutral\n\n"
    if neutral:
        for mineral, notes in neutral:
            result += f"➖ **{mineral.title()}**\n   - {notes}\n\n"

    result += "### Use with Caution\n\n"
    if caution:
        for mineral, notes in caution:
            result += f"⚠️ **{mineral.title()}**\n   - {notes}\n\n"
    else:
        result += "_No specific cautions for your constitution._\n\n"

    result += """### General Guidelines

1. Start with lower doses and observe your response
2. Consider your secondary dosha when fine-tuning
3. Adjust timing based on your constitution
4. Monitor for any imbalance symptoms
5. Consult a practitioner for personalized guidance
"""

    return result
