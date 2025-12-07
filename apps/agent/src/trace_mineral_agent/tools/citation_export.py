"""Citation export tool for academic formats."""

from typing import Literal

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A citation entry for export."""

    title: str = Field(description="Paper title")
    authors: list[str] = Field(description="List of author names")
    year: str = Field(description="Publication year")
    journal: str = Field(description="Journal name")
    volume: str | None = Field(default=None, description="Journal volume")
    issue: str | None = Field(default=None, description="Journal issue")
    pages: str | None = Field(default=None, description="Page range")
    doi: str | None = Field(default=None, description="DOI identifier")
    pmid: str | None = Field(default=None, description="PubMed ID")
    abstract: str | None = Field(default=None, description="Paper abstract")


def _format_bibtex(citations: list[Citation]) -> str:
    """Format citations as BibTeX."""
    output = []

    for i, cit in enumerate(citations, 1):
        # Generate citation key from first author and year
        first_author = cit.authors[0].split()[0].lower() if cit.authors else "unknown"
        key = f"{first_author}{cit.year}_{i}"

        # Build BibTeX entry
        entry = [f"@article{{{key},"]
        entry.append(f"  title = {{{cit.title}}},")

        # Format authors: Last, First and Last, First
        if cit.authors:
            formatted_authors = " and ".join(cit.authors)
            entry.append(f"  author = {{{formatted_authors}}},")

        entry.append(f"  journal = {{{cit.journal}}},")
        entry.append(f"  year = {{{cit.year}}},")

        if cit.volume:
            entry.append(f"  volume = {{{cit.volume}}},")
        if cit.issue:
            entry.append(f"  number = {{{cit.issue}}},")
        if cit.pages:
            entry.append(f"  pages = {{{cit.pages}}},")
        if cit.doi:
            entry.append(f"  doi = {{{cit.doi}}},")
        if cit.pmid:
            entry.append(f"  pmid = {{{cit.pmid}}},")

        entry.append("}")
        output.append("\n".join(entry))

    return "\n\n".join(output)


def _format_ris(citations: list[Citation]) -> str:
    """Format citations as RIS."""
    output = []

    for cit in citations:
        entry = ["TY  - JOUR"]

        # Authors
        for author in cit.authors:
            entry.append(f"AU  - {author}")

        entry.append(f"TI  - {cit.title}")
        entry.append(f"JO  - {cit.journal}")
        entry.append(f"PY  - {cit.year}")

        if cit.volume:
            entry.append(f"VL  - {cit.volume}")
        if cit.issue:
            entry.append(f"IS  - {cit.issue}")
        if cit.pages:
            # Split start and end pages
            if "-" in cit.pages:
                start, end = cit.pages.split("-", 1)
                entry.append(f"SP  - {start.strip()}")
                entry.append(f"EP  - {end.strip()}")
            else:
                entry.append(f"SP  - {cit.pages}")
        if cit.doi:
            entry.append(f"DO  - {cit.doi}")
        if cit.pmid:
            entry.append(f"AN  - PMID:{cit.pmid}")
        if cit.abstract:
            entry.append(f"AB  - {cit.abstract}")

        entry.append("ER  - ")
        output.append("\n".join(entry))

    return "\n\n".join(output)


def _format_endnote_xml(citations: list[Citation]) -> str:
    """Format citations as EndNote XML."""
    records = []

    for i, cit in enumerate(citations, 1):
        authors_xml = "\n".join(
            f"          <author><style face=\"normal\" font=\"default\" size=\"100%\">{author}</style></author>"
            for author in cit.authors
        )

        record = f"""    <record>
      <rec-number>{i}</rec-number>
      <ref-type name="Journal Article">17</ref-type>
      <contributors>
        <authors>
{authors_xml}
        </authors>
      </contributors>
      <titles>
        <title><style face=\"normal\" font=\"default\" size=\"100%\">{cit.title}</style></title>
        <secondary-title><style face=\"normal\" font=\"default\" size=\"100%\">{cit.journal}</style></secondary-title>
      </titles>
      <dates>
        <year><style face=\"normal\" font=\"default\" size=\"100%\">{cit.year}</style></year>
      </dates>"""

        if cit.volume:
            record += f"""
      <volume><style face=\"normal\" font=\"default\" size=\"100%\">{cit.volume}</style></volume>"""
        if cit.issue:
            record += f"""
      <number><style face=\"normal\" font=\"default\" size=\"100%\">{cit.issue}</style></number>"""
        if cit.pages:
            record += f"""
      <pages><style face=\"normal\" font=\"default\" size=\"100%\">{cit.pages}</style></pages>"""
        if cit.doi:
            record += f"""
      <electronic-resource-num><style face=\"normal\" font=\"default\" size=\"100%\">{cit.doi}</style></electronic-resource-num>"""
        if cit.abstract:
            record += f"""
      <abstract><style face=\"normal\" font=\"default\" size=\"100%\">{cit.abstract}</style></abstract>"""

        record += """
    </record>"""
        records.append(record)

    xml_header = """<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <records>
"""
    xml_footer = """
  </records>
</xml>"""

    return xml_header + "\n".join(records) + xml_footer


