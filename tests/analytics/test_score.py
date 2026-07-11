import pandas as pd

from src.analytics.score import (
    winsorize_series,
    normalize_metric,
    calculate_composite_score,
)


def test_winsorization():

    s = pd.Series([1, 2, 3, 4, 1000])

    result = winsorize_series(s)

    assert result.max() < 1000


def test_normalization():

    s = pd.Series([10, 20, 30])

    result = normalize_metric(s)

    assert result.min() == 0
    assert result.max() == 100


def test_composite_score():

    df = pd.DataFrame({

        "profitability_score":[50],
        "cash_quality_score":[50],
        "growth_score":[50],
        "leverage_score":[50],

    })

    df = calculate_composite_score(df)

    assert 0 <= df["composite_quality_score"][0] <= 100