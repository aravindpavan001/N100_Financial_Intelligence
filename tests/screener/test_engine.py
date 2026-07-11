import pandas as pd

from src.screener.engine import (
    apply_filters,
    load_config,
)


def test_load_config():

    config = load_config(
        "config/screener_config.yaml"
    )

    assert isinstance(config, dict)


def test_roe_filter_pass():

    df = pd.DataFrame({
        "return_on_equity_pct": [20]
    })

    config = {
        "filters": {
            "roe_min": 15
        }
    }

    result = apply_filters(df, config)

    assert len(result) == 1


def test_roe_filter_fail():

    df = pd.DataFrame({
        "return_on_equity_pct": [10]
    })

    config = {
        "filters": {
            "roe_min": 15
        }
    }

    result = apply_filters(df, config)

    assert len(result) == 0


def test_de_filter():

    df = pd.DataFrame({
        "debt_to_equity": [0.5, 2.0]
    })

    config = {
        "filters": {
            "debt_to_equity_max": 1
        }
    }

    result = apply_filters(df, config)

    assert len(result) == 1


def test_null_filter():

    df = pd.DataFrame({
        "return_on_equity_pct": [5, 20]
    })

    config = {
        "filters": {
            "roe_min": None
        }
    }

    result = apply_filters(df, config)

    assert len(result) == 2


def test_sorting():

    df = pd.DataFrame({
        "composite_quality_score": [
            10,
            30,
            20,
        ]
    })

    config = {
        "filters": {}
    }

    result = apply_filters(df, config)

    assert (
        result.iloc[0]["composite_quality_score"]
        == 30
    )