@tool
def export_citations(
    citations: list[dict],
    format: Literal["bibtex", "ris", "endnote"] = "bibtex",
) -> str:
    """
    Export citations in academic format.

    Args:
        citations: List of citation dictionaries with keys:
            - title: Paper title (required)
            - authors: List of author names (required)
            - year: Publication year (required)
            - journal: Journal name (required)
            - volume: Journal volume (optional)
            - issue: Journal issue (optional)
            - pages: Page range (optional)
            - doi: DOI identifier (optional)
            - pmid: PubMed ID (optional)
            - abstract: Paper abstract (optional)
        format: Output format - "bibtex", "ris", or "endnote"

    Returns:
        Formatted citation string in the requested format
    """
    if not citations:
        return "No citations provided."

    # Convert dicts to Citation objects
    citation_objects = []
    for cit in citations:
        try:
            # Handle authors as string or list
            authors = cit.get("authors", [])
            if isinstance(authors, str):
                authors = [a.strip() for a in authors.split(",")]

            citation_objects.append(
                Citation(
                    title=cit.get("title", "Untitled"),
                    authors=authors,
                    year=str(cit.get("year", "n.d.")),
                    journal=cit.get("journal", "Unknown Journal"),
                    volume=cit.get("volume"),
                    issue=cit.get("issue"),
                    pages=cit.get("pages"),
                    doi=cit.get("doi"),
                    pmid=cit.get("pmid"),
                    abstract=cit.get("abstract"),
                )
            )
        except Exception:
            continue

    if not citation_objects:
        return "No valid citations to export."

    # Format based on requested format
    format_funcs = {
        "bibtex": _format_bibtex,
        "ris": _format_ris,
        "endnote": _format_endnote_xml,
    }

    formatter = format_funcs.get(format, _format_bibtex)
    formatted = formatter(citation_objects)

    # Add header with citation count
    header = f"# {len(citation_objects)} citation(s) exported in {format.upper()} format\n\n"

    return header + formatted


@tool
def format_citation_for_report(
    title: str,
    authors: str,
    year: str,
    journal: str,
    doi: str | None = None,
) -> str:
    """
    Format a single citation for inline use in reports (Vancouver style).

    Args:
        title: Paper title
        authors: Authors (comma-separated)
        year: Publication year
        journal: Journal name
        doi: DOI identifier (optional)

    Returns:
        Formatted citation string
    """
    # Parse authors and format Vancouver style
    author_list = [a.strip() for a in authors.split(",")]
    if len(author_list) > 3:
        formatted_authors = f"{author_list[0]}, et al."
    else:
        formatted_authors = ", ".join(author_list)

    citation = f"{formatted_authors}. {title}. {journal}. {year}"

    if doi:
        citation += f". doi:{doi}"

    return citation
