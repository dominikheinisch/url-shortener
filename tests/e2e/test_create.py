import pytest
import requests

LONG_URL = "http://example.com/very-very/long/url/even-longer"


def shorten(api_url: str, url: str) -> requests.Response:
    return requests.post(api_url, json={"url": url}, timeout=5)


def test_create_returns_short_url(api_url: str) -> None:
    response = shorten(api_url, LONG_URL)
    assert response.status_code == 201
    assert response.json() == {"short_url": "/shrt/BAAAAB"}


def test_create_returns_next_code_for_each_url(api_url: str) -> None:
    first = shorten(api_url, "https://example.com/a").json()["short_url"]
    second = shorten(api_url, "https://example.com/b").json()["short_url"]
    assert first == "/shrt/BAAAAB"
    assert second == "/shrt/BAAAAC"


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"url": ""},
        {"url": "not a url"},
        {"url": "ftp://example.com"},
        {"url": "javascript:alert(1)"},
        {"url": "https://example.com/" + "a" * 2048},
    ],
)
def test_create_rejects_invalid_url(api_url: str, payload: dict[str, str]) -> None:
    response = requests.post(api_url, json=payload, timeout=5)
    assert response.status_code == 400


def test_create_rejects_non_json_body(api_url: str) -> None:
    response = requests.post(api_url, data="url", headers={"Content-Type": "text/plain"}, timeout=5)
    assert response.status_code == 415
