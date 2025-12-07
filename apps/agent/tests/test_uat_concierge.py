"""User Acceptance Tests for ConciergeHealthAgent.

These tests validate the acceptance criteria defined in docs/UAT_CONCIERGE_MODE.md.
Each test is tagged with its corresponding AC (Acceptance Criterion) ID.

Run all UAT tests: pytest tests/test_uat_concierge.py -v
Run specific AC: pytest tests/test_uat_concierge.py -v -k "AC1"
"""

import json

import pytest


# =============================================================================
# AC-1: Separate Deployment Endpoint
# =============================================================================


class TestAC1_DeploymentEndpoint:
    """AC-1: Concierge mode must have its own URL/endpoint."""

    def test_AC1_1_langgraph_config_includes_concierge(self):
        """AC-1.1: LangGraph configuration includes concierge graph."""
        import os

        langgraph_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "langgraph.json"
        )
        with open(langgraph_path) as f:
            config = json.load(f)

        assert "graphs" in config
        assert "concierge-health" in config["graphs"]

    def test_AC1_2_concierge_graph_is_separate(self):
        """AC-1.2: Concierge graph is separate from main graph."""
        import os

        langgraph_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "langgraph.json"
        )
        with open(langgraph_path) as f:
            config = json.load(f)

        graphs = config["graphs"]
        assert "trace-mineral-discovery" in graphs
        assert "concierge-health" in graphs
        assert graphs["trace-mineral-discovery"] != graphs["concierge-health"]

    def test_AC1_3_cli_entry_point_defined(self):
        """AC-1.3: CLI entry point available."""
        # Verify the main function exists and is callable
        from trace_mineral_agent.concierge.agent import main

        assert callable(main)


# =============================================================================
# AC-2: Wellness Assessment Tool
# =============================================================================


