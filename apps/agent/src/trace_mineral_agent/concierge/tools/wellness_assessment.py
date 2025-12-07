"""Wellness assessment tool for concierge health evaluations."""

from typing import Literal

from langchain_core.tools import tool


@tool
def wellness_assessment(
    age: int,
    biological_sex: Literal["male", "female"],
    health_goals: list[str],
    current_conditions: list[str] | None = None,
    current_medications: list[str] | None = None,
    current_supplements: list[str] | None = None,
    lifestyle_factors: dict | None = None,
    recent_labs: dict | None = None,
) -> str:
    """
    Generate a comprehensive wellness assessment for a patient.

    This tool analyzes patient health data and generates a structured
    wellness assessment identifying priority areas, risk factors, and
    optimization opportunities.

    Args:
        age: Patient's age in years
        biological_sex: Patient's biological sex for metabolic considerations
        health_goals: List of patient's health goals (e.g., ["weight loss", "energy", "longevity"])
        current_conditions: List of current health conditions (e.g., ["type 2 diabetes", "hypertension"])
        current_medications: List of current medications
        current_supplements: List of current supplements
        lifestyle_factors: Dict with keys like "exercise", "sleep_hours", "stress_level", "diet_type"
        recent_labs: Dict with recent lab values (e.g., {"glucose": 95, "HbA1c": 5.4})

    Returns:
        Structured wellness assessment in markdown format
    """
    current_conditions = current_conditions or []
    current_medications = current_medications or []
    current_supplements = current_supplements or []
    lifestyle_factors = lifestyle_factors or {}
    recent_labs = recent_labs or {}

    # Build assessment sections
    sections = []

    # Header
    sections.append("## Wellness Assessment Report\n")

    # Patient Profile
    sections.append("### Patient Profile")
    sections.append(f"- **Age:** {age} years")
    sections.append(f"- **Biological Sex:** {biological_sex.capitalize()}")
    sections.append(f"- **Health Goals:** {', '.join(health_goals)}")
    sections.append("")

    # Life Stage Assessment
    life_stage = _assess_life_stage(age, biological_sex)
    sections.append("### Life Stage Considerations")
    sections.append(f"- **Stage:** {life_stage['stage']}")
    sections.append(f"- **Key Focus Areas:** {', '.join(life_stage['focus_areas'])}")
    sections.append(f"- **Metabolic Considerations:** {life_stage['metabolic_notes']}")
    sections.append("")

    # Health Status
    sections.append("### Current Health Status")
    if current_conditions:
        sections.append("**Active Conditions:**")
        for condition in current_conditions:
            sections.append(f"- {condition}")
    else:
        sections.append("**Active Conditions:** None reported")
    sections.append("")

    # Medications & Supplements
    sections.append("### Current Interventions")
    if current_medications:
        sections.append("**Medications:**")
        for med in current_medications:
            sections.append(f"- {med}")
    else:
        sections.append("**Medications:** None reported")

    if current_supplements:
        sections.append("\n**Supplements:**")
        for supp in current_supplements:
            sections.append(f"- {supp}")
    else:
        sections.append("\n**Supplements:** None reported")
    sections.append("")

    # Lifestyle Assessment
    sections.append("### Lifestyle Factors")
    lifestyle_score, lifestyle_analysis = _assess_lifestyle(lifestyle_factors)
    sections.append(f"**Overall Lifestyle Score:** {lifestyle_score}/100")
    for area, assessment in lifestyle_analysis.items():
        sections.append(f"- **{area}:** {assessment}")
    sections.append("")

    # Lab Analysis (if provided)
    if recent_labs:
        sections.append("### Laboratory Analysis")
        lab_analysis = _analyze_labs(recent_labs, age, biological_sex)
        for marker, analysis in lab_analysis.items():
            sections.append(f"- **{marker}:** {analysis}")
        sections.append("")

    # Risk Assessment
    risk_factors = _assess_risk_factors(age, biological_sex, current_conditions, lifestyle_factors, recent_labs)
    sections.append("### Risk Assessment")
    if risk_factors["high"]:
        sections.append("**High Priority:**")
        for risk in risk_factors["high"]:
            sections.append(f"- {risk}")
    if risk_factors["moderate"]:
        sections.append("\n**Moderate Priority:**")
        for risk in risk_factors["moderate"]:
            sections.append(f"- {risk}")
    if risk_factors["low"]:
        sections.append("\n**Preventive Focus:**")
        for risk in risk_factors["low"]:
            sections.append(f"- {risk}")
    sections.append("")

    # Goal Alignment
    sections.append("### Goal-Aligned Recommendations")
    for goal in health_goals:
        recommendations = _get_goal_recommendations(goal, current_conditions, lifestyle_factors)
        sections.append(f"\n**{goal.title()}:**")
        for rec in recommendations:
            sections.append(f"- {rec}")
    sections.append("")

    # Priority Actions
    sections.append("### Priority Actions")
    priorities = _determine_priorities(health_goals, risk_factors, lifestyle_score)
    for i, priority in enumerate(priorities, 1):
        sections.append(f"{i}. {priority}")
    sections.append("")

    # Disclaimer
    sections.append("---")
    sections.append("*This assessment is for informational purposes only and should be reviewed with a qualified healthcare provider.*")

    return "\n".join(sections)


