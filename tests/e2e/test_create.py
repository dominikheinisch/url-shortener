import pytest
import requests
from django.db import connection

from shortener.codecs import MAX_ID
from shortener.models import ShortUrl

LONG_URL = "http://example.com/very-very/long/url/even-longer"


def shorten(api_url: str, url: str) -> requests.Response:
    return requests.post(api_url, json={"url": url}, timeout=5)


def test_create_basic(api_url: str) -> None:
    response = shorten(api_url, LONG_URL)
    assert response.status_code == 201
    assert response.json() == {"short_url": api_url + "BAAAAB"}
    assert list(ShortUrl.objects.values_list("id", "url")) == [(1, LONG_URL)]


def test_create_very_long_url(api_url: str) -> None:
    response = shorten(api_url, LONG_URL + "1" * 1950)
    assert response.status_code == 201
    assert ShortUrl.objects.count() == 1


def test_create_same_url_twice_returns_existing_short_url(api_url: str) -> None:
    first = shorten(api_url, LONG_URL)
    second = shorten(api_url, LONG_URL)
    assert first.status_code == 201
    assert second.status_code == 200
    assert second.json() == first.json()
    assert ShortUrl.objects.count() == 1


def test_create_returns_next_code_for_each_url(api_url: str) -> None:
    first = shorten(api_url, "https://example.com/a").json()["short_url"]
    second = shorten(api_url, "https://example.com/b").json()["short_url"]
    assert first == api_url + "BAAAAB"
    assert second == api_url + "BAAAAC"


def test_create_returns_503_when_codes_run_out(api_url: str) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT setval(pg_get_serial_sequence('shortener_shorturl', 'id'), %s, false)",
            [MAX_ID],
        )

    last = shorten(api_url, "https://example.com/last")
    assert last.status_code == 201
    assert last.json() == {"short_url": api_url + "______"}
    response = shorten(api_url, "https://example.com/one-too-many")
    assert response.status_code == 503
    assert response.json() == {"detail": "Short URL limit reached."}
    assert list(ShortUrl.objects.values_list("url", flat=True)) == ["https://example.com/last"]
    assert shorten(api_url, "https://example.com/last").status_code == 200


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
    assert not ShortUrl.objects.exists()


def test_create_rejects_non_json_body(api_url: str) -> None:
    response = requests.post(api_url, data="url", headers={"Content-Type": "text/plain"}, timeout=5)
    assert response.status_code == 415
