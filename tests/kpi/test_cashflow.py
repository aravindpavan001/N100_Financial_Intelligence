from src.analytics.cashflow_kpis import (
    calculate_free_cash_flow,
    calculate_cfo_quality,
    calculate_capex_intensity,
    calculate_fcf_conversion,
    get_cashflow_sign,
    classify_capital_allocation,
)


# Test 1
def test_free_cash_flow():
    assert calculate_free_cash_flow(300, -100) == 200


# Test 2
def test_negative_free_cash_flow():
    assert calculate_free_cash_flow(100, -300) == -200


# Test 3
def test_cfo_quality_high():
    average, quality = calculate_cfo_quality(
        [120, 120, 120, 120, 120],
        [100, 100, 100, 100, 100],
    )

    assert round(average, 2) == 1.2
    assert quality == "High Quality"


# Test 4
def test_cfo_quality_moderate():
    average, quality = calculate_cfo_quality(
        [70, 70, 70, 70, 70],
        [100, 100, 100, 100, 100],
    )

    assert round(average, 2) == 0.7
    assert quality == "Moderate"


# Test 5
def test_cfo_quality_accrual():
    average, quality = calculate_cfo_quality(
        [30, 30, 30, 30, 30],
        [100, 100, 100, 100, 100],
    )

    assert round(average, 2) == 0.3
    assert quality == "Accrual Risk"


# Test 6
def test_capex_intensity():
    value, classification = calculate_capex_intensity(
        -150,
        3000,
    )

    assert round(value, 2) == 5
    assert classification == "Moderate"


# Test 7
def test_fcf_conversion():
    assert calculate_fcf_conversion(
        150,
        200,
    ) == 75


# Test 8
def test_fcf_conversion_zero_profit():
    assert calculate_fcf_conversion(
        150,
        0,
    ) is None


# Test 9
def test_reinvestor():
    assert classify_capital_allocation(
        250,
        -140,
        -80,
    ) == "Reinvestor"


# Test 10
def test_distress_signal():
    assert classify_capital_allocation(
        -100,
        50,
        75,
    ) == "Distress Signal"


# Test 11
def test_cash_accumulator():
    assert classify_capital_allocation(
        100,
        50,
        75,
    ) == "Cash Accumulator"


# Test 12
def test_shareholder_returns():
    assert classify_capital_allocation(
        300,
        -100,
        -50,
        "High Quality",
    ) == "Shareholder Returns"