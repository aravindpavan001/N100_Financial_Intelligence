import pandas as pd
import pytest

from src.screener.presets import (
    load_presets,
    run_preset,
)


def test_load_presets():

    presets = load_presets(
        "config/presets.yaml"
    )

    assert isinstance(presets, dict)
    assert len(presets) == 6


def test_invalid_preset():

    df = pd.DataFrame()

    presets = {}

    with pytest.raises(KeyError):

        run_preset(
            df,
            "invalid",
            presets,
        )


def test_quality_compounder():

    df = pd.DataFrame({
        "return_on_equity_pct": [25],
        "debt_to_equity": [0.4],
        "free_cash_flow_cr": [500],
        "revenue_cagr_5yr": [20],
    })

    presets = {
        "quality": {
            "roe_min": 20,
            "debt_to_equity_max": 0.5,
            "free_cash_flow_min": 100,
            "revenue_cagr_5yr_min": 15,
        }
    }

    result = run_preset(
        df,
        "quality",
        presets,
    )

    assert len(result) == 1


def test_growth_accelerator():

    df = pd.DataFrame({
        "pat_cagr_5yr": [25],
        "revenue_cagr_5yr": [20],
        "debt_to_equity": [1],
    })

    presets = {
        "growth": {
            "pat_cagr_5yr_min": 20,
            "revenue_cagr_5yr_min": 15,
            "debt_to_equity_max": 2,
        }
    }

    result = run_preset(
        df,
        "growth",
        presets,
    )

    assert len(result) == 1


def test_cash_generator():

    df = pd.DataFrame({
        "free_cash_flow_cr": [2000],
        "operating_profit_margin_pct": [30],
        "return_on_equity_pct": [30],
        "revenue_cagr_5yr": [15],
    })

    presets = {
        "cash": {
            "free_cash_flow_min": 1500,
            "opm_min": 28,
            "roe_min": 25,
            "revenue_cagr_5yr_min": 10,
        }
    }

    result = run_preset(
        df,
        "cash",
        presets,
    )

    assert len(result) == 1


def test_debt_free_blue_chip():

    df = pd.DataFrame({
        "return_on_equity_pct": [25],
        "debt_to_equity": [0],
    })

    presets = {
        "debtfree": {
            "roe_min": 20,
            "debt_to_equity_max": 0,
        }
    }

    result = run_preset(
        df,
        "debtfree",
        presets,
    )

    assert len(result) == 1