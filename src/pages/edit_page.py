from playwright.sync_api import Page, Locator


class EditPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title_input: Locator = page.locator("#title")
        self.description_input: Locator = page.locator("#description")
        self.status_select: Locator = page.locator("#status")
        self.save_btn: Locator = page.get_by_role("button", name="Save Changes")

    def update(self, title: str | None = None, description: str | None = None, status: str | None = None) -> None:
        if title is not None:
            self.title_input.fill(title)
        if description is not None:
            self.description_input.fill(description)
        if status is not None:
            self.status_select.select_option(status)
        self.save_btn.click()