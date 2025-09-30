from playwright.sync_api import Page, Locator


class IndexPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.new_task_btn: Locator = page.get_by_role("link", name="New Task")
        self.status_select: Locator = page.locator("select#status")
        self.sort_select: Locator = page.locator("select#sort")
        self.task_cards: Locator = page.locator(".task-card")
        self.empty_state: Locator = page.locator(".empty-state")

    def open(self, base_url: str) -> None:
        self.page.goto(base_url)

    def filter_by_status(self, status: str) -> None:
        self.status_select.select_option(status)

    def open_create(self) -> None:
        self.new_task_btn.click()