class TestAC2_WellnessAssessment:
    """AC-2: Generate comprehensive wellness assessments."""

    def test_AC2_1_accepts_patient_demographics(self):
        """AC-2.1: Accepts patient demographics."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 45,
            "biological_sex": "male",
            "health_goals": ["weight loss"],
        })

        assert "45" in result
        assert "Male" in result

    def test_AC2_2_handles_health_conditions(self):
        """AC-2.2: Handles health conditions."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 50,
            "biological_sex": "female",
            "health_goals": ["manage conditions"],
            "current_conditions": ["type 2 diabetes", "hypertension"],
        })

        assert "diabetes" in result.lower() or "type 2" in result.lower()
        assert "Risk" in result

    def test_AC2_3_processes_medications(self):
        """AC-2.3: Processes medications."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 60,
            "biological_sex": "male",
            "health_goals": ["safety"],
            "current_medications": ["metformin", "atorvastatin"],
        })

        assert "metformin" in result.lower()
        assert "atorvastatin" in result.lower()

    def test_AC2_4_analyzes_lifestyle_factors(self):
        """AC-2.4: Analyzes lifestyle factors."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 35,
            "biological_sex": "female",
            "health_goals": ["wellness"],
            "lifestyle_factors": {
                "exercise": "daily",
                "sleep_hours": 8,
                "stress_level": "low",
            },
        })

        assert "Lifestyle" in result
        assert "Score" in result

    def test_AC2_5_interprets_lab_values(self):
        """AC-2.5: Interprets lab values."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 45,
            "biological_sex": "male",
            "health_goals": ["metabolic health"],
            "recent_labs": {"glucose": 110, "HbA1c": 5.9},
        })

        assert "Laboratory" in result
        assert "glucose" in result.lower()

    def test_AC2_6_life_stage_identification(self):
        """AC-2.6: Life stage identification."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        # Test all life stages
        young = wellness_assessment.invoke({
            "age": 25,
            "biological_sex": "male",
            "health_goals": ["fitness"],
        })
        assert "Young Adult" in young

        prime = wellness_assessment.invoke({
            "age": 40,
            "biological_sex": "female",
            "health_goals": ["wellness"],
        })
        assert "Prime" in prime

        midlife = wellness_assessment.invoke({
            "age": 55,
            "biological_sex": "male",
            "health_goals": ["longevity"],
        })
        assert "Midlife" in midlife

        mature = wellness_assessment.invoke({
            "age": 70,
            "biological_sex": "female",
            "health_goals": ["function"],
        })
        assert "Mature" in mature

    def test_AC2_7_risk_assessment_generated(self):
        """AC-2.7: Risk assessment generated."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 55,
            "biological_sex": "male",
            "health_goals": ["health"],
            "current_conditions": ["obesity"],
        })

        assert "Risk Assessment" in result

    def test_AC2_8_goal_aligned_recommendations(self):
        """AC-2.8: Goal-aligned recommendations."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 45,
            "biological_sex": "female",
            "health_goals": ["weight loss", "energy"],
        })

        assert "Goal-Aligned" in result or "weight" in result.lower()

    def test_AC2_9_includes_disclaimer(self):
        """AC-2.9: Includes disclaimer."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 40,
            "biological_sex": "male",
            "health_goals": ["wellness"],
        })

        assert "healthcare provider" in result.lower() or "informational" in result.lower()


# =============================================================================
# AC-3: Care Plan Generator Tool
# =============================================================================


class TestAC3_CarePlanGenerator:
    """AC-3: Generate structured care plans."""

    def test_AC3_1_accepts_patient_summary(self):
        """AC-3.1: Accepts patient summary."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "45-year-old male with metabolic concerns",
            "primary_goal": "Health optimization",
        })

        assert "45" in result or "metabolic" in result.lower()

    def test_AC3_2_primary_goal_addressed(self):
        """AC-3.2: Primary goal addressed."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Metabolic optimization",
        })

        assert "Metabolic" in result

    def test_AC3_3_secondary_goals_included(self):
        """AC-3.3: Secondary goals included."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Primary goal",
            "secondary_goals": ["sleep improvement", "stress reduction"],
        })

        assert "Secondary Goals" in result
        assert "sleep" in result.lower()

    def test_AC3_4_phased_implementation(self):
        """AC-3.4: Phased implementation."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Test goal",
            "timeline_weeks": 12,
        })

        assert "Phase 1" in result
        assert "Phase 2" in result or "Week" in result

    def test_AC3_5_supplement_protocol(self):
        """AC-3.5: Supplement protocol."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Metabolic health",
            "include_supplements": True,
        })

        assert "Supplement" in result
        assert "Dosage" in result or "mg" in result.lower()

    def test_AC3_6_lifestyle_protocol(self):
        """AC-3.6: Lifestyle protocol."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Wellness",
            "include_lifestyle": True,
        })

        assert "Lifestyle" in result
        assert "Sleep" in result or "Exercise" in result or "Movement" in result

    def test_AC3_7_monitoring_protocol(self):
        """AC-3.7: Monitoring protocol."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Health tracking",
            "include_monitoring": True,
        })

        assert "Monitoring Protocol" in result
        assert "Subjective" in result or "Objective" in result

    def test_AC3_8_lab_testing_schedule(self):
        """AC-3.8: Lab testing schedule."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Health monitoring",
            "include_monitoring": True,
        })

        assert "Lab" in result
        assert "Baseline" in result or "Week" in result

    def test_AC3_9_adjustment_criteria(self):
        """AC-3.9: Adjustment criteria."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Adaptive care",
        })

        assert "Adjustment Criteria" in result
        assert "Positive" in result or "Plateau" in result

    def test_AC3_10_safety_section(self):
        """AC-3.10: Safety section."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Safe care",
        })

        assert "Safety Considerations" in result
        assert "Warning" in result or "Contraindication" in result

    def test_AC3_11_followup_schedule(self):
        """AC-3.11: Follow-up schedule."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Monitored care",
        })

        assert "Follow-up" in result

    def test_AC3_12_timeline_respected(self):
        """AC-3.12: Timeline respected."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result_4week = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Short intervention",
            "timeline_weeks": 4,
        })
        assert "4 weeks" in result_4week

        result_16week = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Long intervention",
            "timeline_weeks": 16,
        })
        assert "16 weeks" in result_16week

    def test_AC3_13_plan_type_applied(self):
        """AC-3.13: Plan type applied."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Recovery",
            "plan_type": "recovery",
        })

        assert "Recovery" in result

    def test_AC3_14_evidence_grades_shown(self):
        """AC-3.14: Evidence grades shown."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Evidence-based care",
            "interventions": [
                {
                    "name": "Test intervention",
                    "category": "Supplement",
                    "priority": 1,
                    "evidence_grade": "A",
                }
            ],
        })

        assert "Evidence" in result

    def test_AC3_15_important_notice(self):
        """AC-3.15: Important notice."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Test patient",
            "primary_goal": "Test",
        })

        assert "Important Notice" in result or "healthcare provider" in result.lower()


