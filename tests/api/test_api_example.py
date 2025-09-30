import allure


def test_api_get(api_client):
    with allure.step("GET /get from httpbin"):
        resp = api_client.get("/get", params={"q": "pytest"})
        json = resp.json()
        assert resp.status_code == 200
        assert json["args"].get("q") == "pytest"