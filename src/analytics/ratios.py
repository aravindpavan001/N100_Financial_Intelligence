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