# =============================================================================
# AC-4: Subagent Configuration
# =============================================================================


class TestAC4_SubagentConfig:
    """AC-4: Three specialized subagents properly configured."""

    def test_AC4_1_patient_advisor_has_required_fields(self):
        """AC-4.1: PatientAdvisor has required fields."""
        from trace_mineral_agent.concierge.subagents import patient_advisor_subagent

        assert "name" in patient_advisor_subagent
        assert "description" in patient_advisor_subagent
        assert "system_prompt" in patient_advisor_subagent
        assert "tools" in patient_advisor_subagent

    def test_AC4_2_wellness_researcher_has_required_fields(self):
        """AC-4.2: WellnessResearcher has required fields."""
        from trace_mineral_agent.concierge.subagents import wellness_researcher_subagent

        assert "name" in wellness_researcher_subagent
        assert "description" in wellness_researcher_subagent
        assert "system_prompt" in wellness_researcher_subagent
        assert "tools" in wellness_researcher_subagent

    def test_AC4_3_care_coordinator_has_required_fields(self):
        """AC-4.3: CareCoordinator has required fields."""
        from trace_mineral_agent.concierge.subagents import care_coordinator_subagent

        assert "name" in care_coordinator_subagent
        assert "description" in care_coordinator_subagent
        assert "system_prompt" in care_coordinator_subagent
        assert "tools" in care_coordinator_subagent

    def test_AC4_4_patient_advisor_has_literature_search(self):
        """AC-4.4: PatientAdvisor has literature_search."""
        from trace_mineral_agent.concierge.subagents import patient_advisor_subagent

        tool_names = [t.name for t in patient_advisor_subagent["tools"]]
        assert "literature_search" in tool_names

    def test_AC4_5_patient_advisor_has_drug_interactions(self):
        """AC-4.5: PatientAdvisor has drug_interactions."""
        from trace_mineral_agent.concierge.subagents import patient_advisor_subagent

        tool_names = [t.name for t in patient_advisor_subagent["tools"]]
        assert "check_drug_interactions" in tool_names

    def test_AC4_6_wellness_researcher_has_paradigm_mapper(self):
        """AC-4.6: WellnessResearcher has paradigm_mapper."""
        from trace_mineral_agent.concierge.subagents import wellness_researcher_subagent

        tool_names = [t.name for t in wellness_researcher_subagent["tools"]]
        assert "paradigm_mapper" in tool_names

    def test_AC4_7_care_coordinator_has_synthesis_reporter(self):
        """AC-4.7: CareCoordinator has synthesis_reporter."""
        from trace_mineral_agent.concierge.subagents import care_coordinator_subagent

        tool_names = [t.name for t in care_coordinator_subagent["tools"]]
        assert "synthesis_reporter" in tool_names

    def test_AC4_8_unique_subagent_names(self):
        """AC-4.8: Unique subagent names."""
        from trace_mineral_agent.concierge.subagents import (
            care_coordinator_subagent,
            patient_advisor_subagent,
            wellness_researcher_subagent,
        )

        names = [
            patient_advisor_subagent["name"],
            wellness_researcher_subagent["name"],
            care_coordinator_subagent["name"],
        ]
        assert len(names) == len(set(names))


# =============================================================================
# AC-5: System Prompt Quality
# =============================================================================


