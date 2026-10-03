from web.cleaner import sanitize_text


def test_sanitize_text_removes_control_characters_and_normalizes_whitespace():
    text = "  First\tline\x00\r\n\r\n\nSecond   line  "

    assert sanitize_text(text) == "First line\n\nSecond line"


def test_sanitize_text_handles_empty_input():
    assert sanitize_text("") == ""