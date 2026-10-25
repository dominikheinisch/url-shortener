import pytest
from pytest_django.live_server_helper import LiveServer


@pytest.fixture
def api_url(live_server: LiveServer) -> str:
    return f"{live_server.url}/shrt/"


@pytest.fixture(autouse=True)
def reset_ids(django_db_reset_sequences: None) -> None:
    # every test starts from id 1, so codes are predictable
    pass
