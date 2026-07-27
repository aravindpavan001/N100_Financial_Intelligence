from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

def test_screener_status():

    response = client.get("/api/v1/screener")

    assert response.status_code == 200


def test_min_roe_filter():

    data = client.get(

        "/api/v1/screener?min_roe=15"

    ).json()

    for row in data:

        assert row["return_on_equity_pct"] >= 15


def test_sector_filter():

    data = client.get(

        "/api/v1/screener?sector=Financials"

    ).json()

    for row in data:

        assert row["broad_sector"] == "Financials"


def test_invalid_parameter():

    response = client.get(

        "/api/v1/screener?min_roe=abc"

    )

    assert response.status_code in [400,422]