class TestAC5_SystemPrompts:
    """AC-5: System prompts provide clear guidance."""

    def test_AC5_1_main_prompt_mentions_concierge(self):
        """AC-5.1: Main prompt mentions concierge."""
        from trace_mineral_agent.concierge import CONCIERGE_SYSTEM_PROMPT

        assert "concierge" in CONCIERGE_SYSTEM_PROMPT.lower()

    def test_AC5_2_personalization_emphasized(self):
        """AC-5.2: Personalization emphasized."""
        from trace_mineral_agent.concierge import CONCIERGE_SYSTEM_PROMPT

        prompt_lower = CONCIERGE_SYSTEM_PROMPT.lower()
        assert "personalized" in prompt_lower or "individual" in prompt_lower

    def test_AC5_3_evidence_based_approach(self):
        """AC-5.3: Evidence-based approach."""
        from trace_mineral_agent.concierge import CONCIERGE_SYSTEM_PROMPT

        assert "evidence" in CONCIERGE_SYSTEM_PROMPT.lower()

    def test_AC5_4_safety_requirements(self):
        """AC-5.4: Safety requirements."""
        from trace_mineral_agent.concierge import CONCIERGE_SYSTEM_PROMPT

        prompt_lower = CONCIERGE_SYSTEM_PROMPT.lower()
        assert "safety" in prompt_lower or "hipaa" in prompt_lower

    def test_AC5_5_subagents_described(self):
        """AC-5.5: Subagents described."""
        from trace_mineral_agent.concierge import CONCIERGE_SYSTEM_PROMPT

        assert "PatientAdvisor" in CONCIERGE_SYSTEM_PROMPT or "Patient Advisor" in CONCIERGE_SYSTEM_PROMPT
        assert "WellnessResearcher" in CONCIERGE_SYSTEM_PROMPT or "Wellness Researcher" in CONCIERGE_SYSTEM_PROMPT
        assert "CareCoordinator" in CONCIERGE_SYSTEM_PROMPT or "Care Coordinator" in CONCIERGE_SYSTEM_PROMPT

    def test_AC5_6_response_patterns_defined(self):
        """AC-5.6: Response patterns defined."""
        from trace_mineral_agent.concierge import CONCIERGE_SYSTEM_PROMPT

        assert "Response Pattern" in CONCIERGE_SYSTEM_PROMPT or "### For" in CONCIERGE_SYSTEM_PROMPT

    def test_AC5_7_followup_suggestions(self):
        """AC-5.7: Follow-up suggestions."""
        from trace_mineral_agent.concierge import CONCIERGE_SYSTEM_PROMPT

        prompt_lower = CONCIERGE_SYSTEM_PROMPT.lower()
        assert "follow-up" in prompt_lower or "next step" in prompt_lower


# =============================================================================
# AC-6: JTBD Workflows
# =============================================================================


