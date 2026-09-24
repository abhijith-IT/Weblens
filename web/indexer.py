from __future__ import annotations

import json
import os
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from web.fetcher import fetch_html, fetch_tool, get_internal_links


BASE_URL = "https://www.gecbh.ac.in/"
INDEX_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "gecbh_index.json",
)

MAX_PAGES = 80


def extract_page_title(html: str) -> str:
    """Extract the page title."""
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    if soup.title:
        return soup.title.get_text(" ", strip=True)

    return ""


def build_page_index() -> list[dict]:
    """
    Build a local searchable index of GECBH pages.

    Only pages belonging to the GECBH domain are included.
    """

    print("WebLens Indexer")
    print("=" * 50)

    print(f"Starting from: {BASE_URL}")

    homepage_html = fetch_html(BASE_URL)

    if not homepage_html:
        print("ERROR: Could not fetch GECBH homepage.")
        return []

    # ---------------------------------------------------------
    # Discover internal pages
    # ---------------------------------------------------------

    links = get_internal_links(
        BASE_URL,
        homepage_html,
    )

    urls = []

    seen = set()

    # Always include homepage.
    seen.add(BASE_URL.rstrip("/"))
    urls.append(BASE_URL)

    for link in links:

        url = link["url"]

        parsed = urlparse(url)

        if parsed.netloc != urlparse(BASE_URL).netloc:
            continue

        # Skip fragments.
        url = url.split("#")[0]

        # Avoid duplicates.
        normalized = url.rstrip("/")

        if normalized in seen:
            continue

        seen.add(normalized)
        urls.append(url)

    print(f"Discovered {len(urls)} pages.")

    # ---------------------------------------------------------
    # Fetch pages
    # ---------------------------------------------------------

    pages = []

    for index, url in enumerate(
        urls[:MAX_PAGES],
        start=1,
    ):

        print(
            f"[{index}/{min(len(urls), MAX_PAGES)}] "
            f"{url}"
        )

        html = fetch_html(url)

        if not html:
            print("    skipped: fetch failed")
            continue

        title = extract_page_title(html)

        # Use the existing readable-content extractor.
        content = fetch_tool(url)

        if not content:
            print("    skipped: no readable content")
            continue

        pages.append(
            {
                "url": url,
                "title": title,
                "content": content,
            }
        )

        print(
            f"    indexed: {len(content)} characters"
        )

    return pages


def save_index(pages: list[dict]) -> None:
    """Save the page index as JSON."""

    directory = os.path.dirname(INDEX_FILE)

    os.makedirs(
        directory,
        exist_ok=True,
    )

    with open(
        INDEX_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            pages,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print("=" * 50)
    print(f"Indexed pages: {len(pages)}")
    print(f"Saved to: {INDEX_FILE}")
    print("=" * 50)


def main():
    pages = build_page_index()

    if not pages:
        print("No pages were indexed.")
        return

    save_index(pages)


if __name__ == "__main__":
    main()