import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities as activities_data
from src.app import app


BASELINE_ACTIVITIES = copy.deepcopy(activities_data)


@pytest.fixture()
def client():
    # Arrange: reset in-memory data before each test
    activities_data.clear()
    activities_data.update(copy.deepcopy(BASELINE_ACTIVITIES))

    # Act: create a test client
    test_client = TestClient(app)

    # Assert: client is ready for use
    return test_client
