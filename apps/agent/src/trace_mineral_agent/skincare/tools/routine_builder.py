"""Routine builder tool for constructing personalized skincare routines.

Builds AM/PM routines based on skin profile, concerns, and product preferences,
with proper layering order and active scheduling.
"""

from typing import Literal

from langchain_core.tools import tool


# Product category layering order (thinnest to thickest, water-based to oil-based)
LAYERING_ORDER_AM = [
    "cleanser",
    "toner",
    "essence",
    "treatment_serum",
    "hydrating_serum",
    "eye_cream",
    "moisturizer",
    "facial_oil",
    "sunscreen",
]

LAYERING_ORDER_PM = [
    "first_cleanser",
    "second_cleanser",
    "toner",
    "exfoliant",
    "essence",
    "treatment_serum",
    "retinoid",
    "hydrating_serum",
    "eye_cream",
    "moisturizer",
    "facial_oil",
    "sleeping_mask",
]


# Product recommendations by concern and budget
PRODUCT_TEMPLATES: dict[str, dict] = {
    "cleanser": {
        "purpose": "Remove dirt, oil, and makeup without stripping skin",
        "when": "AM and PM",
        "oily": {
            "ingredients": ["Salicylic acid", "Niacinamide", "Glycolic acid (low %)"],
            "textures": ["Gel", "Foam", "Micellar water"],
            "budget": ["CeraVe Foaming", "La Roche-Posay Effaclar", "Vanicream Gentle"],
            "mid": ["Paula's Choice Pore Normalizing", "Krave Beauty Matcha Hemp"],
            "premium": ["SkinCeuticals LHA Cleanser", "iS Clinical Cleansing Complex"],
        },
        "dry": {
            "ingredients": ["Ceramides", "Glycerin", "Oils"],
            "textures": ["Cream", "Oil", "Milk", "Balm"],
            "budget": ["CeraVe Hydrating", "Vanicream Gentle", "Cetaphil Gentle"],
            "mid": ["Krave Beauty Matcha Hemp", "Youth to the People Kale+Green Tea"],
            "premium": ["Tatcha Rice Wash", "Drunk Elephant Beste"],
        },
        "combination": {
            "ingredients": ["Gentle surfactants", "Niacinamide"],
            "textures": ["Gel-cream", "Low-foam"],
            "budget": ["CeraVe Hydrating", "La Roche-Posay Toleriane"],
            "mid": ["Krave Beauty Matcha Hemp", "Glossier Milky Jelly"],
            "premium": ["Tatcha Rice Wash", "Fresh Soy Face Cleanser"],
        },
        "sensitive": {
            "ingredients": ["Minimal ingredients", "No fragrance", "Ceramides"],
            "textures": ["Cream", "Milk", "Micellar"],
            "budget": ["Vanicream Gentle", "CeraVe Hydrating", "Cetaphil Gentle"],
            "mid": ["La Roche-Posay Toleriane Caring Wash", "Aveeno Calm+Restore"],
            "premium": ["Avène Extremely Gentle", "Bioderma Sensibio"],
        },
    },
    "toner": {
        "purpose": "Balance pH, add hydration, prep skin for treatments",
        "when": "AM and/or PM after cleansing",
        "oily": {
            "ingredients": ["Niacinamide", "BHA", "Witch hazel (alcohol-free)", "AHA"],
            "budget": ["Thayers Witch Hazel (alcohol-free)", "CosRx BHA Power Liquid"],
            "mid": ["Paula's Choice 2% BHA", "Some By Mi AHA/BHA/PHA Toner"],
            "premium": ["Biologique Recherche P50", "SkinCeuticals Equalizing Toner"],
        },
        "dry": {
            "ingredients": ["Hyaluronic acid", "Glycerin", "Centella", "Panthenol"],
            "budget": ["Hada Labo Gokujyun", "Kikumasamune High Moist"],
            "mid": ["Klairs Supple Preparation", "Pyunkang Yul Essence Toner"],
            "premium": ["Tatcha Essence", "SK-II Facial Treatment Essence"],
        },
        "combination": {
            "ingredients": ["Hyaluronic acid", "Niacinamide", "Light exfoliants"],
            "budget": ["CosRx Snail Mucin Essence", "Hada Labo Gokujyun"],
            "mid": ["Klairs Supple Preparation", "Paula's Choice Enriched Calming"],
            "premium": ["Fresh Rose Deep Hydration Toner", "Tatcha Essence"],
        },
        "sensitive": {
            "ingredients": ["Centella", "Panthenol", "Minimal ingredients"],
            "budget": ["Soon Jung pH 5.5 Relief Toner", "Pyunkang Yul Essence Toner"],
            "mid": ["Klairs Supple Preparation Unscented", "Aveeno Calm+Restore Toner"],
            "premium": ["Avène Thermal Spring Water", "La Roche-Posay Thermal Water"],
        },
    },
    "vitamin_c_serum": {
        "purpose": "Antioxidant protection, brightening, collagen support",
        "when": "AM (best for antioxidant protection)",
        "general": {
            "forms": {
                "L-Ascorbic Acid": "Most potent, least stable, can irritate",
                "SAP": "Stable, gentle, good for acne-prone",
                "Ascorbyl Glucoside": "Very stable, very gentle, less potent",
                "Ethyl Ascorbic Acid": "Stable, good penetration",
            },
            "budget": ["Timeless 20% Vitamin C+E+Ferulic", "The Ordinary 23% Vitamin C Suspension"],
            "mid": ["Paula's Choice C15 Booster", "Maelove Glow Maker"],
            "premium": ["SkinCeuticals C E Ferulic", "Drunk Elephant C-Firma"],
        },
    },
    "retinoid": {
        "purpose": "Cell turnover, collagen stimulation, anti-aging, acne",
        "when": "PM only (photosensitizing)",
        "beginner": {
            "ingredients": ["Retinol 0.25-0.5%", "Retinal", "Bakuchiol"],
            "budget": ["The Ordinary Retinol 0.5%", "CeraVe Resurfacing Retinol"],
            "mid": ["Paula's Choice 1% Retinol", "Versed Press Restart"],
            "premium": ["Shani Darden Retinol Reform", "Drunk Elephant A-Passioni"],
        },
        "intermediate": {
            "ingredients": ["Retinol 0.5-1%", "Retinal 0.05-0.1%"],
            "budget": ["The Ordinary Retinol 1%"],
            "mid": ["Paula's Choice Clinical 1% Retinol", "Geek & Gorgeous A-Game 0.1%"],
            "premium": ["SkinCeuticals Retinol 0.5", "Murad Retinol Youth Renewal"],
        },
        "advanced": {
            "ingredients": ["Tretinoin 0.025-0.1% (Rx)", "Adapalene 0.3% (Rx)", "Tazarotene (Rx)"],
            "budget": ["Adapalene 0.1% (Differin OTC)"],
            "mid": ["Tretinoin generic (Rx)"],
            "premium": ["Altreno (tretinoin lotion)", "Retin-A Micro"],
        },
    },
    "moisturizer": {
        "purpose": "Seal in hydration, support barrier function",
        "when": "AM and PM",
        "oily": {
            "ingredients": ["Hyaluronic acid", "Niacinamide", "Light emollients"],
            "textures": ["Gel", "Gel-cream", "Water cream", "Lotion"],
            "budget": ["Neutrogena Hydro Boost", "CeraVe PM", "Vanicream Daily"],
            "mid": ["Paula's Choice Skin Balancing", "Krave Great Barrier Relief"],
            "premium": ["Tatcha Water Cream", "Belif Aqua Bomb"],
        },
        "dry": {
            "ingredients": ["Ceramides", "Squalane", "Shea butter", "Fatty acids"],
            "textures": ["Cream", "Rich cream", "Balm"],
            "budget": ["CeraVe Moisturizing Cream", "Vanicream Moisturizing Cream", "Eucerin Original"],
            "mid": ["La Roche-Posay Toleriane Ultra", "First Aid Beauty Ultra Repair"],
            "premium": ["Dr. Jart Ceramidin Cream", "Charlotte Tilbury Magic Cream"],
        },
        "combination": {
            "ingredients": ["Niacinamide", "Ceramides", "Hyaluronic acid"],
            "textures": ["Lotion", "Light cream", "Gel-cream"],
            "budget": ["CeraVe PM", "Neutrogena Hydro Boost"],
            "mid": ["Paula's Choice Resist Barrier Repair", "Youth to the People Adaptogen"],
            "premium": ["Drunk Elephant Protini", "Tatcha Dewy Skin Cream"],
        },
        "sensitive": {
            "ingredients": ["Ceramides", "Centella", "Minimal ingredients", "No fragrance"],
            "textures": ["Cream", "Lotion"],
            "budget": ["Vanicream Moisturizing Cream", "CeraVe Moisturizing Cream"],
            "mid": ["La Roche-Posay Toleriane Ultra", "Aveeno Calm+Restore Oat Gel"],
            "premium": ["Avène Skin Recovery Cream", "Bioderma Sensibio Light"],
        },
    },
    "sunscreen": {
        "purpose": "Protection from UVA/UVB, prevent photoaging, hyperpigmentation",
        "when": "AM (final step, reapply every 2 hours if exposed)",
        "oily": {
            "types": ["Chemical/organic filters", "Gel", "Fluid", "Mattifying"],
            "budget": ["Neutrogena Clear Face", "La Roche-Posay Anthelios Light Fluid"],
            "mid": ["Supergoop Unseen Sunscreen", "Paula's Choice Essential Glow"],
            "premium": ["Shiseido Ultimate Sun Protector", "Isntree Hyaluronic Acid Watery Sun Gel"],
        },
        "dry": {
            "types": ["Moisturizing chemical", "Hybrid", "Cream texture"],
            "budget": ["CeraVe AM Moisturizing Lotion SPF 30", "Neutrogena Hydro Boost SPF 50"],
            "mid": ["Supergoop Glowscreen", "Australian Gold Botanical Tinted"],
            "premium": ["Tatcha Silken Pore Perfecting SPF", "Elta MD UV Clear"],
        },
        "combination": {
            "types": ["Light fluid", "Gel-cream", "Hybrid"],
            "budget": ["La Roche-Posay Anthelios", "Neutrogena Ultra Sheer"],
            "mid": ["Supergoop Play", "Canmake Mermaid Skin Gel UV"],
            "premium": ["Elta MD UV Clear", "Murad City Skin Age Defense"],
        },
        "sensitive": {
            "types": ["Mineral/physical (zinc, titanium)", "Fragrance-free"],
            "budget": ["CeraVe Hydrating Mineral SPF 30", "Vanicream SPF 30"],
            "mid": ["La Roche-Posay Anthelios Mineral", "Pipette Mineral SPF 50"],
            "premium": ["Elta MD UV Physical", "Colorescience Sunforgettable"],
        },
    },
    "exfoliant": {
        "purpose": "Remove dead skin, improve texture, enhance penetration",
        "when": "PM (start 1-2x/week, build up)",
        "oily": {
            "types": ["BHA (salicylic acid)", "AHA (glycolic)", "Combination acids"],
            "budget": ["Stridex Maximum Pads", "The Ordinary Glycolic Acid 7% Toner"],
            "mid": ["Paula's Choice 2% BHA Liquid", "Drunk Elephant T.L.C. Sukari Babyfacial (weekly)"],
            "premium": ["Biologique Recherche P50", "SkinCeuticals Glycolic 10 Renew"],
        },
        "dry": {
            "types": ["AHA (lactic acid)", "PHA", "Enzyme exfoliants"],
            "budget": ["The Ordinary Lactic Acid 5%", "CosRx AHA/BHA Clarifying Toner"],
            "mid": ["Paula's Choice 8% AHA Gel", "Stratia Soft Touch AHA"],
            "premium": ["Sunday Riley Good Genes", "Drunk Elephant Babyfacial"],
        },
        "combination": {
            "types": ["AHA/BHA combinations", "Mandelic acid"],
            "budget": ["The Ordinary Mandelic Acid 10%", "CosRx AHA 7 Whitehead Power"],
            "mid": ["Paula's Choice 2% BHA Liquid", "By Wishtrend Mandelic Acid 5%"],
            "premium": ["Biologique Recherche P50", "Dr. Dennis Gross Alpha Beta Peel"],
        },
        "sensitive": {
            "types": ["PHA (gluconolactone)", "Mandelic acid", "Enzyme exfoliants"],
            "budget": ["The Ordinary Mandelic Acid 10%", "Inkey List PHA Toner"],
            "mid": ["Paula's Choice Calm Exfoliant", "By Wishtrend Mandelic 5%"],
            "premium": ["Goldfaden MD Fresh A Peel", "Kate Somerville ExfoliKate Gentle"],
        },
    },
}