def _assess_life_stage(age: int, sex: str) -> dict:
    """Assess life stage and related considerations."""
    if age < 30:
        return {
            "stage": "Young Adult",
            "focus_areas": ["Foundation building", "Prevention", "Performance optimization"],
            "metabolic_notes": "Peak metabolic capacity, ideal time for establishing healthy patterns",
        }
    elif age < 45:
        return {
            "stage": "Prime Adult",
            "focus_areas": ["Metabolic maintenance", "Stress management", "Early prevention"],
            "metabolic_notes": "Beginning metabolic shift, focus on maintaining insulin sensitivity",
        }
    elif age < 60:
        if sex == "female":
            return {
                "stage": "Midlife (Perimenopause/Menopause consideration)",
                "focus_areas": ["Hormonal transition support", "Bone health", "Cardiovascular protection"],
                "metabolic_notes": "Significant hormonal changes affecting metabolism, increased cardiovascular attention needed",
            }
        else:
            return {
                "stage": "Midlife",
                "focus_areas": ["Cardiovascular health", "Metabolic optimization", "Hormonal assessment"],
                "metabolic_notes": "Gradual testosterone decline, metabolic slowing, increased cardiovascular focus",
            }
    else:
        return {
            "stage": "Mature Adult",
            "focus_areas": ["Healthy aging", "Cognitive preservation", "Functional maintenance"],
            "metabolic_notes": "Focus on maintaining muscle mass, bone density, and cognitive function",
        }


def _assess_lifestyle(factors: dict) -> tuple[int, dict]:
    """Score lifestyle factors and provide analysis."""
    score = 50  # Base score
    analysis = {}

    # Exercise
    exercise = factors.get("exercise", "unknown")
    if exercise == "daily" or exercise == "5+ times/week":
        score += 15
        analysis["Exercise"] = "Excellent - regular activity supports metabolic health"
    elif exercise == "3-4 times/week":
        score += 10
        analysis["Exercise"] = "Good - consistent activity pattern"
    elif exercise == "1-2 times/week":
        score += 5
        analysis["Exercise"] = "Fair - room for improvement"
    elif exercise == "sedentary" or exercise == "none":
        score -= 10
        analysis["Exercise"] = "Priority area - sedentary lifestyle increases health risks"
    else:
        analysis["Exercise"] = "Not assessed - provide exercise frequency for evaluation"

    # Sleep
    sleep_hours = factors.get("sleep_hours")
    if sleep_hours:
        if 7 <= sleep_hours <= 9:
            score += 15
            analysis["Sleep"] = f"Optimal - {sleep_hours} hours supports recovery and metabolism"
        elif 6 <= sleep_hours < 7:
            score += 5
            analysis["Sleep"] = f"Suboptimal - {sleep_hours} hours may impact recovery"
        else:
            score -= 5
            analysis["Sleep"] = f"Concerning - {sleep_hours} hours significantly impacts health"
    else:
        analysis["Sleep"] = "Not assessed - provide sleep duration for evaluation"

    # Stress
    stress = factors.get("stress_level", "unknown")
    if stress == "low":
        score += 10
        analysis["Stress"] = "Well-managed - low stress supports overall health"
    elif stress == "moderate":
        score += 5
        analysis["Stress"] = "Moderate - consider stress management strategies"
    elif stress == "high":
        score -= 10
        analysis["Stress"] = "Priority area - high stress impacts metabolism and immune function"
    else:
        analysis["Stress"] = "Not assessed - provide stress level for evaluation"

    # Diet
    diet = factors.get("diet_type", "unknown")
    if diet in ["whole foods", "mediterranean", "nutrient-dense"]:
        score += 10
        analysis["Nutrition"] = f"Supportive - {diet} diet provides good foundation"
    elif diet in ["standard", "mixed"]:
        analysis["Nutrition"] = "Average - room for optimization"
    elif diet in ["processed", "fast food", "SAD"]:
        score -= 10
        analysis["Nutrition"] = "Priority area - diet quality impacts all health markers"
    else:
        analysis["Nutrition"] = "Not assessed - provide dietary pattern for evaluation"

    return max(0, min(100, score)), analysis


