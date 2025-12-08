"""Ingredient analyzer tool for deep skincare ingredient analysis.

Designed for Skintellectuals who want mechanism-of-action understanding,
evidence grades, optimal formulation parameters, and interaction warnings.
"""

from typing import Literal

from langchain_core.tools import tool


# Comprehensive ingredient database with scientific depth
INGREDIENT_DATABASE: dict[str, dict] = {
    # RETINOIDS
    "retinol": {
        "category": "Retinoid",
        "inci_name": "Retinol",
        "mechanism": "Binds to retinoic acid receptors (RAR/RXR) after conversion to retinoic acid via retinol dehydrogenase and retinal dehydrogenase. Upregulates collagen I, III, and VII synthesis; increases epidermal turnover; normalizes keratinization; inhibits MMP activity.",
        "conversion_pathway": "Retinol → Retinal → Retinoic Acid (all-trans)",
        "efficacy_vs_tretinoin": "~20x less potent than tretinoin; requires enzymatic conversion",
        "evidence_grade": "A",
        "evidence_summary": "Strong evidence for photoaging, fine lines, hyperpigmentation. Multiple RCTs demonstrate efficacy at 0.25-1%.",
        "optimal_concentration": "0.25-1% (start low, titrate up)",
        "optimal_ph": "5.5-6.5 (stable in slightly acidic to neutral)",
        "stability_concerns": ["Light-sensitive", "Oxygen-sensitive", "Heat-sensitive", "Degrades to less active forms"],
        "encapsulation_benefits": "Encapsulated retinol improves stability and may reduce irritation",
        "best_forms": ["Encapsulated retinol", "Retinol in anhydrous formula", "Airless pump packaging"],
        "time_to_results": "8-12 weeks for visible improvement; 6+ months for collagen effects",
        "side_effects": ["Irritation", "Dryness", "Peeling", "Photosensitivity", "Purging"],
        "contraindications": ["Pregnancy", "Breastfeeding", "Concurrent isotretinoin"],
        "works_well_with": ["Hyaluronic acid", "Niacinamide", "Ceramides", "Peptides"],
        "avoid_combining": ["Benzoyl peroxide (can oxidize)", "AHAs/BHAs (same routine - too irritating)", "Vitamin C (pH conflict, use separately)"],
        "application_tips": "Apply to dry skin, wait 20min post-cleansing if sensitive. Start 2-3x/week, build to nightly.",
    },
    "tretinoin": {
        "category": "Retinoid (Rx)",
        "inci_name": "Retinoic Acid / Tretinoin",
        "mechanism": "Direct binding to RAR/RXR receptors without conversion. Gold standard for photoaging. Increases collagen synthesis, accelerates cell turnover, reduces hyperpigmentation.",
        "conversion_pathway": "None - already active form",
        "efficacy_vs_tretinoin": "Reference standard (1x)",
        "evidence_grade": "A+",
        "evidence_summary": "Decades of research. Gold standard for photoaging, acne, hyperpigmentation. FDA-approved.",
        "optimal_concentration": "0.025% (start), 0.05% (standard), 0.1% (max)",
        "optimal_ph": "4.0-6.0",
        "stability_concerns": ["Extremely light-sensitive", "Oxidizes readily", "Must be in opaque packaging"],
        "best_forms": ["Micronized tretinoin", "Microsphere formulations (Retin-A Micro)"],
        "time_to_results": "4-6 weeks for acne; 3-6 months for anti-aging",
        "side_effects": ["Significant irritation initially", "Dryness", "Peeling", "Photosensitivity"],
        "contraindications": ["Pregnancy (Category C)", "Breastfeeding", "Eczema on face"],
        "works_well_with": ["Hyaluronic acid", "Ceramides", "Niacinamide (buffer)"],
        "avoid_combining": ["Benzoyl peroxide", "AHAs/BHAs", "Other retinoids"],
        "application_tips": "Pea-sized amount for whole face. 'Sandwich' method with moisturizer if irritated.",
    },
    "adapalene": {
        "category": "Retinoid",
        "inci_name": "Adapalene",
        "mechanism": "Selective RAR-β and RAR-γ agonist. More selective than tretinoin = better tolerability. Normalizes follicular keratinization, anti-inflammatory.",
        "conversion_pathway": "None - synthetic retinoid, directly active",
        "efficacy_vs_tretinoin": "Comparable for acne; slightly less for photoaging",
        "evidence_grade": "A",
        "evidence_summary": "Strong evidence for acne. FDA-approved OTC at 0.1%. Better tolerated than tretinoin.",
        "optimal_concentration": "0.1% (OTC), 0.3% (Rx)",
        "optimal_ph": "Stable across wide pH range (more stable than tretinoin)",
        "stability_concerns": ["More photostable than tretinoin", "Still recommend PM use"],
        "best_forms": ["Gel formulation", "Cream for dry skin"],
        "time_to_results": "8-12 weeks for acne improvement",
        "side_effects": ["Milder than tretinoin", "Some dryness", "Peeling"],
        "contraindications": ["Pregnancy", "Breastfeeding"],
        "works_well_with": ["Benzoyl peroxide (Epiduo)", "Niacinamide", "Ceramides"],
        "avoid_combining": ["Other retinoids"],
        "application_tips": "Can be used with benzoyl peroxide (unlike other retinoids). Good starter retinoid.",
    },
    "retinal": {
        "category": "Retinoid",
        "inci_name": "Retinaldehyde / Retinal",
        "mechanism": "One conversion step from retinoic acid (vs two for retinol). Binds RAR after conversion. Also has direct antibacterial properties.",
        "conversion_pathway": "Retinal → Retinoic Acid (one step)",
        "efficacy_vs_tretinoin": "~10x less potent than tretinoin; ~10x more potent than retinol",
        "evidence_grade": "A-",
        "evidence_summary": "Good evidence, fewer studies than retinol. Faster results than retinol with better tolerability.",
        "optimal_concentration": "0.05-0.1%",
        "optimal_ph": "5.5-6.5",
        "stability_concerns": ["Light-sensitive", "More stable than retinol", "Yellow color indicates active form"],
        "best_forms": ["Encapsulated", "Airless packaging"],
        "time_to_results": "4-8 weeks (faster than retinol)",
        "side_effects": ["Less irritating than tretinoin", "Some adjustment period"],
        "contraindications": ["Pregnancy", "Breastfeeding"],
        "works_well_with": ["Hyaluronic acid", "Niacinamide", "Peptides"],
        "avoid_combining": ["AHAs/BHAs (same routine)", "Vitamin C (separate routines)"],
        "application_tips": "Good middle ground between retinol and tretinoin.",
    },
    "bakuchiol": {
        "category": "Retinoid Alternative",
        "inci_name": "Bakuchiol",
        "mechanism": "Plant-derived (Psoralea corylifolia). Functionally similar to retinol via different mechanism - upregulates collagen without RAR binding. Antioxidant and anti-inflammatory.",
        "conversion_pathway": "None - not a true retinoid",
        "efficacy_vs_tretinoin": "One study showed comparable results to 0.5% retinol at 0.5% bakuchiol",
        "evidence_grade": "B",
        "evidence_summary": "Promising but limited studies. One key RCT vs retinol. Good option for retinoid-intolerant.",
        "optimal_concentration": "0.5-2%",
        "optimal_ph": "Stable across wide pH range",
        "stability_concerns": ["More stable than retinoids", "Not light-sensitive"],
        "best_forms": ["Any - very stable"],
        "time_to_results": "12+ weeks",
        "side_effects": ["Generally well-tolerated", "Safe in pregnancy (limited data)"],
        "contraindications": ["None known"],
        "works_well_with": ["Can be combined with almost anything", "Vitamin C", "AHAs", "Niacinamide"],
        "avoid_combining": ["None - very compatible"],
        "application_tips": "Good alternative during pregnancy or for very sensitive skin. Can use AM or PM.",
    },

    # VITAMIN C
    "ascorbic_acid": {
        "category": "Antioxidant / Brightening",
        "inci_name": "L-Ascorbic Acid",
        "mechanism": "Potent antioxidant neutralizing ROS. Inhibits tyrosinase (melanin production). Essential cofactor for collagen synthesis (prolyl and lysyl hydroxylase). Regenerates vitamin E.",
        "evidence_grade": "A",
        "evidence_summary": "Extensive evidence for photoprotection, brightening, collagen synthesis. Most studied form of vitamin C.",
        "optimal_concentration": "10-20% (diminishing returns above 20%)",
        "optimal_ph": "2.5-3.5 (CRITICAL - must be acidic for penetration)",
        "stability_concerns": ["Extremely unstable", "Oxidizes to dehydroascorbic acid (yellow/brown)", "Light, air, heat, water all degrade it"],
        "best_forms": ["Anhydrous formulas", "Ferulic acid + vitamin E combo (stabilizing)", "Fresh or well-preserved"],
        "formulation_gold_standard": "15-20% L-AA + 1% Vitamin E + 0.5% Ferulic Acid (Skinceuticals patent)",
        "time_to_results": "4-12 weeks for brightening; ongoing for protection",
        "side_effects": ["Tingling/stinging (normal at low pH)", "Irritation if oxidized", "Can cause breakouts in some"],
        "contraindications": ["None absolute", "Caution with very sensitive skin"],
        "works_well_with": ["Vitamin E (synergistic)", "Ferulic acid (stabilizing + synergistic)", "Sunscreen (enhanced protection)"],
        "avoid_combining": ["Niacinamide (old myth - actually fine)", "High pH products immediately after", "Benzoyl peroxide (oxidizes it)"],
        "application_tips": "AM use for antioxidant protection. Apply to clean, dry skin. Wait before layering.",
    },
    "sodium_ascorbyl_phosphate": {
        "category": "Antioxidant / Brightening",
        "inci_name": "Sodium Ascorbyl Phosphate (SAP)",
        "mechanism": "Stable vitamin C derivative. Converted to ascorbic acid by phosphatases in skin. Also has antibacterial properties against P. acnes.",
        "evidence_grade": "B+",
        "evidence_summary": "Good evidence for brightening and acne. More stable than L-AA. May be less potent.",
        "optimal_concentration": "5-10%",
        "optimal_ph": "6-7 (stable at neutral pH)",
        "stability_concerns": ["Much more stable than L-AA", "Water-soluble"],
        "best_forms": ["Water-based serums"],
        "time_to_results": "8-12 weeks",
        "side_effects": ["Generally well-tolerated", "Less irritating than L-AA"],
        "contraindications": ["None known"],
        "works_well_with": ["Most ingredients", "Niacinamide", "Retinoids"],
        "avoid_combining": ["None specific"],
        "application_tips": "Good alternative if L-AA is too irritating. Works at skin-friendly pH.",
    },
    "ascorbyl_glucoside": {
        "category": "Antioxidant / Brightening",
        "inci_name": "Ascorbyl Glucoside",
        "mechanism": "Glucose-bound vitamin C derivative. Released by glucosidase enzymes in skin. Very stable.",
        "evidence_grade": "B",
        "evidence_summary": "Moderate evidence. Very stable but conversion to active form is slow and incomplete.",
        "optimal_concentration": "2-5%",
        "optimal_ph": "5-7 (very stable)",
        "stability_concerns": ["Excellent stability", "Can be formulated at higher pH"],
        "best_forms": ["Water-based serums", "Creams"],
        "time_to_results": "12+ weeks",
        "side_effects": ["Very well-tolerated"],
        "contraindications": ["None known"],
        "works_well_with": ["Everything"],
        "avoid_combining": ["None"],
        "application_tips": "Good for sensitive skin. Less potent but very gentle.",
    },
    "ethyl_ascorbic_acid": {
        "category": "Antioxidant / Brightening",
        "inci_name": "3-O-Ethyl Ascorbic Acid",
        "mechanism": "Oil-soluble vitamin C derivative with good stability and penetration. Converts to L-AA in skin.",
        "evidence_grade": "B+",
        "evidence_summary": "Good evidence for stability and efficacy. Penetrates better than water-soluble derivatives.",
        "optimal_concentration": "1-3%",
        "optimal_ph": "4-6",
        "stability_concerns": ["Good stability", "Better than L-AA"],
        "best_forms": ["Serums", "Can be in oil-based formulas"],
        "time_to_results": "8-12 weeks",
        "side_effects": ["Generally well-tolerated"],
        "contraindications": ["None known"],
        "works_well_with": ["Most ingredients"],
        "avoid_combining": ["None specific"],
        "application_tips": "Good middle ground - more stable than L-AA with good efficacy.",
    },

    # NIACINAMIDE
    "niacinamide": {
        "category": "Multi-functional",
        "inci_name": "Niacinamide (Nicotinamide, Vitamin B3)",
        "mechanism": "Precursor to NAD+/NADP+. Reduces melanin transfer to keratinocytes. Increases ceramide synthesis. Anti-inflammatory (inhibits NF-κB). Reduces sebum production. Improves barrier function.",
        "evidence_grade": "A",
        "evidence_summary": "Extensive evidence for multiple benefits: brightening, anti-aging, acne, rosacea, barrier support.",
        "optimal_concentration": "2-5% (sweet spot); up to 10% (may increase irritation without added benefit)",
        "optimal_ph": "5-7 (very stable across pH range)",
        "stability_concerns": ["Very stable", "Heat-stable", "pH-stable"],
        "best_forms": ["Water-based serums", "Can be in any formula type"],
        "time_to_results": "4-8 weeks for visible benefits",
        "side_effects": ["Generally excellent tolerability", "High concentrations (>10%) may cause flushing"],
        "contraindications": ["None known"],
        "works_well_with": ["Almost everything", "Retinoids", "Vitamin C (myth debunked)", "AHAs/BHAs", "Peptides"],
        "avoid_combining": ["Very high concentrations with other actives if sensitive"],
        "application_tips": "Workhorse ingredient. Layer-friendly. AM and/or PM use.",
    },

    # HYDROXY ACIDS
    "glycolic_acid": {
        "category": "AHA (Alpha Hydroxy Acid)",
        "inci_name": "Glycolic Acid",
        "mechanism": "Smallest AHA molecule - best penetration. Disrupts corneocyte cohesion (desmosomes). Increases hyaluronic acid synthesis. Stimulates collagen at higher concentrations.",
        "evidence_grade": "A",
        "evidence_summary": "Gold standard AHA. Extensive evidence for exfoliation, photoaging, hyperpigmentation.",
        "optimal_concentration": "5-10% daily use; 20-70% professional peels",
        "optimal_ph": "3-4 (must be acidic to work; higher pH = less irritation but less efficacy)",
        "free_acid_value": "Check 'free acid' percentage, not just total glycolic",
        "stability_concerns": ["Stable", "Water-soluble"],
        "best_forms": ["Toners", "Serums", "Peel pads"],
        "time_to_results": "2-4 weeks for texture; 8-12 weeks for hyperpigmentation",
        "side_effects": ["Sun sensitivity (MUST use SPF)", "Irritation", "Stinging", "Dryness"],
        "contraindications": ["Very sensitive skin", "Compromised barrier", "Recent procedures"],
        "works_well_with": ["Hyaluronic acid", "Niacinamide", "Ceramides"],
        "avoid_combining": ["Retinoids (same routine)", "Other exfoliating acids (same routine)", "Vitamin C (pH conflict)"],
        "application_tips": "Start 2-3x/week. PM use recommended. Non-negotiable SPF the next day.",
    },
    "lactic_acid": {
        "category": "AHA (Alpha Hydroxy Acid)",
        "inci_name": "Lactic Acid",
        "mechanism": "Larger molecule than glycolic - gentler. Exfoliates + has humectant properties. Inhibits tyrosinase.",
        "evidence_grade": "A",
        "evidence_summary": "Well-studied. Gentler alternative to glycolic. Good for dry or sensitive skin.",
        "optimal_concentration": "5-10% for daily use",
        "optimal_ph": "3.5-4",
        "stability_concerns": ["Stable"],
        "best_forms": ["Serums", "Toners"],
        "time_to_results": "4-8 weeks",
        "side_effects": ["Gentler than glycolic", "Still causes sun sensitivity"],
        "contraindications": ["Very sensitive skin", "Compromised barrier"],
        "works_well_with": ["Hyaluronic acid", "Niacinamide"],
        "avoid_combining": ["Retinoids (same routine)", "Other AHAs/BHAs (same routine)"],
        "application_tips": "Good starter AHA. More hydrating than glycolic.",
    },
    "salicylic_acid": {
        "category": "BHA (Beta Hydroxy Acid)",
        "inci_name": "Salicylic Acid",
        "mechanism": "Oil-soluble - penetrates pores. Keratolytic (dissolves keratin). Anti-inflammatory. Antibacterial. Desmolytic (breaks cell bonds).",
        "evidence_grade": "A",
        "evidence_summary": "Gold standard for acne and blackheads. FDA-approved OTC acne treatment.",
        "optimal_concentration": "0.5-2% (OTC max is 2%)",
        "optimal_ph": "3-4",
        "stability_concerns": ["Stable", "Can crystallize at high concentrations"],
        "best_forms": ["Leave-on serums/toners", "Cleansers (less effective, short contact)", "Spot treatments"],
        "time_to_results": "2-4 weeks for clearer pores; 6-8 weeks for acne improvement",
        "side_effects": ["Dryness", "Peeling", "Sun sensitivity (less than AHAs)"],
        "contraindications": ["Aspirin allergy (related compound)", "Pregnancy (limited systemic absorption but caution)"],
        "works_well_with": ["Niacinamide", "Hyaluronic acid", "Benzoyl peroxide (different times)"],
        "avoid_combining": ["AHAs (same routine)", "Retinoids (same routine)", "Multiple exfoliants"],
        "application_tips": "Best for oily/acne-prone. Can use AM or PM. Less photosensitizing than AHAs.",
    },
    "mandelic_acid": {
        "category": "AHA (Alpha Hydroxy Acid)",
        "inci_name": "Mandelic Acid",
        "mechanism": "Largest common AHA molecule - slowest penetration, gentlest. Derived from almonds. Also has antibacterial properties.",
        "evidence_grade": "B+",
        "evidence_summary": "Good evidence, especially for darker skin tones (less PIH risk). Gentlest AHA.",
        "optimal_concentration": "5-10%",
        "optimal_ph": "3.5-4",
        "stability_concerns": ["Stable"],
        "best_forms": ["Serums", "Peels"],
        "time_to_results": "6-12 weeks (slower but gentler)",
        "side_effects": ["Minimal irritation", "Still some sun sensitivity"],
        "contraindications": ["Nut allergy (derived from almonds - but typically safe)"],
        "works_well_with": ["Niacinamide", "Hyaluronic acid"],
        "avoid_combining": ["Other strong exfoliants (same routine)"],
        "application_tips": "Excellent for sensitive skin or melanin-rich skin. Good starter acid.",
    },

    # HYDRATORS
    "hyaluronic_acid": {
        "category": "Humectant / Hydrator",
        "inci_name": "Hyaluronic Acid (Sodium Hyaluronate)",
        "mechanism": "Glycosaminoglycan that holds 1000x its weight in water. Different molecular weights penetrate to different depths. Plumps, hydrates, supports wound healing.",
        "molecular_weights": {
            "high_mw": ">1000 kDa - sits on surface, film-forming",
            "medium_mw": "100-1000 kDa - superficial hydration",
            "low_mw": "50-100 kDa - penetrates epidermis",
            "ultra_low_mw": "<50 kDa - deeper penetration, may stimulate HA synthesis",
        },
        "evidence_grade": "A",
        "evidence_summary": "Excellent evidence for hydration. Multi-weight formulas provide layered benefits.",
        "optimal_concentration": "0.1-2% (more isn't always better)",
        "optimal_ph": "5-7",
        "stability_concerns": ["Stable", "Can support microbial growth - needs preservation"],
        "best_forms": ["Multi-weight serums", "Hydrating toners"],
        "time_to_results": "Immediate plumping; ongoing hydration support",
        "side_effects": ["Can draw moisture from skin in very dry climates (use with occlusive)"],
        "contraindications": ["None known"],
        "works_well_with": ["Everything", "Best sealed with moisturizer/occlusive"],
        "avoid_combining": ["None - universal ingredient"],
        "application_tips": "Apply to damp skin. Layer under moisturizer. In dry climates, MUST seal with occlusive.",
    },
    "ceramides": {
        "category": "Barrier Repair / Lipid",
        "inci_name": "Ceramides (Ceramide NP, AP, EOP, etc.)",
        "mechanism": "Naturally occurring skin lipids (50% of stratum corneum). Maintain barrier integrity, prevent TEWL, protect against irritants.",
        "evidence_grade": "A",
        "evidence_summary": "Essential for barrier function. Therapeutic for eczema, dry skin, sensitized skin.",
        "optimal_concentration": "Ratio matters more than % - ideal is 3:1:1 ceramides:cholesterol:fatty acids",
        "optimal_ph": "5-7",
        "stability_concerns": ["Can be unstable - look for encapsulated or stable forms"],
        "best_forms": ["Moisturizers", "Barrier repair serums"],
        "time_to_results": "Days to weeks for barrier improvement",
        "side_effects": ["None - naturally occurring in skin"],
        "contraindications": ["None"],
        "works_well_with": ["Cholesterol", "Fatty acids", "Niacinamide", "Everything"],
        "avoid_combining": ["None"],
        "application_tips": "Essential for anyone using actives. CeraVe, Stratia Liquid Gold are good sources.",
    },
    "squalane": {
        "category": "Emollient / Lipid",
        "inci_name": "Squalane",
        "mechanism": "Hydrogenated form of squalene (naturally in sebum). Emollient, antioxidant, enhances penetration of other ingredients.",
        "evidence_grade": "B+",
        "evidence_summary": "Good evidence as emollient. Non-comedogenic. Stable form of squalene.",
        "optimal_concentration": "Pure (100%) or as part of formula",
        "optimal_ph": "N/A (oil)",
        "stability_concerns": ["Very stable (unlike squalene)", "Won't oxidize"],
        "best_forms": ["Pure oil", "In moisturizers/serums"],
        "time_to_results": "Immediate softening; ongoing moisture support",
        "side_effects": ["Generally non-comedogenic", "Rare sensitivity"],
        "contraindications": ["None known"],
        "works_well_with": ["Everything - excellent carrier"],
        "avoid_combining": ["None"],
        "application_tips": "Can be used alone or mixed into moisturizer. Good for all skin types.",
    },

    # ACNE TREATMENTS
    "benzoyl_peroxide": {
        "category": "Antibacterial / Acne Treatment",
        "inci_name": "Benzoyl Peroxide",
        "mechanism": "Releases oxygen into pores, killing anaerobic P. acnes bacteria. Also keratolytic. Bacteria cannot develop resistance.",
        "evidence_grade": "A",
        "evidence_summary": "Gold standard OTC acne treatment. Extensive evidence. No bacterial resistance (unlike antibiotics).",
        "optimal_concentration": "2.5% (as effective as 10% with less irritation)",
        "optimal_ph": "4-7",
        "stability_concerns": ["Can bleach fabrics", "Degrades some ingredients"],
        "best_forms": ["Leave-on treatment", "Short-contact therapy (wash off after 2-10 min)", "Spot treatment"],
        "time_to_results": "2-4 weeks for improvement",
        "side_effects": ["Dryness", "Peeling", "Irritation", "Bleaches fabrics/hair"],
        "contraindications": ["Allergy to benzoyl peroxide"],
        "works_well_with": ["Adapalene (Epiduo)", "Clindamycin (prescription combos)"],
        "avoid_combining": ["Most retinoids (oxidizes them)", "Vitamin C (oxidizes it)"],
        "application_tips": "2.5% is sufficient. White towels/pillowcases. Can use short-contact method.",
    },
    "azelaic_acid": {
        "category": "Multi-functional",
        "inci_name": "Azelaic Acid",
        "mechanism": "Antibacterial, anti-inflammatory, tyrosinase inhibitor. Normalizes keratinization. Antioxidant.",
        "evidence_grade": "A",
        "evidence_summary": "Excellent evidence for acne, rosacea, hyperpigmentation. Prescription (15-20%) and OTC (10%).",
        "optimal_concentration": "10% (OTC), 15-20% (Rx)",
        "optimal_ph": "4-5",
        "stability_concerns": ["Stable"],
        "best_forms": ["Gel", "Cream", "Suspension"],
        "time_to_results": "4-8 weeks",
        "side_effects": ["Mild tingling initially", "Generally well-tolerated", "Safe in pregnancy"],
        "contraindications": ["None known - safe in pregnancy"],
        "works_well_with": ["Niacinamide", "Retinoids (different times)", "Most ingredients"],
        "avoid_combining": ["None specific"],
        "application_tips": "Underrated ingredient. Great for acne + PIH. Safe during pregnancy.",
    },

    # PEPTIDES
    "matrixyl": {
        "category": "Peptide / Anti-aging",
        "inci_name": "Palmitoyl Pentapeptide-4 (Matrixyl)",
        "mechanism": "Signal peptide that mimics collagen fragments, signaling fibroblasts to produce more collagen and ECM components.",
        "evidence_grade": "B+",
        "evidence_summary": "Good evidence from manufacturer studies. Independent research more limited but promising.",
        "optimal_concentration": "Proprietary - follow product guidance",
        "optimal_ph": "5-7",
        "stability_concerns": ["Generally stable in formulations"],
        "best_forms": ["Serums", "Moisturizers"],
        "time_to_results": "8-12 weeks",
        "side_effects": ["Excellent tolerability"],
        "contraindications": ["None known"],
        "works_well_with": ["Most ingredients", "Hyaluronic acid", "Niacinamide"],
        "avoid_combining": ["Direct acids may degrade peptides (separate routines)"],
        "application_tips": "Apply before heavier creams. Don't combine with strong acids.",
    },
    "copper_peptides": {
        "category": "Peptide / Anti-aging",
        "inci_name": "Copper Tripeptide-1 (GHK-Cu)",
        "mechanism": "Carries copper to skin cells. Promotes wound healing, collagen synthesis, glycosaminoglycan synthesis. Anti-inflammatory. Remodels damaged tissue.",
        "evidence_grade": "B+",
        "evidence_summary": "Good evidence for wound healing and anti-aging. Blue color indicates active copper.",
        "optimal_concentration": "Proprietary",
        "optimal_ph": "5-7",
        "stability_concerns": ["Sensitive to low pH", "Blue color should remain"],
        "best_forms": ["Serums"],
        "time_to_results": "4-12 weeks",
        "side_effects": ["Generally well-tolerated", "Rare sensitivity"],
        "contraindications": ["None known"],
        "works_well_with": ["Hyaluronic acid", "Niacinamide"],
        "avoid_combining": ["Strong acids", "Vitamin C (copper can oxidize it)", "AHAs/BHAs"],
        "application_tips": "Use at night. Don't combine with exfoliating acids or vitamin C.",
    },
    "argireline": {
        "category": "Peptide / Anti-aging",
        "inci_name": "Acetyl Hexapeptide-3 (Argireline)",
        "mechanism": "Inhibits SNARE complex, reducing neurotransmitter release. 'Topical Botox' - reduces muscle contraction.",
        "evidence_grade": "B",
        "evidence_summary": "Moderate evidence. Some studies show wrinkle reduction. Not as effective as Botox but non-invasive.",
        "optimal_concentration": "5-10%",
        "optimal_ph": "5-7",
        "stability_concerns": ["Relatively stable"],
        "best_forms": ["Targeted serums", "Eye creams"],
        "time_to_results": "4-8 weeks",
        "side_effects": ["Well-tolerated"],
        "contraindications": ["None known"],
        "works_well_with": ["Other peptides", "Hyaluronic acid"],
        "avoid_combining": ["Strong acids"],
        "application_tips": "Apply to expression line areas. Don't expect Botox results.",
    },

    # BRIGHTENING
    "alpha_arbutin": {
        "category": "Brightening",
        "inci_name": "Alpha-Arbutin",
        "mechanism": "Tyrosinase inhibitor. More stable and effective than beta-arbutin. Derived from bearberry. Blocks melanin synthesis.",
        "evidence_grade": "A-",
        "evidence_summary": "Good evidence for hyperpigmentation. Safer than hydroquinone. Works well with vitamin C.",
        "optimal_concentration": "1-2%",
        "optimal_ph": "4-6",
        "stability_concerns": ["Stable", "Heat-stable"],
        "best_forms": ["Serums"],
        "time_to_results": "6-12 weeks",
        "side_effects": ["Generally well-tolerated"],
        "contraindications": ["None known"],
        "works_well_with": ["Vitamin C", "Niacinamide", "Kojic acid"],
        "avoid_combining": ["None specific"],
        "application_tips": "Layer with vitamin C for enhanced brightening. Use consistently.",
    },
    "tranexamic_acid": {
        "category": "Brightening",
        "inci_name": "Tranexamic Acid",
        "mechanism": "Inhibits plasminogen/keratinocyte interaction, reducing UV-induced melanogenesis. Also anti-inflammatory.",
        "evidence_grade": "A-",
        "evidence_summary": "Strong evidence for melasma specifically. Also effective for PIH. Originally oral medication.",
        "optimal_concentration": "2-5%",
        "optimal_ph": "5-7",
        "stability_concerns": ["Stable"],
        "best_forms": ["Serums", "Toners"],
        "time_to_results": "8-12 weeks",
        "side_effects": ["Well-tolerated topically"],
        "contraindications": ["None for topical use"],
        "works_well_with": ["Niacinamide", "Vitamin C", "Other brighteners"],
        "avoid_combining": ["None specific"],
        "application_tips": "Excellent for hormonal pigmentation/melasma. Very stable and well-tolerated.",
    },
    "kojic_acid": {
        "category": "Brightening",
        "inci_name": "Kojic Acid",
        "mechanism": "Tyrosinase inhibitor. Chelates copper required for tyrosinase function. Derived from fungi.",
        "evidence_grade": "B+",
        "evidence_summary": "Good evidence for hyperpigmentation. Can be sensitizing. Often combined with other brighteners.",
        "optimal_concentration": "1-4%",
        "optimal_ph": "4-5",
        "stability_concerns": ["Oxidizes easily (turns brown)", "Light-sensitive"],
        "best_forms": ["Stabilized formulas", "Kojic dipalmitate is more stable"],
        "time_to_results": "8-12 weeks",
        "side_effects": ["Can cause contact dermatitis", "Sensitizing for some"],
        "contraindications": ["Sensitive skin (use with caution)"],
        "works_well_with": ["Alpha arbutin", "Niacinamide"],
        "avoid_combining": ["Too many actives if sensitive"],
        "application_tips": "Patch test first. More sensitizing than other brighteners.",
    },

    # SOOTHING
    "centella_asiatica": {
        "category": "Soothing / Healing",
        "inci_name": "Centella Asiatica Extract (CICA)",
        "mechanism": "Contains madecassoside, asiaticoside, madecassic acid, asiatic acid. Promotes collagen synthesis, wound healing, anti-inflammatory.",
        "evidence_grade": "A-",
        "evidence_summary": "Good evidence for wound healing, barrier repair, anti-inflammatory. Popular in K-beauty.",
        "optimal_concentration": "Varies - look for standardized extracts",
        "optimal_ph": "5-7",
        "stability_concerns": ["Generally stable"],
        "best_forms": ["Serums", "Creams", "Toners"],
        "time_to_results": "2-4 weeks for soothing; ongoing for barrier support",
        "side_effects": ["Excellent tolerability"],
        "contraindications": ["None known"],
        "works_well_with": ["Everything - great barrier support during active use"],
        "avoid_combining": ["None"],
        "application_tips": "Excellent for irritation, post-procedure, or during retinoid adjustment period.",
    },
    "allantoin": {
        "category": "Soothing / Healing",
        "inci_name": "Allantoin",
        "mechanism": "Keratolytic, promotes wound healing, moisturizing, soothing. Derived from comfrey or synthesized.",
        "evidence_grade": "B+",
        "evidence_summary": "Good evidence for skin soothing and healing. Very safe and well-tolerated.",
        "optimal_concentration": "0.5-2%",
        "optimal_ph": "5-7",
        "stability_concerns": ["Very stable"],
        "best_forms": ["Any"],
        "time_to_results": "Ongoing soothing",
        "side_effects": ["None known"],
        "contraindications": ["None"],
        "works_well_with": ["Everything"],
        "avoid_combining": ["None"],
        "application_tips": "Supportive ingredient. Won't see dramatic results but supports skin health.",
    },
    "panthenol": {
        "category": "Hydrating / Soothing",
        "inci_name": "Panthenol (Pro-Vitamin B5)",
        "mechanism": "Converted to pantothenic acid in skin. Humectant, promotes wound healing, anti-inflammatory, improves barrier function.",
        "evidence_grade": "A-",
        "evidence_summary": "Good evidence for hydration, wound healing, barrier support.",
        "optimal_concentration": "1-5%",
        "optimal_ph": "5-7",
        "stability_concerns": ["Stable"],
        "best_forms": ["Serums", "Moisturizers", "Mists"],
        "time_to_results": "Immediate hydration; ongoing barrier support",
        "side_effects": ["Excellent tolerability"],
        "contraindications": ["None known"],
        "works_well_with": ["Everything"],
        "avoid_combining": ["None"],
        "application_tips": "Great supporting ingredient. Hydrating and soothing.",
    },
}


