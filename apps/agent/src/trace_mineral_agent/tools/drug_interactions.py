"""Drug interaction checker tool for trace minerals."""

from typing import Literal

from langchain_core.tools import tool

# Known drug-mineral interactions database
# Source: Various pharmacology references, Natural Medicines Database
INTERACTIONS = {
    "chromium": {
        "high": [
            {
                "drug": "insulin",
                "drugs": ["insulin", "insulin glargine", "insulin lispro", "insulin aspart"],
                "effect": "May enhance hypoglycemic effect",
                "mechanism": "Additive insulin sensitization",
                "recommendation": "Monitor blood glucose closely. May need insulin dose adjustment.",
            },
            {
                "drug": "sulfonylureas",
                "drugs": ["glipizide", "glyburide", "glimepiride"],
                "effect": "May enhance hypoglycemic effect",
                "mechanism": "Additive effect on insulin secretion/sensitivity",
                "recommendation": "Monitor blood glucose. Consider dose reduction.",
            },
        ],
        "moderate": [
            {
                "drug": "metformin",
                "drugs": ["metformin"],
                "effect": "Additive glucose-lowering effect",
                "mechanism": "Both improve insulin sensitivity",
                "recommendation": "Monitor blood glucose. Generally safe combination.",
            },
            {
                "drug": "levothyroxine",
                "drugs": ["levothyroxine", "synthroid", "tirosint"],
                "effect": "May affect thyroid hormone levels",
                "mechanism": "Chromium may affect thyroid function",
                "recommendation": "Monitor thyroid function. Space doses 4 hours apart.",
            },
        ],
        "low": [
            {
                "drug": "NSAIDs",
                "drugs": ["ibuprofen", "naproxen", "aspirin"],
                "effect": "May increase chromium absorption",
                "mechanism": "NSAID-induced GI irritation may increase absorption",
                "recommendation": "No action typically needed.",
            },
        ],
    },
    "zinc": {
        "high": [
            {
                "drug": "penicillamine",
                "drugs": ["penicillamine", "cuprimine"],
                "effect": "Reduced absorption of both",
                "mechanism": "Chelation complex formation",
                "recommendation": "Space doses by at least 2 hours.",
            },
        ],
        "moderate": [
            {
                "drug": "quinolone antibiotics",
                "drugs": ["ciprofloxacin", "levofloxacin", "moxifloxacin"],
                "effect": "Reduced antibiotic absorption",
                "mechanism": "Zinc chelates quinolones in GI tract",
                "recommendation": "Take antibiotic 2 hours before or 6 hours after zinc.",
            },
            {
                "drug": "tetracycline antibiotics",
                "drugs": ["tetracycline", "doxycycline", "minocycline"],
                "effect": "Reduced absorption of both",
                "mechanism": "Chelation in GI tract",
                "recommendation": "Space doses by at least 2 hours.",
            },
            {
                "drug": "ACE inhibitors",
                "drugs": ["lisinopril", "enalapril", "ramipril", "captopril"],
                "effect": "May decrease zinc levels",
                "mechanism": "ACE inhibitors increase zinc excretion",
                "recommendation": "Monitor zinc status with long-term ACE inhibitor use.",
            },
        ],
        "low": [
            {
                "drug": "diuretics",
                "drugs": ["furosemide", "hydrochlorothiazide", "chlorthalidone"],
                "effect": "May increase zinc excretion",
                "mechanism": "Increased urinary zinc loss",
                "recommendation": "Consider zinc status monitoring with chronic use.",
            },
        ],
    },
    "magnesium": {
        "high": [
            {
                "drug": "muscle relaxants",
                "drugs": ["succinylcholine", "vecuronium", "rocuronium"],
                "effect": "Enhanced neuromuscular blockade",
                "mechanism": "Magnesium enhances neuromuscular block",
                "recommendation": "Use caution in surgical settings. Alert anesthesiologist.",
            },
        ],
        "moderate": [
            {
                "drug": "bisphosphonates",
                "drugs": ["alendronate", "risedronate", "zoledronic acid"],
                "effect": "Reduced bisphosphonate absorption",
                "mechanism": "Chelation in GI tract",
                "recommendation": "Take bisphosphonate 30 min before magnesium.",
            },
            {
                "drug": "quinolone antibiotics",
                "drugs": ["ciprofloxacin", "levofloxacin", "moxifloxacin"],
                "effect": "Reduced antibiotic absorption",
                "mechanism": "Magnesium chelates quinolones",
                "recommendation": "Space doses by 2-4 hours.",
            },
            {
                "drug": "digoxin",
                "drugs": ["digoxin"],
                "effect": "Low magnesium increases digoxin toxicity risk",
                "mechanism": "Hypomagnesemia sensitizes to digoxin effects",
                "recommendation": "Maintain adequate magnesium levels.",
            },
        ],
        "low": [
            {
                "drug": "proton pump inhibitors",
                "drugs": ["omeprazole", "pantoprazole", "esomeprazole"],
                "effect": "May reduce magnesium absorption",
                "mechanism": "Reduced gastric acid impairs mineral absorption",
                "recommendation": "Monitor magnesium with long-term PPI use.",
            },
        ],
    },
    "iron": {
        "high": [
            {
                "drug": "levothyroxine",
                "drugs": ["levothyroxine", "synthroid"],
                "effect": "Reduced levothyroxine absorption",
                "mechanism": "Iron binds thyroid hormone in GI tract",
                "recommendation": "Space doses by at least 4 hours.",
            },
        ],
        "moderate": [
            {
                "drug": "quinolone antibiotics",
                "drugs": ["ciprofloxacin", "levofloxacin"],
                "effect": "Reduced antibiotic absorption",
                "mechanism": "Iron chelates quinolones",
                "recommendation": "Space doses by 2 hours.",
            },
            {
                "drug": "tetracycline antibiotics",
                "drugs": ["tetracycline", "doxycycline"],
                "effect": "Reduced absorption of both",
                "mechanism": "Chelation complex formation",
                "recommendation": "Space doses by 2 hours.",
            },
            {
                "drug": "levodopa",
                "drugs": ["levodopa", "carbidopa-levodopa", "sinemet"],
                "effect": "Reduced levodopa absorption",
                "mechanism": "Iron chelates levodopa",
                "recommendation": "Space doses by 2 hours. Monitor Parkinson's symptoms.",
            },
            {
                "drug": "methyldopa",
                "drugs": ["methyldopa", "aldomet"],
                "effect": "Reduced methyldopa absorption",
                "mechanism": "Iron chelates methyldopa",
                "recommendation": "Space doses by 2 hours.",
            },
        ],
        "low": [
            {
                "drug": "antacids",
                "drugs": ["calcium carbonate", "magnesium hydroxide", "aluminum hydroxide"],
                "effect": "Reduced iron absorption",
                "mechanism": "Increased gastric pH reduces iron solubility",
                "recommendation": "Space doses by 1-2 hours.",
            },
        ],
    },
    "selenium": {
        "moderate": [
            {
                "drug": "statins",
                "drugs": ["atorvastatin", "simvastatin", "rosuvastatin"],
                "effect": "May reduce statin-related muscle symptoms",
                "mechanism": "Antioxidant protection of muscle tissue",
                "recommendation": "Generally beneficial interaction. No adjustment needed.",
            },
            {
                "drug": "chemotherapy",
                "drugs": ["cisplatin", "carboplatin", "doxorubicin"],
                "effect": "May protect against oxidative damage",
                "mechanism": "Antioxidant effect",
                "recommendation": "Consult oncologist before supplementing during chemo.",
            },
        ],
        "low": [
            {
                "drug": "anticoagulants",
                "drugs": ["warfarin", "heparin"],
                "effect": "Theoretical bleeding risk at high doses",
                "mechanism": "High-dose selenium may affect clotting",
                "recommendation": "Stay within recommended dose range.",
            },
        ],
    },
    "copper": {
        "high": [
            {
                "drug": "penicillamine",
                "drugs": ["penicillamine"],
                "effect": "Reduced copper absorption (therapeutic intent)",
                "mechanism": "Penicillamine chelates copper",
                "recommendation": "Expected effect in Wilson's disease treatment.",
            },
        ],
        "moderate": [
            {
                "drug": "zinc supplements",
                "drugs": ["zinc sulfate", "zinc gluconate", "zinc picolinate"],
                "effect": "Reduced copper absorption",
                "mechanism": "Zinc induces metallothionein which binds copper",
                "recommendation": "Maintain 8:1 zinc to copper ratio. Monitor copper status.",
            },
        ],
        "low": [
            {
                "drug": "antacids",
                "drugs": ["calcium carbonate", "magnesium hydroxide"],
                "effect": "May reduce copper absorption",
                "mechanism": "Increased gastric pH affects solubility",
                "recommendation": "Space doses if taking high-dose antacids.",
            },
        ],
    },
    "iodine": {
        "high": [
            {
                "drug": "amiodarone",
                "drugs": ["amiodarone"],
                "effect": "Increased risk of thyroid dysfunction",
                "mechanism": "Amiodarone contains iodine; additive iodine load",
                "recommendation": "Avoid iodine supplements. Monitor thyroid closely.",
            },
            {
                "drug": "lithium",
                "drugs": ["lithium"],
                "effect": "May worsen lithium-induced hypothyroidism",
                "mechanism": "Both affect thyroid hormone synthesis",
                "recommendation": "Monitor thyroid function. Use iodine cautiously.",
            },
        ],
        "moderate": [
            {
                "drug": "antithyroid drugs",
                "drugs": ["methimazole", "propylthiouracil"],
                "effect": "May counteract antithyroid effect",
                "mechanism": "Iodine is substrate for thyroid hormones",
                "recommendation": "Avoid high-dose iodine during hyperthyroid treatment.",
            },
        ],
    },
}