@tool
def routine_builder(
    skin_type: Literal["oily", "dry", "combination", "normal", "sensitive"],
    primary_concerns: list[str],
    routine_complexity: Literal["minimal", "basic", "standard", "comprehensive"] = "standard",
    budget: Literal["budget", "mid", "premium", "mixed"] = "mixed",
    current_products: list[dict] | None = None,
    retinoid_experience: Literal["none", "beginner", "intermediate", "advanced"] = "beginner",
    lifestyle_constraints: dict | None = None,
    climate: Literal["humid", "dry", "temperate", "variable"] = "temperate",
) -> str:
    """Build a personalized skincare routine with proper layering and active scheduling.

    Creates AM/PM routines based on skin profile, concerns, and preferences,
    with detailed product recommendations and usage instructions.

    Args:
        skin_type: Primary skin type classification
        primary_concerns: Main skin concerns to address (e.g., acne, aging, hyperpigmentation)
        routine_complexity: How many steps (minimal=3, basic=5, standard=7, comprehensive=10+)
        budget: Budget level for recommendations (mixed allows combo of budget + splurge items)
        current_products: Products user already has (to integrate into routine)
        retinoid_experience: Experience level with retinoids for appropriate recommendations
        lifestyle_constraints: Time/lifestyle factors (e.g., minutes_am, minutes_pm, wears_makeup)
        climate: Primary climate for texture recommendations

    Returns:
        Comprehensive routine with AM/PM steps, product recommendations, and schedule
    """
    # Determine routine steps based on complexity
    complexity_config = {
        "minimal": {"am_steps": 3, "pm_steps": 3, "actives": 1},
        "basic": {"am_steps": 4, "pm_steps": 5, "actives": 2},
        "standard": {"am_steps": 5, "pm_steps": 7, "actives": 3},
        "comprehensive": {"am_steps": 6, "pm_steps": 9, "actives": 4},
    }
    config = complexity_config[routine_complexity]

    # Build concern-based active recommendations
    concern_actives = _get_actives_for_concerns(primary_concerns, skin_type)

    # Build AM routine
    am_routine = _build_am_routine(
        skin_type=skin_type,
        concerns=primary_concerns,
        max_steps=config["am_steps"],
        budget=budget,
        climate=climate,
    )

    # Build PM routine
    pm_routine = _build_pm_routine(
        skin_type=skin_type,
        concerns=primary_concerns,
        max_steps=config["pm_steps"],
        budget=budget,
        retinoid_level=retinoid_experience,
        climate=climate,
    )

    # Create weekly schedule for actives
    weekly_schedule = _create_weekly_schedule(
        concerns=primary_concerns,
        retinoid_level=retinoid_experience,
        skin_type=skin_type,
    )

    # Generate the report
    report = f"""# Personalized Skincare Routine

## Profile Summary

| Attribute | Value |
|-----------|-------|
| **Skin Type** | {skin_type.title()} |
| **Primary Concerns** | {', '.join(c.title() for c in primary_concerns)} |
| **Routine Complexity** | {routine_complexity.title()} |
| **Budget Preference** | {budget.title()} |
| **Climate** | {climate.title()} |
| **Retinoid Experience** | {retinoid_experience.title()} |

---

## ☀️ Morning Routine (AM)

*Goal: Protect, hydrate, prepare for the day*

| Step | Category | Wait Time | Purpose |
|------|----------|-----------|---------|
"""

    for i, step in enumerate(am_routine, 1):
        report += f"| {i} | {step['category']} | {step.get('wait_time', 'None')} | {step['purpose']} |\n"

    report += "\n### AM Product Recommendations\n\n"

    for step in am_routine:
        report += f"**{step['category'].title()}**\n"
        if "note" in step:
            report += f"*{step['note']}*\n"
        if "recommendations" in step:
            for level, products in step["recommendations"].items():
                if budget in ["mixed", level] or (budget == "mixed"):
                    report += f"- {level.title()}: {', '.join(products[:2])}\n"
        report += "\n"

    report += f"""---

## 🌙 Evening Routine (PM)

*Goal: Cleanse thoroughly, treat, repair*

| Step | Category | Wait Time | Purpose |
|------|----------|-----------|---------|
"""

    for i, step in enumerate(pm_routine, 1):
        report += f"| {i} | {step['category']} | {step.get('wait_time', 'None')} | {step['purpose']} |\n"

    report += "\n### PM Product Recommendations\n\n"

    for step in pm_routine:
        report += f"**{step['category'].title()}**\n"
        if "note" in step:
            report += f"*{step['note']}*\n"
        if "recommendations" in step:
            for level, products in step["recommendations"].items():
                if budget in ["mixed", level] or (budget == "mixed"):
                    report += f"- {level.title()}: {', '.join(products[:2])}\n"
        report += "\n"

    report += """---

## 📅 Weekly Active Schedule

*Rotating actives properly prevents over-exfoliation and maximizes efficacy*

"""

    for day, routine in weekly_schedule.items():
        report += f"**{day}**\n"
        report += f"- AM: {routine['am']}\n"
        report += f"- PM: {routine['pm']}\n"
        report += "\n"

    report += """---

## 🎯 Key Actives for Your Concerns

"""

    for concern, actives in concern_actives.items():
        report += f"### {concern.title()}\n\n"
        for active in actives:
            report += f"- **{active['name']}**: {active['why']}\n"
        report += "\n"

    report += """---

## ⚠️ Important Rules

### Layering Order
1. Thinnest to thickest consistency
2. Water-based before oil-based
3. Actives before moisturizer (usually)
4. Sunscreen ALWAYS last in AM

### Wait Times
- After Vitamin C: 1-2 minutes (let absorb)
- After acids: 5-10 minutes (if using with other actives)
- After retinoid: 20 minutes (if buffering)
- Before sunscreen: Let moisturizer absorb

### Don't Combine (Same Routine)
- Retinoid + AHA/BHA (too irritating)
- Retinoid + Benzoyl Peroxide (oxidizes retinoid)
- Vitamin C + Niacinamide (old myth - actually OK)
- Multiple exfoliating acids

### Sunscreen Non-Negotiables
- SPF 30 minimum, SPF 50 preferred
- Apply generously (1/4 teaspoon for face)
- Reapply every 2 hours if outdoors
- Even on cloudy days, even indoors near windows

---

## 🚀 Progression Plan

### Week 1-2: Foundation
- Focus on cleansing, moisturizing, sunscreen
- Introduce ONE active (start with niacinamide or vitamin C)
- No exfoliating acids or retinoids yet

### Week 3-4: Add Treatment
- Introduce chemical exfoliant 1x/week
- OR start retinoid 1x/week (not both)
- Monitor for irritation

### Week 5-8: Build Tolerance
- Slowly increase active frequency
- Add second active if tolerated
- Exfoliant up to 2-3x/week
- Retinoid up to 3x/week

### Week 9-12: Optimize
- Fine-tune routine based on results
- Can use retinoid more frequently if tolerated
- Maintain consistent routine

---

## 💡 Pro Tips

"""

    # Skin type specific tips
    tips = {
        "oily": [
            "Don't skip moisturizer - dehydrated skin produces MORE oil",
            "Niacinamide is your friend - regulates sebum",
            "Blotting papers > powder for midday touch-ups",
            "Gel cleansers work great, but don't over-cleanse",
        ],
        "dry": [
            "Apply products to damp skin to lock in moisture",
            "Consider a facial oil as the last step",
            "Hyaluronic acid MUST be sealed with moisturizer",
            "Avoid hot water - lukewarm only",
        ],
        "combination": [
            "Multi-masking is your friend (clay on T-zone, hydrating on cheeks)",
            "You may need different moisturizers for AM vs PM",
            "BHA works great for the T-zone specifically",
            "Don't be afraid to use different products on different zones",
        ],
        "sensitive": [
            "Patch test EVERYTHING for 24-48 hours",
            "Introduce one new product at a time, wait 2 weeks",
            "Fragrance-free doesn't mean unscented - check labels",
            "Mineral sunscreens are often better tolerated",
        ],
        "normal": [
            "Focus on prevention and maintenance",
            "You can experiment more freely with actives",
            "Don't overcomplicate - your skin is balanced",
            "SPF is still non-negotiable",
        ],
    }

    for tip in tips.get(skin_type, tips["normal"]):
        report += f"- {tip}\n"

    report += """

---

*This routine is a starting point. Listen to your skin and adjust as needed.
If you experience persistent irritation, scale back. Consult a dermatologist
for persistent concerns.*
"""

    return report