def _get_interaction_details(ingredient1: str, ingredient2: str) -> dict | None:
    """Get detailed interaction information between two ingredients."""
    # Define interaction matrix
    interactions = {
        ("retinol", "benzoyl_peroxide"): {
            "interaction_type": "Negative",
            "severity": "Moderate",
            "mechanism": "Benzoyl peroxide oxidizes retinol, reducing efficacy of both",
            "recommendation": "Use at different times (BP in AM, retinoid in PM) or different days",
        },
        ("retinol", "vitamin_c"): {
            "interaction_type": "Timing-dependent",
            "severity": "Low",
            "mechanism": "pH incompatibility - vitamin C needs low pH, retinol prefers higher. Both work but may irritate together.",
            "recommendation": "Use vitamin C in AM, retinol in PM. Or wait 30 min between applications.",
        },
        ("retinol", "aha"): {
            "interaction_type": "Caution",
            "severity": "Moderate",
            "mechanism": "Both are exfoliating/irritating. Combined use increases irritation risk.",
            "recommendation": "Use on alternating nights, or AHA 1-2x/week with nightly retinol",
        },
        ("retinol", "bha"): {
            "interaction_type": "Caution",
            "severity": "Moderate",
            "mechanism": "Both are exfoliating. Combined use increases irritation.",
            "recommendation": "Alternate nights or use BHA in AM, retinol in PM",
        },
        ("retinol", "niacinamide"): {
            "interaction_type": "Positive",
            "severity": "None",
            "mechanism": "Niacinamide can buffer retinol irritation. Complementary benefits.",
            "recommendation": "Use together - niacinamide before retinol can reduce irritation",
        },
        ("vitamin_c", "niacinamide"): {
            "interaction_type": "Positive",
            "severity": "None",
            "mechanism": "Old myth that they conflict (niacin formation). Modern formulations are fine together.",
            "recommendation": "Can use together. Both are antioxidants with complementary benefits.",
        },
        ("vitamin_c", "aha"): {
            "interaction_type": "Timing-dependent",
            "severity": "Low",
            "mechanism": "Both are acidic. L-AA may be less stable at AHA pH levels.",
            "recommendation": "Use at different times or wait between applications",
        },
        ("aha", "bha"): {
            "interaction_type": "Caution",
            "severity": "Moderate",
            "mechanism": "Double exfoliation. Can over-exfoliate and damage barrier.",
            "recommendation": "Generally don't combine. If using both, alternate days.",
        },
        ("benzoyl_peroxide", "vitamin_c"): {
            "interaction_type": "Negative",
            "severity": "Moderate",
            "mechanism": "Benzoyl peroxide oxidizes vitamin C, making both less effective",
            "recommendation": "Use at different times of day",
        },
        ("copper_peptides", "vitamin_c"): {
            "interaction_type": "Negative",
            "severity": "Moderate",
            "mechanism": "Copper can oxidize vitamin C. May also interfere with peptide function.",
            "recommendation": "Use in separate routines (one AM, one PM)",
        },
        ("copper_peptides", "aha"): {
            "interaction_type": "Negative",
            "severity": "Moderate",
            "mechanism": "Acidic pH can denature peptides, reducing efficacy",
            "recommendation": "Use in separate routines",
        },
    }

    # Normalize and check both directions
    key1 = (ingredient1.lower().replace(" ", "_"), ingredient2.lower().replace(" ", "_"))
    key2 = (ingredient2.lower().replace(" ", "_"), ingredient1.lower().replace(" ", "_"))

    return interactions.get(key1) or interactions.get(key2)


