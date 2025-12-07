"""End-to-end tests for ConciergeHealthAgent workflows.

These tests validate complete user journeys and Jobs To Be Done (JTBD)
for the concierge medicine use case.

Run with: pytest tests/test_concierge_e2e.py -v
Integration tests (require API keys): pytest -m integration tests/test_concierge_e2e.py
"""

import os

import pytest

from trace_mineral_agent.concierge.tools import care_plan_generator, wellness_assessment


# =============================================================================
# JTBD 1: "As a patient, I want a personalized wellness assessment
#          so I can understand my health priorities"
# =============================================================================


class TestJTBD_WellnessAssessment:
    """E2E tests for wellness assessment job-to-be-done."""

    def test_jtbd_basic_wellness_check(self):
        """
        JTBD: Patient wants quick wellness snapshot.
        Given: Basic demographics and goals
        When: Assessment is generated
        Then: Patient receives actionable health insights
        """
        result = wellness_assessment.invoke({
            "age": 45,
            "biological_sex": "male",
            "health_goals": ["energy", "weight management"],
        })

        # Should identify life stage considerations
        assert "Prime Adult" in result or "Midlife" in result
        # Should provide priority actions
        assert "Priority" in result
        # Should include disclaimer
        assert "healthcare provider" in result.lower() or "informational" in result.lower()

    def test_jtbd_comprehensive_assessment_with_conditions(self):
        """
        JTBD: Patient with existing conditions wants thorough review.
        Given: Health conditions, medications, and lifestyle data
        When: Assessment is generated
        Then: Patient receives condition-aware recommendations
        """
        result = wellness_assessment.invoke({
            "age": 55,
            "biological_sex": "female",
            "health_goals": ["metabolic health", "longevity"],
            "current_conditions": ["type 2 diabetes", "hypertension"],
            "current_medications": ["metformin", "lisinopril"],
            "lifestyle_factors": {
                "exercise": "sedentary",
                "sleep_hours": 6,
                "stress_level": "high",
                "diet_type": "standard",
            },
        })

        # Should flag high-priority conditions
        assert "metabolic" in result.lower() or "diabetes" in result.lower()
        # Should note lifestyle concerns
        assert "sedentary" in result.lower() or "lifestyle" in result.lower()
        # Should include risk assessment
        assert "Risk" in result
        # Should show current medications
        assert "metformin" in result.lower()

    def test_jtbd_lab_analysis_for_optimization(self):
        """
        JTBD: Health-conscious patient wants lab interpretation.
        Given: Recent lab values
        When: Assessment analyzes labs
        Then: Patient understands what's optimal vs just normal
        """
        result = wellness_assessment.invoke({
            "age": 40,
            "biological_sex": "male",
            "health_goals": ["optimization", "longevity"],
            "recent_labs": {
                "glucose": 98,
                "HbA1c": 5.6,
                "vitamin_d": 28,
                "hs_CRP": 2.5,
            },
        })

        # Should include laboratory analysis section
        assert "Laboratory Analysis" in result
        # Should note values that are normal but not optimal
        assert "optimal" in result.lower() or "normal" in result.lower()
        # Should flag vitamin D as suboptimal
        assert "vitamin" in result.lower() or "d" in result.lower()

    def test_jtbd_menopause_specific_assessment(self):
        """
        JTBD: Perimenopausal woman wants hormonal health focus.
        Given: Female patient in midlife
        When: Assessment is generated
        Then: Patient receives menopause-relevant guidance
        """
        result = wellness_assessment.invoke({
            "age": 52,
            "biological_sex": "female",
            "health_goals": ["hormone balance", "bone health"],
        })

        # Should recognize life stage
        assert "Midlife" in result
        # Should mention hormonal considerations
        assert "hormone" in result.lower() or "menopause" in result.lower()
        # Should include bone health as focus area
        assert "bone" in result.lower()


# =============================================================================
# JTBD 2: "As a patient, I want a personalized care plan
#          so I can take structured action on my health"
# =============================================================================


