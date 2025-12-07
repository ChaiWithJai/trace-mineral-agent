"""Tests for the concierge-specific tools."""

import pytest

from trace_mineral_agent.concierge.tools import care_plan_generator, wellness_assessment


class TestWellnessAssessment:
    """Tests for the wellness_assessment tool."""

    def test_wellness_assessment_basic(self):
        """Wellness assessment should generate basic report."""
        result = wellness_assessment.invoke(
            {
                "age": 45,
                "biological_sex": "male",
                "health_goals": ["weight loss", "energy"],
            }
        )

        assert "Wellness Assessment Report" in result
        assert "45" in result
        assert "Male" in result
        assert "weight loss" in result.lower() or "Weight Loss" in result

    def test_wellness_assessment_with_conditions(self):
        """Wellness assessment should handle current conditions."""
        result = wellness_assessment.invoke(
            {
                "age": 55,
                "biological_sex": "female",
                "health_goals": ["metabolic health"],
                "current_conditions": ["type 2 diabetes", "hypertension"],
            }
        )

        assert "Wellness Assessment Report" in result
        assert "Risk Assessment" in result
        # Should flag diabetes as priority
        assert "metabolic" in result.lower() or "diabetes" in result.lower()

    def test_wellness_assessment_with_medications(self):
        """Wellness assessment should include medications."""
        result = wellness_assessment.invoke(
            {
                "age": 60,
                "biological_sex": "male",
                "health_goals": ["longevity"],
                "current_medications": ["metformin", "lisinopril"],
            }
        )

        assert "Current Interventions" in result
        assert "metformin" in result.lower()
        assert "lisinopril" in result.lower()

    def test_wellness_assessment_with_lifestyle_factors(self):
        """Wellness assessment should analyze lifestyle factors."""
        result = wellness_assessment.invoke(
            {
                "age": 35,
                "biological_sex": "female",
                "health_goals": ["energy"],
                "lifestyle_factors": {
                    "exercise": "3-4 times/week",
                    "sleep_hours": 7,
                    "stress_level": "moderate",
                    "diet_type": "mediterranean",
                },
            }
        )

        assert "Lifestyle Factors" in result
        assert "Lifestyle Score" in result

    def test_wellness_assessment_with_labs(self):
        """Wellness assessment should analyze lab values."""
        result = wellness_assessment.invoke(
            {
                "age": 50,
                "biological_sex": "male",
                "health_goals": ["metabolic health"],
                "recent_labs": {
                    "glucose": 105,
                    "HbA1c": 5.8,
                    "vitamin_d": 25,
                },
            }
        )

        assert "Laboratory Analysis" in result
        # Should note elevated glucose
        assert "glucose" in result.lower()

    def test_wellness_assessment_life_stages(self):
        """Wellness assessment should identify life stage considerations."""
        # Young adult
        result_young = wellness_assessment.invoke(
            {
                "age": 25,
                "biological_sex": "male",
                "health_goals": ["performance"],
            }
        )
        assert "Young Adult" in result_young

        # Midlife female
        result_midlife = wellness_assessment.invoke(
            {
                "age": 52,
                "biological_sex": "female",
                "health_goals": ["hormone balance"],
            }
        )
        assert "Midlife" in result_midlife

        # Mature adult
        result_mature = wellness_assessment.invoke(
            {
                "age": 70,
                "biological_sex": "male",
                "health_goals": ["cognitive health"],
            }
        )
        assert "Mature" in result_mature

    def test_wellness_assessment_includes_disclaimer(self):
        """Wellness assessment should include disclaimer."""
        result = wellness_assessment.invoke(
            {
                "age": 40,
                "biological_sex": "female",
                "health_goals": ["wellness"],
            }
        )

        assert "informational" in result.lower() or "healthcare provider" in result.lower()


