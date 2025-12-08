"""Skin profile assessment tool for personalized skincare analysis."""

from typing import Literal

from langchain_core.tools import tool


@tool
def skin_profile_assessment(
    age: int,
    skin_type: Literal["oily", "dry", "combination", "normal", "sensitive"],
    primary_concerns: list[str],
    secondary_concerns: list[str] | None = None,
    known_sensitivities: list[str] | None = None,
    current_routine_steps: int | None = None,
    budget_level: Literal["budget", "mid-range", "premium", "luxury"] = "mid-range",
    time_available_minutes: int = 10,
    climate: Literal["humid", "dry", "temperate", "variable"] = "temperate",
    lifestyle_factors: dict | None = None,
) -> str:
    """Generate a comprehensive skin profile assessment for personalized recommendations.

    This tool analyzes skin characteristics, concerns, and lifestyle factors to create
    a detailed profile that informs routine building and product recommendations.

    Args:
        age: Current age in years
        skin_type: Primary skin type classification
        primary_concerns: Main skin concerns to address (e.g., acne, aging, hyperpigmentation)
        secondary_concerns: Additional concerns of lower priority
        known_sensitivities: Ingredients or product types that cause reactions
        current_routine_steps: Number of steps in current routine (0 if none)
        budget_level: Budget category for product recommendations
        time_available_minutes: Minutes available for skincare routine
        climate: Primary climate/environment
        lifestyle_factors: Additional factors like stress, sleep, diet, sun exposure

    Returns:
        Formatted skin profile assessment with recommendations framework
    """
    # Determine skin generation/life stage
    life_stage = _determine_life_stage(age)

    # Analyze skin type characteristics
    skin_type_analysis = _analyze_skin_type(skin_type, climate)

    # Categorize and prioritize concerns
    concern_analysis = _analyze_concerns(
        primary_concerns, secondary_concerns or [], age, skin_type
    )

    # Assess sensitivity profile
    sensitivity_profile = _assess_sensitivities(known_sensitivities or [], skin_type)

    # Calculate routine complexity recommendation
    routine_rec = _recommend_routine_complexity(
        current_routine_steps or 0, time_available_minutes, len(primary_concerns)
    )

    # Analyze lifestyle impact
    lifestyle_analysis = _analyze_lifestyle(lifestyle_factors or {}, primary_concerns)

    # Generate budget-appropriate guidance
    budget_guidance = _generate_budget_guidance(budget_level, primary_concerns)

    # Build the report
    report = f"""# Skin Profile Assessment

## Profile Summary

| Attribute | Value |
|-----------|-------|
| **Age** | {age} years |
| **Life Stage** | {life_stage['stage']} |
| **Skin Type** | {skin_type.title()} |
| **Climate** | {climate.title()} |
| **Budget Level** | {budget_level.replace('-', ' ').title()} |
| **Time Available** | {time_available_minutes} minutes |

---

## Life Stage Considerations

**{life_stage['stage']}** ({life_stage['age_range']})

{life_stage['description']}

**Key Focus Areas:**
{_format_list(life_stage['focus_areas'])}

**Ingredient Priorities:**
{_format_list(life_stage['ingredient_priorities'])}

---

## Skin Type Analysis

**Type:** {skin_type.title()}

{skin_type_analysis['description']}

**Characteristics:**
{_format_list(skin_type_analysis['characteristics'])}

**Climate Interaction ({climate.title()}):**
{skin_type_analysis['climate_impact']}

**Product Texture Preferences:**
{_format_list(skin_type_analysis['texture_preferences'])}

---

## Concern Analysis

### Primary Concerns
"""

    for concern in concern_analysis['primary']:
        report += f"""
#### {concern['name'].title()}
- **Priority Level:** {concern['priority']}
- **Root Causes:** {', '.join(concern['root_causes'])}
- **Key Ingredients:** {', '.join(concern['key_ingredients'])}
- **Timeframe for Results:** {concern['timeframe']}
"""

    if concern_analysis['secondary']:
        report += "\n### Secondary Concerns\n"
        for concern in concern_analysis['secondary']:
            report += f"- **{concern['name'].title()}:** {', '.join(concern['key_ingredients'][:3])}\n"

    report += f"""
---

## Sensitivity Profile

**Risk Level:** {sensitivity_profile['risk_level']}

"""

    if sensitivity_profile['known_triggers']:
        report += f"""**Known Triggers:**
{_format_list(sensitivity_profile['known_triggers'])}

"""

    report += f"""**Ingredients to Approach with Caution:**
{_format_list(sensitivity_profile['caution_ingredients'])}

**Patch Testing Recommendation:** {sensitivity_profile['patch_test_rec']}

---

## Routine Complexity Recommendation

**Current Routine:** {current_routine_steps or 0} steps
**Recommended Routine:** {routine_rec['recommended_steps']} steps

**Rationale:** {routine_rec['rationale']}

**Suggested Structure:**

| Time | Steps | Focus |
|------|-------|-------|
| **AM** | {routine_rec['am_steps']} steps | {routine_rec['am_focus']} |
| **PM** | {routine_rec['pm_steps']} steps | {routine_rec['pm_focus']} |

**Progression Plan:**
{routine_rec['progression']}

---

## Lifestyle Impact Assessment

"""

    if lifestyle_analysis['factors']:
        report += "| Factor | Status | Impact on Skin |\n|--------|--------|----------------|\n"
        for factor in lifestyle_analysis['factors']:
            report += f"| {factor['name']} | {factor['status']} | {factor['impact']} |\n"

    report += f"""
**Lifestyle Recommendations:**
{_format_list(lifestyle_analysis['recommendations'])}

---

## Budget Guidance

**Budget Category:** {budget_level.replace('-', ' ').title()}

{budget_guidance['philosophy']}

**Splurge vs Save Strategy:**
{_format_list(budget_guidance['strategy'])}

**Estimated Monthly Investment:** {budget_guidance['monthly_estimate']}

---

## Profile Tags

These tags summarize your profile for quick reference:

`{skin_type}` `{life_stage['tag']}` `{climate}` `{budget_level}`
"""

    for concern in primary_concerns[:3]:
        report += f" `{concern.lower().replace(' ', '-')}`"

    report += """

---

## Next Steps

Based on your profile, recommended next actions:

1. **Routine Building** - Use the routine_builder tool with this profile
2. **Ingredient Education** - Learn about key ingredients for your concerns
3. **Product Selection** - Get personalized product recommendations

---

*This assessment is for informational purposes. For persistent skin conditions, consult a dermatologist.*
"""

    return report


