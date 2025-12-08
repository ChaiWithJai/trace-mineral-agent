"""Trend evaluator tool for validating skincare trends against scientific evidence.

Designed to help consumers distinguish between evidence-based practices and
viral trends that may be ineffective or harmful.
"""

from typing import Literal

from langchain_core.tools import tool


# Database of known trends with scientific evaluation
TREND_DATABASE: dict[str, dict] = {
    # VALIDATED TRENDS (actually work)
    "slugging": {
        "description": "Applying a thick layer of occlusive (like Vaseline) as the final PM step",
        "verdict": "VALIDATED",
        "evidence_grade": "B+",
        "mechanism": "Occlusion prevents transepidermal water loss (TEWL). Petrolatum is 98% effective at reducing TEWL.",
        "scientific_basis": "Occlusive therapy is well-established in dermatology for barrier repair",
        "benefits": [
            "Seals in moisture and actives",
            "Supports barrier repair",
            "Helps with dry, flaky skin",
            "Non-comedogenic despite heavy texture",
        ],
        "risks": ["May trap bacteria if skin isn't clean", "Not ideal for acne-prone skin", "Can feel heavy"],
        "who_should_try": ["Dry skin", "Compromised barrier", "Tretinoin users", "Winter/dry climate"],
        "who_should_avoid": ["Oily/acne-prone skin", "Fungal acne"],
        "how_to_do_it": "Cleanse thoroughly, apply all PM products, wait 10min, apply thin layer of Vaseline/Aquaphor",
    },
    "skin_cycling": {
        "description": "4-night rotation: exfoliate, retinoid, recovery, recovery",
        "verdict": "VALIDATED",
        "evidence_grade": "B",
        "mechanism": "Allows skin to recover between active use, reducing irritation while maintaining benefits",
        "scientific_basis": "Based on dermatological principles of allowing barrier recovery between active treatments",
        "benefits": [
            "Reduces irritation from actives",
            "Sustainable long-term",
            "Good for beginners",
            "Maintains efficacy while improving tolerance",
        ],
        "risks": ["May be slower progress than nightly use (for tolerant skin)"],
        "who_should_try": ["Beginners", "Sensitive skin", "Those who over-exfoliated", "Anyone struggling with actives"],
        "who_should_avoid": ["Those who tolerate nightly actives well (no need to scale back)"],
        "how_to_do_it": "Night 1: Exfoliant (AHA/BHA), Night 2: Retinoid, Nights 3-4: Recovery (hydration only)",
    },
    "double_cleansing": {
        "description": "Using an oil-based cleanser followed by a water-based cleanser",
        "verdict": "VALIDATED",
        "evidence_grade": "B+",
        "mechanism": "Oil dissolves oil-based impurities (sunscreen, sebum, makeup); water-based removes residue",
        "scientific_basis": "'Like dissolves like' - oil-based cleansers emulsify oil-soluble debris",
        "benefits": [
            "More thorough makeup/SPF removal",
            "Gentler than harsh single cleanse",
            "Prevents clogged pores from residue",
            "Can actually be less stripping than one harsh cleanser",
        ],
        "risks": ["Unnecessary if not wearing SPF/makeup", "Over-cleansing if using harsh products"],
        "who_should_try": ["SPF wearers (everyone)", "Makeup wearers", "Oily skin", "Congested pores"],
        "who_should_avoid": ["Those not wearing anything to remove", "Over-stripped skin (simplify routine)"],
        "how_to_do_it": "PM: Oil/balm cleanser on dry skin, massage, rinse. Follow with gentle water-based cleanser.",
    },
    "sandwich_method": {
        "description": "Applying moisturizer before AND after retinoid to buffer irritation",
        "verdict": "VALIDATED",
        "evidence_grade": "B",
        "mechanism": "Dilutes retinoid concentration reaching skin, slowing penetration and reducing irritation",
        "scientific_basis": "Reduces irritation without eliminating efficacy (studies show buffered retinoids still work)",
        "benefits": [
            "Reduces retinoid irritation significantly",
            "Allows sensitive skin to use retinoids",
            "Doesn't eliminate efficacy",
        ],
        "risks": ["Slightly reduced efficacy vs direct application", "May extend adaptation period"],
        "who_should_try": ["Retinoid beginners", "Sensitive skin", "Those experiencing irritation"],
        "who_should_avoid": ["Those tolerating retinoid well (direct application is fine)"],
        "how_to_do_it": "Moisturizer first → wait 5min → retinoid → wait 5min → moisturizer again",
    },
    "niacinamide_for_sebum": {
        "description": "Using niacinamide to reduce oil production and pore appearance",
        "verdict": "VALIDATED",
        "evidence_grade": "A",
        "mechanism": "Niacinamide reduces sebum production and improves barrier function",
        "scientific_basis": "Multiple studies show 2% niacinamide reduces sebum excretion rate",
        "benefits": [
            "Reduces oil production",
            "Minimizes pore appearance",
            "Strengthens barrier",
            "Anti-inflammatory",
        ],
        "risks": ["Very high concentrations (>10%) may cause flushing"],
        "who_should_try": ["Oily skin", "Large pores", "Acne-prone", "Anyone wanting multi-benefit ingredient"],
        "who_should_avoid": ["Those sensitive to niacinamide (rare)"],
        "how_to_do_it": "Use 2-5% niacinamide serum in AM and/or PM. Can layer with most actives.",
    },

    # MIXED EVIDENCE TRENDS
    "ice_rolling": {
        "description": "Rolling ice or cold tools on face for 'de-puffing' and 'pore shrinking'",
        "verdict": "MIXED",
        "evidence_grade": "C",
        "mechanism": "Cold causes vasoconstriction, temporarily reducing puffiness. No effect on actual pore size.",
        "scientific_basis": "Temporary vasoconstriction is real; permanent pore reduction claims are false",
        "benefits": [
            "Temporary de-puffing (real)",
            "Can feel soothing for inflamed skin",
            "May help product absorption slightly",
        ],
        "risks": [
            "Can cause broken capillaries with too much pressure",
            "Cold urticaria (cold allergy)",
            "Won't deliver promised permanent results",
        ],
        "who_should_try": ["Morning puffiness", "Those who enjoy it (self-care)", "Hot/inflamed skin"],
        "who_should_avoid": ["Rosacea", "Broken capillaries", "Cold sensitivity", "Those expecting miracles"],
        "how_to_do_it": "Gentle pressure, clean tool, limited time. Don't expect permanent pore changes.",
    },
    "gua_sha": {
        "description": "Traditional Chinese facial massage tool for 'sculpting' and 'lymphatic drainage'",
        "verdict": "MIXED",
        "evidence_grade": "C+",
        "mechanism": "Massage increases circulation; lymphatic drainage is real but temporary",
        "scientific_basis": "Lymphatic system exists, massage can move fluid, but 'face sculpting' is temporary",
        "benefits": [
            "Relaxing self-care ritual",
            "Temporary reduction in puffiness",
            "May increase product absorption",
            "Promotes circulation",
        ],
        "risks": [
            "Broken capillaries with too much pressure",
            "No permanent 'sculpting' effect",
            "Can spread acne bacteria if not clean",
        ],
        "who_should_try": ["Puffiness", "Self-care enthusiasts", "Those with tension (jaw clenching)"],
        "who_should_avoid": ["Active acne", "Rosacea", "Those expecting permanent structural changes"],
        "how_to_do_it": "Gentle pressure, always with slip (oil/serum), clean tool. Morning for de-puffing.",
    },
    "vitamin_c_with_niacinamide": {
        "description": "Combining vitamin C and niacinamide in the same routine",
        "verdict": "VALIDATED (myth debunked)",
        "evidence_grade": "A",
        "mechanism": "Old research (1960s) found high heat + low pH could convert niacinamide to niacin. Modern formulas don't have this issue.",
        "scientific_basis": "This 'rule' comes from outdated research. Modern formulations are stable together.",
        "benefits": [
            "Complementary antioxidant effects",
            "Both brighten skin",
            "No actual incompatibility in modern products",
        ],
        "risks": ["None from the combination itself"],
        "who_should_try": ["Anyone wanting both ingredients"],
        "who_should_avoid": ["Only avoid if skin is reactive to one of them individually"],
        "how_to_do_it": "Use together freely. The 'rule' is a myth.",
    },
    "hyaluronic_acid_in_dry_climate": {
        "description": "Warning that HA can 'draw moisture from skin' in dry climates",
        "verdict": "PARTIALLY TRUE",
        "evidence_grade": "B",
        "mechanism": "Humectants draw water - from air if humid, potentially from deeper skin if air is very dry",
        "scientific_basis": "Thermodynamically possible, but easily solved by sealing with occlusive",
        "benefits": ["HA still works if used correctly"],
        "risks": ["Theoretical moisture loss if used without occlusive in very dry air"],
        "who_should_try": ["Everyone - just use correctly"],
        "who_should_avoid": ["No one needs to avoid, just adjust technique"],
        "how_to_do_it": "Apply to damp skin, IMMEDIATELY seal with moisturizer. Use occlusive in dry climates.",
    },

    # DEBUNKED TRENDS
    "diy_sunscreen": {
        "description": "Making sunscreen at home from natural ingredients",
        "verdict": "DANGEROUS",
        "evidence_grade": "F",
        "mechanism": "Homemade mixtures cannot achieve proper SPF. UV filters require precise formulation.",
        "scientific_basis": "SPF testing requires standardized methods. No DIY can match commercial formulation.",
        "benefits": ["None - provides false sense of protection"],
        "risks": [
            "SEVERE: No actual UV protection",
            "Burns, skin cancer risk",
            "Photoaging",
            "False security",
        ],
        "who_should_try": ["NO ONE"],
        "who_should_avoid": ["EVERYONE"],
        "how_to_do_it": "DON'T. Use tested, commercial sunscreens.",
    },
    "lemon_on_face": {
        "description": "Using lemon juice for 'brightening' and 'vitamin C'",
        "verdict": "HARMFUL",
        "evidence_grade": "F",
        "mechanism": "Citric acid pH is too low (~2), causes chemical burns. Psoralen compounds cause phototoxicity.",
        "scientific_basis": "Documented phytophotodermatitis from citrus. pH is skin-damaging.",
        "benefits": ["None that justify the risks"],
        "risks": [
            "Chemical burns",
            "Phytophotodermatitis (severe burns in sun)",
            "Permanent hyperpigmentation",
            "Destroyed moisture barrier",
        ],
        "who_should_try": ["NO ONE"],
        "who_should_avoid": ["EVERYONE"],
        "how_to_do_it": "DON'T. Use formulated vitamin C products instead.",
    },
    "toothpaste_on_pimples": {
        "description": "Applying toothpaste to spots to 'dry them out'",
        "verdict": "HARMFUL",
        "evidence_grade": "F",
        "mechanism": "Toothpaste contains SLS, fluoride, menthol - all irritating to facial skin",
        "scientific_basis": "Not formulated for skin. Causes contact dermatitis and irritation.",
        "benefits": ["None"],
        "risks": [
            "Contact dermatitis",
            "Chemical burns",
            "Worsened inflammation",
            "Prolonged healing",
        ],
        "who_should_try": ["NO ONE"],
        "who_should_avoid": ["EVERYONE"],
        "how_to_do_it": "DON'T. Use proper spot treatments (benzoyl peroxide, salicylic acid patches).",
    },
    "baking_soda_scrub": {
        "description": "Using baking soda as a face scrub or mask",
        "verdict": "HARMFUL",
        "evidence_grade": "F",
        "mechanism": "pH of ~9 disrupts acid mantle (skin is pH 4.5-5.5). Abrasive particles cause microtears.",
        "scientific_basis": "High pH damages barrier, disrupts microbiome, causes irritation",
        "benefits": ["None"],
        "risks": [
            "Destroyed acid mantle",
            "Barrier damage",
            "Increased sensitivity",
            "Breakouts from microbiome disruption",
        ],
        "who_should_try": ["NO ONE"],
        "who_should_avoid": ["EVERYONE"],
        "how_to_do_it": "DON'T. Use pH-appropriate formulated exfoliants.",
    },
    "pore_strips": {
        "description": "Adhesive strips pulled off nose to remove blackheads",
        "verdict": "INEFFECTIVE",
        "evidence_grade": "D",
        "mechanism": "Removes sebaceous filaments (normal), not true blackheads. Refills within 24-48 hours.",
        "scientific_basis": "Doesn't address cause of congestion. Can damage pore walls with repeated use.",
        "benefits": [
            "Temporary cosmetic improvement (very short-lived)",
            "Satisfying to see results (psychologically)",
        ],
        "risks": [
            "Can damage pore walls",
            "Strips return within 1-2 days",
            "Doesn't address root cause",
            "Can cause broken capillaries",
        ],
        "who_should_try": ["Skip it - better alternatives exist"],
        "who_should_avoid": ["Everyone long-term", "Sensitive skin", "Rosacea"],
        "how_to_do_it": "Better alternatives: BHA (salicylic acid) for long-term pore clarity",
    },
    "facial_exercises": {
        "description": "Exercises claiming to 'lift' or 'tone' facial muscles",
        "verdict": "INEFFECTIVE/COUNTERPRODUCTIVE",
        "evidence_grade": "D",
        "mechanism": "Face muscles are attached to skin, not bone like body muscles. Repetitive movement = more wrinkles.",
        "scientific_basis": "No evidence for lifting. Repetitive movement causes expression lines (why Botox works).",
        "benefits": ["May increase blood flow temporarily"],
        "risks": [
            "Can worsen wrinkles from repetitive movement",
            "No lifting effect",
            "Time wasted",
        ],
        "who_should_try": ["No one for anti-aging purposes"],
        "who_should_avoid": ["Everyone seeking wrinkle reduction"],
        "how_to_do_it": "Don't for anti-aging. If you enjoy it for circulation, very gentle only.",
    },
    "drinking_water_for_skin": {
        "description": "Drinking lots of water for 'glowing skin' and 'hydration'",
        "verdict": "OVERSTATED",
        "evidence_grade": "C",
        "mechanism": "Severe dehydration affects skin, but excess water doesn't super-hydrate skin",
        "scientific_basis": "No evidence that drinking above adequate hydration improves skin appearance",
        "benefits": [
            "Adequate hydration is important (not excess)",
            "General health benefits",
        ],
        "risks": [
            "Overhydration in extreme cases",
            "Expecting miracles that won't come",
        ],
        "who_should_try": ["Everyone should stay adequately hydrated"],
        "who_should_avoid": ["Don't over-hydrate expecting skin miracles"],
        "how_to_do_it": "Stay adequately hydrated (8 cups/day guideline). Don't expect excess water to fix skin.",
    },
    "apple_cider_vinegar_toner": {
        "description": "Using diluted ACV as a toner for 'pH balancing'",
        "verdict": "RISKY",
        "evidence_grade": "D",
        "mechanism": "ACV is acidic (~3 pH), but concentration varies. Chemical burn risk.",
        "scientific_basis": "Skin doesn't need external pH 'balancing' - it self-regulates. Risk outweighs any benefit.",
        "benefits": ["None that justify risks"],
        "risks": [
            "Chemical burns (variable concentration)",
            "Irritation",
            "Destroyed barrier",
            "Unpredictable pH",
        ],
        "who_should_try": ["No one"],
        "who_should_avoid": ["Everyone"],
        "how_to_do_it": "Don't. Use formulated toners with controlled pH.",
    },

    # EMERGING TRENDS
    "skin_flooding": {
        "description": "Applying multiple layers of hydrating products to damp skin",
        "verdict": "PROMISING",
        "evidence_grade": "B-",
        "mechanism": "Layering humectants on damp skin maximizes hydration. Similar principle to 7-skin method.",
        "scientific_basis": "Humectant layering is established; 'flooding' is a repackaged concept",
        "benefits": [
            "Maximizes hydration",
            "Good for dehydrated skin",
            "Works with existing products",
        ],
        "risks": [
            "Product pilling if layering incompatible textures",
            "May be too heavy for oily skin",
        ],
        "who_should_try": ["Dehydrated skin", "Dry skin", "Post-treatment recovery"],
        "who_should_avoid": ["Oily/acne-prone (may be too much)", "Fungal acne"],
        "how_to_do_it": "On damp skin: layer toner → essence → serum → moisturizer quickly before each dries",
    },
    "retinol_sandwich": {
        "description": "Moisturizer → Retinol → Moisturizer to buffer irritation",
        "verdict": "VALIDATED",
        "evidence_grade": "B",
        "mechanism": "Same as sandwich method - dilutes concentration, reduces irritation",
        "scientific_basis": "Dermatologist-recommended technique for retinoid beginners",
        "benefits": ["Reduces irritation", "Allows sensitive skin to use retinoids"],
        "risks": ["Slightly slower results than direct application"],
        "who_should_try": ["Retinoid beginners", "Sensitive skin"],
        "who_should_avoid": ["Those tolerating direct application well"],
        "how_to_do_it": "Apply moisturizer → wait 5-10min → retinoid → wait 5-10min → moisturizer",
    },
    "snail_mucin": {
        "description": "Using snail secretion filtrate for hydration and healing",
        "verdict": "PROMISING",
        "evidence_grade": "B-",
        "mechanism": "Contains glycoproteins, hyaluronic acid, glycolic acid. Wound healing properties.",
        "scientific_basis": "Some studies show wound healing benefits. Limited but promising research.",
        "benefits": [
            "Hydrating",
            "May support wound healing",
            "Well-tolerated",
            "Soothes irritation",
        ],
        "risks": [
            "Shellfish allergies may cross-react",
            "Quality varies by brand",
        ],
        "who_should_try": ["Dehydrated skin", "Post-treatment recovery", "Irritated skin"],
        "who_should_avoid": ["Shellfish allergies (caution)", "Those preferring vegan products"],
        "how_to_do_it": "Use as hydrating serum after cleansing/toning. CosRx is popular brand.",
    },
    "dermaplaning": {
        "description": "Shaving face with blade to remove peach fuzz and exfoliate",
        "verdict": "MIXED",
        "evidence_grade": "C+",
        "mechanism": "Physical exfoliation + hair removal. Does NOT make hair grow back thicker (myth).",
        "scientific_basis": "Physical exfoliation is real; hair growth myth is debunked",
        "benefits": [
            "Smooth makeup application",
            "Removes peach fuzz",
            "Physical exfoliation",
            "Hair does NOT grow back thicker",
        ],
        "risks": [
            "Irritation if done incorrectly",
            "Can spread acne bacteria",
            "Risk of cuts",
            "Not for active acne or sensitive skin",
        ],
        "who_should_try": ["Normal skin wanting smoother texture", "Professional treatment preferred"],
        "who_should_avoid": ["Active acne", "Sensitive skin", "Rosacea", "Eczema"],
        "how_to_do_it": "Best done professionally. If DIY: clean blade, gentle strokes, no active breakouts.",
    },
}


