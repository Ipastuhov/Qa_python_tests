from typing import Any, Dict, List, Optional

from requests import Response

from src.api.client import ApiClient


class TaskManagerApi:
    def __init__(self, base_url: str) -> None:
        self.client = ApiClient(base_url=base_url)

    def list_tasks(self, status: Optional[str] = None) -> Response:
        params = {"status": status} if status else None
        return self.client.get("/tasks", params=params)

    def create_task(self, title: str, description: str = "", status: str = "pending") -> Response:
        payload: Dict[str, Any] = {"title": title, "description": description, "status": status}
        return self.client.post("/tasks", json=payload)

    def get_task(self, task_id: int) -> Response:
        return self.client.get(f"/tasks/{task_id}")

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None) -> Response:
        payload: Dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if status is not None:
            payload["status"] = status
        return self.client.put(f"/tasks/{task_id}", json=payload)

    def delete_task(self, task_id: int) -> Response:
        return self.client.delete(f"/tasks/{task_id}")