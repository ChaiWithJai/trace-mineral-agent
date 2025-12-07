"""Care plan generator tool for creating structured care plans."""

from typing import Literal

from langchain_core.tools import tool


@tool
def care_plan_generator(
    patient_summary: str,
    primary_goal: str,
    secondary_goals: list[str] | None = None,
    interventions: list[dict] | None = None,
    timeline_weeks: int = 12,
    plan_type: Literal["wellness", "condition_management", "recovery", "lifestyle_transformation"] = "wellness",
    include_supplements: bool = True,
    include_lifestyle: bool = True,
    include_monitoring: bool = True,
) -> str:
    """
    Generate a comprehensive, structured care plan.

    This tool creates detailed care plans with phased implementation,
    specific interventions, monitoring protocols, and adjustment criteria.

    Args:
        patient_summary: Brief summary of patient context and relevant health factors
        primary_goal: The main health goal for this care plan
        secondary_goals: Additional health goals to address
        interventions: List of interventions, each with keys: name, category, priority (1-5), evidence_grade
        timeline_weeks: Total plan duration in weeks (default 12)
        plan_type: Type of care plan to generate
        include_supplements: Whether to include supplement recommendations
        include_lifestyle: Whether to include lifestyle recommendations
        include_monitoring: Whether to include monitoring protocols

    Returns:
        Structured care plan in markdown format
    """
    secondary_goals = secondary_goals or []
    interventions = interventions or []

    sections = []

    # Header
    sections.append(f"# Personalized Care Plan: {primary_goal.title()}")
    sections.append(f"\n**Plan Type:** {plan_type.replace('_', ' ').title()}")
    sections.append(f"**Duration:** {timeline_weeks} weeks")
    sections.append(f"**Generated:** For discussion with healthcare provider\n")

    # Patient Summary
    sections.append("## Patient Context")
    sections.append(patient_summary)
    sections.append("")

    # Goals
    sections.append("## Goals")
    sections.append(f"### Primary Goal\n{primary_goal}")
    if secondary_goals:
        sections.append("\n### Secondary Goals")
        for goal in secondary_goals:
            sections.append(f"- {goal}")
    sections.append("")

    # Generate interventions if not provided
    if not interventions:
        interventions = _generate_default_interventions(
            primary_goal, plan_type, include_supplements, include_lifestyle
        )

    # Sort interventions by priority
    sorted_interventions = sorted(interventions, key=lambda x: x.get("priority", 3))

    # Interventions Overview
    sections.append("## Intervention Summary")
    sections.append("| Intervention | Category | Priority | Evidence |")
    sections.append("|-------------|----------|----------|----------|")
    for intervention in sorted_interventions:
        name = intervention.get("name", "Unnamed")
        category = intervention.get("category", "General")
        priority = intervention.get("priority", 3)
        evidence = intervention.get("evidence_grade", "N/A")
        priority_label = {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Optional"}.get(priority, "Medium")
        sections.append(f"| {name} | {category} | {priority_label} | {evidence} |")
    sections.append("")

    # Phased Implementation
    sections.append("## Phased Implementation")
    phases = _generate_phases(sorted_interventions, timeline_weeks, plan_type)
    for phase_name, phase_data in phases.items():
        sections.append(f"\n### {phase_name}")
        sections.append(f"**Duration:** {phase_data['duration']}")
        sections.append(f"**Focus:** {phase_data['focus']}")
        sections.append("\n**Actions:**")
        for action in phase_data["actions"]:
            sections.append(f"- [ ] {action}")
        if phase_data.get("milestones"):
            sections.append("\n**Milestones:**")
            for milestone in phase_data["milestones"]:
                sections.append(f"- {milestone}")
    sections.append("")

    # Detailed Protocols
    sections.append("## Detailed Protocols")

    if include_supplements:
        supp_interventions = [i for i in sorted_interventions if i.get("category") == "Supplement"]
        if supp_interventions:
            sections.append("\n### Supplementation Protocol")
            sections.append("| Supplement | Dosage | Timing | Duration | Notes |")
            sections.append("|------------|--------|--------|----------|-------|")
            for supp in supp_interventions:
                details = supp.get("details", {})
                sections.append(
                    f"| {supp['name']} | {details.get('dosage', 'Per label')} | "
                    f"{details.get('timing', 'With meals')} | {details.get('duration', 'Ongoing')} | "
                    f"{details.get('notes', '-')} |"
                )
            sections.append("")

    if include_lifestyle:
        lifestyle_interventions = [i for i in sorted_interventions if i.get("category") == "Lifestyle"]
        if lifestyle_interventions:
            sections.append("\n### Lifestyle Protocol")
            for lifestyle in lifestyle_interventions:
                sections.append(f"\n**{lifestyle['name']}**")
                details = lifestyle.get("details", {})
                if details.get("frequency"):
                    sections.append(f"- Frequency: {details['frequency']}")
                if details.get("duration"):
                    sections.append(f"- Duration: {details['duration']}")
                if details.get("specifics"):
                    sections.append(f"- Specifics: {details['specifics']}")
                if details.get("progression"):
                    sections.append(f"- Progression: {details['progression']}")
            sections.append("")

    # Monitoring Protocol
    if include_monitoring:
        sections.append("## Monitoring Protocol")
        monitoring = _generate_monitoring_protocol(primary_goal, plan_type, timeline_weeks)

        sections.append("\n### Subjective Tracking (Daily/Weekly)")
        for item in monitoring["subjective"]:
            sections.append(f"- {item}")

        sections.append("\n### Objective Markers")
        sections.append("| Marker | Frequency | Target | Method |")
        sections.append("|--------|-----------|--------|--------|")
        for marker in monitoring["objective"]:
            sections.append(
                f"| {marker['name']} | {marker['frequency']} | {marker['target']} | {marker['method']} |"
            )

        sections.append("\n### Lab Testing Schedule")
        for timepoint, tests in monitoring["labs"].items():
            sections.append(f"- **{timepoint}:** {', '.join(tests)}")
        sections.append("")

    # Adjustment Criteria
    sections.append("## Adjustment Criteria")
    adjustments = _generate_adjustment_criteria(plan_type)
    sections.append("\n### Positive Response (Continue/Advance)")
    for criterion in adjustments["positive"]:
        sections.append(f"- {criterion}")
    sections.append("\n### Plateau (Modify)")
    for criterion in adjustments["plateau"]:
        sections.append(f"- {criterion}")
    sections.append("\n### Adverse Response (Pause/Consult)")
    for criterion in adjustments["adverse"]:
        sections.append(f"- {criterion}")
    sections.append("")

    # Safety Considerations
    sections.append("## Safety Considerations")
    safety = _generate_safety_section(sorted_interventions)
    sections.append("\n### Contraindications to Review")
    for item in safety["contraindications"]:
        sections.append(f"- {item}")
    sections.append("\n### Potential Interactions")
    for item in safety["interactions"]:
        sections.append(f"- {item}")
    sections.append("\n### Warning Signs")
    for item in safety["warning_signs"]:
        sections.append(f"- {item}")
    sections.append("")

    # Follow-up Schedule
    sections.append("## Follow-up Schedule")
    followups = _generate_followup_schedule(timeline_weeks)
    for followup in followups:
        sections.append(f"- **{followup['timing']}:** {followup['focus']}")
    sections.append("")

    # Disclaimer
    sections.append("---")
    sections.append("## Important Notice")
    sections.append(
        "*This care plan is generated for educational and discussion purposes. "
        "All interventions should be reviewed and approved by a qualified healthcare "
        "provider before implementation. Individual responses vary, and this plan "
        "should be customized based on ongoing assessment and professional guidance.*"
    )

    return "\n".join(sections)


def _generate_default_interventions(
    goal: str, plan_type: str, include_supplements: bool, include_lifestyle: bool
) -> list[dict]:
    """Generate default interventions based on goal and plan type."""
    interventions = []
    goal_lower = goal.lower()

    # Lifestyle interventions
    if include_lifestyle:
        interventions.extend([
            {
                "name": "Sleep Optimization",
                "category": "Lifestyle",
                "priority": 2,
                "evidence_grade": "A",
                "details": {
                    "frequency": "Daily",
                    "duration": "7-9 hours",
                    "specifics": "Consistent sleep/wake times, dark room, cool temperature",
                    "progression": "Track sleep quality weekly",
                },
            },
            {
                "name": "Movement Protocol",
                "category": "Lifestyle",
                "priority": 2,
                "evidence_grade": "A",
                "details": {
                    "frequency": "5x weekly",
                    "duration": "30-60 minutes",
                    "specifics": "Mix of resistance and cardiovascular training",
                    "progression": "Increase intensity every 2 weeks",
                },
            },
            {
                "name": "Stress Management",
                "category": "Lifestyle",
                "priority": 3,
                "evidence_grade": "B",
                "details": {
                    "frequency": "Daily",
                    "duration": "10-20 minutes",
                    "specifics": "Breathwork, meditation, or mindfulness practice",
                    "progression": "Extend duration as tolerance builds",
                },
            },
        ])

    # Goal-specific supplements
    if include_supplements:
        if "metabolic" in goal_lower or "weight" in goal_lower or "glucose" in goal_lower:
            interventions.extend([
                {
                    "name": "Magnesium Glycinate",
                    "category": "Supplement",
                    "priority": 2,
                    "evidence_grade": "A",
                    "details": {
                        "dosage": "300-400mg elemental",
                        "timing": "Evening",
                        "duration": "Ongoing",
                        "notes": "Supports glucose metabolism and sleep",
                    },
                },
                {
                    "name": "Chromium",
                    "category": "Supplement",
                    "priority": 3,
                    "evidence_grade": "B",
                    "details": {
                        "dosage": "200-500mcg",
                        "timing": "With meals",
                        "duration": "12 weeks minimum",
                        "notes": "May support insulin sensitivity",
                    },
                },
            ])
        elif "energy" in goal_lower or "fatigue" in goal_lower:
            interventions.extend([
                {
                    "name": "B-Complex",
                    "category": "Supplement",
                    "priority": 2,
                    "evidence_grade": "B",
                    "details": {
                        "dosage": "Active forms",
                        "timing": "Morning with food",
                        "duration": "Ongoing",
                        "notes": "Supports energy metabolism",
                    },
                },
                {
                    "name": "CoQ10",
                    "category": "Supplement",
                    "priority": 3,
                    "evidence_grade": "B",
                    "details": {
                        "dosage": "100-200mg",
                        "timing": "With fat-containing meal",
                        "duration": "8 weeks minimum",
                        "notes": "Mitochondrial support",
                    },
                },
            ])
        elif "cognitive" in goal_lower or "brain" in goal_lower:
            interventions.extend([
                {
                    "name": "Omega-3 (EPA/DHA)",
                    "category": "Supplement",
                    "priority": 2,
                    "evidence_grade": "A",
                    "details": {
                        "dosage": "2-3g combined EPA/DHA",
                        "timing": "With meals",
                        "duration": "Ongoing",
                        "notes": "Brain structure and anti-inflammatory",
                    },
                },
                {
                    "name": "Lion's Mane",
                    "category": "Supplement",
                    "priority": 3,
                    "evidence_grade": "B",
                    "details": {
                        "dosage": "500-1000mg",
                        "timing": "Morning",
                        "duration": "12 weeks minimum",
                        "notes": "NGF support, neuroplasticity",
                    },
                },
            ])
        else:
            # General wellness supplements
            interventions.extend([
                {
                    "name": "Vitamin D3",
                    "category": "Supplement",
                    "priority": 2,
                    "evidence_grade": "A",
                    "details": {
                        "dosage": "2000-5000 IU (based on levels)",
                        "timing": "With fat-containing meal",
                        "duration": "Ongoing with monitoring",
                        "notes": "Check levels at baseline and 3 months",
                    },
                },
                {
                    "name": "Magnesium",
                    "category": "Supplement",
                    "priority": 2,
                    "evidence_grade": "A",
                    "details": {
                        "dosage": "300-400mg elemental",
                        "timing": "Evening",
                        "duration": "Ongoing",
                        "notes": "Most common deficiency",
                    },
                },
            ])

    return interventions


def _generate_phases(interventions: list[dict], timeline_weeks: int, plan_type: str) -> dict:
    """Generate phased implementation plan."""
    # Divide timeline into phases
    if timeline_weeks <= 4:
        phase_weeks = [(1, timeline_weeks)]
    elif timeline_weeks <= 8:
        phase_weeks = [(1, 2), (3, timeline_weeks)]
    else:
        phase_weeks = [(1, 2), (3, 6), (7, timeline_weeks)]

    phases = {}

    # Phase 1: Foundation
    high_priority = [i for i in interventions if i.get("priority", 3) <= 2]
    phases["Phase 1: Foundation"] = {
        "duration": f"Weeks {phase_weeks[0][0]}-{phase_weeks[0][1]}",
        "focus": "Establish core habits and high-priority interventions",
        "actions": [
            "Complete baseline assessment and any required lab work",
            *[f"Start {i['name']} ({i['category']})" for i in high_priority[:4]],
            "Begin daily tracking of key metrics",
            "Schedule first follow-up check-in",
        ],
        "milestones": [
            "All foundation interventions started",
            "Baseline data collected",
            "Initial tolerance assessed",
        ],
    }

    if len(phase_weeks) > 1:
        # Phase 2: Building
        medium_priority = [i for i in interventions if i.get("priority", 3) == 3]
        phases["Phase 2: Building"] = {
            "duration": f"Weeks {phase_weeks[1][0]}-{phase_weeks[1][1]}",
            "focus": "Add supporting interventions and optimize dosing",
            "actions": [
                "Review response to Phase 1 interventions",
                *[f"Add {i['name']} ({i['category']})" for i in medium_priority[:3]],
                "Adjust dosing based on response",
                "Increase exercise intensity if tolerated",
                "Mid-point assessment",
            ],
            "milestones": [
                "Positive response to foundation protocol",
                "All Phase 2 interventions integrated",
                "Measurable progress on primary goal",
            ],
        }

    if len(phase_weeks) > 2:
        # Phase 3: Optimization
        low_priority = [i for i in interventions if i.get("priority", 3) >= 4]
        phases["Phase 3: Optimization"] = {
            "duration": f"Weeks {phase_weeks[2][0]}-{phase_weeks[2][1]}",
            "focus": "Fine-tune protocol and transition to maintenance",
            "actions": [
                "Comprehensive progress review",
                *[f"Consider adding {i['name']} if appropriate" for i in low_priority[:2]],
                "Optimize timing and combinations",
                "Develop maintenance protocol",
                "Final assessment and planning",
            ],
            "milestones": [
                "Primary goal progress achieved",
                "Sustainable protocol established",
                "Maintenance plan defined",
            ],
        }

    return phases


def _generate_monitoring_protocol(goal: str, plan_type: str, timeline_weeks: int) -> dict:
    """Generate monitoring protocol based on goal and plan type."""
    goal_lower = goal.lower()

    # Subjective tracking
    subjective = [
        "Energy levels (1-10 scale)",
        "Sleep quality (1-10 scale)",
        "Mood/stress (1-10 scale)",
        "Digestive comfort",
        "Any adverse effects or concerns",
    ]

    # Objective markers
    objective = [
        {"name": "Body weight", "frequency": "Weekly", "target": "Per goal", "method": "Morning, fasted"},
        {"name": "Blood pressure", "frequency": "Weekly", "target": "<120/80", "method": "Seated, rested"},
        {"name": "Resting heart rate", "frequency": "Daily", "target": "Trending down", "method": "Morning, before rising"},
    ]

    # Goal-specific markers
    if "metabolic" in goal_lower or "glucose" in goal_lower:
        objective.extend([
            {"name": "Fasting glucose", "frequency": "Weekly", "target": "<90 mg/dL", "method": "CGM or fingerstick"},
            {"name": "Waist circumference", "frequency": "Bi-weekly", "target": "Decreasing", "method": "Navel level"},
        ])
    elif "cognitive" in goal_lower:
        subjective.extend([
            "Focus/concentration (1-10)",
            "Memory recall subjective",
        ])
    elif "energy" in goal_lower:
        subjective.extend([
            "Afternoon energy (1-10)",
            "Post-meal energy (1-10)",
        ])

    # Lab schedule
    labs = {
        "Baseline (Week 0)": ["Comprehensive metabolic panel", "Lipid panel", "CBC", "Vitamin D", "HbA1c"],
        f"Mid-point (Week {timeline_weeks // 2})": ["Focused panel based on goals"],
        f"End of Protocol (Week {timeline_weeks})": ["Comprehensive metabolic panel", "Lipid panel", "Vitamin D", "HbA1c", "Compare to baseline"],
    }

    return {"subjective": subjective, "objective": objective, "labs": labs}


def _generate_adjustment_criteria(plan_type: str) -> dict:
    """Generate criteria for when to adjust the protocol."""
    return {
        "positive": [
            "Subjective improvement in energy, mood, or target symptoms",
            "Objective markers moving toward targets",
            "Good tolerance of all interventions",
            "No adverse effects",
            "→ Continue protocol, consider advancing to next phase",
        ],
        "plateau": [
            "Initial improvement followed by stagnation (>2 weeks)",
            "Partial response to interventions",
            "Variable day-to-day response",
            "→ Review compliance, consider dose adjustment, add supporting interventions",
        ],
        "adverse": [
            "New symptoms that may be related to interventions",
            "Worsening of existing symptoms",
            "Lab markers moving away from targets",
            "Significant digestive distress",
            "→ Pause new additions, consult healthcare provider, reassess approach",
        ],
    }


def _generate_safety_section(interventions: list[dict]) -> dict:
    """Generate safety considerations based on interventions."""
    contraindications = [
        "Review all interventions against current medications",
        "Confirm no allergies to supplement ingredients",
        "Check for condition-specific contraindications",
        "Verify appropriate for current life stage (pregnancy, etc.)",
    ]

    interactions = [
        "Some supplements may affect medication absorption (take separately)",
        "High-dose magnesium may interact with certain antibiotics",
        "Vitamin D requires adequate magnesium for metabolism",
        "Some herbs may affect cytochrome P450 drug metabolism",
    ]

    warning_signs = [
        "Allergic reactions (rash, swelling, difficulty breathing) → Stop all, seek medical attention",
        "Severe digestive upset → Reduce dose or discontinue suspected agent",
        "Unusual fatigue or weakness → Check labs, consult provider",
        "Changes in heart rhythm or palpitations → Consult provider",
        "Any symptom that feels concerning → Trust your body, consult provider",
    ]

    return {
        "contraindications": contraindications,
        "interactions": interactions,
        "warning_signs": warning_signs,
    }


def _generate_followup_schedule(timeline_weeks: int) -> list[dict]:
    """Generate follow-up schedule."""
    followups = [
        {"timing": "Week 1", "focus": "Tolerance check, address any early concerns"},
        {"timing": "Week 2", "focus": "Initial response assessment, adjust if needed"},
    ]

    if timeline_weeks >= 4:
        followups.append({"timing": "Week 4", "focus": "First milestone review, Phase 1 assessment"})

    if timeline_weeks >= 8:
        followups.append({"timing": "Week 8", "focus": "Mid-protocol review, Phase 2 assessment, consider adjustments"})

    if timeline_weeks >= 12:
        followups.append({"timing": "Week 12", "focus": "Comprehensive review, outcome assessment, maintenance planning"})

    if timeline_weeks > 12:
        followups.append({"timing": f"Week {timeline_weeks}", "focus": "Final assessment, long-term maintenance protocol"})

    return followups