@tool
def check_drug_interactions(
    mineral: Literal[
        "chromium", "zinc", "magnesium", "iron", "selenium", "copper", "iodine"
    ],
    medications: list[str],
) -> str:
    """
    Check for potential drug-mineral interactions.

    Args:
        mineral: Trace mineral to check
        medications: List of medications to check against

    Returns:
        Markdown-formatted interaction warnings
    """
    if mineral not in INTERACTIONS:
        return f"**No interaction data available** for {mineral}."

    mineral_interactions = INTERACTIONS[mineral]
    medications_lower = [m.lower() for m in medications]

    found_interactions = {"high": [], "moderate": [], "low": []}

    for severity in ["high", "moderate", "low"]:
        for interaction in mineral_interactions.get(severity, []):
            # Check if any of the medication variants match
            interaction_drugs = [d.lower() for d in interaction["drugs"]]
            for med in medications_lower:
                if any(drug in med or med in drug for drug in interaction_drugs):
                    found_interactions[severity].append(interaction)
                    break

    # Format output
    output = f"## Interaction Report: {mineral.title()}\n\n"

    if not any(found_interactions.values()):
        output += f"**No interactions found** between {mineral} and the specified medications.\n\n"
        output += "### Medications Checked\n"
        for med in medications:
            output += f"- {med}\n"
        output += "\n*This does not guarantee safety. Consult a healthcare provider.*\n"
        return output

    if found_interactions["high"]:
        output += "### High Severity Interactions\n\n"
        for interaction in found_interactions["high"]:
            output += f"**{interaction['drug'].title()}**\n"
            output += f"- **Effect:** {interaction['effect']}\n"
            output += f"- **Mechanism:** {interaction['mechanism']}\n"
            output += f"- **Recommendation:** {interaction['recommendation']}\n\n"

    if found_interactions["moderate"]:
        output += "### Moderate Severity Interactions\n\n"
        for interaction in found_interactions["moderate"]:
            output += f"**{interaction['drug'].title()}**\n"
            output += f"- **Effect:** {interaction['effect']}\n"
            output += f"- **Mechanism:** {interaction['mechanism']}\n"
            output += f"- **Recommendation:** {interaction['recommendation']}\n\n"

    if found_interactions["low"]:
        output += "### Low Severity Interactions\n\n"
        for interaction in found_interactions["low"]:
            output += f"**{interaction['drug'].title()}**\n"
            output += f"- **Effect:** {interaction['effect']}\n"
            output += f"- **Recommendation:** {interaction['recommendation']}\n\n"

    output += "---\n\n"
    output += "*This is informational only. Always consult a healthcare provider or pharmacist for personalized advice.*\n"

    return output