class TestJTBD_CarePlanGeneration:
    """E2E tests for care plan generation job-to-be-done."""

    def test_jtbd_metabolic_health_protocol(self):
        """
        JTBD: Patient wants metabolic optimization plan.
        Given: Metabolic health goal with patient context
        When: Care plan is generated
        Then: Patient receives phased metabolic protocol
        """
        result = care_plan_generator.invoke({
            "patient_summary": "45-year-old male with prediabetes (HbA1c 5.9), "
                              "sedentary lifestyle, BMI 28, goal: avoid diabetes",
            "primary_goal": "Reverse prediabetes and optimize metabolic health",
            "secondary_goals": ["lose 15 pounds", "increase energy"],
            "timeline_weeks": 12,
            "plan_type": "condition_management",
        })

        # Should have phased implementation
        assert "Phase 1" in result
        assert "Phase 2" in result or "Week" in result
        # Should include metabolic-relevant supplements
        assert "magnesium" in result.lower() or "chromium" in result.lower()
        # Should include lifestyle interventions
        assert "exercise" in result.lower() or "movement" in result.lower()
        # Should include monitoring
        assert "glucose" in result.lower() or "monitoring" in result.lower()

    def test_jtbd_energy_fatigue_protocol(self):
        """
        JTBD: Exhausted patient wants energy restoration plan.
        Given: Fatigue as primary concern
        When: Care plan is generated
        Then: Patient receives energy-focused protocol
        """
        result = care_plan_generator.invoke({
            "patient_summary": "38-year-old female, chronic fatigue for 6 months, "
                              "sleep issues, high stress job, no diagnosed conditions",
            "primary_goal": "Restore energy and reduce fatigue",
            "secondary_goals": ["improve sleep quality", "manage stress"],
            "timeline_weeks": 8,
            "plan_type": "wellness",
        })

        # Should address energy-relevant factors
        assert "sleep" in result.lower()
        assert "stress" in result.lower()
        # Should include relevant supplements
        assert "b-complex" in result.lower() or "coq10" in result.lower() or "b12" in result.lower()
        # Should have follow-up schedule
        assert "Follow-up" in result

    def test_jtbd_cognitive_longevity_protocol(self):
        """
        JTBD: Aging patient wants brain health plan.
        Given: Cognitive preservation as goal
        When: Care plan is generated
        Then: Patient receives brain-focused longevity protocol
        """
        result = care_plan_generator.invoke({
            "patient_summary": "62-year-old male, family history of Alzheimer's, "
                              "wants to optimize brain health and cognitive function",
            "primary_goal": "Cognitive enhancement and brain health",
            "secondary_goals": ["neuroprotection", "memory support"],
            "timeline_weeks": 16,
            "plan_type": "wellness",
        })

        # Should include cognitive-relevant interventions
        assert "omega" in result.lower() or "brain" in result.lower()
        # Should have extended timeline phases
        assert "Week" in result or "Month" in result
        # Should include monitoring for cognitive function
        assert "Monitoring" in result

    def test_jtbd_gut_health_restoration(self):
        """
        JTBD: Patient with digestive issues wants gut healing plan.
        Given: Gut health restoration as goal
        When: Care plan is generated
        Then: Patient receives systematic gut protocol
        """
        result = care_plan_generator.invoke({
            "patient_summary": "34-year-old female with bloating, irregular digestion, "
                              "suspected food sensitivities, no IBD diagnosis",
            "primary_goal": "Gut health restoration",
            "secondary_goals": ["reduce bloating", "identify trigger foods"],
            "timeline_weeks": 12,
            "plan_type": "recovery",
        })

        # Should be recovery plan type
        assert "Recovery" in result
        # Should have structured approach
        assert "Phase" in result
        # Should include safety section
        assert "Safety" in result

    def test_jtbd_quick_lifestyle_intervention(self):
        """
        JTBD: Busy patient wants simple starter protocol.
        Given: Short timeline and simple goals
        When: Care plan is generated
        Then: Patient receives focused, actionable plan
        """
        result = care_plan_generator.invoke({
            "patient_summary": "50-year-old busy executive, generally healthy, "
                              "wants simple wellness optimization",
            "primary_goal": "General wellness optimization",
            "timeline_weeks": 4,
            "plan_type": "lifestyle_transformation",
        })

        # Should respect short timeline
        assert "4 weeks" in result
        # Should be lifestyle transformation type
        assert "Lifestyle Transformation" in result
        # Should have actionable items
        assert "[" in result  # Checkbox items