def _determine_life_stage(age: int) -> dict:
    """Determine skin life stage based on age."""
    if age < 20:
        return {
            "stage": "Teen Skin",
            "tag": "teen",
            "age_range": "13-19",
            "description": "Hormonal fluctuations drive most skin concerns. Focus on establishing good habits without overcomplicating routines.",
            "focus_areas": [
                "Oil control without over-stripping",
                "Acne prevention and treatment",
                "Sun protection habits",
                "Gentle, consistent routine building",
            ],
            "ingredient_priorities": [
                "Salicylic acid (BHA) for pores",
                "Niacinamide for oil control",
                "Benzoyl peroxide for acne (spot treatment)",
                "SPF 30+ daily",
            ],
        }
    elif age < 26:
        return {
            "stage": "Young Adult",
            "tag": "young-adult",
            "age_range": "20-25",
            "description": "Skin is generally resilient but establishing preventive habits now pays dividends. Great time to introduce actives gradually.",
            "focus_areas": [
                "Prevention-focused routine",
                "Antioxidant protection",
                "Texture refinement",
                "Building consistent habits",
            ],
            "ingredient_priorities": [
                "Vitamin C (antioxidant protection)",
                "Niacinamide (barrier support)",
                "Light retinol introduction (0.25-0.5%)",
                "Hyaluronic acid (hydration)",
            ],
        }
    elif age < 36:
        return {
            "stage": "Prime Skin",
            "tag": "prime",
            "age_range": "26-35",
            "description": "Collagen production begins declining around 25. This is the optimal window for preventive anti-aging while addressing current concerns.",
            "focus_areas": [
                "Collagen stimulation",
                "Sun damage prevention",
                "Fine line prevention",
                "Hyperpigmentation prevention",
            ],
            "ingredient_priorities": [
                "Retinol/retinoids (0.5-1%)",
                "Vitamin C (15-20%)",
                "Peptides",
                "AHAs for cell turnover",
            ],
        }
    elif age < 46:
        return {
            "stage": "Maintenance Mode",
            "tag": "maintenance",
            "age_range": "36-45",
            "description": "Visible signs of aging may appear. Focus shifts to maintenance, repair, and optimizing skin health.",
            "focus_areas": [
                "Fine line treatment",
                "Skin firmness",
                "Even tone",
                "Hydration optimization",
            ],
            "ingredient_priorities": [
                "Prescription retinoids (if tolerated)",
                "Growth factors",
                "Ceramides",
                "Peptide complexes",
            ],
        }
    elif age < 56:
        return {
            "stage": "Perimenopause/Andropause Transition",
            "tag": "transition",
            "age_range": "46-55",
            "description": "Hormonal shifts significantly impact skin. Estrogen decline (in women) affects collagen, oil production, and hydration.",
            "focus_areas": [
                "Barrier repair",
                "Deep hydration",
                "Firmness restoration",
                "Hormonal skin changes",
            ],
            "ingredient_priorities": [
                "Phytoestrogens (topical)",
                "Rich ceramide formulations",
                "Bakuchiol (retinol alternative if sensitive)",
                "Nourishing oils",
            ],
        }
    else:
        return {
            "stage": "Mature Skin",
            "tag": "mature",
            "age_range": "56+",
            "description": "Focus on comfort, protection, and gentle efficacy. Skin may be thinner and more sensitive.",
            "focus_areas": [
                "Gentle but effective actives",
                "Maximum hydration",
                "Barrier protection",
                "Comfort-focused formulations",
            ],
            "ingredient_priorities": [
                "Gentle retinoids or bakuchiol",
                "Squalane and rich emollients",
                "Centella asiatica (soothing)",
                "Peptides for firmness",
            ],
        }


