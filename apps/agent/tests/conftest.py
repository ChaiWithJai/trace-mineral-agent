"""Pytest configuration and fixtures."""

import os

import pytest


@pytest.fixture(autouse=True)
def mock_api_keys(monkeypatch):
    """Set mock API keys for testing."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
    monkeypatch.setenv("NCBI_API_KEY", "test-ncbi-key")


@pytest.fixture
def sample_pubmed_xml():
    """Sample PubMed XML response for testing."""
    return """<?xml version="1.0" encoding="UTF-8"?>
    <PubmedArticleSet>
        <PubmedArticle>
            <MedlineCitation>
                <Article>
                    <ArticleTitle>Effects of chromium on insulin sensitivity</ArticleTitle>
                    <Abstract>
                        <AbstractText>This study examines the effects of chromium supplementation on insulin sensitivity in adults with type 2 diabetes.</AbstractText>
                    </Abstract>
                    <AuthorList>
                        <Author>
                            <LastName>Smith</LastName>
                            <ForeName>John</ForeName>
                        </Author>
                        <Author>
                            <LastName>Doe</LastName>
                            <ForeName>Jane</ForeName>
                        </Author>
                    </AuthorList>
                    <Journal>
                        <Title>Journal of Clinical Nutrition</Title>
                        <JournalIssue>
                            <PubDate>
                                <Year>2023</Year>
                            </PubDate>
                        </JournalIssue>
                    </Journal>
                </Article>
            </MedlineCitation>
            <ArticleIdList>
                <ArticleId IdType="doi">10.1234/example.2023</ArticleId>
            </ArticleIdList>
        </PubmedArticle>
    </PubmedArticleSet>
    """


@pytest.fixture
def sample_hypothesis():
    """Sample research hypothesis for testing."""
    return {
        "hypothesis": "Chromium picolinate improves insulin sensitivity in adults with metabolic syndrome",
        "mineral": "chromium",
        "target_pathways": ["insulin signaling", "glucose uptake", "GLUT4 translocation"],
        "target_outcomes": ["HbA1c", "fasting glucose", "HOMA-IR"],
    }


@pytest.fixture
def sample_paradigm_findings():
    """Sample findings from each paradigm."""
    return {
        "allopathy": "3 RCTs (n=450) show modest HbA1c reduction (-0.3%, 95% CI -0.5 to -0.1)",
        "naturopathy": "Commonly used in blood sugar support protocols; synergy with biotin noted",
        "ayurveda": "No direct bhasma equivalent; associated with Earth element and Spleen function",
        "tcm": "Earth element mineral; supports Spleen Qi; addresses Phlegm-Dampness pattern",
    }
