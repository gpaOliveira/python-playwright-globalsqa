def test_example_domain(page, logger):
    page.goto("https://example.com")
    title = page.title()
    assert "Example Domain" in title
    logger.info(f"Page title is: {title}")