def _analyze_skin_type(skin_type: str, climate: str) -> dict:
    """Analyze skin type characteristics and climate interaction."""
    type_data = {
        "oily": {
            "description": "Overactive sebaceous glands produce excess sebum. Often genetic, but can be exacerbated by harsh products that strip the skin.",
            "characteristics": [
                "Visible shine, especially in T-zone",
                "Enlarged pores",
                "Prone to blackheads and breakouts",
                "Makeup may slide or separate",
                "Often ages slower due to natural moisture",
            ],
            "texture_preferences": [
                "Gel cleansers",
                "Water-based serums",
                "Gel or gel-cream moisturizers",
                "Mattifying primers",
                "Lightweight SPF",
            ],
        },
        "dry": {
            "description": "Underactive sebaceous glands produce insufficient natural oils. Skin may feel tight and appear dull.",
            "characteristics": [
                "Tight feeling after cleansing",
                "Visible flaking or rough patches",
                "Fine lines appear more pronounced",
                "Dull or ashy appearance",
                "May be prone to irritation",
            ],
            "texture_preferences": [
                "Cream or oil cleansers",
                "Oil-based serums",
                "Rich cream moisturizers",
                "Facial oils",
                "Hydrating SPF formulas",
            ],
        },
        "combination": {
            "description": "Mixed skin type with oily T-zone (forehead, nose, chin) and normal-to-dry cheeks. Most common skin type.",
            "characteristics": [
                "Oily T-zone, dry/normal elsewhere",
                "May need different products for different areas",
                "Pores more visible in T-zone",
                "Seasonal variation common",
                "Can be tricky to balance",
            ],
            "texture_preferences": [
                "Gel or light foam cleansers",
                "Lightweight serums",
                "Gel-cream or lotion moisturizers",
                "Multi-masking approach",
                "Balanced SPF formulas",
            ],
        },
        "normal": {
            "description": "Well-balanced skin with adequate oil and hydration. Neither too oily nor too dry.",
            "characteristics": [
                "Balanced oil production",
                "Small, barely visible pores",
                "Even tone and texture",
                "Rare breakouts",
                "Tolerates most products well",
            ],
            "texture_preferences": [
                "Flexible with cleanser types",
                "Most serum textures work",
                "Lotion to light cream moisturizers",
                "Can experiment with actives",
                "Most SPF formats",
            ],
        },
        "sensitive": {
            "description": "Reactive skin that easily becomes irritated, red, or uncomfortable. May co-occur with other skin types.",
            "characteristics": [
                "Easily irritated by products",
                "Redness or flushing",
                "Stinging or burning sensation",
                "May react to fragrance/certain ingredients",
                "Often thin or delicate appearance",
            ],
            "texture_preferences": [
                "Cream or micellar cleansers",
                "Fragrance-free everything",
                "Minimal ingredient formulas",
                "Soothing, barrier-focused products",
                "Mineral SPF often better tolerated",
            ],
        },
    }

    climate_impacts = {
        "oily": {
            "humid": "Humidity increases oil production. Focus on oil control without over-drying. Blotting papers are your friend.",
            "dry": "Dry climate may actually help balance oil, but don't skip moisturizer - dehydrated oily skin overproduces oil.",
            "temperate": "Ideal climate for oily skin. Maintain consistent routine with lightweight hydration.",
            "variable": "Adjust routine seasonally. Lighter in humid months, add hydration in dry periods.",
        },
        "dry": {
            "humid": "Humidity helps, but you still need occlusive moisturizers. Don't skip routine because air feels moist.",
            "dry": "Challenging environment. Layer hydration, use humidifier indoors, add facial oil. Avoid hot water.",
            "temperate": "Moderate challenge. Focus on hydrating layers and barrier protection.",
            "variable": "Increase hydration in dry seasons. Have a 'winter routine' ready with richer products.",
        },
        "combination": {
            "humid": "T-zone may get oilier. Consider multi-masking or zone-specific products.",
            "dry": "Cheeks may get drier. Focus hydration there while maintaining T-zone balance.",
            "temperate": "Easiest to manage. Standard combination-skin approach works well.",
            "variable": "Most flexible - adjust zone treatment based on current conditions.",
        },
        "normal": {
            "humid": "Lucky you - maintain current routine with perhaps lighter textures.",
            "dry": "May need to add hydration layers. Don't assume you're immune to dryness.",
            "temperate": "Ideal conditions. Focus on maintenance and prevention.",
            "variable": "Minor adjustments needed seasonally. Add hydration in winter, lighten in summer.",
        },
        "sensitive": {
            "humid": "Heat and humidity can trigger flushing. Keep routine minimal and cool.",
            "dry": "Barrier is stressed. Focus heavily on ceramides and avoiding irritants.",
            "temperate": "Best conditions for sensitive skin. Fewer environmental triggers.",
            "variable": "Each change can trigger reactions. Maintain very consistent, minimal routine.",
        },
    }

    data = type_data[skin_type]
    data["climate_impact"] = climate_impacts[skin_type][climate]

    return data


