import os
import allure
import pytest
from _pytest.config import Config
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from src.api.client import ApiClient
from src.logging.logger import get_logger


def pytest_configure(config: Config) -> None:
    
    os.environ.setdefault("BASE_URL", "http://127.0.0.1:5000/")
    os.environ.setdefault("API_BASE_URL", "http://127.0.0.1:9999")


@pytest.fixture(scope="session")
def logger():
    return get_logger("tests")


@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    base_url = os.environ.get("API_BASE_URL", "")
    return ApiClient(base_url=base_url)


@pytest.fixture(scope="session")
def browser() -> Browser:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    context.tracing.stop(path=f"reports/traces/trace_{pytest.uuid}.zip") if hasattr(pytest, 'uuid') else context.tracing.stop()
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    if page.is_closed() is False:
        page.close()