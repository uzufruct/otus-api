import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru",
    )

    parser.addoption(
        "--status_code",
        default=200
    )


@pytest.fixture
def input_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def expected_status_code(request):
    return int(request.config.getoption("--status_code"))
