"""End-to-end JTBD (Jobs To Be Done) workflow tests for skincare features.

These tests validate complete user workflows based on jobs users hire
the SkinIntelligenceAgent to do.

Target Demographics:
- Skintellectuals: Ingredient-obsessed, science-first consumers
- Problem-Skin Sufferers: Acne, rosacea, hyperpigmentation seekers
- Preventive Agers: Those optimizing before visible damage
- Budget Hunters: Finding effective alternatives at lower prices
"""

import pytest

from trace_mineral_agent.skincare.tools import (
    ingredient_analyzer,
    routine_builder,
    skin_profile_assessment,
    trend_evaluator,
)


class TestJTBD_SkinProfile:
    """JTBD: "Help me understand my skin and what it needs"

    User Personas:
    - Beginner who doesn't know their skin type
    - Experienced user wanting deeper analysis
    - Someone overwhelmed by conflicting advice
    """

    def test_complete_profile_analysis(self):
        """Test complete skin profile workflow."""
        # User provides comprehensive information
        result = skin_profile_assessment.invoke({
            "age": 28,
            "skin_type": "combination",
            "primary_concerns": ["acne", "hyperpigmentation"],
            "secondary_concerns": ["texture", "pores"],
            "known_sensitivities": ["fragrance"],
            "current_routine_steps": 5,
            "budget_level": "mid-range",
            "time_available_minutes": 15,
            "climate": "humid",
            "lifestyle_factors": {
                "sleep_hours": 7,
                "water_glasses": 8,
                "stress_level": "moderate",
                "sun_exposure": "moderate",
            },
        })

        # Should provide comprehensive analysis
        assert "Profile Summary" in result or "profile" in result.lower()
        assert "combination" in result.lower()
        assert "acne" in result.lower()
        assert "hyperpigmentation" in result.lower()

        # Should provide actionable guidance
        assert "recommendation" in result.lower() or "suggest" in result.lower() or "step" in result.lower()

    def test_minimal_info_profile(self):
        """Test profile with minimal information."""
        # User provides just basics
        result = skin_profile_assessment.invoke({
            "age": 35,
            "skin_type": "oily",
            "primary_concerns": ["aging"],
        })

        # Should still provide useful analysis
        assert "oily" in result.lower()
        assert "aging" in result.lower()
        assert len(result) > 500  # Should be substantial

    def test_sensitive_skin_profile(self):
        """Test profile for sensitive skin user."""
        result = skin_profile_assessment.invoke({
            "age": 42,
            "skin_type": "sensitive",
            "primary_concerns": ["redness", "dehydration"],
            "known_sensitivities": ["fragrance", "essential oils", "alcohol"],
        })

        # Should emphasize caution
        assert "sensitive" in result.lower()
        assert "caution" in result.lower() or "gentle" in result.lower() or "patch test" in result.lower()


class TestJTBD_IngredientResearch:
    """JTBD: "Help me understand what ingredients actually work"

    User Personas:
    - Skintellectual wanting mechanism details
    - Shopper comparing product claims
    - Someone checking if ingredients are safe together
    """

    def test_deep_ingredient_understanding(self):
        """Test deep dive into a single ingredient."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["tretinoin"],
            "analysis_depth": "comprehensive",
        })

        # Should provide mechanism
        assert "mechanism" in result.lower()
        assert "receptor" in result.lower() or "collagen" in result.lower()

        # Should provide evidence grade
        assert "evidence" in result.lower()
        assert "A" in result  # Tretinoin is grade A

        # Should provide formulation guidance
        assert "concentration" in result.lower() or "%" in result
        assert "pH" in result.lower() or "ph" in result.lower()

    def test_ingredient_comparison(self):
        """Test comparing multiple ingredients in same category."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["retinol", "tretinoin", "adapalene", "bakuchiol"],
            "analysis_depth": "detailed",
        })

        # Should analyze all four
        assert "retinol" in result.lower()
        assert "tretinoin" in result.lower()
        assert "adapalene" in result.lower()
        assert "bakuchiol" in result.lower()

        # Should enable comparison
        assert "evidence" in result.lower()

    def test_interaction_checking(self):
        """Test checking ingredient interactions."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["retinol", "benzoyl peroxide", "vitamin c"],
            "check_interactions": True,
        })

        # Should identify interactions
        assert "interaction" in result.lower()

        # Should note retinol + BP conflict
        assert "benzoyl" in result.lower()

    def test_skin_type_specific_analysis(self):
        """Test ingredient analysis with skin type context."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["salicylic acid", "glycolic acid"],
            "skin_type": "sensitive",
        })

        # Should provide sensitive skin guidance
        assert "sensitive" in result.lower()

    def test_vitamin_c_form_comparison(self):
        """Test comparing vitamin C forms - common Skintellectual research."""
        result = ingredient_analyzer.invoke({
            "ingredients": [
                "ascorbic acid",
                "sodium ascorbyl phosphate",
                "ascorbyl glucoside",
            ],
            "analysis_depth": "comprehensive",
        })

        # Should differentiate the forms
        assert "L-Ascorbic" in result or "ascorbic acid" in result.lower()
        assert "stability" in result.lower()
        assert "pH" in result.lower() or "ph" in result.lower()