@tool
def ingredient_analyzer(
    ingredients: list[str],
    analysis_depth: Literal["quick", "detailed", "comprehensive"] = "detailed",
    check_interactions: bool = True,
    skin_type: str | None = None,
    concerns: list[str] | None = None,
) -> str:
    """Analyze skincare ingredients with scientific depth for the Skintellectual consumer.

    Provides mechanism of action, evidence grades, optimal formulation parameters,
    and interaction warnings. Designed for consumers who want to understand what
    they're putting on their skin at a deeper level.

    Args:
        ingredients: List of ingredient names to analyze
        analysis_depth: Level of detail - quick (summary), detailed (full analysis), comprehensive (with interactions)
        check_interactions: Whether to check for ingredient interactions
        skin_type: User's skin type for personalized cautions
        concerns: User's skin concerns for relevance scoring

    Returns:
        Comprehensive ingredient analysis with evidence grades and interactions
    """
    report = """# Ingredient Analysis Report

*For the evidence-based skincare consumer*

---

"""

    analyzed_ingredients = []
    unknown_ingredients = []

    # Analyze each ingredient
    for ing_name in ingredients:
        normalized = ing_name.lower().strip().replace(" ", "_").replace("-", "_")

        # Try to find in database
        data = None
        matched_name = None

        # Direct match
        if normalized in INGREDIENT_DATABASE:
            data = INGREDIENT_DATABASE[normalized]
            matched_name = normalized

        # Fuzzy matching for common variations
        else:
            aliases = {
                "vitamin_c": "ascorbic_acid",
                "l_ascorbic_acid": "ascorbic_acid",
                "laa": "ascorbic_acid",
                "vit_c": "ascorbic_acid",
                "sap": "sodium_ascorbyl_phosphate",
                "vitamin_b3": "niacinamide",
                "nicotinamide": "niacinamide",
                "retinoic_acid": "tretinoin",
                "retin_a": "tretinoin",
                "differin": "adapalene",
                "retinaldehyde": "retinal",
                "bha": "salicylic_acid",
                "aha": "glycolic_acid",
                "ha": "hyaluronic_acid",
                "sodium_hyaluronate": "hyaluronic_acid",
                "bp": "benzoyl_peroxide",
                "cica": "centella_asiatica",
                "ghk_cu": "copper_peptides",
            }

            if normalized in aliases:
                matched_name = aliases[normalized]
                data = INGREDIENT_DATABASE.get(matched_name)

        if data:
            analyzed_ingredients.append((ing_name, matched_name, data))
        else:
            unknown_ingredients.append(ing_name)

    # Generate report for each ingredient
    for original_name, matched_name, data in analyzed_ingredients:
        report += f"## {original_name.title()}\n\n"

        if matched_name != original_name.lower().replace(" ", "_"):
            report += f"*Matched to: {matched_name.replace('_', ' ').title()}*\n\n"

        report += f"**INCI Name:** {data.get('inci_name', 'N/A')}\n"
        report += f"**Category:** {data.get('category', 'N/A')}\n"
        report += f"**Evidence Grade:** {data.get('evidence_grade', 'N/A')}\n\n"

        if analysis_depth in ["detailed", "comprehensive"]:
            report += f"### Mechanism of Action\n\n{data.get('mechanism', 'Not documented')}\n\n"

            if "conversion_pathway" in data:
                report += f"**Conversion Pathway:** {data['conversion_pathway']}\n\n"

            if "efficacy_vs_tretinoin" in data:
                report += f"**Efficacy vs Tretinoin:** {data['efficacy_vs_tretinoin']}\n\n"

            report += f"### Evidence Summary\n\n{data.get('evidence_summary', 'Not documented')}\n\n"

            report += "### Formulation Parameters\n\n"
            report += f"| Parameter | Value |\n|-----------|-------|\n"
            report += f"| **Optimal Concentration** | {data.get('optimal_concentration', 'Varies')} |\n"
            report += f"| **Optimal pH** | {data.get('optimal_ph', 'Varies')} |\n"
            report += f"| **Time to Results** | {data.get('time_to_results', 'Varies')} |\n\n"

            if "molecular_weights" in data:
                report += "### Molecular Weight Considerations\n\n"
                for mw, desc in data["molecular_weights"].items():
                    report += f"- **{mw.replace('_', ' ').title()}:** {desc}\n"
                report += "\n"

            if "formulation_gold_standard" in data:
                report += f"**Gold Standard Formulation:** {data['formulation_gold_standard']}\n\n"

        if analysis_depth == "comprehensive":
            report += "### Stability Concerns\n\n"
            for concern in data.get("stability_concerns", []):
                report += f"- {concern}\n"
            report += "\n"

            report += "### Best Product Forms\n\n"
            for form in data.get("best_forms", []):
                report += f"- {form}\n"
            report += "\n"

        # Side effects and contraindications (always show)
        report += "### Safety Profile\n\n"
        report += "**Side Effects:**\n"
        for effect in data.get("side_effects", ["Generally well-tolerated"]):
            report += f"- {effect}\n"

        report += "\n**Contraindications:**\n"
        for contra in data.get("contraindications", ["None known"]):
            report += f"- {contra}\n"
        report += "\n"

        # Compatibility (always show)
        report += "### Compatibility\n\n"
        report += "**Works Well With:**\n"
        for compat in data.get("works_well_with", []):
            report += f"- ✅ {compat}\n"

        report += "\n**Avoid Combining With:**\n"
        avoid_list = data.get("avoid_combining", [])
        if avoid_list and avoid_list != ["None"]:
            for avoid in avoid_list:
                report += f"- ⚠️ {avoid}\n"
        else:
            report += "- None specific\n"
        report += "\n"

        # Application tips
        if "application_tips" in data:
            report += f"### Application Tips\n\n{data['application_tips']}\n\n"

        # Skin type specific notes
        if skin_type:
            report += f"### Notes for {skin_type.title()} Skin\n\n"
            type_notes = _get_skin_type_notes(matched_name, skin_type)
            report += f"{type_notes}\n\n"

        report += "---\n\n"

    # Unknown ingredients
    if unknown_ingredients:
        report += "## ⚠️ Ingredients Not Found\n\n"
        report += "The following ingredients were not found in the database:\n\n"
        for ing in unknown_ingredients:
            report += f"- {ing}\n"
        report += "\n*Consider checking INCI names or scientific names.*\n\n"
        report += "---\n\n"

    # Interaction analysis
    if check_interactions and len(analyzed_ingredients) > 1:
        report += "## 🔬 Interaction Analysis\n\n"

        interactions_found = []

        for i, (name1, key1, _) in enumerate(analyzed_ingredients):
            for name2, key2, _ in analyzed_ingredients[i + 1 :]:
                interaction = _get_interaction_details(key1, key2)
                if interaction:
                    interactions_found.append((name1, name2, interaction))

        if interactions_found:
            for name1, name2, interaction in interactions_found:
                icon = {
                    "Negative": "🔴",
                    "Caution": "🟡",
                    "Timing-dependent": "🟠",
                    "Positive": "🟢",
                }.get(interaction["interaction_type"], "⚪")

                report += f"### {icon} {name1.title()} + {name2.title()}\n\n"
                report += f"**Interaction Type:** {interaction['interaction_type']}\n"
                report += f"**Severity:** {interaction['severity']}\n\n"
                report += f"**Mechanism:** {interaction['mechanism']}\n\n"
                report += f"**Recommendation:** {interaction['recommendation']}\n\n"
        else:
            report += "✅ No significant interactions detected between these ingredients.\n\n"

        report += "---\n\n"

    # Summary
    report += "## Summary\n\n"
    report += "| Ingredient | Category | Evidence Grade |\n"
    report += "|------------|----------|----------------|\n"

    for name, _, data in analyzed_ingredients:
        report += f"| {name.title()} | {data.get('category', 'N/A')} | {data.get('evidence_grade', 'N/A')} |\n"

    for name in unknown_ingredients:
        report += f"| {name} | Unknown | N/A |\n"

    report += """

---

### Evidence Grade Key

| Grade | Meaning |
|-------|---------|
| **A+** | Gold standard, extensive RCTs, FDA-approved |
| **A** | Strong evidence from multiple high-quality studies |
| **A-** | Good evidence, well-established efficacy |
| **B+** | Good evidence, some high-quality studies |
| **B** | Moderate evidence, promising but limited studies |
| **C** | Limited evidence, mostly anecdotal or early research |

---

*This analysis is for educational purposes. Consult a dermatologist for personalized advice.*
"""

    return report