def _analyze_labs(labs: dict, age: int, sex: str) -> dict:
    """Analyze lab values against optimal ranges."""
    analysis = {}

    # Reference ranges (simplified - would be more comprehensive in production)
    ranges = {
        "glucose": {"optimal": (70, 90), "normal": (70, 100), "unit": "mg/dL"},
        "HbA1c": {"optimal": (4.5, 5.2), "normal": (4.0, 5.7), "unit": "%"},
        "fasting_insulin": {"optimal": (2, 6), "normal": (2, 25), "unit": "uIU/mL"},
        "vitamin_d": {"optimal": (50, 80), "normal": (30, 100), "unit": "ng/mL"},
        "TSH": {"optimal": (1.0, 2.5), "normal": (0.5, 4.5), "unit": "mIU/L"},
        "ferritin": {
            "optimal": (50, 150) if sex == "male" else (30, 100),
            "normal": (30, 300) if sex == "male" else (15, 150),
            "unit": "ng/mL",
        },
        "hs_CRP": {"optimal": (0, 1.0), "normal": (0, 3.0), "unit": "mg/L"},
    }

    for marker, value in labs.items():
        marker_lower = marker.lower().replace(" ", "_").replace("-", "_")
        if marker_lower in ranges:
            ref = ranges[marker_lower]
            opt_low, opt_high = ref["optimal"]
            norm_low, norm_high = ref["normal"]
            unit = ref["unit"]

            if opt_low <= value <= opt_high:
                analysis[marker] = f"{value} {unit} - Optimal range"
            elif norm_low <= value <= norm_high:
                if value < opt_low:
                    analysis[marker] = f"{value} {unit} - Normal but below optimal"
                else:
                    analysis[marker] = f"{value} {unit} - Normal but above optimal"
            else:
                if value < norm_low:
                    analysis[marker] = f"{value} {unit} - Below normal range (investigate)"
                else:
                    analysis[marker] = f"{value} {unit} - Above normal range (investigate)"
        else:
            analysis[marker] = f"{value} - Value recorded (reference range not configured)"

    return analysis


