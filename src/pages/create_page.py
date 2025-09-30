from playwright.sync_api import Page, Locator


class CreatePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title_input: Locator = page.locator("#title")
        self.description_input: Locator = page.locator("#description")
        self.status_select: Locator = page.locator("#status")
        self.submit_btn: Locator = page.get_by_role("button", name="Create Task")

    def create_task(self, title: str, description: str = "", status: str = "pending") -> None:
        self.title_input.fill(title)
        if description:
            self.description_input.fill(description)
        self.status_select.select_option(status)
        self.submit_btn.click()