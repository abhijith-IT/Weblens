import requests
import trafilatura


def fetch_tool(url: str) -> str:
    """Fetch and extract readable text from a web page."""
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "WebLens/1.0",
            },
        )

        response.raise_for_status()

        if not response.text.strip():
            return "No content was returned from this source."

        text = trafilatura.extract(response.text)

        if not text:
            return "Could not extract readable content from this source."

        return text

    except requests.exceptions.Timeout:
        return "The source request timed out."

    except requests.exceptions.RequestException as exc:
        return f"Failed to fetch the source: {exc}"