import os
import time
import pytest
import allure

from src.pages.index_page import IndexPage
from src.pages.create_page import CreatePage
from src.pages.detail_page import DetailPage
from src.pages.edit_page import EditPage


BASE_WEB_URL = os.environ.get("BASE_URL", "http://127.0.0.1:5000/")


@allure.feature("UI")
def test_create_task_via_ui(page):
    index = IndexPage(page)
    index.open(BASE_WEB_URL)

    index.open_create()

    create = CreatePage(page)
    title = f"ui-task-{int(time.time())}"
    create.create_task(title=title, description="from ui", status="pending")

    
    index = IndexPage(page)
    page.wait_for_load_state("domcontentloaded")
    assert index.task_cards.count() >= 1


@allure.feature("UI")
def test_view_and_edit_task(page):
    index = IndexPage(page)
    index.open(BASE_WEB_URL)

    
    if index.task_cards.count() == 0:
        index.open_create()
        CreatePage(page).create_task(title=f"seed-{int(time.time())}")
        index = IndexPage(page)

    
    index.task_cards.first.locator("a.btn-view").click()
    detail = DetailPage(page)

    
    detail.open_edit()
    edit = EditPage(page)
    edit.update(status="completed")

   
    detail = DetailPage(page)
    detail.go_back()
    index = IndexPage(page)
    assert index.task_cards.first.locator(".status-badge.completed").is_visible()


@allure.feature("UI")
def test_filter_by_status(page):
    index = IndexPage(page)
    index.open(BASE_WEB_URL)

    index.filter_by_status("completed")
    page.wait_for_load_state("domcontentloaded")

    
    if index.empty_state.is_visible():
        assert True
    else:
        assert index.task_cards.count() >= 1
        expect_all_completed = index.task_cards.filter(has=page.locator(".status-badge.completed"))
        assert expect_all_completed.count() == index.task_cards.count()