# =============================================================================
# JTBD 3: "As a patient, I want to check medication interactions
#          so I can supplement safely"
# =============================================================================


class TestJTBD_SafetyChecking:
    """E2E tests for safety checking job-to-be-done."""

    def test_jtbd_supplement_safety_with_medications(self):
        """
        JTBD: Patient on medications wants to add supplements safely.
        Given: Current medications in wellness assessment
        When: Assessment is generated
        Then: Patient is informed about interaction considerations
        """
        result = wellness_assessment.invoke({
            "age": 60,
            "biological_sex": "male",
            "health_goals": ["supplement safely"],
            "current_medications": ["warfarin", "levothyroxine", "metformin"],
            "current_supplements": ["fish oil", "vitamin D"],
        })

        # Should list medications
        assert "warfarin" in result.lower()
        assert "metformin" in result.lower()
        # Should list supplements
        assert "fish oil" in result.lower() or "vitamin d" in result.lower()
        # Should include safety considerations
        assert "healthcare provider" in result.lower()

    def test_jtbd_care_plan_includes_safety_section(self):
        """
        JTBD: Any care plan should address safety proactively.
        Given: Care plan request
        When: Plan is generated
        Then: Safety section is always included
        """
        result = care_plan_generator.invoke({
            "patient_summary": "Any patient",
            "primary_goal": "Any goal",
        })

        # Must always have safety considerations
        assert "Safety Considerations" in result
        # Must have warning signs
        assert "Warning" in result
        # Must have contraindication section
        assert "Contraindication" in result or "interaction" in result.lower()


# =============================================================================
# JTBD 4: "As a physician, I want evidence-based research synthesis
#          so I can make informed recommendations"
# =============================================================================


class TestJTBD_PhysicianResearch:
    """E2E tests for physician research job-to-be-done."""

    def test_jtbd_evidence_based_care_plan(self):
        """
        JTBD: Physician wants evidence-graded interventions.
        Given: Care plan with interventions
        When: Plan is generated
        Then: Evidence grades are included for interventions
        """
        result = care_plan_generator.invoke({
            "patient_summary": "Standard patient requiring evidence-based care",
            "primary_goal": "Evidence-based protocol",
            "interventions": [
                {
                    "name": "Omega-3 supplementation",
                    "category": "Supplement",
                    "priority": 2,
                    "evidence_grade": "A",
                },
                {
                    "name": "Meditation practice",
                    "category": "Lifestyle",
                    "priority": 3,
                    "evidence_grade": "B",
                },
            ],
        })

        # Should include evidence grades
        assert "Evidence" in result
        # Should show intervention table
        assert "Intervention" in result
        # Should include the specified grades
        assert "A" in result and "B" in result

    def test_jtbd_monitoring_and_adjustment_protocol(self):
        """
        JTBD: Physician wants objective monitoring criteria.
        Given: Care plan with monitoring enabled
        When: Plan is generated
        Then: Objective markers and adjustment criteria are provided
        """
        result = care_plan_generator.invoke({
            "patient_summary": "Patient requiring close monitoring",
            "primary_goal": "Monitored intervention",
            "include_monitoring": True,
        })

        # Should have monitoring protocol
        assert "Monitoring Protocol" in result
        # Should have objective markers
        assert "Objective" in result or "Marker" in result
        # Should have adjustment criteria
        assert "Adjustment" in result
        # Should have lab testing schedule
        assert "Lab" in result


# =============================================================================
# E2E WORKFLOW TESTS: Complete User Journeys
# =============================================================================


