"""Literature search tool for multi-paradigm medical research."""

import os
from typing import Literal

import httpx
from defusedxml import ElementTree
from langchain_core.tools import tool

from ..cache import cached_search


@tool
def literature_search(
    query: str,
    paradigm: Literal["allopathy", "naturopathy", "ayurveda", "tcm"],
    max_results: int = 10,
) -> str:
    """
    Search medical literature for a specific paradigm.

    Args:
        query: Search terms (e.g., "chromium insulin sensitivity")
        paradigm: Medical paradigm to search within
        max_results: Maximum number of papers to return (default 10)

    Returns:
        Markdown-formatted search results with citations
    """
    # Select search function based on paradigm
    search_funcs = {
        "allopathy": _search_pubmed,
        "naturopathy": _search_integrative_medicine,
        "ayurveda": _search_ayurveda_databases,
        "tcm": _search_tcm_databases,
    }

    if paradigm not in search_funcs:
        return f"Unknown paradigm: {paradigm}"

    # Use cached search
    results = cached_search(search_funcs[paradigm], query, paradigm, max_results)

    # Format results as markdown
    if not results:
        return f"**No results found** for '{query}' in {paradigm} literature."

    # Check for error in results
    if results and "error" in results[0]:
        return f"**Search error:** {results[0]['error']}"

    output = f"## {paradigm.title()} Literature Results\n\n"
    output += f"**Query:** {query}\n"
    output += f"**Results:** {len(results)} papers found\n\n"

    for i, paper in enumerate(results, 1):
        output += f"### {i}. {paper['title']}\n"
        output += f"- **Authors:** {paper['authors']}\n"
        output += f"- **Year:** {paper['year']}\n"
        output += f"- **Journal:** {paper['journal']}\n"
        output += f"- **DOI:** {paper.get('doi', 'N/A')}\n"
        abstract = paper.get("abstract", "No abstract available")
        if len(abstract) > 300:
            abstract = abstract[:300] + "..."
        output += f"- **Abstract:** {abstract}\n\n"

    return output


def _search_pubmed(query: str, max_results: int) -> list:
    """Search PubMed using E-utilities API."""
    api_key = os.getenv("NCBI_API_KEY", "")
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    # Search for article IDs
    search_url = f"{base_url}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
    }
    if api_key:
        params["api_key"] = api_key

    try:
        response = httpx.get(search_url, params=params, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        ids = data.get("esearchresult", {}).get("idlist", [])

        if not ids:
            return []

        # Fetch article details
        fetch_url = f"{base_url}/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml",
        }
        if api_key:
            fetch_params["api_key"] = api_key

        fetch_response = httpx.get(fetch_url, params=fetch_params, timeout=60.0)
        return _parse_pubmed_xml(fetch_response.text)
    except Exception as e:
        return [{"error": str(e)}]


def _search_integrative_medicine(query: str, max_results: int) -> list:
    """Search integrative medicine databases via Tavily."""
    try:
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return [{"error": "TAVILY_API_KEY not set"}]

        client = TavilyClient(api_key=api_key)
        results = client.search(
            query=f"{query} site:ndnr.com OR site:naturalmedicinejournal.com OR site:restorativemedicine.org",
            max_results=max_results,
        )

        return [
            {
                "title": r.get("title", "Untitled"),
                "authors": "Various",
                "year": "2024",
                "journal": "Naturopathic Literature",
                "abstract": r.get("content", "")[:500],
                "doi": r.get("url", ""),
            }
            for r in results.get("results", [])
        ]
    except Exception as e:
        return [{"error": str(e)}]


def _search_ayurveda_databases(query: str, max_results: int) -> list:
    """Search Ayurveda-specific databases."""
    try:
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return [{"error": "TAVILY_API_KEY not set"}]

        client = TavilyClient(api_key=api_key)
        results = client.search(
            query=f"{query} ayurveda bhasma rasa shastra",
            max_results=max_results,
        )

        return [
            {
                "title": r.get("title", "Untitled"),
                "authors": "Classical/Modern",
                "year": "Traditional",
                "journal": "Ayurvedic Literature",
                "abstract": r.get("content", "")[:500],
                "doi": r.get("url", ""),
            }
            for r in results.get("results", [])
        ]
    except Exception as e:
        return [{"error": str(e)}]


def _search_tcm_databases(query: str, max_results: int) -> list:
    """Search TCM-specific databases."""
    try:
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return [{"error": "TAVILY_API_KEY not set"}]

        client = TavilyClient(api_key=api_key)
        results = client.search(
            query=f"{query} traditional chinese medicine TCM five elements",
            max_results=max_results,
        )

        return [
            {
                "title": r.get("title", "Untitled"),
                "authors": "Classical/Modern",
                "year": "Traditional",
                "journal": "TCM Literature",
                "abstract": r.get("content", "")[:500],
                "doi": r.get("url", ""),
            }
            for r in results.get("results", [])
        ]
    except Exception as e:
        return [{"error": str(e)}]


def _parse_pubmed_xml(xml_text: str) -> list:
    """Parse PubMed XML response into structured data."""
    papers = []
    try:
        root = ElementTree.fromstring(xml_text)
        for article in root.findall(".//PubmedArticle"):
            medline = article.find(".//MedlineCitation")
            if medline is None:
                continue

            article_data = medline.find(".//Article")
            if article_data is None:
                continue

            title = article_data.findtext(".//ArticleTitle", "No title")
            abstract_elem = article_data.find(".//Abstract/AbstractText")
            abstract = abstract_elem.text if abstract_elem is not None else "No abstract"
            journal = article_data.findtext(".//Journal/Title", "Unknown")
            year = article_data.findtext(".//Journal/JournalIssue/PubDate/Year", "N/A")

            authors_list = []
            for author in article_data.findall(".//AuthorList/Author"):
                last = author.findtext("LastName", "")
                first = author.findtext("ForeName", "")
                if last:
                    authors_list.append(f"{last} {first[:1] if first else ''}")

            doi = ""
            for eid in article.findall(".//ArticleIdList/ArticleId"):
                if eid.get("IdType") == "doi":
                    doi = eid.text or ""
                    break

            papers.append(
                {
                    "title": title,
                    "authors": ", ".join(authors_list[:3])
                    + ("..." if len(authors_list) > 3 else ""),
                    "year": year,
                    "journal": journal,
                    "abstract": abstract or "No abstract",
                    "doi": doi,
                }
            )
    except ElementTree.ParseError:
        pass

    return papers
