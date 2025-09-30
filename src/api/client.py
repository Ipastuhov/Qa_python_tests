from typing import Any, Dict, Optional

import requests
from requests import Response

from src.logging.logger import get_logger
from src.logging.exceptions import ApiError


class ApiClient:
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update(default_headers or {})
        self.timeout = timeout
        self.logger = get_logger("api")

    def _full_url(self, path: str) -> str:
        if path.startswith('http'):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _log_request(self, method: str, url: str, **kwargs: Any) -> None:
        redacted = {k: ('***' if k.lower() == 'authorization' else v) for k, v in (kwargs.get('headers') or {}).items()}
        self.logger.info(f"{method.upper()} {url} headers={redacted} params={kwargs.get('params')} json={kwargs.get('json')}")

    def _handle_response(self, response: Response) -> Response:
        self.logger.info(f"<- {response.status_code} {response.url}")
        if response.status_code >= 400:
            raise ApiError(f"API error {response.status_code}: {response.text}")
        return response

    def get(self, path: str, **kwargs: Any) -> Response:
        url = self._full_url(path)
        self._log_request('GET', url, **kwargs)
        resp = self.session.get(url, timeout=self.timeout, **kwargs)
        return self._handle_response(resp)

    def post(self, path: str, **kwargs: Any) -> Response:
        url = self._full_url(path)
        self._log_request('POST', url, **kwargs)
        resp = self.session.post(url, timeout=self.timeout, **kwargs)
        return self._handle_response(resp)

    def put(self, path: str, **kwargs: Any) -> Response:
        url = self._full_url(path)
        self._log_request('PUT', url, **kwargs)
        resp = self.session.put(url, timeout=self.timeout, **kwargs)
        return self._handle_response(resp)

    def delete(self, path: str, **kwargs: Any) -> Response:
        url = self._full_url(path)
        self._log_request('DELETE', url, **kwargs)
        resp = self.session.delete(url, timeout=self.timeout, **kwargs)
        return self._handle_response(resp)