def _get_actives_for_concerns(concerns: list[str], skin_type: str) -> dict:
    """Get recommended active ingredients for each concern."""
    concern_mapping = {
        "acne": [
            {"name": "Salicylic Acid (BHA)", "why": "Oil-soluble, penetrates pores, antibacterial"},
            {"name": "Benzoyl Peroxide", "why": "Kills acne bacteria, no resistance develops"},
            {"name": "Niacinamide", "why": "Regulates sebum, anti-inflammatory"},
            {"name": "Retinoid", "why": "Prevents clogged pores, speeds cell turnover"},
        ],
        "aging": [
            {"name": "Retinoid", "why": "Gold standard for collagen stimulation"},
            {"name": "Vitamin C", "why": "Antioxidant protection, collagen synthesis"},
            {"name": "Peptides", "why": "Signal collagen production"},
            {"name": "SPF", "why": "Prevents future damage (most important!)"},
        ],
        "hyperpigmentation": [
            {"name": "Vitamin C", "why": "Inhibits tyrosinase, antioxidant"},
            {"name": "Niacinamide", "why": "Prevents melanin transfer"},
            {"name": "Alpha Arbutin", "why": "Tyrosinase inhibitor"},
            {"name": "Tranexamic Acid", "why": "Especially effective for melasma"},
        ],
        "texture": [
            {"name": "AHA (Glycolic/Lactic)", "why": "Exfoliates surface, smooths texture"},
            {"name": "Retinoid", "why": "Increases cell turnover"},
            {"name": "BHA (Salicylic)", "why": "Clears pores, smooths skin"},
            {"name": "Niacinamide", "why": "Improves skin texture over time"},
        ],
        "dryness": [
            {"name": "Hyaluronic Acid", "why": "Humectant, holds 1000x weight in water"},
            {"name": "Ceramides", "why": "Repairs and maintains barrier"},
            {"name": "Squalane", "why": "Emollient, mimics natural sebum"},
            {"name": "Glycerin", "why": "Humectant, draws moisture"},
        ],
        "redness": [
            {"name": "Centella Asiatica", "why": "Anti-inflammatory, healing"},
            {"name": "Niacinamide", "why": "Calming, strengthens barrier"},
            {"name": "Azelaic Acid", "why": "Anti-inflammatory, safe for rosacea"},
            {"name": "Panthenol", "why": "Soothing, barrier support"},
        ],
        "pores": [
            {"name": "BHA (Salicylic)", "why": "Clears pore congestion"},
            {"name": "Niacinamide", "why": "Minimizes pore appearance"},
            {"name": "Retinoid", "why": "Keeps pores clear, improves texture"},
            {"name": "Clay Masks", "why": "Absorbs excess oil (weekly)"},
        ],
        "dark circles": [
            {"name": "Vitamin C", "why": "Brightens, especially if pigmentation-based"},
            {"name": "Caffeine", "why": "Reduces puffiness, constricts blood vessels"},
            {"name": "Retinol (gentle)", "why": "Thickens skin over time"},
            {"name": "Peptides", "why": "Supports collagen in thin under-eye skin"},
        ],
    }

    result = {}
    for concern in concerns:
        normalized = concern.lower().strip()
        # Try direct match or partial match
        for key in concern_mapping:
            if key in normalized or normalized in key:
                result[concern] = concern_mapping[key]
                break
        if concern not in result:
            # Default recommendations
            result[concern] = [
                {"name": "Consult dermatologist", "why": "For specific guidance on this concern"}
            ]

    return result


