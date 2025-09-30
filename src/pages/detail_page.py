from playwright.sync_api import Page, Locator


class DetailPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.back_btn: Locator = page.get_by_role("link", name="Back to List")
        self.edit_btn: Locator = page.get_by_role("link", name="Edit")
        self.delete_btn: Locator = page.get_by_role("button", name="Delete")

    def go_back(self) -> None:
        self.back_btn.click()

    def open_edit(self) -> None:
        self.edit_btn.click()