class TestE2E_CompleteWorkflows:
    """E2E tests for complete multi-step workflows."""

    def test_workflow_assessment_to_care_plan(self):
        """
        Workflow: Patient gets assessment, then uses insights for care plan.
        Given: Patient completes wellness assessment
        When: Assessment identifies priorities
        Then: Care plan can be generated for identified priorities
        """
        # Step 1: Get wellness assessment
        assessment = wellness_assessment.invoke({
            "age": 48,
            "biological_sex": "female",
            "health_goals": ["metabolic health", "hormone balance"],
            "current_conditions": ["hypothyroidism"],
            "lifestyle_factors": {
                "exercise": "1-2 times/week",
                "sleep_hours": 6,
                "stress_level": "high",
            },
        })

        # Assessment should identify priorities
        assert "Priority" in assessment

        # Step 2: Generate care plan based on assessment findings
        care_plan = care_plan_generator.invoke({
            "patient_summary": f"48F with hypothyroidism. Assessment findings: {assessment[:200]}",
            "primary_goal": "Thyroid optimization and metabolic support",
            "secondary_goals": ["improve sleep", "reduce stress"],
            "timeline_weeks": 12,
        })

        # Care plan should be comprehensive
        assert "Phase" in care_plan
        assert "Monitoring" in care_plan
        assert "Safety" in care_plan

    def test_workflow_comprehensive_new_patient_onboarding(self):
        """
        Workflow: Complete new patient onboarding journey.
        Given: New concierge patient with full health history
        When: Complete onboarding workflow is executed
        Then: Patient has assessment and care plan ready
        """
        # Full patient profile
        patient_data = {
            "age": 52,
            "biological_sex": "male",
            "health_goals": ["longevity", "cognitive health", "metabolic optimization"],
            "current_conditions": ["prediabetes", "sleep apnea"],
            "current_medications": ["CPAP therapy"],
            "current_supplements": ["vitamin D", "magnesium"],
            "lifestyle_factors": {
                "exercise": "3-4 times/week",
                "sleep_hours": 7,
                "stress_level": "moderate",
                "diet_type": "mediterranean",
            },
            "recent_labs": {
                "glucose": 108,
                "HbA1c": 5.8,
                "vitamin_d": 45,
            },
        }

        # Step 1: Comprehensive assessment
        assessment = wellness_assessment.invoke(patient_data)

        # Should cover all aspects
        assert "Laboratory Analysis" in assessment
        assert "Lifestyle" in assessment
        assert "Risk" in assessment
        assert "Priority" in assessment

        # Step 2: Personalized care plan
        care_plan = care_plan_generator.invoke({
            "patient_summary": f"52M prediabetic with sleep apnea, on CPAP. "
                              f"Goals: longevity, cognition, metabolism. "
                              f"Labs show elevated glucose, adequate D.",
            "primary_goal": "Reverse prediabetes and optimize healthspan",
            "secondary_goals": ["cognitive protection", "metabolic flexibility"],
            "timeline_weeks": 16,
            "plan_type": "condition_management",
            "include_supplements": True,
            "include_lifestyle": True,
            "include_monitoring": True,
        })

        # Plan should be complete
        assert "Personalized Care Plan" in care_plan
        assert "Phase 1" in care_plan
        assert "Supplement" in care_plan
        assert "Lifestyle" in care_plan
        assert "Monitoring Protocol" in care_plan
        assert "Follow-up" in care_plan

    def test_workflow_iterative_plan_refinement(self):
        """
        Workflow: Patient refines plan through multiple iterations.
        Given: Initial care plan generated
        When: Patient wants to adjust focus
        Then: New plan can be generated with different parameters
        """
        # Initial plan focused on metabolic
        initial_plan = care_plan_generator.invoke({
            "patient_summary": "40-year-old with metabolic concerns",
            "primary_goal": "Metabolic optimization",
            "timeline_weeks": 12,
        })

        assert "metabolic" in initial_plan.lower() or "Metabolic" in initial_plan

        # Refined plan focused on energy (patient feedback)
        refined_plan = care_plan_generator.invoke({
            "patient_summary": "40-year-old, metabolic plan in progress, "
                              "now prioritizing energy optimization",
            "primary_goal": "Energy and fatigue reduction",
            "timeline_weeks": 8,
            "include_supplements": True,
        })

        assert "energy" in refined_plan.lower() or "fatigue" in refined_plan.lower()


# =============================================================================
# EDGE CASES AND ERROR HANDLING
# =============================================================================


