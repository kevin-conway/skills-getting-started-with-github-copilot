from fastapi.testclient import TestClient
import copy
import pytest
import src.app as app_module

_SNAPSHOT = copy.deepcopy(app_module.activities)

@pytest.fixture()
def client():
    return TestClient(app_module.app)

@pytest.fixture(autouse=True)
def reset_activities():
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_SNAPSHOT))
