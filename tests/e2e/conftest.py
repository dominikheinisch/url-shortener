import pytest
from pytest_django.live_server_helper import LiveServer

from shortener import views


@pytest.fixture
def api_url(live_server: LiveServer) -> str:
    return f"{live_server.url}/shrt/"


@pytest.fixture(autouse=True)
def reset_counter() -> None:
    views.acc = 1