def _assess_risk_factors(
    age: int, sex: str, conditions: list[str], lifestyle: dict, labs: dict
) -> dict[str, list[str]]:
    """Assess risk factors based on all available data."""
    risks: dict[str, list[str]] = {"high": [], "moderate": [], "low": []}

    # Age-related risks
    if age > 45:
        risks["moderate"].append("Age-related metabolic changes - monitor markers regularly")
    if age > 60:
        risks["moderate"].append("Age-related cognitive and bone health monitoring recommended")

    # Condition-based risks
    condition_risks = {
        "type 2 diabetes": ("high", "Metabolic disease - comprehensive management required"),
        "prediabetes": ("moderate", "Prediabetes - lifestyle intervention priority"),
        "hypertension": ("moderate", "Cardiovascular risk - blood pressure management needed"),
        "obesity": ("moderate", "Metabolic and cardiovascular risk - weight management priority"),
        "thyroid disorder": ("moderate", "Thyroid function - regular monitoring required"),
        "autoimmune": ("moderate", "Autoimmune condition - inflammation management important"),
    }

    for condition in conditions:
        condition_lower = condition.lower()
        for key, (level, message) in condition_risks.items():
            if key in condition_lower:
                risks[level].append(message)

    # Lifestyle-based risks
    if lifestyle.get("exercise") in ["sedentary", "none"]:
        risks["moderate"].append("Sedentary lifestyle - increases all-cause mortality risk")
    if lifestyle.get("stress_level") == "high":
        risks["moderate"].append("Chronic stress - impacts cortisol, immunity, and metabolism")
    if lifestyle.get("sleep_hours") and lifestyle["sleep_hours"] < 6:
        risks["moderate"].append("Sleep deprivation - affects hormones and cognitive function")

    # Lab-based risks
    if labs.get("glucose", 0) > 100:
        risks["moderate"].append("Elevated fasting glucose - metabolic attention needed")
    if labs.get("HbA1c", 0) > 5.7:
        risks["high" if labs["HbA1c"] > 6.4 else "moderate"].append("Elevated HbA1c - glycemic management priority")
    if labs.get("hs_CRP", 0) > 3:
        risks["moderate"].append("Elevated inflammation markers - investigate underlying cause")

    # Prevention focus for low-risk individuals
    if not risks["high"] and not risks["moderate"]:
        risks["low"].append("General preventive care - maintain healthy patterns")
        risks["low"].append("Age-appropriate screening - follow guidelines")

    return risks


def _get_goal_recommendations(goal: str, conditions: list[str], lifestyle: dict) -> list[str]:
    """Get recommendations aligned with specific health goals."""
    goal_lower = goal.lower()

    recommendations = {
        "weight loss": [
            "Metabolic assessment to identify barriers",
            "Nutrition optimization focusing on protein and fiber",
            "Resistance training for metabolic rate support",
            "Sleep and stress optimization (cortisol management)",
            "Consider metabolic support supplements (based on labs)",
        ],
        "energy": [
            "Mitochondrial support assessment",
            "Thyroid and adrenal function evaluation",
            "Sleep quality optimization",
            "Blood sugar stabilization strategies",
            "Micronutrient status check (B vitamins, iron, magnesium)",
        ],
        "longevity": [
            "Comprehensive metabolic panel",
            "Inflammation and oxidative stress markers",
            "Hormonal optimization assessment",
            "Autophagy-supporting interventions",
            "Cardiovascular health optimization",
        ],
        "cognitive": [
            "Brain health markers assessment",
            "Inflammation and vascular health evaluation",
            "Sleep optimization for cognitive recovery",
            "Omega-3 and antioxidant status",
            "Stress management for cortisol control",
        ],
        "gut health": [
            "Comprehensive digestive assessment",
            "Elimination diet consideration",
            "Prebiotic and probiotic strategies",
            "Gut barrier support protocols",
            "Stress-gut axis management",
        ],
        "hormone": [
            "Comprehensive hormone panel",
            "HPA axis assessment",
            "Lifestyle factors affecting hormones",
            "Targeted nutritional support",
            "Toxin exposure minimization",
        ],
    }

    # Find matching recommendations
    for key, recs in recommendations.items():
        if key in goal_lower:
            return recs

    # Default recommendations
    return [
        "Baseline health assessment",
        "Personalized nutrition evaluation",
        "Lifestyle optimization review",
        "Targeted supplementation assessment",
    ]


def _determine_priorities(goals: list[str], risks: dict[str, list[str]], lifestyle_score: int) -> list[str]:
    """Determine priority actions based on all assessments."""
    priorities = []

    # High risks first
    if risks["high"]:
        priorities.append("Address high-priority health concerns with healthcare provider")

    # Lifestyle if poor
    if lifestyle_score < 50:
        priorities.append("Implement foundational lifestyle improvements (sleep, movement, stress)")

    # Goal-aligned priorities
    if len(goals) > 0:
        priorities.append(f"Develop targeted protocol for primary goal: {goals[0]}")

    # Moderate risks
    if risks["moderate"]:
        priorities.append("Monitor and address moderate risk factors with preventive strategies")

    # Optimization
    if lifestyle_score >= 70:
        priorities.append("Optimize existing healthy patterns with targeted interventions")

    # Regular monitoring
    priorities.append("Establish regular monitoring schedule for progress tracking")

    return priorities[:5]  # Return top 5 priorities