def _get_skin_type_notes(ingredient: str, skin_type: str) -> str:
    """Get skin-type specific notes for an ingredient."""
    notes = {
        "retinol": {
            "oily": "May help regulate sebum. Start with lighter gel formulations.",
            "dry": "Will likely experience more dryness. Buffer with moisturizer, start very slowly.",
            "combination": "Apply to full face; may help oilier areas more.",
            "normal": "Standard approach - start low, increase gradually.",
            "sensitive": "High irritation risk. Consider retinal or bakuchiol first.",
        },
        "glycolic_acid": {
            "oily": "Well-suited. May use more frequently. Watch for dehydration.",
            "dry": "Use less frequently. Consider lactic acid instead.",
            "combination": "Good option. May focus on oilier areas.",
            "normal": "Standard approach works well.",
            "sensitive": "Not recommended. Try mandelic acid or PHAs.",
        },
        "hyaluronic_acid": {
            "oily": "Lightweight hydration without heaviness. Excellent choice.",
            "dry": "Essential, but MUST seal with occlusive/moisturizer.",
            "combination": "Works well for all areas.",
            "normal": "Standard use - great for all.",
            "sensitive": "Generally very well tolerated.",
        },
        "niacinamide": {
            "oily": "Excellent - helps regulate sebum and minimize pores.",
            "dry": "Good for barrier support. Combine with hydrators.",
            "combination": "Ideal - balancing for all areas.",
            "normal": "Multi-benefit for maintenance.",
            "sensitive": "Usually well-tolerated. Start with 5% max.",
        },
        "benzoyl_peroxide": {
            "oily": "Well-suited but can still overdry. Use 2.5%.",
            "dry": "May be too drying. Consider alternatives or short-contact.",
            "combination": "Use as spot treatment or T-zone only.",
            "normal": "Spot treatment approach recommended.",
            "sensitive": "Often too irritating. Try azelaic acid.",
        },
        "salicylic_acid": {
            "oily": "Excellent match - oil-soluble penetrates pores well.",
            "dry": "May be too drying. Use sparingly or skip.",
            "combination": "Great for T-zone; avoid dry areas.",
            "normal": "Good for occasional pore-clearing.",
            "sensitive": "Lower percentages (0.5%) or willow bark extract.",
        },
        "ascorbic_acid": {
            "oily": "Use water-based serum. May tingle - normal.",
            "dry": "Look for formulas with added hydrators.",
            "combination": "Works well; may prefer lighter texture.",
            "normal": "Standard L-AA serums work well.",
            "sensitive": "May be too irritating. Try SAP or ascorbyl glucoside.",
        },
    }

    ingredient_notes = notes.get(ingredient, {})
    return ingredient_notes.get(
        skin_type, "No specific notes for this skin type. General usage guidelines apply."
    )
