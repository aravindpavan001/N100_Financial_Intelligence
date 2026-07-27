from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

def test_company_list():

    response = client.get("/api/v1/companies")

    assert response.status_code == 200


def test_company_count():

    data = client.get("/api/v1/companies").json()

    assert len(data) >= 90


def test_company_profile():

    response = client.get("/api/v1/companies/TCS")

    assert response.status_code == 200


def test_company_name():

    data = client.get("/api/v1/companies/TCS").json()

    assert data["company"]["company_name"] == "Tata Consultancy Services Ltd"


def test_invalid_company():

    response = client.get("/api/v1/companies/INVALID")

    assert response.status_code == 404