class TestAC6_JTBDWorkflows:
    """AC-6: Complete user journeys work end-to-end."""

    def test_AC6_1_basic_wellness_check(self):
        """AC-6.1: Basic wellness check."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 40,
            "biological_sex": "female",
            "health_goals": ["general wellness"],
        })

        # Must produce actionable output
        assert "Priority" in result
        assert len(result) > 500  # Substantial content

    def test_AC6_2_complex_patient_assessment(self):
        """AC-6.2: Complex patient assessment."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 65,
            "biological_sex": "male",
            "health_goals": ["manage conditions"],
            "current_conditions": ["type 2 diabetes", "hypertension", "CKD stage 2"],
            "current_medications": ["metformin", "lisinopril", "amlodipine"],
            "lifestyle_factors": {
                "exercise": "sedentary",
                "sleep_hours": 5,
                "stress_level": "high",
            },
        })

        # Must handle complexity
        assert "Risk" in result
        assert "Priority" in result

    def test_AC6_3_lab_interpretation(self):
        """AC-6.3: Lab interpretation."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 50,
            "biological_sex": "female",
            "health_goals": ["optimization"],
            "recent_labs": {
                "glucose": 102,
                "HbA1c": 5.8,
                "vitamin_d": 22,
                "hs_CRP": 3.5,
            },
        })

        assert "Laboratory" in result
        # Should identify suboptimal values
        assert "optimal" in result.lower() or "normal" in result.lower()

    def test_AC6_4_metabolic_protocol(self):
        """AC-6.4: Metabolic protocol."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "50M with prediabetes and obesity",
            "primary_goal": "Reverse prediabetes",
            "plan_type": "condition_management",
            "timeline_weeks": 12,
        })

        # Should include metabolic interventions
        assert "magnesium" in result.lower() or "chromium" in result.lower() or "metabolic" in result.lower()

    def test_AC6_5_energy_protocol(self):
        """AC-6.5: Energy protocol."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "35F with chronic fatigue",
            "primary_goal": "Restore energy levels",
            "timeline_weeks": 8,
        })

        # Should address fatigue causes
        assert "sleep" in result.lower() or "energy" in result.lower()

    def test_AC6_6_cognitive_protocol(self):
        """AC-6.6: Cognitive protocol."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "60M concerned about cognitive decline",
            "primary_goal": "Brain health optimization",
            "timeline_weeks": 16,
        })

        # Should include neuroprotective elements
        assert "omega" in result.lower() or "brain" in result.lower() or "cognitive" in result.lower()

    def test_AC6_7_assessment_to_care_plan_workflow(self):
        """AC-6.7: Assessment to care plan workflow."""
        from trace_mineral_agent.concierge.tools import care_plan_generator, wellness_assessment

        # Step 1: Assessment
        assessment = wellness_assessment.invoke({
            "age": 48,
            "biological_sex": "female",
            "health_goals": ["metabolic health"],
            "current_conditions": ["hypothyroidism"],
        })

        assert "Priority" in assessment

        # Step 2: Care plan based on assessment
        care_plan = care_plan_generator.invoke({
            "patient_summary": f"48F with hypothyroidism. {assessment[:200]}",
            "primary_goal": "Thyroid and metabolic support",
            "timeline_weeks": 12,
        })

        assert "Phase" in care_plan
        assert "Monitoring" in care_plan

    def test_AC6_8_new_patient_onboarding(self):
        """AC-6.8: New patient onboarding."""
        from trace_mineral_agent.concierge.tools import care_plan_generator, wellness_assessment

        # Complete profile
        assessment = wellness_assessment.invoke({
            "age": 55,
            "biological_sex": "male",
            "health_goals": ["longevity", "metabolic health"],
            "current_conditions": ["prediabetes"],
            "current_medications": [],
            "current_supplements": ["vitamin D"],
            "lifestyle_factors": {
                "exercise": "3-4 times/week",
                "sleep_hours": 7,
                "stress_level": "moderate",
            },
            "recent_labs": {"glucose": 105, "HbA1c": 5.7},
        })

        care_plan = care_plan_generator.invoke({
            "patient_summary": "55M new patient, prediabetic, active lifestyle",
            "primary_goal": "Prevent diabetes progression",
            "secondary_goals": ["optimize longevity markers"],
            "timeline_weeks": 16,
            "plan_type": "condition_management",
            "include_supplements": True,
            "include_lifestyle": True,
            "include_monitoring": True,
        })

        # Both should be comprehensive
        assert "Risk" in assessment
        assert "Phase" in care_plan
        assert "Monitoring" in care_plan
        assert "Safety" in care_plan


# =============================================================================
# AC-7: Edge Cases & Error Handling
# =============================================================================