def _analyze_concerns(
    primary: list[str], secondary: list[str], age: int, skin_type: str
) -> dict:
    """Analyze and prioritize skin concerns."""
    concern_data = {
        "acne": {
            "priority": "High",
            "root_causes": [
                "Excess sebum",
                "P. acnes bacteria",
                "Dead skin buildup",
                "Hormones",
                "Inflammation",
            ],
            "key_ingredients": [
                "Salicylic acid (BHA)",
                "Benzoyl peroxide",
                "Niacinamide",
                "Retinoids",
                "Azelaic acid",
            ],
            "timeframe": "4-12 weeks for improvement",
        },
        "aging": {
            "priority": "Medium-High",
            "root_causes": [
                "Collagen loss",
                "UV damage",
                "Oxidative stress",
                "Glycation",
                "Genetics",
            ],
            "key_ingredients": [
                "Retinoids",
                "Vitamin C",
                "Peptides",
                "Niacinamide",
                "Sunscreen",
            ],
            "timeframe": "3-6 months for visible results",
        },
        "hyperpigmentation": {
            "priority": "Medium",
            "root_causes": [
                "UV exposure",
                "Post-inflammatory (PIH)",
                "Hormonal (melasma)",
                "Age spots",
            ],
            "key_ingredients": [
                "Vitamin C",
                "Niacinamide",
                "Alpha arbutin",
                "Tranexamic acid",
                "Azelaic acid",
            ],
            "timeframe": "2-6 months depending on type",
        },
        "dehydration": {
            "priority": "High",
            "root_causes": [
                "Damaged moisture barrier",
                "Environmental factors",
                "Over-exfoliation",
                "Harsh products",
            ],
            "key_ingredients": [
                "Hyaluronic acid",
                "Glycerin",
                "Ceramides",
                "Squalane",
                "Panthenol",
            ],
            "timeframe": "1-4 weeks for improvement",
        },
        "redness": {
            "priority": "Medium-High",
            "root_causes": [
                "Rosacea",
                "Sensitized barrier",
                "Inflammation",
                "Broken capillaries",
            ],
            "key_ingredients": [
                "Centella asiatica",
                "Niacinamide",
                "Azelaic acid",
                "Green tea",
                "Licorice root",
            ],
            "timeframe": "4-8 weeks for calming",
        },
        "texture": {
            "priority": "Medium",
            "root_causes": [
                "Dead skin buildup",
                "Clogged pores",
                "Dehydration",
                "Sun damage",
            ],
            "key_ingredients": [
                "AHAs (glycolic, lactic)",
                "BHA (salicylic)",
                "Retinoids",
                "Niacinamide",
                "Enzymes",
            ],
            "timeframe": "4-8 weeks for smoother texture",
        },
        "pores": {
            "priority": "Medium",
            "root_causes": [
                "Genetics",
                "Excess sebum",
                "Loss of elasticity",
                "Clogged pores",
            ],
            "key_ingredients": [
                "Niacinamide",
                "BHA",
                "Retinoids",
                "Clay masks",
                "AHAs",
            ],
            "timeframe": "4-8 weeks (can minimize appearance, not size)",
        },
        "dullness": {
            "priority": "Medium",
            "root_causes": [
                "Dead skin buildup",
                "Dehydration",
                "Poor circulation",
                "Oxidative stress",
            ],
            "key_ingredients": [
                "Vitamin C",
                "AHAs",
                "Niacinamide",
                "Hyaluronic acid",
                "Exfoliating enzymes",
            ],
            "timeframe": "2-4 weeks for glow",
        },
        "dark circles": {
            "priority": "Medium",
            "root_causes": [
                "Genetics",
                "Thin under-eye skin",
                "Pigmentation",
                "Lack of sleep",
                "Allergies",
            ],
            "key_ingredients": [
                "Vitamin C",
                "Caffeine",
                "Retinol (gentle)",
                "Peptides",
                "Vitamin K",
            ],
            "timeframe": "6-12 weeks (results vary by cause)",
        },
        "fine lines": {
            "priority": "Medium-High",
            "root_causes": [
                "Collagen loss",
                "Dehydration",
                "Repetitive movements",
                "UV damage",
            ],
            "key_ingredients": [
                "Retinoids",
                "Peptides",
                "Hyaluronic acid",
                "Vitamin C",
                "Bakuchiol",
            ],
            "timeframe": "8-12 weeks for softening",
        },
    }

    def get_concern_info(concern_name: str) -> dict:
        # Normalize concern name
        normalized = concern_name.lower().strip()

        # Direct match
        if normalized in concern_data:
            return {"name": concern_name, **concern_data[normalized]}

        # Fuzzy matching for common variations
        mappings = {
            "anti-aging": "aging",
            "wrinkles": "aging",
            "fine lines": "fine lines",
            "dark spots": "hyperpigmentation",
            "sun spots": "hyperpigmentation",
            "melasma": "hyperpigmentation",
            "pih": "hyperpigmentation",
            "breakouts": "acne",
            "blemishes": "acne",
            "dry skin": "dehydration",
            "oily skin": "pores",
            "large pores": "pores",
            "uneven texture": "texture",
            "rough skin": "texture",
            "rosacea": "redness",
            "flushing": "redness",
            "tired skin": "dullness",
            "lackluster": "dullness",
        }

        for key, value in mappings.items():
            if key in normalized or normalized in key:
                return {"name": concern_name, **concern_data[value]}

        # Default for unknown concerns
        return {
            "name": concern_name,
            "priority": "Medium",
            "root_causes": ["Varies - consult dermatologist for specific guidance"],
            "key_ingredients": ["Depends on specific manifestation"],
            "timeframe": "Varies",
        }

    primary_analyzed = [get_concern_info(c) for c in primary]
    secondary_analyzed = [get_concern_info(c) for c in secondary]

    return {"primary": primary_analyzed, "secondary": secondary_analyzed}


