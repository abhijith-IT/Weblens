from web.site_search import find_relevant_pages


def test_find_faculty_pages():
    pages = find_relevant_pages(
        "What information is available about faculty at GECBH?",
        "https://www.gecbh.ac.in/",
    )

    assert pages