@tool
def trend_evaluator(
    trend_name: str | None = None,
    trend_description: str | None = None,
    claims: list[str] | None = None,
    source_platform: Literal["tiktok", "instagram", "youtube", "reddit", "other"] = "tiktok",
) -> str:
    """Evaluate a skincare trend against scientific evidence.

    Helps consumers distinguish between evidence-based practices and viral trends
    that may be ineffective or harmful. Provides verdict, evidence grade, and
    detailed scientific analysis.

    Args:
        trend_name: Name of the trend (e.g., "slugging", "skin cycling")
        trend_description: Description of the trend if not in database
        claims: Specific claims made about the trend to evaluate
        source_platform: Where the trend was encountered

    Returns:
        Scientific evaluation of the trend with verdict and recommendations
    """
    report = """# Trend Evaluation Report

*Separating science from social media hype*

---

"""

    # Try to find trend in database
    trend_data = None
    matched_name = None

    if trend_name:
        normalized = trend_name.lower().strip().replace(" ", "_").replace("-", "_")

        # Direct match
        if normalized in TREND_DATABASE:
            trend_data = TREND_DATABASE[normalized]
            matched_name = normalized
        else:
            # Fuzzy matching
            aliases = {
                "vaseline_slug": "slugging",
                "aquaphor_slug": "slugging",
                "skin_cycle": "skin_cycling",
                "cycling": "skin_cycling",
                "double_cleanse": "double_cleansing",
                "oil_cleansing": "double_cleansing",
                "retinoid_sandwich": "sandwich_method",
                "moisturizer_sandwich": "sandwich_method",
                "buffering_retinol": "sandwich_method",
                "ice_facial": "ice_rolling",
                "cryotherapy_facial": "ice_rolling",
                "jade_roller": "gua_sha",
                "facial_massage": "gua_sha",
                "lymphatic_massage": "gua_sha",
                "diy_spf": "diy_sunscreen",
                "homemade_sunscreen": "diy_sunscreen",
                "lemon_juice": "lemon_on_face",
                "citrus_brightening": "lemon_on_face",
                "toothpaste_acne": "toothpaste_on_pimples",
                "face_yoga": "facial_exercises",
                "facial_yoga": "facial_exercises",
                "gallon_water": "drinking_water_for_skin",
                "water_gallon": "drinking_water_for_skin",
                "acv_toner": "apple_cider_vinegar_toner",
                "vinegar_toner": "apple_cider_vinegar_toner",
                "skin_flood": "skin_flooding",
                "hydration_flooding": "skin_flooding",
                "cosrx_snail": "snail_mucin",
                "snail_essence": "snail_mucin",
                "face_shaving": "dermaplaning",
            }

            if normalized in aliases:
                matched_name = aliases[normalized]
                trend_data = TREND_DATABASE.get(matched_name)

            # Partial matching
            if not trend_data:
                for key in TREND_DATABASE:
                    if key in normalized or normalized in key:
                        trend_data = TREND_DATABASE[key]
                        matched_name = key
                        break

    if trend_data:
        # Known trend - provide full analysis
        verdict_emoji = {
            "VALIDATED": "✅",
            "MIXED": "🟡",
            "PARTIALLY TRUE": "🟡",
            "PROMISING": "🔵",
            "INEFFECTIVE": "❌",
            "HARMFUL": "🔴",
            "DANGEROUS": "🚨",
            "OVERSTATED": "⚠️",
            "RISKY": "⚠️",
        }.get(trend_data["verdict"], "❓")

        report += f"## {verdict_emoji} {trend_name or matched_name.replace('_', ' ').title()}\n\n"

        if matched_name and trend_name and matched_name.replace("_", " ") != trend_name.lower():
            report += f"*Matched to known trend: {matched_name.replace('_', ' ').title()}*\n\n"

        report += f"**Description:** {trend_data['description']}\n\n"

        # Verdict box
        verdict_color = {
            "VALIDATED": "green",
            "MIXED": "yellow",
            "PROMISING": "blue",
            "INEFFECTIVE": "red",
            "HARMFUL": "red",
            "DANGEROUS": "red",
        }.get(trend_data["verdict"], "gray")

        report += f"""### Verdict: {trend_data['verdict']}

| Attribute | Assessment |
|-----------|------------|
| **Overall Verdict** | {verdict_emoji} {trend_data['verdict']} |
| **Evidence Grade** | {trend_data['evidence_grade']} |
| **Source Platform** | {source_platform.title()} |

---

### Scientific Analysis

**Mechanism:**
{trend_data['mechanism']}

**Scientific Basis:**
{trend_data['scientific_basis']}

---

### Benefits
"""
        for benefit in trend_data["benefits"]:
            report += f"- ✓ {benefit}\n"

        report += "\n### Risks\n"
        for risk in trend_data["risks"]:
            if "SEVERE" in risk or "chemical burn" in risk.lower() or "cancer" in risk.lower():
                report += f"- 🚨 {risk}\n"
            else:
                report += f"- ⚠️ {risk}\n"

        report += f"""
---

### Who Should Try This?

**Good candidates:**
"""
        for candidate in trend_data["who_should_try"]:
            report += f"- {candidate}\n"

        report += "\n**Should avoid:**\n"
        for avoid in trend_data["who_should_avoid"]:
            report += f"- {avoid}\n"

        if trend_data["verdict"] not in ["HARMFUL", "DANGEROUS", "INEFFECTIVE"]:
            report += f"""
---

### How To Do It Correctly

{trend_data['how_to_do_it']}
"""
        else:
            report += f"""
---

### ⚠️ Recommendation

**DO NOT TRY THIS TREND.**

{trend_data['how_to_do_it']}
"""

    else:
        # Unknown trend - provide general evaluation framework
        report += f"## 🔍 Unknown Trend: {trend_name or 'Not specified'}\n\n"

        if trend_description:
            report += f"**Description:** {trend_description}\n\n"

        report += """This trend is not in our database. Here's a framework to evaluate it:

### Red Flags to Watch For

🚨 **Immediate Disqualifiers:**
- Claims to be "natural" and therefore safe (naturalistic fallacy)
- Uses food-grade ingredients not meant for skin (lemon, baking soda, etc.)
- DIY sunscreen or claims to replace SPF
- Promises permanent structural changes (face "lifting" without procedures)
- Involves putting anything near eyes that isn't ophthalmologist-tested

⚠️ **Yellow Flags (Proceed with Caution):**
- No peer-reviewed studies cited
- Only anecdotal evidence ("it worked for me!")
- Creator is selling the product they're recommending
- Before/after photos without controlling for lighting
- Claims that seem too good to be true

✅ **Green Flags (More Likely Legitimate):**
- Dermatologists/scientists verify the mechanism
- Based on established skincare science
- Ingredient has peer-reviewed research
- Reasonable, realistic claims
- Acknowledges that results vary

---

### Questions to Ask

1. **What's the mechanism?** How does this supposedly work? If no one can explain it, it probably doesn't.

2. **What's the evidence?** Anecdotes ≠ evidence. Look for studies.

3. **What could go wrong?** Every treatment has potential downsides. If someone claims there are none, be suspicious.

4. **Who's promoting this?** Are they selling something? What are their credentials?

5. **Is this just repackaged old advice?** Many "trends" are established practices with new names.

---

### How to Research a Trend

1. **PubMed search** - Search for the key ingredient or technique
2. **Dermatologist review** - Search for board-certified derm opinions
3. **Check the claims** - Are benefits specific and measurable, or vague?
4. **Look for risks** - What happens if this goes wrong?

"""

        if claims:
            report += "### Claims to Evaluate\n\n"
            for claim in claims:
                report += f"**Claim:** \"{claim}\"\n"
                report += _evaluate_claim(claim)
                report += "\n"

    report += """---

## Evidence Grade Key

| Grade | Meaning |
|-------|---------|
| **A** | Strong peer-reviewed evidence, multiple RCTs |
| **B** | Good evidence, some quality studies |
| **C** | Limited evidence, mostly observational |
| **D** | Very limited evidence, mostly anecdotal |
| **F** | Contrary to evidence, potentially harmful |

---

## Quick Reference: Common Trend Categories

| Category | Examples | General Verdict |
|----------|----------|-----------------|
| **Occlusion/Barrier** | Slugging, skin flooding | Usually valid |
| **Physical tools** | Gua sha, ice rolling | Temporary effects, overpromised |
| **DIY ingredients** | Lemon, ACV, baking soda | Usually harmful |
| **Routine strategies** | Skin cycling, double cleansing | Usually valid |
| **"Natural" claims** | Replace SPF with oils | Dangerous |

---

*When in doubt, ask a dermatologist. No trend is worth damaging your skin.*
"""

    return report


