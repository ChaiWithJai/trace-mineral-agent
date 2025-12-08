"""Unit tests for skincare tools."""

import pytest

from trace_mineral_agent.skincare.tools import (
    ingredient_analyzer,
    routine_builder,
    skin_profile_assessment,
    trend_evaluator,
)


class TestSkinProfileAssessment:
    """Tests for the skin_profile_assessment tool."""

    def test_basic_profile_generation(self):
        """Test basic skin profile generation."""
        result = skin_profile_assessment.invoke({
            "age": 28,
            "skin_type": "combination",
            "primary_concerns": ["acne", "hyperpigmentation"],
        })

        assert isinstance(result, str)
        assert "Skin Profile Assessment" in result
        assert "combination" in result.lower()
        assert "28" in result

    def test_all_skin_types_supported(self):
        """Test that all skin types are handled."""
        skin_types = ["oily", "dry", "combination", "normal", "sensitive"]

        for skin_type in skin_types:
            result = skin_profile_assessment.invoke({
                "age": 30,
                "skin_type": skin_type,
                "primary_concerns": ["aging"],
            })
            assert skin_type in result.lower()

    def test_life_stages_by_age(self):
        """Test life stage determination by age."""
        test_cases = [
            (18, "Teen"),
            (23, "Young Adult"),
            (32, "Prime"),
            (42, "Maintenance"),
            (50, "Transition"),
            (60, "Mature"),
        ]

        for age, expected_stage in test_cases:
            result = skin_profile_assessment.invoke({
                "age": age,
                "skin_type": "normal",
                "primary_concerns": ["dryness"],
            })
            assert expected_stage.lower() in result.lower(), f"Expected {expected_stage} for age {age}"

    def test_concern_analysis(self):
        """Test that primary concerns are analyzed."""
        result = skin_profile_assessment.invoke({
            "age": 25,
            "skin_type": "oily",
            "primary_concerns": ["acne", "pores", "texture"],
        })

        assert "acne" in result.lower()
        assert "pores" in result.lower()
        assert "texture" in result.lower()

    def test_budget_guidance(self):
        """Test budget level guidance."""
        for budget in ["budget", "mid-range", "premium", "luxury"]:
            result = skin_profile_assessment.invoke({
                "age": 30,
                "skin_type": "normal",
                "primary_concerns": ["aging"],
                "budget_level": budget,
            })
            assert "Budget" in result or "budget" in result.lower()

    def test_sensitivity_profile(self):
        """Test sensitivity profile generation."""
        result = skin_profile_assessment.invoke({
            "age": 35,
            "skin_type": "sensitive",
            "primary_concerns": ["redness"],
            "known_sensitivities": ["fragrance", "essential oils"],
        })

        assert "fragrance" in result.lower() or "sensitivity" in result.lower()

    def test_routine_complexity_recommendation(self):
        """Test routine complexity recommendations."""
        # Minimal time
        result_minimal = skin_profile_assessment.invoke({
            "age": 30,
            "skin_type": "normal",
            "primary_concerns": ["dryness"],
            "time_available_minutes": 5,
        })
        assert "step" in result_minimal.lower()

        # More time available
        result_full = skin_profile_assessment.invoke({
            "age": 30,
            "skin_type": "normal",
            "primary_concerns": ["dryness"],
            "time_available_minutes": 20,
        })
        assert "step" in result_full.lower()

    def test_climate_consideration(self):
        """Test climate factor consideration."""
        for climate in ["humid", "dry", "temperate", "variable"]:
            result = skin_profile_assessment.invoke({
                "age": 30,
                "skin_type": "dry",
                "primary_concerns": ["dehydration"],
                "climate": climate,
            })
            assert climate in result.lower()

    def test_lifestyle_analysis(self):
        """Test lifestyle factors analysis."""
        result = skin_profile_assessment.invoke({
            "age": 30,
            "skin_type": "combination",
            "primary_concerns": ["acne"],
            "lifestyle_factors": {
                "sleep_hours": 5,
                "water_glasses": 4,
                "stress_level": "high",
            },
        })

        # Should include lifestyle recommendations
        assert "sleep" in result.lower() or "lifestyle" in result.lower()