class TestJTBD_RoutineBuilding:
    """JTBD: "Build me a skincare routine that actually works"

    User Personas:
    - Beginner starting from scratch
    - Someone with existing routine needing optimization
    - Budget-conscious user wanting effective routine
    """

    def test_beginner_routine_creation(self):
        """Test building routine for complete beginner."""
        result = routine_builder.invoke({
            "skin_type": "normal",
            "primary_concerns": ["prevention", "hydration"],
            "routine_complexity": "basic",
            "budget": "budget",
            "retinoid_experience": "none",
        })

        # Should have AM and PM routines
        assert "AM" in result or "Morning" in result
        assert "PM" in result or "Evening" in result

        # Should include essentials
        assert "cleanser" in result.lower()
        assert "moisturizer" in result.lower()
        assert "SPF" in result or "sunscreen" in result.lower()

        # Should have progression plan for beginner
        assert "week" in result.lower() or "start" in result.lower()

    def test_acne_focused_routine(self):
        """Test building routine for acne-prone skin."""
        result = routine_builder.invoke({
            "skin_type": "oily",
            "primary_concerns": ["acne", "pores", "oiliness"],
            "routine_complexity": "standard",
            "budget": "mid",
            "retinoid_experience": "beginner",
        })

        # Should address acne concerns
        assert "BHA" in result or "salicylic" in result.lower()

        # Should include appropriate actives
        assert "retinoid" in result.lower() or "retinol" in result.lower()
        assert "niacinamide" in result.lower()

    def test_anti_aging_routine(self):
        """Test building anti-aging routine."""
        result = routine_builder.invoke({
            "skin_type": "combination",
            "primary_concerns": ["aging", "fine lines", "dullness"],
            "routine_complexity": "comprehensive",
            "budget": "premium",
            "retinoid_experience": "intermediate",
        })

        # Should include anti-aging actives
        assert "retinoid" in result.lower() or "retinol" in result.lower()
        assert "vitamin c" in result.lower()

        # Should be comprehensive
        assert "serum" in result.lower()

    def test_budget_routine(self):
        """Test building effective budget routine."""
        result = routine_builder.invoke({
            "skin_type": "dry",
            "primary_concerns": ["dehydration", "dullness"],
            "routine_complexity": "basic",
            "budget": "budget",
        })

        # Should include budget recommendations
        assert "CeraVe" in result or "Vanicream" in result or "Cetaphil" in result or "budget" in result.lower()

    def test_minimal_routine(self):
        """Test building minimal routine for busy user."""
        result = routine_builder.invoke({
            "skin_type": "normal",
            "primary_concerns": ["maintenance"],
            "routine_complexity": "minimal",
        })

        # Should be simple
        assert "3" in result or "three" in result.lower() or "minimal" in result.lower()

        # But still complete basics
        assert "cleanser" in result.lower()
        assert "SPF" in result or "sunscreen" in result.lower()


