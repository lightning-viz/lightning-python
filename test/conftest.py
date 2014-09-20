# content of conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="http://localhost:3000",
        help="host url: defaults to http://localhost:3000")

@pytest.fixture
def host(request):
    return request.config.getoption("--host")