def _build_am_routine(
    skin_type: str,
    concerns: list[str],
    max_steps: int,
    budget: str,
    climate: str,
) -> list[dict]:
    """Build morning routine."""
    routine = []

    # Always: Cleanser
    cleanser_data = PRODUCT_TEMPLATES["cleanser"]
    skin_recs = cleanser_data.get(skin_type, cleanser_data.get("combination"))
    routine.append({
        "category": "Cleanser",
        "purpose": "Cleanse overnight buildup",
        "wait_time": "None",
        "note": "Gentle cleanser in AM, or just water if dry",
        "recommendations": {
            "budget": skin_recs.get("budget", [])[:2],
            "mid": skin_recs.get("mid", [])[:2],
            "premium": skin_recs.get("premium", [])[:2],
        },
    })

    if max_steps > 3:
        # Toner (if complexity allows)
        toner_data = PRODUCT_TEMPLATES["toner"]
        toner_recs = toner_data.get(skin_type, toner_data.get("combination"))
        routine.append({
            "category": "Hydrating Toner",
            "purpose": "Hydrate, balance pH",
            "wait_time": "None",
            "note": "Optional but adds hydration layer",
            "recommendations": {
                "budget": toner_recs.get("budget", [])[:2],
                "mid": toner_recs.get("mid", [])[:2],
                "premium": toner_recs.get("premium", [])[:2],
            },
        })

    if max_steps > 4:
        # Vitamin C (treatment)
        vc_data = PRODUCT_TEMPLATES["vitamin_c_serum"]["general"]
        routine.append({
            "category": "Vitamin C Serum",
            "purpose": "Antioxidant protection, brightening",
            "wait_time": "1-2 min",
            "note": "Best used in AM for antioxidant protection throughout day",
            "recommendations": {
                "budget": vc_data.get("budget", [])[:2],
                "mid": vc_data.get("mid", [])[:2],
                "premium": vc_data.get("premium", [])[:2],
            },
        })

    # Moisturizer
    moist_data = PRODUCT_TEMPLATES["moisturizer"]
    moist_recs = moist_data.get(skin_type, moist_data.get("combination"))
    routine.append({
        "category": "Moisturizer",
        "purpose": "Hydrate, seal in previous layers",
        "wait_time": "1 min",
        "note": "Lighter texture for AM, especially if oily",
        "recommendations": {
            "budget": moist_recs.get("budget", [])[:2],
            "mid": moist_recs.get("mid", [])[:2],
            "premium": moist_recs.get("premium", [])[:2],
        },
    })

    # ALWAYS: Sunscreen
    spf_data = PRODUCT_TEMPLATES["sunscreen"]
    spf_recs = spf_data.get(skin_type, spf_data.get("combination"))
    routine.append({
        "category": "Sunscreen",
        "purpose": "CRITICAL: UV protection",
        "wait_time": "None (last step)",
        "note": "SPF 30 minimum, apply generously. Non-negotiable!",
        "recommendations": {
            "budget": spf_recs.get("budget", [])[:2],
            "mid": spf_recs.get("mid", [])[:2],
            "premium": spf_recs.get("premium", [])[:2],
        },
    })

    return routine[:max_steps]


