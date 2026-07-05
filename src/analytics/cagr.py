DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
TURNAROUND = "TURNAROUND"
BOTH_NEGATIVE = "BOTH_NEGATIVE"
ZERO_BASE = "ZERO_BASE"
INSUFFICIENT = "INSUFFICIENT"


def calculate_cagr(start_value, end_value, years):
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Returns:
        (value, flag)
    """

    if years <= 0:
        return (None, INSUFFICIENT)

    if start_value == 0:
        return (None, ZERO_BASE)

    if start_value > 0 and end_value < 0:
        return (None, DECLINE_TO_LOSS)

    if start_value < 0 and end_value > 0:
        return (None, TURNAROUND)

    if start_value < 0 and end_value < 0:
        return (None, BOTH_NEGATIVE)

    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return (cagr, None)


def get_cagr_window(values, years):
    """
    Returns the first and last values needed for CAGR.
    """

    if len(values) < years:
        return None

    return (values[0], values[years - 1])


def calculate_growth_metrics(values, years):
    """
    Generic helper for Revenue, PAT and EPS CAGR.
    """

    window = get_cagr_window(values, years)

    if window is None:
        return (None, INSUFFICIENT)

    start_value, end_value = window

    return calculate_cagr(start_value, end_value, years)