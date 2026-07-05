def calculate_net_profit_margin(net_profit, sales):
    """
    Calculate Net Profit Margin.

    Formula:
        (Net Profit / Sales) * 100

    Returns:
        float or None if sales is 0.
    """
    if sales == 0:
        return None

    return (net_profit / sales) * 100


def calculate_operating_profit_margin(operating_profit, sales):
    """
    Calculate Operating Profit Margin.

    Formula:
        (Operating Profit / Sales) * 100

    Returns:
        float or None if sales is 0.
    """
    if sales == 0:
        return None

    return (operating_profit / sales) * 100


def check_opm_difference(calculated, source):
    """
    Check whether the difference between the calculated
    OPM and the source OPM is greater than 1%.

    Returns:
        True if difference > 1
        False otherwise
    """
    difference = abs(calculated - source)
    return difference > 1


def calculate_roe(net_profit, equity, reserves):
    """
    Calculate Return on Equity (ROE).

    Formula:
        (Net Profit / (Equity + Reserves)) * 100

    Returns:
        float or None if total equity is less than or equal to 0.
    """
    total_equity = equity + reserves

    if total_equity <= 0:
        return None

    return (net_profit / total_equity) * 100


def calculate_roce(ebit, equity, reserves, borrowings, sector):
    """
    Calculate Return on Capital Employed (ROCE).

    Formula:
        (EBIT / (Equity + Reserves + Borrowings)) * 100

    Note:
        The 'sector' parameter is kept for future use.

    Returns:
        float or None if total capital is less than or equal to 0.
    """
    total_capital = equity + reserves + borrowings

    if total_capital <= 0:
        return None

    return (ebit / total_capital) * 100


def calculate_roa(net_profit, total_assets):
    """
    Calculate Return on Assets (ROA).

    Formula:
        (Net Profit / Total Assets) * 100

    Returns:
        float or None if total assets is 0.
    """
    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100

def calculate_debt_to_equity(borrowings, equity, reserves):
    """
    Calculate Debt-to-Equity Ratio.

    Formula:
        Borrowings / (Equity + Reserves)

    Returns:
        0 if borrowings are 0.
        None if equity + reserves <= 0.
    """
    if borrowings == 0:
        return 0

    total_equity = equity + reserves

    if total_equity <= 0:
        return None

    return borrowings / total_equity


def get_high_leverage_flag(debt_to_equity, sector):
    """
    Returns True if Debt-to-Equity is greater than 5
    and the company is not in the Financials sector.
    """
    if debt_to_equity is None:
        return False

    if sector.lower() == "financials":
        return False

    return debt_to_equity > 5


def calculate_interest_coverage(operating_profit, other_income, interest):
    """
    Calculate Interest Coverage Ratio.

    Formula:
        (Operating Profit + Other Income) / Interest

    Returns:
        None if interest is 0.
    """
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def get_icr_label(interest):
    """
    Returns 'Debt Free' when interest is 0.
    """
    if interest == 0:
        return "Debt Free"

    return None


def get_icr_warning(icr):
    """
    Returns True if ICR is less than 1.5.

    Returns False when ICR is None.
    """
    if icr is None:
        return False

    return icr < 1.5


def calculate_net_debt(borrowings, investments):
    """
    Calculate Net Debt.

    Formula:
        Borrowings - Investments

    Negative values are allowed.
    """
    return borrowings - investments


def calculate_asset_turnover(sales, total_assets):
    """
    Calculate Asset Turnover.

    Formula:
        Sales / Total Assets

    Returns:
        None if total assets are 0.
    """
    if total_assets == 0:
        return None

    return sales / total_assets