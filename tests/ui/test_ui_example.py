import allure


def test_ui_example(page):
    with allure.step("Open example.com"):
        page.goto("https://example.com")
        assert page.title().lower().find("example") != -1