class TestIngredientAnalyzer:
    """Tests for the ingredient_analyzer tool."""

    def test_single_known_ingredient(self):
        """Test analysis of a single known ingredient."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["retinol"],
        })

        assert isinstance(result, str)
        assert "retinol" in result.lower()
        assert "mechanism" in result.lower()
        assert "evidence" in result.lower()

    def test_multiple_ingredients(self):
        """Test analysis of multiple ingredients."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["retinol", "niacinamide", "hyaluronic acid"],
        })

        assert "retinol" in result.lower()
        assert "niacinamide" in result.lower()
        assert "hyaluronic" in result.lower()

    def test_interaction_analysis(self):
        """Test ingredient interaction checking."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["retinol", "vitamin c"],
            "check_interactions": True,
        })

        assert "interaction" in result.lower()

    def test_unknown_ingredient_handling(self):
        """Test handling of unknown ingredients."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["unknownxyz123"],
        })

        assert "not found" in result.lower() or "unknown" in result.lower()

    def test_evidence_grades_present(self):
        """Test that evidence grades are included."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["tretinoin"],
            "analysis_depth": "detailed",
        })

        # Should include evidence grade
        assert "A" in result or "evidence" in result.lower()

    def test_vitamin_c_forms(self):
        """Test recognition of vitamin C forms."""
        forms = ["ascorbic acid", "vitamin c", "SAP", "sodium ascorbyl phosphate"]

        for form in forms:
            result = ingredient_analyzer.invoke({
                "ingredients": [form],
            })
            assert "vitamin" in result.lower() or "ascorb" in result.lower()

    def test_retinoid_family(self):
        """Test recognition of retinoid family."""
        retinoids = ["retinol", "tretinoin", "adapalene", "retinal", "bakuchiol"]

        for retinoid in retinoids:
            result = ingredient_analyzer.invoke({
                "ingredients": [retinoid],
            })
            assert "retin" in result.lower() or "bakuchiol" in result.lower()

    def test_analysis_depth_levels(self):
        """Test different analysis depth levels."""
        for depth in ["quick", "detailed", "comprehensive"]:
            result = ingredient_analyzer.invoke({
                "ingredients": ["niacinamide"],
                "analysis_depth": depth,
            })
            assert "niacinamide" in result.lower()

    def test_skin_type_notes(self):
        """Test skin type specific notes."""
        result = ingredient_analyzer.invoke({
            "ingredients": ["salicylic acid"],
            "skin_type": "oily",
        })

        assert "oily" in result.lower()


class TestRoutineBuilder:
    """Tests for the routine_builder tool."""

    def test_basic_routine_generation(self):
        """Test basic routine generation."""
        result = routine_builder.invoke({
            "skin_type": "combination",
            "primary_concerns": ["acne"],
        })

        assert isinstance(result, str)
        assert "AM" in result or "Morning" in result
        assert "PM" in result or "Evening" in result

    def test_all_skin_types(self):
        """Test routine generation for all skin types."""
        for skin_type in ["oily", "dry", "combination", "normal", "sensitive"]:
            result = routine_builder.invoke({
                "skin_type": skin_type,
                "primary_concerns": ["aging"],
            })
            assert "cleanser" in result.lower() or "Cleanser" in result

    def test_complexity_levels(self):
        """Test different complexity levels."""
        for complexity in ["minimal", "basic", "standard", "comprehensive"]:
            result = routine_builder.invoke({
                "skin_type": "normal",
                "primary_concerns": ["dryness"],
                "routine_complexity": complexity,
            })
            assert "Routine" in result or "routine" in result.lower()

    def test_sunscreen_always_included(self):
        """Test that sunscreen is always included in AM routine."""
        result = routine_builder.invoke({
            "skin_type": "oily",
            "primary_concerns": ["acne"],
        })

        assert "sunscreen" in result.lower() or "SPF" in result

    def test_retinoid_levels(self):
        """Test retinoid experience levels."""
        for level in ["none", "beginner", "intermediate", "advanced"]:
            result = routine_builder.invoke({
                "skin_type": "normal",
                "primary_concerns": ["aging"],
                "retinoid_experience": level,
            })
            assert "retinoid" in result.lower() or "retinol" in result.lower()

    def test_budget_recommendations(self):
        """Test budget-based product recommendations."""
        for budget in ["budget", "mid", "premium"]:
            result = routine_builder.invoke({
                "skin_type": "dry",
                "primary_concerns": ["dehydration"],
                "budget": budget,
            })
            assert "budget" in result.lower() or "Budget" in result

    def test_weekly_schedule_included(self):
        """Test that weekly active schedule is included."""
        result = routine_builder.invoke({
            "skin_type": "normal",
            "primary_concerns": ["texture"],
            "routine_complexity": "standard",
        })

        assert "monday" in result.lower() or "weekly" in result.lower() or "schedule" in result.lower()

    def test_layering_order(self):
        """Test that layering order information is included."""
        result = routine_builder.invoke({
            "skin_type": "combination",
            "primary_concerns": ["aging"],
        })

        # Should mention layering or step order
        assert "step" in result.lower() or "layer" in result.lower() or "order" in result.lower()


class TestTrendEvaluator:
    """Tests for the trend_evaluator tool."""

    def test_known_validated_trend(self):
        """Test evaluation of a known validated trend."""
        result = trend_evaluator.invoke({
            "trend_name": "slugging",
        })

        assert isinstance(result, str)
        assert "slugging" in result.lower()
        assert "VALIDATED" in result or "validated" in result.lower()

    def test_known_harmful_trend(self):
        """Test evaluation of a known harmful trend."""
        result = trend_evaluator.invoke({
            "trend_name": "lemon on face",
        })

        assert "HARMFUL" in result or "harmful" in result.lower() or "DANGEROUS" in result

    def test_known_mixed_trend(self):
        """Test evaluation of a mixed verdict trend."""
        result = trend_evaluator.invoke({
            "trend_name": "ice rolling",
        })

        assert "MIXED" in result or "mixed" in result.lower()

    def test_unknown_trend(self):
        """Test evaluation framework for unknown trends."""
        result = trend_evaluator.invoke({
            "trend_name": "unknown trend xyz",
            "trend_description": "Rubbing xyz on face for glow",
        })

        assert "unknown" in result.lower() or "red flag" in result.lower() or "framework" in result.lower()

    def test_alias_recognition(self):
        """Test recognition of trend aliases."""
        aliases = {
            "vaseline slug": "slugging",
            "skin cycle": "skin_cycling",
            "double cleanse": "double_cleansing",
        }

        for alias, expected in aliases.items():
            result = trend_evaluator.invoke({
                "trend_name": alias,
            })
            # Should recognize and analyze the trend
            assert "verdict" in result.lower() or "Verdict" in result

    def test_evidence_grade_included(self):
        """Test that evidence grades are included."""
        result = trend_evaluator.invoke({
            "trend_name": "skin cycling",
        })

        assert "evidence" in result.lower()

    def test_risk_assessment(self):
        """Test that risks are assessed."""
        result = trend_evaluator.invoke({
            "trend_name": "diy sunscreen",
        })

        assert "risk" in result.lower() or "DANGEROUS" in result

    def test_claim_evaluation(self):
        """Test specific claim evaluation."""
        result = trend_evaluator.invoke({
            "trend_name": "pore treatment",
            "claims": ["shrinks pores permanently", "detoxes skin"],
        })

        # Should flag these false claims
        assert "pore" in result.lower()

    def test_source_platform_noted(self):
        """Test that source platform is noted."""
        result = trend_evaluator.invoke({
            "trend_name": "slugging",
            "source_platform": "tiktok",
        })

        assert "tiktok" in result.lower() or "TikTok" in result


class TestToolIntegration:
    """Integration tests for skincare tools working together."""

    def test_profile_to_routine_workflow(self):
        """Test workflow from profile assessment to routine building."""
        # First, create a profile
        profile_result = skin_profile_assessment.invoke({
            "age": 28,
            "skin_type": "oily",
            "primary_concerns": ["acne", "hyperpigmentation"],
            "budget_level": "mid-range",
        })

        assert "oily" in profile_result.lower()

        # Then build a routine based on similar inputs
        routine_result = routine_builder.invoke({
            "skin_type": "oily",
            "primary_concerns": ["acne", "hyperpigmentation"],
            "budget": "mid",
        })

        assert "routine" in routine_result.lower() or "Routine" in routine_result

    def test_ingredient_analysis_informs_routine(self):
        """Test that ingredient analysis aligns with routine recommendations."""
        # Analyze key acne ingredients
        ingredient_result = ingredient_analyzer.invoke({
            "ingredients": ["salicylic acid", "niacinamide", "benzoyl peroxide"],
            "skin_type": "oily",
        })

        assert "salicylic" in ingredient_result.lower()

        # Build routine for acne
        routine_result = routine_builder.invoke({
            "skin_type": "oily",
            "primary_concerns": ["acne"],
        })

        # Routine should reference similar ingredients/categories
        assert "BHA" in routine_result or "salicylic" in routine_result.lower() or "exfoliant" in routine_result.lower()

    def test_trend_validation_consistency(self):
        """Test that trend verdicts are consistent across similar trends."""
        # Both should be validated
        slugging = trend_evaluator.invoke({"trend_name": "slugging"})
        skin_cycling = trend_evaluator.invoke({"trend_name": "skin cycling"})

        assert "VALIDATED" in slugging or "validated" in slugging.lower()
        assert "VALIDATED" in skin_cycling or "validated" in skin_cycling.lower()

        # Both should be harmful
        lemon = trend_evaluator.invoke({"trend_name": "lemon on face"})
        diy_spf = trend_evaluator.invoke({"trend_name": "diy sunscreen"})

        assert "HARMFUL" in lemon or "DANGEROUS" in lemon
        assert "DANGEROUS" in diy_spf or "harmful" in diy_spf.lower()
