from web.fetcher import fetch_tool


def test_fetch_real_gecbh_website():
    content = fetch_tool("https://www.gecbh.ac.in/")

    assert content
    assert "VISION" in content.upper()


def test_fetch_real_csi_website():
    content = fetch_tool("https://csigecbh.in/")

    assert content
    assert len(content) > 100