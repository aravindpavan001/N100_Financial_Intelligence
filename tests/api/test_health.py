from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

def test_health_status():

    response = client.get("/api/v1/health")

    assert response.status_code == 200


def test_health_ok():

    data = client.get("/api/v1/health").json()

    assert data["status"] == "ok"


def test_version_exists():

    data = client.get("/api/v1/health").json()

    assert "version" in data


def test_uptime_exists():

    data = client.get("/api/v1/health").json()

    assert "uptime_seconds" in data


def test_db_counts_exist():

    data = client.get("/api/v1/health").json()

    tables = [

        "companies",

        "analysis",

        "balancesheet",

        "cashflow",

        "financial_ratios",

        "market_cap",

        "peer_groups",

        "profitandloss",

        "sectors",

        "stock_prices"

    ]

    for table in tables:

        assert table in data["db_row_counts"]