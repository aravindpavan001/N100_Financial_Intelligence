from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)