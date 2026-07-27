from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

def test_sector_list():

    response = client.get("/api/v1/sectors")

    assert response.status_code == 200


def test_sector_count():

    data = client.get("/api/v1/sectors").json()

    assert len(data) == 10


def test_financial_sector():

    response = client.get(

        "/api/v1/sectors/Financials/companies"

    )

    assert response.status_code == 200


def test_invalid_sector():

    response = client.get(

        "/api/v1/sectors/INVALID/companies"

    )

    assert response.status_code == 404