@tool
def list_mineral_interactions(
    mineral: Literal[
        "chromium", "zinc", "magnesium", "iron", "selenium", "copper", "iodine"
    ],
) -> str:
    """
    List all known drug interactions for a mineral.

    Args:
        mineral: Trace mineral to list interactions for

    Returns:
        Markdown-formatted list of all interactions
    """
    if mineral not in INTERACTIONS:
        return f"**No interaction data available** for {mineral}."

    mineral_interactions = INTERACTIONS[mineral]

    output = f"## All Known Interactions: {mineral.title()}\n\n"

    total_count = sum(len(v) for v in mineral_interactions.values())
    output += f"**Total interactions:** {total_count}\n\n"

    for severity in ["high", "moderate", "low"]:
        interactions = mineral_interactions.get(severity, [])
        if interactions:
            severity_emoji = {"high": "🔴", "moderate": "🟡", "low": "🟢"}[severity]
            output += f"### {severity_emoji} {severity.title()} Severity ({len(interactions)})\n\n"

            output += "| Drug Class | Examples | Effect |\n"
            output += "|------------|----------|--------|\n"

            for interaction in interactions:
                examples = ", ".join(interaction["drugs"][:3])
                if len(interaction["drugs"]) > 3:
                    examples += "..."
                output += f"| {interaction['drug'].title()} | {examples} | {interaction['effect'][:50]}... |\n"

            output += "\n"

    output += "---\n\n"
    output += "*Consult healthcare provider for complete interaction assessment.*\n"

    return output
