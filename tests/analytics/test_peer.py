import pytest
import pandas as pd

from src.analytics.peer import (
    calculate_percentile_rank,
    merge_peer_data,
)


def test_highest_roe():

    df = pd.DataFrame({
        "roe": [10, 20, 30]
    })

    rank = calculate_percentile_rank(
        df,
        "roe",
        True,
    )

    assert rank.iloc[2] == pytest.approx(100)


def test_lowest_roe():

    df = pd.DataFrame({
        "roe": [10, 20, 30]
    })

    rank = calculate_percentile_rank(
        df,
        "roe",
        True,
    )

    assert rank.iloc[0] == pytest.approx(100 / 3)


def test_lowest_de():

    df = pd.DataFrame({
        "de": [0.2, 1, 2]
    })

    rank = calculate_percentile_rank(
        df,
        "de",
        False,
    )

    assert rank.iloc[0] == pytest.approx(100)


def test_highest_de():

    df = pd.DataFrame({
        "de": [0.2, 1, 2]
    })

    rank = calculate_percentile_rank(
        df,
        "de",
        False,
    )

    assert rank.iloc[2] == pytest.approx(100 / 3)


def test_percentile_between_0_and_100():

    df = pd.DataFrame({
        "roe": [5, 10, 20]
    })

    rank = calculate_percentile_rank(
        df,
        "roe",
        True,
    )

    assert rank.min() >= 0
    assert rank.max() <= 100


def test_merge():

    peer = pd.DataFrame({

        "company_id": ["A"],

        "peer_group_name": ["IT"],

    })

    ratio = pd.DataFrame({

        "company_id": ["A"],

        "year": [2024],

        "return_on_equity_pct": [20],

    })

    merged = merge_peer_data(
        peer,
        ratio,
    )

    assert len(merged) == 1
    assert merged.iloc[0]["peer_group_name"] == "IT"


def test_output_columns():

    peer = pd.DataFrame({

        "company_id": ["A"],

        "peer_group_name": ["IT"],

    })

    ratio = pd.DataFrame({

        "company_id": ["A"],

        "year": [2024],

        "return_on_equity_pct": [20],

    })

    merged = merge_peer_data(
        peer,
        ratio,
    )

    expected_columns = [
        "company_id",
        "peer_group_name",
        "year",
    ]

    for column in expected_columns:
        assert column in merged.columns