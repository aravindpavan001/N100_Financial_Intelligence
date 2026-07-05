from src.analytics.cagr import (
    calculate_cagr,
    get_cagr_window,
    calculate_growth_metrics,
    DECLINE_TO_LOSS,
    TURNAROUND,
    BOTH_NEGATIVE,
    ZERO_BASE,
    INSUFFICIENT,
)


def test_normal_cagr():
    value, flag = calculate_cagr(100, 200, 5)
    assert round(value, 2) == 14.87
    assert flag is None


def test_decline_to_loss():
    assert calculate_cagr(100, -30, 5) == (
        None,
        DECLINE_TO_LOSS,
    )


def test_turnaround():
    assert calculate_cagr(-20, 50, 5) == (
        None,
        TURNAROUND,
    )


def test_both_negative():
    assert calculate_cagr(-40, -10, 5) == (
        None,
        BOTH_NEGATIVE,
    )


def test_zero_base():
    assert calculate_cagr(0, 100, 5) == (
        None,
        ZERO_BASE,
    )


def test_invalid_years():
    assert calculate_cagr(100, 200, 0) == (
        None,
        INSUFFICIENT,
    )


def test_insufficient_values():
    assert calculate_growth_metrics(
        [100, 120, 140],
        5,
    ) == (
        None,
        INSUFFICIENT,
    )


def test_get_cagr_window():
    assert get_cagr_window(
        [100, 120, 150, 180, 200],
        5,
    ) == (
        100,
        200,
    )


def test_growth_metrics():
    value, flag = calculate_growth_metrics(
        [100, 120, 150, 180, 200],
        5,
    )

    assert round(value, 2) == 14.87
    assert flag is None


def test_growth_metrics_insufficient():
    assert calculate_growth_metrics(
        [100, 120],
        5,
    ) == (
        None,
        INSUFFICIENT,
    )