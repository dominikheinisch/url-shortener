import pytest
import requests

LONG_URL = "http://example.com/very-very/long/url/even-longer"


def shorten(api_url: str, url: str) -> str:
    response = requests.post(api_url, json={"url": url}, timeout=5)
    assert response.status_code == 201
    short_url: str = response.json()["short_url"]
    return short_url


def test_resolve_returns_original_url(api_url: str) -> None:
    short_url = shorten(api_url, LONG_URL)
    response = requests.get(short_url, timeout=5)
    assert response.status_code == 200
    assert response.json() == {"url": LONG_URL}


def test_resolve_returns_url_for_each_code(api_url: str) -> None:
    first = shorten(api_url, "https://example.com/a")
    second = shorten(api_url, "https://example.com/b")
    assert requests.get(first, timeout=5).json() == {"url": "https://example.com/a"}
    assert requests.get(second, timeout=5).json() == {"url": "https://example.com/b"}


def test_resolve_unknown_code_returns_404(api_url: str) -> None:
    shorten(api_url, LONG_URL)
    response = requests.get(api_url + "BAAAAC", timeout=5)
    assert response.status_code == 404


@pytest.mark.parametrize("code", ["BAAAA", "BAAAAAA", "AAAAAA", "BAAAA=", "%5C%60"])
def test_resolve_malformed_code_returns_404(api_url: str, code: str) -> None:
    response = requests.get(api_url + code, timeout=5)
    assert response.status_code == 404
