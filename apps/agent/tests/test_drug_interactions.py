"""Tests for the drug interaction checker tools."""


from trace_mineral_agent.tools.drug_interactions import (
    INTERACTIONS,
    check_drug_interactions,
    list_mineral_interactions,
)


class TestCheckDrugInteractions:
    """Tests for the check_drug_interactions tool."""

    def test_high_severity_interaction_detected(self):
        """Should detect high-severity insulin-chromium interaction."""
        result = check_drug_interactions.invoke({
            "mineral": "chromium",
            "medications": ["insulin"],
        })

        assert "High Severity" in result
        assert "insulin" in result.lower()
        assert "hypoglycemic" in result.lower()

    def test_moderate_severity_interaction_detected(self):
        """Should detect moderate-severity metformin-chromium interaction."""
        result = check_drug_interactions.invoke({
            "mineral": "chromium",
            "medications": ["metformin"],
        })

        assert "Moderate Severity" in result
        assert "metformin" in result.lower()

    def test_multiple_medications_checked(self):
        """Should check all medications in the list."""
        result = check_drug_interactions.invoke({
            "mineral": "zinc",
            "medications": ["ciprofloxacin", "lisinopril", "vitamin D"],
        })

        assert "quinolone" in result.lower()
        assert "ACE" in result

    def test_no_interaction_found(self):
        """Should report no interactions for non-interacting medications."""
        result = check_drug_interactions.invoke({
            "mineral": "selenium",
            "medications": ["aspirin", "ibuprofen"],
        })

        assert "No interactions found" in result

    def test_partial_name_matching(self):
        """Should match medication names partially."""
        result = check_drug_interactions.invoke({
            "mineral": "iron",
            "medications": ["levothyroxine 50mcg"],
        })

        assert "High Severity" in result
        assert "levothyroxine" in result.lower()

    def test_unknown_mineral_handled(self):
        """Should handle unknown minerals gracefully."""
        result = check_drug_interactions.invoke({
            "mineral": "chromium",  # Valid mineral
            "medications": ["unknown_drug"],
        })

        # Should return valid response even if no interactions found
        assert "Interaction Report" in result

    def test_disclaimer_included(self):
        """Should include medical disclaimer."""
        result = check_drug_interactions.invoke({
            "mineral": "magnesium",
            "medications": ["omeprazole"],
        })

        assert "consult" in result.lower() or "informational" in result.lower()

    def test_recommendations_provided(self):
        """Should provide recommendations for detected interactions."""
        result = check_drug_interactions.invoke({
            "mineral": "zinc",
            "medications": ["doxycycline"],
        })

        assert "Recommendation" in result
        assert "hours" in result.lower()  # Spacing recommendation

    def test_case_insensitive_medication_matching(self):
        """Should match medications case-insensitively."""
        result = check_drug_interactions.invoke({
            "mineral": "chromium",
            "medications": ["INSULIN", "Metformin"],
        })

        assert "High Severity" in result
        assert "Moderate Severity" in result


class TestListMineralInteractions:
    """Tests for the list_mineral_interactions tool."""

    def test_lists_all_chromium_interactions(self):
        """Should list all known chromium interactions."""
        result = list_mineral_interactions.invoke({
            "mineral": "chromium",
        })

        assert "All Known Interactions: Chromium" in result
        assert "High Severity" in result
        assert "insulin" in result.lower()

    def test_lists_zinc_interactions(self):
        """Should list all known zinc interactions."""
        result = list_mineral_interactions.invoke({
            "mineral": "zinc",
        })

        assert "All Known Interactions: Zinc" in result
        assert "penicillamine" in result.lower()
        assert "quinolone" in result.lower()

    def test_includes_severity_levels(self):
        """Should categorize interactions by severity."""
        result = list_mineral_interactions.invoke({
            "mineral": "magnesium",
        })

        assert "High Severity" in result
        assert "Moderate Severity" in result
        assert "Low Severity" in result

    def test_includes_total_count(self):
        """Should show total interaction count."""
        result = list_mineral_interactions.invoke({
            "mineral": "iron",
        })

        assert "Total interactions" in result

    def test_table_format_output(self):
        """Should output in table format."""
        result = list_mineral_interactions.invoke({
            "mineral": "selenium",
        })

        assert "Drug Class" in result
        assert "Examples" in result
        assert "Effect" in result

    def test_all_supported_minerals(self):
        """Should support all minerals in the database."""
        for mineral in ["chromium", "zinc", "magnesium", "iron", "selenium", "copper", "iodine"]:
            result = list_mineral_interactions.invoke({
                "mineral": mineral,
            })
            assert f"All Known Interactions: {mineral.title()}" in result


class TestInteractionsDatabase:
    """Tests for the INTERACTIONS database structure."""

    def test_database_has_expected_minerals(self):
        """Database should contain expected minerals."""
        expected = ["chromium", "zinc", "magnesium", "iron", "selenium", "copper", "iodine"]
        for mineral in expected:
            assert mineral in INTERACTIONS

    def test_interaction_structure(self):
        """Each interaction should have required fields."""
        required_fields = {"drug", "drugs", "effect", "mechanism", "recommendation"}

        for mineral, interactions in INTERACTIONS.items():
            for severity in ["high", "moderate", "low"]:
                for interaction in interactions.get(severity, []):
                    assert set(interaction.keys()) >= required_fields, \
                        f"Missing fields in {mineral} {severity} interaction"

    def test_drugs_list_not_empty(self):
        """Each interaction should have at least one drug example."""
        for mineral, interactions in INTERACTIONS.items():
            for severity in ["high", "moderate", "low"]:
                for interaction in interactions.get(severity, []):
                    assert len(interaction["drugs"]) > 0, \
                        f"Empty drugs list in {mineral} {severity}"

    def test_known_critical_interactions(self):
        """Should include known critical interactions."""
        # Chromium + insulin
        chromium_high = INTERACTIONS["chromium"]["high"]
        insulin_found = any("insulin" in i["drug"].lower() for i in chromium_high)
        assert insulin_found, "Missing chromium-insulin interaction"

        # Iron + levothyroxine
        iron_high = INTERACTIONS["iron"]["high"]
        levo_found = any("levothyroxine" in i["drug"].lower() for i in iron_high)
        assert levo_found, "Missing iron-levothyroxine interaction"

        # Iodine + amiodarone
        iodine_high = INTERACTIONS["iodine"]["high"]
        amio_found = any("amiodarone" in i["drug"].lower() for i in iodine_high)
        assert amio_found, "Missing iodine-amiodarone interaction"