def _assess_sensitivities(known: list[str], skin_type: str) -> dict:
    """Assess sensitivity profile and caution ingredients."""
    common_sensitizers = [
        "Fragrance/Parfum",
        "Essential oils",
        "Alcohol denat (high concentrations)",
        "Sodium lauryl sulfate (SLS)",
        "Certain dyes",
    ]

    caution_by_type = {
        "oily": ["Heavy oils", "Comedogenic ingredients", "Over-occlusion"],
        "dry": ["Alcohol denat", "Strong astringents", "Harsh sulfates"],
        "combination": ["One-size-fits-all products", "Extreme formulations"],
        "normal": ["Generally tolerant - introduce actives gradually"],
        "sensitive": [
            "Fragrance",
            "Essential oils",
            "High-concentration actives",
            "Physical exfoliants",
            "Alcohol denat",
        ],
    }

    if known:
        risk_level = "Elevated" if len(known) >= 3 else "Moderate"
        patch_test = "Essential - always patch test new products for 24-48 hours"
    elif skin_type == "sensitive":
        risk_level = "Elevated"
        patch_test = "Highly recommended - patch test all new products"
    else:
        risk_level = "Standard"
        patch_test = "Recommended for active ingredients and new product categories"

    return {
        "risk_level": risk_level,
        "known_triggers": known if known else ["None identified yet"],
        "caution_ingredients": caution_by_type.get(skin_type, common_sensitizers),
        "patch_test_rec": patch_test,
    }


