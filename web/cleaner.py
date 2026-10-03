"""Utilities for normalizing text extracted from web pages."""

import re


CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_text(text: str) -> str:
	"""Remove control characters and normalize scraped text whitespace."""
	if not text:
		return ""

	text = text.replace("\r\n", "\n").replace("\r", "\n")
	text = CONTROL_CHARACTERS.sub("", text)
	text = re.sub(r"[ \t]+", " ", text)
	text = re.sub(r"\n[ \t]+", "\n", text)
	text = re.sub(r"\n{3,}", "\n\n", text)

	return text.strip()
