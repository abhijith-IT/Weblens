from __future__ import annotations

import re
from collections import Counter
from heapq import nlargest
from urllib.parse import urljoin, urlparse

import requests
import trafilatura
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/153.0.0.0 Safari/537.36"
)

TIMEOUT = 5


def fetch_html(url: str) -> str:
    """Fetch raw HTML from a URL safely."""
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )

        if response.status_code != 200:
            return ""

        return response.text

    except requests.RequestException:
        return ""


def fetch_tool(url: str) -> str:
    """
    Fetch readable text from a webpage.

    Returns an empty string if the page cannot be fetched or
    meaningful text cannot be extracted.
    """
    html = fetch_html(url)

    if not html:
        return ""

    try:
        text = trafilatura.extract(
            html,
            include_links=True,
            include_tables=True,
        )

        if text and text.strip():
            return text.strip()

    except Exception:
        pass

    # Fallback extraction using BeautifulSoup
    try:
        soup = BeautifulSoup(html, "html.parser")

        for element in soup(
            ["script", "style", "noscript", "svg", "header", "footer"]
        ):
            element.decompose()

        text = soup.get_text(" ", strip=True)

        return text.strip()

    except Exception:
        return ""


def normalize_text(text: str) -> str:
    """Normalize text for local relevance matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def query_terms(query: str) -> list[str]:
    """
    Extract useful terms from the user's query.

    Very common question words are ignored because they don't help
    identify relevant pages.
    """
    stop_words = {
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

    words = normalize_text(query).split()

    return [
        word
        for word in words
        if word not in stop_words and len(word) >= 3
    ]


def tokenize(text: str) -> list[str]:
    return normalize_text(text).split()


def term_overlap(query_words: list[str], text: str) -> float:
    """
    Calculate how strongly the query terms overlap with some text.
    """
    if not query_words or not text:
        return 0.0

    words = set(tokenize(text))

    matches = sum(1 for word in query_words if word in words)

    return matches / len(set(query_words))


def get_internal_links(base_url: str, html: str) -> list[dict]:
    """
    Extract internal links from a page.

    Each result contains:
        url
        text
    """
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")

    base_domain = urlparse(base_url).netloc

    links = []
    seen = set()

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()

        if not href:
            continue

        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue

        url = urljoin(base_url, href)

        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            continue

        if parsed.netloc != base_domain:
            continue

        # Remove fragments
        clean_url = parsed._replace(fragment="").geturl()

        if clean_url in seen:
            continue

        seen.add(clean_url)

        link_text = anchor.get_text(" ", strip=True)

        links.append(
            {
                "url": clean_url,
                "text": link_text,
            }
        )

    return links


def get_page_metadata(url: str, html: str) -> dict:
    """
    Extract lightweight metadata used for relevance ranking.
    """
    soup = BeautifulSoup(html, "html.parser")

    title = ""

    if soup.title:
        title = soup.title.get_text(" ", strip=True)

    description = ""

    meta_description = soup.find(
        "meta",
        attrs={"name": re.compile("^description$", re.I)},
    )

    if meta_description:
        description = meta_description.get("content", "")

    headings = []

    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = heading.get_text(" ", strip=True)

        if text:
            headings.append(text)

    return {
        "title": title,
        "description": description,
        "headings": " ".join(headings),
    }


def score_page(
    query: str,
    url: str,
    link_text: str = "",
    html: str = "",
) -> float:
    """
    Score an already-fetched page against the user's query.

    The important difference from the previous version is that
    pages are scored AFTER their HTML has been fetched.
    """

    words = query_terms(query)

    if not words:
        return 0.0

    metadata = get_page_metadata(url, html)

    url_text = url.replace("-", " ").replace("_", " ")

    title_score = term_overlap(
        words,
        metadata["title"],
    )

    heading_score = term_overlap(
        words,
        metadata["headings"],
    )

    link_score = term_overlap(
        words,
        link_text,
    )

    url_score = term_overlap(
        words,
        url_text,
    )

    description_score = term_overlap(
        words,
        metadata["description"],
    )

    body_score = 0.0

    try:
        body = trafilatura.extract(html) or ""

        # Body text is useful, but weaker than title/headings.
        body_score = term_overlap(words, body)

    except Exception:
        pass

    score = (
        title_score * 40
        + heading_score * 30
        + link_score * 25
        + url_score * 20
        + description_score * 15
        + body_score * 5
    )

    return round(score, 2)


def score_candidate(
    query: str,
    candidate: dict,
) -> dict:
    """
    Fetch and score one candidate page.
    """

    url = candidate["url"]

    html = fetch_html(url)

    if not html:
        return {
            **candidate,
            "score": 0.0,
            "html": "",
        }

    score = score_page(
        query=query,
        url=url,
        link_text=candidate.get("text", ""),
        html=html,
    )

    return {
        **candidate,
        "score": score,
        "html": html,
    }


def search_site(
    query: str,
    base_url: str,
    first_level: int = 25,
    second_level: int = 6,
    max_results: int = 5,
) -> list[dict]:
    """
    Search a trusted website using local relevance ranking.

    Strategy:

    1. Fetch the homepage.
    2. Discover its internal links.
    3. Fetch a limited number of candidate pages.
    4. Score the actual page content against the query.
    5. Take the strongest pages.
    6. Explore links from those strong pages.
    7. Fetch and score those deeper pages.
    8. Return the best matching pages.

    This avoids blindly crawling the whole website.
    """

    print("WebLens: analyzing homepage...")

    homepage_html = fetch_html(base_url)

    if not homepage_html:
        return []

    # ---------------------------------------------------------
    # Homepage
    # ---------------------------------------------------------

    homepage_score = score_page(
        query=query,
        url=base_url,
        link_text="GECBH Official Website",
        html=homepage_html,
    )

    candidates = [
        {
            "url": base_url,
            "score": homepage_score,
            "level": 0,
            "link_text": "GECBH Official Website",
            "html": homepage_html,
        }
    ]

    # ---------------------------------------------------------
    # Discover homepage links
    # ---------------------------------------------------------

    homepage_links = get_internal_links(
        base_url,
        homepage_html,
    )

    # Remove duplicate URLs.
    unique_links = {}

    for link in homepage_links:
        unique_links[link["url"]] = link

    homepage_links = list(unique_links.values())

    print(
        f"WebLens: discovered "
        f"{len(homepage_links)} internal homepage links."
    )

    # ---------------------------------------------------------
    # IMPORTANT:
    # Fetch candidate pages BEFORE scoring them.
    # ---------------------------------------------------------

    first_level_pages = []

    for index, link in enumerate(
        homepage_links[:first_level],
        start=1,
    ):

        print(
            f"WebLens: checking page "
            f"{index}/{min(len(homepage_links), first_level)} "
            f"-> {link['url']}"
        )

        page = score_candidate(
            query=query,
            candidate=link,
        )

        if page["html"]:
            page["level"] = 1
            first_level_pages.append(page)

    # ---------------------------------------------------------
    # Rank actual fetched pages
    # ---------------------------------------------------------

    first_level_pages.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    print("WebLens: best matching pages:")

    for page in first_level_pages[:10]:
        print(
            f"  {page['score']:.1f} "
            f"{page['url']}"
        )

    candidates.extend(
        first_level_pages
    )

    # ---------------------------------------------------------
    # Explore only the strongest first-level pages
    # ---------------------------------------------------------

    second_level_candidates = {}

    for page in first_level_pages[:second_level]:

        print(
            f"WebLens: exploring "
            f"{page['url']}"
        )

        links = get_internal_links(
            page["url"],
            page["html"],
        )

        for link in links:

            url = link["url"]

            # Don't revisit pages we already fetched.
            if any(
                item["url"] == url
                for item in candidates
            ):
                continue

            existing = second_level_candidates.get(url)

            if existing is None:
                second_level_candidates[url] = link

    # ---------------------------------------------------------
    # Fetch deeper candidates
    # ---------------------------------------------------------

    second_level_pages = []

    for index, link in enumerate(
        list(second_level_candidates.values())[:25],
        start=1,
    ):

        print(
            f"WebLens: checking deeper page "
            f"{index} "
            f"-> {link['url']}"
        )

        page = score_candidate(
            query=query,
            candidate=link,
        )

        if page["html"]:
            page["level"] = 2
            second_level_pages.append(page)

    # ---------------------------------------------------------
    # Final ranking
    # ---------------------------------------------------------

    candidates.extend(
        second_level_pages
    )

    unique_candidates = {}

    for candidate in candidates:

        url = candidate["url"]

        existing = unique_candidates.get(url)

        if (
            existing is None
            or candidate["score"] > existing["score"]
        ):
            unique_candidates[url] = candidate

    final_results = sorted(
        unique_candidates.values(),
        key=lambda item: item["score"],
        reverse=True,
    )

    # ---------------------------------------------------------
    # Return only the relevant pages
    # ---------------------------------------------------------

    results = []

    for result in final_results[:max_results]:

        results.append(
            {
                "url": result["url"],
                "score": result["score"],
                "level": result["level"],
                "content": result["html"],
            }
        )

    return results