class TestJTBD_TrendValidation:
    """JTBD: "Is this TikTok trend actually safe/effective?"

    User Personas:
    - TikTok user skeptical of viral trends
    - Someone burned by bad advice before
    - Evidence-seeker wanting truth
    """

    def test_validate_good_trend(self):
        """Test validating a trend that actually works."""
        result = trend_evaluator.invoke({
            "trend_name": "skin cycling",
            "source_platform": "tiktok",
        })

        # Should validate it
        assert "VALIDATED" in result or "valid" in result.lower()

        # Should explain why
        assert "evidence" in result.lower()
        assert "rotation" in result.lower() or "schedule" in result.lower()

    def test_debunk_harmful_trend(self):
        """Test identifying harmful trend."""
        result = trend_evaluator.invoke({
            "trend_name": "lemon on face",
            "source_platform": "tiktok",
        })

        # Should warn against it
        assert "HARMFUL" in result or "harmful" in result.lower() or "DANGEROUS" in result

        # Should explain risks
        assert "pH" in result.lower() or "burn" in result.lower() or "irritat" in result.lower()

    def test_evaluate_mixed_trend(self):
        """Test evaluating trend with mixed verdict."""
        result = trend_evaluator.invoke({
            "trend_name": "gua sha",
            "source_platform": "instagram",
        })

        # Should give nuanced verdict
        assert "MIXED" in result or "temporary" in result.lower()

        # Should clarify what's valid vs overpromised
        assert "benefit" in result.lower() or "valid" in result.lower()

    def test_evaluate_dangerous_diy(self):
        """Test flagging dangerous DIY trends."""
        result = trend_evaluator.invoke({
            "trend_name": "diy sunscreen",
            "claims": ["coconut oil provides SPF", "natural protection"],
        })

        # Should strongly warn
        assert "DANGEROUS" in result or "DO NOT" in result or "harmful" in result.lower()

        # Should explain why
        assert "SPF" in result or "protection" in result.lower()

    def test_evaluate_unknown_trend(self):
        """Test evaluating an unknown/new trend."""
        result = trend_evaluator.invoke({
            "trend_name": "new viral trend xyz",
            "trend_description": "Putting xyz ingredient on face overnight",
            "claims": ["clears skin in 3 days", "natural detox"],
        })

        # Should provide evaluation framework
        assert "red flag" in result.lower() or "warning" in result.lower() or "caution" in result.lower()

        # Should flag problematic claims
        assert "detox" in result.lower()