def _build_pm_routine(
    skin_type: str,
    concerns: list[str],
    max_steps: int,
    budget: str,
    retinoid_level: str,
    climate: str,
) -> list[dict]:
    """Build evening routine."""
    routine = []

    # Double cleanse (if comprehensive)
    if max_steps >= 7:
        routine.append({
            "category": "Oil/Balm Cleanser",
            "purpose": "Remove sunscreen, makeup, sebum",
            "wait_time": "None",
            "note": "First cleanse dissolves oil-based impurities",
            "recommendations": {
                "budget": ["Kose Softymo Speedy", "DHC Deep Cleansing Oil"],
                "mid": ["Banila Co Clean It Zero", "Clinique Take the Day Off"],
                "premium": ["Tatcha Pure One Step", "Drunk Elephant Slaai"],
            },
        })

    # Second cleanser / only cleanser
    cleanser_data = PRODUCT_TEMPLATES["cleanser"]
    skin_recs = cleanser_data.get(skin_type, cleanser_data.get("combination"))
    routine.append({
        "category": "Water-Based Cleanser",
        "purpose": "Remove remaining residue",
        "wait_time": "None",
        "note": "Second cleanse removes water-based impurities",
        "recommendations": {
            "budget": skin_recs.get("budget", [])[:2],
            "mid": skin_recs.get("mid", [])[:2],
            "premium": skin_recs.get("premium", [])[:2],
        },
    })

    if max_steps > 4:
        # Toner
        toner_data = PRODUCT_TEMPLATES["toner"]
        toner_recs = toner_data.get(skin_type, toner_data.get("combination"))
        routine.append({
            "category": "Toner",
            "purpose": "Balance, prep for treatments",
            "wait_time": "None",
            "recommendations": {
                "budget": toner_recs.get("budget", [])[:2],
                "mid": toner_recs.get("mid", [])[:2],
                "premium": toner_recs.get("premium", [])[:2],
            },
        })

    # Exfoliant OR Retinoid (alternating - show both)
    if max_steps > 5:
        exf_data = PRODUCT_TEMPLATES["exfoliant"]
        exf_recs = exf_data.get(skin_type, exf_data.get("combination"))
        routine.append({
            "category": "Exfoliant (alternate nights)",
            "purpose": "Cell turnover, texture refinement",
            "wait_time": "10-20 min (if using other actives)",
            "note": "Use 2-3x/week. Skip on retinoid nights.",
            "recommendations": {
                "budget": exf_recs.get("budget", [])[:2],
                "mid": exf_recs.get("mid", [])[:2],
                "premium": exf_recs.get("premium", [])[:2],
            },
        })

    # Retinoid
    ret_data = PRODUCT_TEMPLATES["retinoid"]
    ret_recs = ret_data.get(retinoid_level, ret_data["beginner"])
    routine.append({
        "category": "Retinoid (alternate nights)",
        "purpose": "Anti-aging, acne, cell turnover",
        "wait_time": "20 min (if sensitive, apply to dry skin)",
        "note": f"Level: {retinoid_level}. Build up slowly. Skip on exfoliant nights.",
        "recommendations": {
            "budget": ret_recs.get("budget", [])[:2],
            "mid": ret_recs.get("mid", [])[:2],
            "premium": ret_recs.get("premium", [])[:2],
        },
    })

    if max_steps > 6:
        # Treatment serum
        routine.append({
            "category": "Treatment Serum",
            "purpose": "Target specific concerns",
            "wait_time": "1-2 min",
            "note": "Niacinamide, peptides, or concern-specific serum",
            "recommendations": {
                "budget": ["The Ordinary Niacinamide 10%", "Inkey List Peptide Moisturizer"],
                "mid": ["Paula's Choice 10% Niacinamide Booster", "Stratia Rewind"],
                "premium": ["SkinCeuticals Discoloration Defense", "Drunk Elephant Protini"],
            },
        })

    # Moisturizer
    moist_data = PRODUCT_TEMPLATES["moisturizer"]
    moist_recs = moist_data.get(skin_type, moist_data.get("combination"))
    routine.append({
        "category": "Moisturizer",
        "purpose": "Seal in treatments, overnight repair",
        "wait_time": "None",
        "note": "Can use richer cream at night than AM",
        "recommendations": {
            "budget": moist_recs.get("budget", [])[:2],
            "mid": moist_recs.get("mid", [])[:2],
            "premium": moist_recs.get("premium", [])[:2],
        },
    })

    if max_steps >= 8 and skin_type in ["dry", "sensitive"]:
        routine.append({
            "category": "Facial Oil (optional)",
            "purpose": "Extra moisture seal for dry skin",
            "wait_time": "None (last step)",
            "note": "Optional for dry skin types. Skip if oily.",
            "recommendations": {
                "budget": ["The Ordinary 100% Squalane", "TO Rosehip Oil"],
                "mid": ["Herbivore Lapis Oil", "Youth to the People Superberry"],
                "premium": ["Drunk Elephant Marula Oil", "Tatcha Gold Camellia Oil"],
            },
        })

    return routine[:max_steps]


