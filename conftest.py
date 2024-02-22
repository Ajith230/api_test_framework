import pytest

import config
from framework.driver import Driver


@pytest.fixture
def simple_api_driver():
    driver = Driver(config.API_URL)
    yield driver
