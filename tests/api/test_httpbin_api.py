import os
import pytest
import allure

from src.api.httpbin import HttpBinApi


@pytest.fixture(scope="session")
def httpbin() -> HttpBinApi:
    base = os.environ.get("API_BASE_URL_HTTPBIN")
    if not base:
        pytest.skip("API_BASE_URL_HTTPBIN is not set; skipping httpbin tests")
    return HttpBinApi(base_url=base)


@allure.feature("GET")
@pytest.mark.parametrize("params", [
    {"q": "test"},
    {"page": 1, "size": 10},
    {},
])
def test_get_echo_params(httpbin: HttpBinApi, params):
    resp = httpbin.get(params=params)
    assert resp.status_code == 200
    data = resp.json()
    for k, v in params.items():
        assert data["args"].get(k) == str(v)


@allure.feature("POST")
def test_post_json_echo(httpbin: HttpBinApi):
    payload = {"name": "pytest", "version": 1}
    resp = httpbin.post_json(payload)
    assert resp.status_code == 200
    assert resp.json()["json"] == payload


@allure.feature("STATUS")
@pytest.mark.parametrize("code", [200, 201, 204])
def test_status_success(httpbin: HttpBinApi, code):
    resp = httpbin.status(code)
    assert resp.status_code == code


@allure.feature("STATUS")
@pytest.mark.parametrize("code", [400, 401, 403, 404, 500])
def test_status_error(httpbin: HttpBinApi, code):
    with pytest.raises(Exception):
        httpbin.status(code)


@allure.feature("AUTH")
def test_basic_auth_success(httpbin: HttpBinApi):
    user, pwd = "user", "passwd"
    resp = httpbin.basic_auth(user, pwd)
    assert resp.status_code == 200
    body = resp.json()
    assert body["authenticated"] is True
    assert body["user"] == user


@allure.feature("AUTH")
def test_basic_auth_fail(httpbin: HttpBinApi):
    user, pwd = "user", "wrong"
    with pytest.raises(Exception):
        httpbin.basic_auth(user, pwd)


@allure.feature("HEADERS")
def test_custom_headers_sent(httpbin: HttpBinApi):
    headers = {"X-Correlation-Id": "123", "Authorization": "Bearer secret"}
    resp = httpbin.headers(headers)
    assert resp.status_code == 200
    echoed = resp.json()["headers"]
    assert echoed.get("X-Correlation-Id") == "123"