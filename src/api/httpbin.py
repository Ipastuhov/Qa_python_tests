from typing import Any, Dict, Optional

from requests import Response

from src.api.client import ApiClient


class HttpBinApi:


    def __init__(self, base_url: str) -> None:
        self.client = ApiClient(base_url=base_url)

    
    def get(self, params: Optional[Dict[str, Any]] = None) -> Response:
        return self.client.get("/get", params=params)

    
    def post_json(self, payload: Dict[str, Any]) -> Response:
        return self.client.post("/post", json=payload)

    
    def status(self, code: int) -> Response:
        return self.client.get(f"/status/{code}")

    
    def basic_auth(self, user: str, password: str) -> Response:
        return self.client.get(f"/basic-auth/{user}/{password}", auth=(user, password))

    
    def headers(self, headers: Dict[str, str]) -> Response:
        return self.client.get("/headers", headers=headers)