from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    check_opm_difference,
    calculate_roe,
    calculate_roce,
    calculate_roa,
)

from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    check_opm_difference,
    calculate_roe,
    calculate_roce,
    calculate_roa,
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