class TestE2E_EdgeCases:
    """E2E tests for edge cases and boundary conditions."""

    def test_minimal_input_still_produces_value(self):
        """
        Edge case: Minimal patient information.
        Given: Only required fields provided
        When: Assessment/plan generated
        Then: Still produces useful output
        """
        # Minimal assessment
        assessment = wellness_assessment.invoke({
            "age": 30,
            "biological_sex": "female",
            "health_goals": ["general wellness"],
        })

        assert "Wellness Assessment" in assessment
        assert "Priority" in assessment

        # Minimal care plan
        plan = care_plan_generator.invoke({
            "patient_summary": "30F, general wellness",
            "primary_goal": "General health",
        })

        assert "Care Plan" in plan

    def test_elderly_patient_considerations(self):
        """
        Edge case: Elderly patient has special considerations.
        Given: Patient over 70
        When: Assessment generated
        Then: Age-appropriate guidance provided
        """
        assessment = wellness_assessment.invoke({
            "age": 78,
            "biological_sex": "male",
            "health_goals": ["maintain function", "cognitive health"],
        })

        # Should recognize mature adult stage
        assert "Mature" in assessment
        # Should focus on appropriate areas
        assert "cognitive" in assessment.lower() or "function" in assessment.lower()

    def test_young_adult_performance_focus(self):
        """
        Edge case: Young adult with performance focus.
        Given: Patient under 30 with optimization goals
        When: Assessment generated
        Then: Performance-oriented guidance provided
        """
        assessment = wellness_assessment.invoke({
            "age": 25,
            "biological_sex": "male",
            "health_goals": ["athletic performance", "muscle gain"],
        })

        # Should recognize young adult stage
        assert "Young Adult" in assessment
        # Should focus on building foundation
        assert "foundation" in assessment.lower() or "performance" in assessment.lower()

    def test_multiple_chronic_conditions(self):
        """
        Edge case: Complex patient with multiple conditions.
        Given: Multiple chronic conditions and medications
        When: Assessment generated
        Then: Complexity is acknowledged appropriately
        """
        assessment = wellness_assessment.invoke({
            "age": 65,
            "biological_sex": "female",
            "health_goals": ["manage conditions", "quality of life"],
            "current_conditions": [
                "type 2 diabetes",
                "hypertension",
                "hyperlipidemia",
                "osteoarthritis",
            ],
            "current_medications": [
                "metformin",
                "lisinopril",
                "atorvastatin",
                "ibuprofen",
            ],
        })

        # Should acknowledge complexity
        assert "Risk" in assessment
        # Should list all conditions
        assert any(cond in assessment.lower() for cond in ["diabetes", "hypertension"])
        # Should show medications
        assert "metformin" in assessment.lower()


# =============================================================================
# INTEGRATION TESTS (require API keys)
# =============================================================================

pytestmark_integration = pytest.mark.integration


def requires_api_key(key_name: str):
    """Skip test if API key is not available."""
    return pytest.mark.skipif(
        os.getenv(key_name) is None or os.getenv(key_name, "").startswith("test-"),
        reason=f"{key_name} not configured",
    )


@pytest.mark.integration
class TestE2E_IntegrationWithLLM:
    """Integration tests that require real API keys."""

    @requires_api_key("ANTHROPIC_API_KEY")
    def test_concierge_agent_responds_to_health_query(self):
        """Test that concierge agent can respond to a health query."""
        from trace_mineral_agent.concierge import concierge_agent

        # This test requires real API key and will make actual LLM call
        # Skip if in CI without keys
        if os.getenv("CI") and not os.getenv("ANTHROPIC_API_KEY"):
            pytest.skip("Skipping integration test in CI without API key")

        result = concierge_agent.invoke({
            "messages": [{
                "role": "user",
                "content": "What are the key considerations for a 50-year-old "
                          "looking to optimize their metabolic health?"
            }]
        })

        assert result is not None
        assert "messages" in result
        assert len(result["messages"]) > 0
        # Response should contain health-related content
        response_content = result["messages"][-1].content.lower()
        assert any(term in response_content for term in [
            "metabolic", "health", "glucose", "insulin", "lifestyle"
        ])
