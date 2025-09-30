import os
import time
import pytest
import allure

from src.api.task_manager import TaskManagerApi


@pytest.fixture(scope="session")
def task_api() -> TaskManagerApi:
    base = os.environ.get("TASK_API_BASE_URL", "http://127.0.0.1:5000/api")
    return TaskManagerApi(base_url=base)


@allure.feature("Tasks")
def test_create_task(task_api: TaskManagerApi):
    resp = task_api.create_task(title=f"task-{int(time.time())}", description="desc")
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] > 0
    assert body["title"].startswith("task-")


@allure.feature("Tasks")
def test_get_task_after_create(task_api: TaskManagerApi):
    created = task_api.create_task(title="read-me", description="to-read").json()
    resp = task_api.get_task(created["id"]) 
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "read-me"
    assert body["description"] == "to-read"


@allure.feature("Tasks")
def test_update_task(task_api: TaskManagerApi):
    created = task_api.create_task(title="to-update", description="d").json()
    resp = task_api.update_task(created["id"], title="updated", status="completed")
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "updated"
    assert body["status"] == "completed"


@allure.feature("Tasks")
def test_list_tasks_with_status_filter(task_api: TaskManagerApi):
    task_api.create_task(title="p1", status="pending")
    task_api.create_task(title="c1", status="completed")
    pending = task_api.list_tasks(status="pending").json()
    assert all(t["status"] == "pending" for t in pending)


@allure.feature("Tasks")
def test_delete_task(task_api: TaskManagerApi):
    created = task_api.create_task(title="to-delete").json()
    resp = task_api.delete_task(created["id"]) 
    assert resp.status_code == 204


@allure.feature("Tasks")
def test_get_not_found(task_api: TaskManagerApi):
    with pytest.raises(Exception):
        task_api.get_task(999_999)


@allure.feature("Tasks")
def test_update_not_found(task_api: TaskManagerApi):
    with pytest.raises(Exception):
        task_api.update_task(999_999, title="x")


@allure.feature("Tasks")
def test_create_validation_error(task_api: TaskManagerApi):
    with pytest.raises(Exception):
        task_api.create_task(title="")