def _recommend_routine_complexity(
    current_steps: int, time_available: int, concern_count: int
) -> dict:
    """Recommend appropriate routine complexity."""
    # Base recommendation on time and concerns
    if time_available <= 5:
        rec_steps = 3
        am_steps = 3
        pm_steps = 3
        am_focus = "Protect (cleanser, moisturizer, SPF)"
        pm_focus = "Basic care (cleanser, treatment, moisturizer)"
        rationale = "With limited time, focus on the essentials. A 3-step routine can be highly effective."
    elif time_available <= 10:
        rec_steps = 5
        am_steps = 4
        pm_steps = 5
        am_focus = "Protect & treat (cleanser, serum, moisturizer, SPF)"
        pm_focus = "Treat & repair (cleanser, treatment, serum, moisturizer)"
        rationale = "A 4-5 step routine balances efficacy with sustainability."
    elif time_available <= 20:
        rec_steps = 7
        am_steps = 5
        pm_steps = 7
        am_focus = "Full morning routine with actives"
        pm_focus = "Comprehensive treatment routine"
        rationale = "You have time for a thorough routine. Don't overwhelm skin with too many actives."
    else:
        rec_steps = 8
        am_steps = 6
        pm_steps = 8
        am_focus = "Complete AM protocol"
        pm_focus = "Full evening treatment protocol"
        rationale = "Maximize routine but be cautious of over-treatment. Quality over quantity."

    # Determine progression plan
    if current_steps == 0:
        progression = """Start with 3-step basics for 2 weeks, then add one product at a time every 1-2 weeks.
This allows you to identify what works and what might cause issues."""
    elif current_steps < rec_steps:
        progression = f"""Gradually add steps from {current_steps} to {rec_steps}.
Add one new product every 1-2 weeks to monitor for reactions."""
    elif current_steps > rec_steps:
        progression = f"""Consider simplifying from {current_steps} to {rec_steps} steps.
More isn't always better. Focus on key actives for your concerns."""
    else:
        progression = "Your current routine complexity is appropriate. Focus on product optimization."

    return {
        "recommended_steps": rec_steps,
        "am_steps": am_steps,
        "pm_steps": pm_steps,
        "am_focus": am_focus,
        "pm_focus": pm_focus,
        "rationale": rationale,
        "progression": progression,
    }