class TestJTBD_DemographicWorkflows:
    """Complete workflows for each target demographic."""

    def test_skintellectual_workflow(self):
        """Test complete Skintellectual research workflow.

        Job: "I want to deeply understand my skincare choices"
        """
        # Step 1: Understand ingredient they're curious about
        ingredient_result = ingredient_analyzer.invoke({
            "ingredients": ["retinol", "tretinoin"],
            "analysis_depth": "comprehensive",
            "check_interactions": True,
        })

        assert "mechanism" in ingredient_result.lower()
        assert "evidence" in ingredient_result.lower()

        # Step 2: Validate trend they heard about
        trend_result = trend_evaluator.invoke({
            "trend_name": "retinol sandwich",
        })

        assert "verdict" in trend_result.lower() or "VALIDATED" in trend_result

        # Step 3: Build optimized routine
        routine_result = routine_builder.invoke({
            "skin_type": "combination",
            "primary_concerns": ["aging", "texture"],
            "routine_complexity": "comprehensive",
            "retinoid_experience": "intermediate",
        })

        assert "retinoid" in routine_result.lower()

    def test_problem_skin_workflow(self):
        """Test Problem-Skin Sufferer workflow.

        Job: "Help me fix my [acne/rosacea/etc]"
        """
        # Step 1: Assess their skin situation
        profile_result = skin_profile_assessment.invoke({
            "age": 24,
            "skin_type": "oily",
            "primary_concerns": ["acne", "post-acne marks"],
            "secondary_concerns": ["oiliness", "pores"],
        })

        assert "acne" in profile_result.lower()

        # Step 2: Understand acne-fighting ingredients
        ingredient_result = ingredient_analyzer.invoke({
            "ingredients": ["salicylic acid", "benzoyl peroxide", "niacinamide", "adapalene"],
            "skin_type": "oily",
        })

        assert "acne" in ingredient_result.lower() or "pores" in ingredient_result.lower()

        # Step 3: Build targeted routine
        routine_result = routine_builder.invoke({
            "skin_type": "oily",
            "primary_concerns": ["acne", "post-acne marks"],
            "routine_complexity": "standard",
            "budget": "mid",
        })

        assert "BHA" in routine_result or "salicylic" in routine_result.lower()

    def test_preventive_ager_workflow(self):
        """Test Preventive Ager workflow.

        Job: "Help me prevent aging before it starts"
        """
        # Step 1: Profile assessment
        profile_result = skin_profile_assessment.invoke({
            "age": 28,
            "skin_type": "normal",
            "primary_concerns": ["prevention", "maintaining skin health"],
        })

        assert "prevention" in profile_result.lower() or "Prime" in profile_result

        # Step 2: Research anti-aging ingredients
        ingredient_result = ingredient_analyzer.invoke({
            "ingredients": ["vitamin c", "retinol", "niacinamide", "peptides"],
        })

        assert "collagen" in ingredient_result.lower() or "antioxidant" in ingredient_result.lower()

        # Step 3: Build prevention-focused routine
        routine_result = routine_builder.invoke({
            "skin_type": "normal",
            "primary_concerns": ["aging", "prevention"],
            "routine_complexity": "standard",
            "retinoid_experience": "beginner",
        })

        assert "vitamin c" in routine_result.lower()
        assert "retinoid" in routine_result.lower() or "retinol" in routine_result.lower()

    def test_budget_hunter_workflow(self):
        """Test Budget Hunter workflow.

        Job: "Help me get effective skincare without breaking the bank"
        """
        # Step 1: Profile with budget constraint
        profile_result = skin_profile_assessment.invoke({
            "age": 32,
            "skin_type": "combination",
            "primary_concerns": ["dullness", "texture"],
            "budget_level": "budget",
        })

        assert "budget" in profile_result.lower()

        # Step 2: Build budget routine
        routine_result = routine_builder.invoke({
            "skin_type": "combination",
            "primary_concerns": ["dullness", "texture"],
            "routine_complexity": "basic",
            "budget": "budget",
        })

        # Should recommend affordable options
        assert "CeraVe" in routine_result or "Ordinary" in routine_result or "budget" in routine_result.lower()

        # Step 3: Validate they don't need expensive products
        trend_result = trend_evaluator.invoke({
            "trend_name": "expensive products aren't necessary",
        })

        # Should get evaluation
        assert len(trend_result) > 100


class TestJTBD_EdgeCases:
    """Edge cases and boundary conditions."""

    def test_very_young_user(self):
        """Test recommendations for teenage user."""
        profile_result = skin_profile_assessment.invoke({
            "age": 15,
            "skin_type": "oily",
            "primary_concerns": ["acne"],
        })

        assert "teen" in profile_result.lower()

    def test_mature_user(self):
        """Test recommendations for mature user."""
        profile_result = skin_profile_assessment.invoke({
            "age": 65,
            "skin_type": "dry",
            "primary_concerns": ["dryness", "aging"],
        })

        assert "mature" in profile_result.lower()

    def test_multiple_sensitivities(self):
        """Test user with many sensitivities."""
        profile_result = skin_profile_assessment.invoke({
            "age": 40,
            "skin_type": "sensitive",
            "primary_concerns": ["redness"],
            "known_sensitivities": [
                "fragrance",
                "essential oils",
                "alcohol",
                "retinoids",
                "vitamin c",
            ],
        })

        assert "sensitive" in profile_result.lower()
        assert "caution" in profile_result.lower() or "patch" in profile_result.lower()

    def test_conflicting_concerns(self):
        """Test user with seemingly conflicting concerns."""
        routine_result = routine_builder.invoke({
            "skin_type": "oily",
            "primary_concerns": ["acne", "dryness"],  # Can coexist as dehydrated oily
        })

        # Should handle this gracefully
        assert "routine" in routine_result.lower() or "Routine" in routine_result

    def test_all_concerns_at_once(self):
        """Test user with many concerns."""
        profile_result = skin_profile_assessment.invoke({
            "age": 35,
            "skin_type": "combination",
            "primary_concerns": [
                "acne",
                "aging",
                "hyperpigmentation",
                "texture",
                "redness",
            ],
        })

        # Should still provide useful guidance
        assert len(profile_result) > 500
        assert "priority" in profile_result.lower() or "primary" in profile_result.lower()
