from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    check_opm_difference,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    get_high_leverage_flag,
    calculate_interest_coverage,
    get_icr_label,
    get_icr_warning,
    calculate_net_debt,
    calculate_asset_turnover,
)

# Test 1
def test_net_profit_margin():
    assert calculate_net_profit_margin(100, 1000) == 10.0


# Test 2
def test_net_profit_margin_zero_sales():
    assert calculate_net_profit_margin(100, 0) is None


# Test 3
def test_roe():
    assert calculate_roe(300, 1000, 500) == 20.0


# Test 4
def test_roe_negative_equity():
    assert calculate_roe(300, -100, 20) is None


# Test 5
def test_roce():
    assert calculate_roce(450, 1000, 500, 500, "IT") == 22.5


# Test 6
def test_roa_zero_assets():
    assert calculate_roa(120, 0) is None


# Test 7
def test_opm_difference_true():
    assert check_opm_difference(20, 18) is True


# Test 8
def test_opm_difference_false():
    assert check_opm_difference(20, 20.5) is False


# Test 9
def test_debt_to_equity():
    assert calculate_debt_to_equity(500, 250, 250) == 1


# Test 10
def test_debt_to_equity_zero_borrowings():
    assert calculate_debt_to_equity(0, 250, 250) == 0


# Test 11
def test_debt_to_equity_negative_equity():
    assert calculate_debt_to_equity(100, -200, 100) is None


# Test 12
def test_high_leverage_flag():
    assert get_high_leverage_flag(6, "IT") is True


# Test 13
def test_high_leverage_financials():
    assert get_high_leverage_flag(9, "Financials") is False


# Test 14
def test_interest_coverage():
    assert calculate_interest_coverage(100, 20, 30) == 4


# Test 15
def test_interest_zero():
    assert calculate_interest_coverage(100, 20, 0) is None
    assert get_icr_label(0) == "Debt Free"


# Test 16
def test_icr_warning():
    assert get_icr_warning(1.2) is True
    assert get_icr_warning(3) is False
    assert get_icr_warning(None) is False    