def _analyze_lifestyle(factors: dict, concerns: list[str]) -> dict:
    """Analyze lifestyle factors and their skin impact."""
    analyzed_factors = []
    recommendations = []

    # Sleep analysis
    if "sleep_hours" in factors:
        hours = factors["sleep_hours"]
        if hours < 6:
            analyzed_factors.append(
                {
                    "name": "Sleep",
                    "status": f"{hours} hours (insufficient)",
                    "impact": "Impaired skin repair, increased cortisol, accelerated aging",
                }
            )
            recommendations.append("Prioritize 7-9 hours of sleep for optimal skin repair")
        elif hours < 7:
            analyzed_factors.append(
                {
                    "name": "Sleep",
                    "status": f"{hours} hours (borderline)",
                    "impact": "Suboptimal repair cycle, may affect skin health",
                }
            )
            recommendations.append("Aim for 7-9 hours for better skin regeneration")
        else:
            analyzed_factors.append(
                {
                    "name": "Sleep",
                    "status": f"{hours} hours (good)",
                    "impact": "Supports skin repair and collagen production",
                }
            )

    # Water intake
    if "water_glasses" in factors:
        glasses = factors["water_glasses"]
        if glasses < 6:
            analyzed_factors.append(
                {
                    "name": "Hydration",
                    "status": f"{glasses} glasses/day (low)",
                    "impact": "May contribute to skin dehydration, dullness",
                }
            )
            recommendations.append("Increase water intake to 8+ glasses daily")
        else:
            analyzed_factors.append(
                {
                    "name": "Hydration",
                    "status": f"{glasses} glasses/day (good)",
                    "impact": "Supports skin hydration from within",
                }
            )

    # Sun exposure
    if "sun_exposure" in factors:
        exposure = factors["sun_exposure"]
        if exposure in ["high", "very high"]:
            analyzed_factors.append(
                {
                    "name": "Sun Exposure",
                    "status": exposure.title(),
                    "impact": "Primary driver of aging, hyperpigmentation, skin cancer risk",
                }
            )
            recommendations.append(
                "SPF 30+ daily is non-negotiable. Reapply every 2 hours when outdoors"
            )

    # Stress level
    if "stress_level" in factors:
        stress = factors["stress_level"]
        if stress in ["high", "very high"]:
            analyzed_factors.append(
                {
                    "name": "Stress",
                    "status": stress.title(),
                    "impact": "Triggers cortisol, can cause breakouts, accelerate aging, impair barrier",
                }
            )
            recommendations.append(
                "Stress management (meditation, exercise) benefits skin significantly"
            )

    # Diet
    if "diet_quality" in factors:
        diet = factors["diet_quality"]
        if diet in ["poor", "fair"]:
            analyzed_factors.append(
                {
                    "name": "Diet",
                    "status": diet.title(),
                    "impact": "High glycemic foods can trigger acne; lack of nutrients affects skin health",
                }
            )
            recommendations.append(
                "Consider more vegetables, omega-3s, and reducing sugar/dairy if acne-prone"
            )

    # Exercise
    if "exercise_frequency" in factors:
        exercise = factors["exercise_frequency"]
        analyzed_factors.append(
            {
                "name": "Exercise",
                "status": exercise,
                "impact": "Improves circulation and skin health; remember to cleanse post-workout",
            }
        )
        if "never" in exercise.lower() or "rarely" in exercise.lower():
            recommendations.append("Regular exercise improves skin circulation and health")

    # Default recommendations if no factors provided
    if not recommendations:
        recommendations = [
            "Sleep 7-9 hours for optimal skin repair",
            "Stay hydrated with 8+ glasses of water daily",
            "Wear SPF 30+ daily regardless of weather",
            "Manage stress - it directly impacts skin",
            "Eat a balanced diet rich in antioxidants",
        ]

    return {"factors": analyzed_factors, "recommendations": recommendations}