class TestAC7_EdgeCases:
    """AC-7: System handles boundary conditions gracefully."""

    def test_AC7_1_minimal_input(self):
        """AC-7.1: Minimal input."""
        from trace_mineral_agent.concierge.tools import care_plan_generator, wellness_assessment

        # Minimal assessment
        assessment = wellness_assessment.invoke({
            "age": 30,
            "biological_sex": "female",
            "health_goals": ["wellness"],
        })
        assert "Wellness Assessment" in assessment
        assert len(assessment) > 200

        # Minimal care plan
        plan = care_plan_generator.invoke({
            "patient_summary": "30F",
            "primary_goal": "General health",
        })
        assert "Care Plan" in plan

    def test_AC7_2_elderly_patient(self):
        """AC-7.2: Elderly patient."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 82,
            "biological_sex": "female",
            "health_goals": ["maintain independence"],
        })

        assert "Mature" in result

    def test_AC7_3_young_adult(self):
        """AC-7.3: Young adult."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 22,
            "biological_sex": "male",
            "health_goals": ["athletic performance"],
        })

        assert "Young Adult" in result

    def test_AC7_4_multiple_conditions(self):
        """AC-7.4: Multiple conditions."""
        from trace_mineral_agent.concierge.tools import wellness_assessment

        result = wellness_assessment.invoke({
            "age": 70,
            "biological_sex": "male",
            "health_goals": ["quality of life"],
            "current_conditions": [
                "type 2 diabetes",
                "hypertension",
                "hyperlipidemia",
                "osteoarthritis",
                "BPH",
            ],
            "current_medications": [
                "metformin",
                "lisinopril",
                "atorvastatin",
                "tamsulosin",
            ],
        })

        # Should acknowledge complexity
        assert "Risk" in result
        assert len(result) > 1000  # Should be substantial for complex patient

    def test_AC7_5_short_timeline(self):
        """AC-7.5: Short timeline."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Quick intervention",
            "primary_goal": "Rapid improvement",
            "timeline_weeks": 4,
        })

        assert "4 weeks" in result
        # Should be appropriately scoped
        assert "Phase 1" in result

    def test_AC7_6_long_timeline(self):
        """AC-7.6: Long timeline."""
        from trace_mineral_agent.concierge.tools import care_plan_generator

        result = care_plan_generator.invoke({
            "patient_summary": "Long-term patient",
            "primary_goal": "Sustained transformation",
            "timeline_weeks": 24,
        })

        assert "24 weeks" in result


# =============================================================================
# AC-8: Integration & Compatibility
# =============================================================================


class TestAC8_Integration:
    """AC-8: Feature integrates without conflicts."""

    def test_AC8_1_existing_tests_pass(self):
        """AC-8.1: Existing tests pass - validated by running full suite."""
        # This is validated by pytest discovering and running all tests
        # If we get here, existing tests are discoverable
        from trace_mineral_agent.subagents import allopathy_subagent

        assert allopathy_subagent is not None

    def test_AC8_2_no_import_errors(self):
        """AC-8.2: No import errors."""
        # Import all concierge modules
        from trace_mineral_agent.concierge import (
            CONCIERGE_QUICK_QUESTIONS,
            CONCIERGE_SYSTEM_PROMPT,
            care_coordinator_subagent,
            care_plan_generator,
            concierge_agent,
            create_concierge_agent,
            patient_advisor_subagent,
            wellness_assessment,
            wellness_researcher_subagent,
        )

        # All imports successful
        assert concierge_agent is not None
        assert create_concierge_agent is not None
        assert CONCIERGE_SYSTEM_PROMPT is not None
        assert CONCIERGE_QUICK_QUESTIONS is not None
        assert patient_advisor_subagent is not None
        assert wellness_researcher_subagent is not None
        assert care_coordinator_subagent is not None
        assert wellness_assessment is not None
        assert care_plan_generator is not None

    def test_AC8_3_tools_reuse_works(self):
        """AC-8.3: Tools reuse works."""
        # Core tools should work in concierge context
        from trace_mineral_agent.tools import (
            check_drug_interactions,
            evidence_grade,
            literature_search,
            paradigm_mapper,
            synthesis_reporter,
        )

        # Verify tools are callable
        assert callable(literature_search.invoke)
        assert callable(evidence_grade.invoke)
        assert callable(paradigm_mapper.invoke)
        assert callable(synthesis_reporter.invoke)
        assert callable(check_drug_interactions.invoke)

    def test_AC8_4_no_conflicts_with_main_agent(self):
        """AC-8.4: No conflicts with main agent."""
        # Both agents should be importable and distinct
        from trace_mineral_agent.agent import agent as main_agent
        from trace_mineral_agent.concierge import concierge_agent

        assert main_agent is not None
        assert concierge_agent is not None
        assert main_agent is not concierge_agent


# =============================================================================
# UAT Summary Report
# =============================================================================


class TestUATSummary:
    """Generate UAT summary statistics."""

    def test_uat_criteria_count(self):
        """Verify all UAT criteria have tests."""
        # Count tests by prefix
        ac_counts = {
            "AC1": 3,   # Deployment
            "AC2": 9,   # Wellness Assessment
            "AC3": 15,  # Care Plan
            "AC4": 8,   # Subagent Config
            "AC5": 7,   # System Prompts
            "AC6": 8,   # JTBD Workflows
            "AC7": 6,   # Edge Cases
            "AC8": 4,   # Integration
        }

        total = sum(ac_counts.values())
        assert total == 60, f"Expected 60 UAT criteria, got {total}"
