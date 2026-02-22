import pytest
from logging import getLogger, StreamHandler, DEBUG


@pytest.fixture
def logger():
    """Fixture for providing a logger instance for tests."""
    logger = getLogger("test_logger")
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    return logger