def _generate_budget_guidance(budget: str, concerns: list[str]) -> dict:
    """Generate budget-appropriate guidance."""
    guidance = {
        "budget": {
            "philosophy": "Effective skincare doesn't require luxury prices. Many drugstore products contain identical active ingredients to expensive counterparts. Focus on proven actives, not fancy packaging.",
            "strategy": [
                "SPLURGE: Sunscreen (you'll use it daily, get one you love)",
                "SAVE: Cleanser (on face briefly, drugstore is fine)",
                "SAVE: Basic moisturizer (CeraVe, Vanicream, Cetaphil)",
                "SPLURGE: One targeted treatment for primary concern",
                "SAVE: AHAs/BHAs (The Ordinary, Paula's Choice sales)",
            ],
            "monthly_estimate": "$30-60",
        },
        "mid-range": {
            "philosophy": "Balance of quality and value. You can access better formulations and textures while being strategic about spending.",
            "strategy": [
                "SPLURGE: Vitamin C serum (stability matters)",
                "SPLURGE: Retinoid (formulation affects efficacy and tolerance)",
                "SAVE: Cleanser and basic moisturizer",
                "MID: Targeted treatments from quality brands",
                "SAVE: Basic hydrating serums",
            ],
            "monthly_estimate": "$80-150",
        },
        "premium": {
            "philosophy": "Access to advanced formulations, elegant textures, and comprehensive ranges. Worth it for hero products, diminishing returns for basics.",
            "strategy": [
                "SPLURGE: Advanced treatments (prescription-level OTC)",
                "SPLURGE: Elegant daily-use products you love",
                "MID: Professional-grade actives",
                "SAVE: Can still save on basics if you choose",
                "INVEST: Professional treatments quarterly",
            ],
            "monthly_estimate": "$200-350",
        },
        "luxury": {
            "philosophy": "Top-tier formulations with premium textures and cutting-edge ingredients. Remember that price doesn't always equal efficacy.",
            "strategy": [
                "INVEST: Comprehensive routines from luxury houses",
                "INVEST: Advanced treatments and devices",
                "SPLURGE: Sensorial experience products",
                "CONSIDER: Professional treatments monthly",
                "REMEMBER: Even luxury needs SPF basics",
            ],
            "monthly_estimate": "$400+",
        },
    }

    return guidance.get(budget, guidance["mid-range"])


def _format_list(items: list[str]) -> str:
    """Format a list as markdown bullet points."""
    return "\n".join(f"- {item}" for item in items)