def _evaluate_claim(claim: str) -> str:
    """Evaluate a specific claim against scientific knowledge."""
    claim_lower = claim.lower()

    evaluations = []

    # Check for common false claims
    if "shrink pores permanently" in claim_lower or "close pores" in claim_lower:
        evaluations.append(
            "⚠️ **Pore size is genetic.** You can minimize appearance temporarily, but you cannot permanently shrink pores."
        )

    if "detox" in claim_lower and "skin" in claim_lower:
        evaluations.append(
            "⚠️ **Skin doesn't 'detox.'** Your liver and kidneys handle detoxification. Skincare doesn't detoxify."
        )

    if "lift" in claim_lower or "sculpt" in claim_lower:
        if "permanent" in claim_lower or "tone muscle" in claim_lower:
            evaluations.append(
                "⚠️ **Topicals and massage cannot permanently lift skin.** Only procedures (surgery, threads, lasers) can restructure."
            )

    if "instant" in claim_lower and ("wrinkle" in claim_lower or "aging" in claim_lower):
        evaluations.append(
            "⚠️ **Anti-aging takes time.** Retinoids take 3-6 months. 'Instant' results are temporary optical illusions."
        )

    if "replace sunscreen" in claim_lower or "natural spf" in claim_lower:
        evaluations.append(
            "🚨 **DANGEROUS CLAIM.** No food-grade or DIY ingredient can replace tested SPF. This leads to burns and skin cancer risk."
        )

    if "cure" in claim_lower and ("acne" in claim_lower or "eczema" in claim_lower or "rosacea" in claim_lower):
        evaluations.append(
            "⚠️ **No topical 'cures' these conditions.** They can be managed, not cured. Be wary of cure claims."
        )

    if not evaluations:
        evaluations.append(
            "ℹ️ *Unable to specifically evaluate this claim. Apply the general framework above.*"
        )

    return "\n".join(evaluations)
