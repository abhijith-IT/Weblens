from web.registry import get_tool_registry


def test_registry_contains_required_sources():
    registry = get_tool_registry()

    assert len(registry) >= 3

    assert "gecbh_official" in registry
    assert "gecbh_csi" in registry
    assert "csi_student_branch" in registry


def test_registry_entries_have_required_fields():
    registry = get_tool_registry()

    for source_id, source in registry.items():
        assert source_id
        assert source["name"]
        assert source["url"]
        assert source["description"]


def test_registry_urls_are_https():
    registry = get_tool_registry()

    for source in registry.values():
        assert source["url"].startswith("https://")