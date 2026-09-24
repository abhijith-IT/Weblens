from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path


INDEX_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "gecbh_index.json"
)


STOP_WORDS = {
    "what",
    "which",
    "who",
    "where",
    "when",
    "why",
    "how",
    "is",
    "are",
    "was",
    "were",
    "the",
    "a",
    "an",
    "at",
    "of",
    "to",
    "for",
    "from",
    "about",
    "available",
    "information",
    "does",
    "do",
    "can",
    "on",
    "in",
    "and",
    "or",
    "me",
    "tell",
    "give",
    "please",
    "gecbh",
}


def normalize(text: str) -> str:
    """Normalize text for matching."""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def terms_from_query(query: str) -> list[str]:
    """Extract meaningful terms from the query."""

    words = normalize(query).split()

    return [
        word
        for word in words
        if word not in STOP_WORDS
        and len(word) >= 3
    ]


def load_index() -> list[dict]:
    """Load the locally indexed GECBH pages."""

    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            "GECBH index not found.\n"
            "Run: python -m web.indexer"
        )

    with open(
        INDEX_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def extract_headings(content: str) -> list[str]:
    """
    Extract likely headings from the extracted text.

    Markdown-style headings are supported because trafilatura
    commonly preserves them.
    """

    headings = []

    for line in content.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            headings.append(
                line.lstrip("#").strip()
            )

    return headings


def find_matching_context(
    content: str,
    terms: list[str],
) -> list[str]:
    """
    Find short pieces of content containing query terms.

    This is used for debugging and contextual relevance.
    """

    matches = []

    lines = content.splitlines()

    for line in lines:

        normalized = normalize(line)

        if any(
            term in normalized.split()
            for term in terms
        ):
            matches.append(line.strip())

    return matches


def score_page(
    query: str,
    page: dict,
) -> float:
    """
    Calculate semantic-ish local relevance.

    Strong signals:
      - exact phrase
      - heading match
      - multiple query terms close together
      - URL match

    Weak signal:
      - ordinary body-text frequency
    """

    terms = terms_from_query(query)

    if not terms:
        return 0.0

    content = page.get(
        "content",
        "",
    )

    title = page.get(
        "title",
        "",
    )

    url = page.get(
        "url",
        "",
    )

    normalized_content = normalize(
        content
    )

    normalized_title = normalize(
        title
    )

    normalized_url = normalize(
        url
    )

    score = 0.0

    # ---------------------------------------------------------
    # 1. Exact phrase matching
    # ---------------------------------------------------------

    query_phrase = normalize(query)

    # Ignore the question words and build the important phrase.
    important_phrase = " ".join(terms)

    if important_phrase and important_phrase in normalized_content:
        score += 30

    # ---------------------------------------------------------
    # 2. Heading matching
    # ---------------------------------------------------------

    headings = extract_headings(content)

    for heading in headings:

        heading_normalized = normalize(
            heading
        )

        heading_words = set(
            heading_normalized.split()
        )

        matching_terms = [
            term
            for term in terms
            if term in heading_words
        ]

        if matching_terms:

            # One matching term in a heading is already strong.
            score += 35

            # Multiple matching terms are even stronger.
            score += (
                len(matching_terms) - 1
            ) * 20

    # ---------------------------------------------------------
    # 3. Special phrase detection
    # ---------------------------------------------------------

    important_phrases = [
        "our vision",
        "vision",
        "mission",
        "faculty",
        "teaching faculty",
        "faculty members",
        "staff",
        "departments",
        "department",
        "facilities",
        "campus facilities",
        "placement",
        "placements",
        "training and placement",
        "library",
        "hostel",
        "laboratory",
        "laboratories",
    ]

    for phrase in important_phrases:

        if phrase in query_phrase:

            if phrase in normalized_content:

                score += 15

            if phrase in normalized_title:

                score += 25

            if phrase in normalized_url:

                score += 20

    # ---------------------------------------------------------
    # 4. URL matching
    # ---------------------------------------------------------

    for term in terms:

        if term in normalized_url.split():

            score += 8

    # ---------------------------------------------------------
    # 5. Body frequency
    # ---------------------------------------------------------

    content_words = normalized_content.split()

    if content_words:

        counts = Counter(
            content_words
        )

        for term in terms:

            count = counts.get(
                term,
                0,
            )

            if count:

                # Diminishing returns.
                score += min(
                    math.log(count + 1) * 2,
                    8,
                )

    # ---------------------------------------------------------
    # 6. Context quality
    # ---------------------------------------------------------

    matching_lines = find_matching_context(
        content,
        terms,
    )

    if matching_lines:

        # A page where several query terms occur
        # in meaningful lines gets a small bonus.
        matched_terms = set()

        for line in matching_lines:

            words = set(
                normalize(line).split()
            )

            matched_terms.update(
                term
                for term in terms
                if term in words
            )

        score += (
            len(matched_terms) * 4
        )

    return round(
        score,
        3,
    )


def find_relevant_pages(
    query: str,
    base_url: str,
    max_results: int = 5,
) -> list[str]:
    """
    Search the locally indexed GECBH pages.

    No crawling happens here.
    """

    pages = load_index()

    # ---------------------------------------------------------
    # Restrict results to trusted domain
    # ---------------------------------------------------------

    base_domain = (
        base_url
        .replace("https://", "")
        .replace("http://", "")
        .rstrip("/")
        .split("/")[0]
    )

    trusted_pages = []

    for page in pages:

        url = page.get(
            "url",
            "",
        )

        if base_domain in url:
            trusted_pages.append(
                page
            )

    # ---------------------------------------------------------
    # Score pages
    # ---------------------------------------------------------

    results = []

    for page in trusted_pages:

        score = score_page(
            query,
            page,
        )

        if score > 0:

            results.append(
                {
                    "url": page["url"],
                    "score": score,
                }
            )

    # ---------------------------------------------------------
    # Sort
    # ---------------------------------------------------------

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    print(
        f"WebLens: searched "
        f"{len(trusted_pages)} indexed pages."
    )

    print(
        "WebLens: most relevant pages:"
    )

    for result in results[:max_results]:

        print(
            f"  {result['score']:.3f} "
            f"{result['url']}"
        )

    return [
        result["url"]
        for result in results[:max_results]
    ]