class TestCarePlanGenerator:
    """Tests for the care_plan_generator tool."""

    def test_care_plan_basic(self):
        """Care plan generator should create basic plan."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "45-year-old male seeking metabolic optimization",
                "primary_goal": "Improve metabolic health",
            }
        )

        assert "Personalized Care Plan" in result
        assert "metabolic" in result.lower()
        assert "Phase" in result  # Should have phased implementation

    def test_care_plan_with_secondary_goals(self):
        """Care plan should include secondary goals."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "35-year-old female with energy concerns",
                "primary_goal": "Increase daily energy",
                "secondary_goals": ["improve sleep", "reduce stress"],
            }
        )

        assert "Secondary Goals" in result
        assert "sleep" in result.lower()
        assert "stress" in result.lower()

    def test_care_plan_with_interventions(self):
        """Care plan should organize custom interventions."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "50-year-old male with cognitive concerns",
                "primary_goal": "Cognitive enhancement",
                "interventions": [
                    {
                        "name": "Omega-3 supplementation",
                        "category": "Supplement",
                        "priority": 2,
                        "evidence_grade": "A",
                    },
                    {
                        "name": "Aerobic exercise",
                        "category": "Lifestyle",
                        "priority": 1,
                        "evidence_grade": "A",
                    },
                ],
            }
        )

        assert "Intervention Summary" in result
        assert "Omega-3" in result
        assert "exercise" in result.lower()

    def test_care_plan_timeline_customization(self):
        """Care plan should respect custom timeline."""
        result_short = care_plan_generator.invoke(
            {
                "patient_summary": "Quick intervention patient",
                "primary_goal": "Short-term goal",
                "timeline_weeks": 4,
            }
        )
        assert "4 weeks" in result_short

        result_long = care_plan_generator.invoke(
            {
                "patient_summary": "Long-term intervention patient",
                "primary_goal": "Long-term goal",
                "timeline_weeks": 24,
            }
        )
        assert "24 weeks" in result_long

    def test_care_plan_types(self):
        """Care plan should handle different plan types."""
        plan_types = ["wellness", "condition_management", "recovery", "lifestyle_transformation"]

        for plan_type in plan_types:
            result = care_plan_generator.invoke(
                {
                    "patient_summary": f"Patient for {plan_type} plan",
                    "primary_goal": "Test goal",
                    "plan_type": plan_type,
                }
            )
            assert "Personalized Care Plan" in result
            assert plan_type.replace("_", " ").title() in result

    def test_care_plan_includes_monitoring(self):
        """Care plan should include monitoring protocol when requested."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "Patient requiring monitoring",
                "primary_goal": "Health optimization",
                "include_monitoring": True,
            }
        )

        assert "Monitoring Protocol" in result
        assert "Subjective" in result or "Objective" in result
        assert "Lab" in result

    def test_care_plan_includes_safety(self):
        """Care plan should always include safety section."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "Any patient",
                "primary_goal": "Any goal",
            }
        )

        assert "Safety Considerations" in result
        assert "Warning" in result or "Contraindication" in result

    def test_care_plan_includes_followup(self):
        """Care plan should include follow-up schedule."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "Patient needing follow-up",
                "primary_goal": "Goal requiring monitoring",
            }
        )

        assert "Follow-up Schedule" in result
        assert "Week" in result

    def test_care_plan_includes_adjustment_criteria(self):
        """Care plan should include adjustment criteria."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "Patient for adaptive plan",
                "primary_goal": "Goal requiring adjustment",
            }
        )

        assert "Adjustment Criteria" in result
        assert "Positive" in result or "Plateau" in result or "Adverse" in result

    def test_care_plan_includes_disclaimer(self):
        """Care plan should include important disclaimer."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "Any patient",
                "primary_goal": "Any goal",
            }
        )

        assert "Important Notice" in result or "healthcare provider" in result.lower()


class TestCarePlanGoalSpecificContent:
    """Tests for goal-specific content generation in care plans."""

    def test_metabolic_goal_supplements(self):
        """Metabolic goals should include relevant supplements."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "Patient with metabolic concerns",
                "primary_goal": "Metabolic optimization",
                "include_supplements": True,
            }
        )

        # Should include metabolic-relevant supplements
        assert "magnesium" in result.lower() or "chromium" in result.lower()

    def test_energy_goal_supplements(self):
        """Energy goals should include relevant supplements."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "Patient with fatigue",
                "primary_goal": "Combat fatigue and improve energy",
                "include_supplements": True,
            }
        )

        # Should include energy-relevant supplements
        assert "b-complex" in result.lower() or "coq10" in result.lower() or "b12" in result.lower()

    def test_cognitive_goal_supplements(self):
        """Cognitive goals should include relevant supplements."""
        result = care_plan_generator.invoke(
            {
                "patient_summary": "Patient seeking cognitive support",
                "primary_goal": "Cognitive enhancement and brain health",
                "include_supplements": True,
            }
        )

        # Should include cognitive-relevant supplements
        assert "omega" in result.lower() or "lion" in result.lower()