def _create_weekly_schedule(
    concerns: list[str],
    retinoid_level: str,
    skin_type: str,
) -> dict:
    """Create weekly schedule for actives."""
    # Base schedule varies by retinoid experience
    if retinoid_level == "none" or retinoid_level == "beginner":
        schedule = {
            "Monday": {"am": "Vitamin C, SPF", "pm": "Hydrating serums only"},
            "Tuesday": {"am": "Vitamin C, SPF", "pm": "Exfoliant (AHA/BHA)"},
            "Wednesday": {"am": "Vitamin C, SPF", "pm": "Retinoid (start here)"},
            "Thursday": {"am": "Vitamin C, SPF", "pm": "Hydrating serums only"},
            "Friday": {"am": "Vitamin C, SPF", "pm": "Exfoliant (AHA/BHA)"},
            "Saturday": {"am": "Vitamin C, SPF", "pm": "Hydrating serums only"},
            "Sunday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
        }
    elif retinoid_level == "intermediate":
        schedule = {
            "Monday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
            "Tuesday": {"am": "Vitamin C, SPF", "pm": "Exfoliant (AHA/BHA)"},
            "Wednesday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
            "Thursday": {"am": "Vitamin C, SPF", "pm": "Hydrating serums only"},
            "Friday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
            "Saturday": {"am": "Vitamin C, SPF", "pm": "Exfoliant (AHA/BHA)"},
            "Sunday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
        }
    else:  # advanced
        schedule = {
            "Monday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
            "Tuesday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
            "Wednesday": {"am": "Vitamin C, SPF", "pm": "Exfoliant (AHA/BHA)"},
            "Thursday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
            "Friday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
            "Saturday": {"am": "Vitamin C, SPF", "pm": "Retinoid"},
            "Sunday": {"am": "Vitamin C, SPF", "pm": "Hydrating mask or light peel"},
        }

    return schedule
