def calculate_free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow (FCF)

    Formula:
        Operating Activity + Investing Activity
    """
    return operating_activity + investing_activity


def calculate_cfo_quality(cfo_values, pat_values):
    """
    Calculate average CFO/PAT ratio over all years.

    Returns:
        (average_ratio, classification)

    Classification:
        >1.0 -> High Quality
        0.5 to 1.0 -> Moderate
        <0.5 -> Accrual Risk

    If any PAT value is zero:
        return (None, None)
    """

    if len(cfo_values) != len(pat_values):
        raise ValueError("CFO and PAT lists must have the same length.")

    ratios = []

    for cfo, pat in zip(cfo_values, pat_values):
        if pat == 0:
            return (None, None)

        ratios.append(cfo / pat)

    average_ratio = sum(ratios) / len(ratios)

    if average_ratio > 1:
        classification = "High Quality"
    elif average_ratio >= 0.5:
        classification = "Moderate"
    else:
        classification = "Accrual Risk"

    return (average_ratio, classification)


def calculate_capex_intensity(investing_activity, sales):
    """
    CapEx Intensity

    Formula:
        abs(Investing Activity) / Sales * 100
    """

    if sales == 0:
        return (None, None)

    value = abs(investing_activity) / sales * 100

    if value < 3:
        classification = "Asset Light"
    elif value <= 8:
        classification = "Moderate"
    else:
        classification = "Capital Intensive"

    return (value, classification)


def calculate_fcf_conversion(free_cash_flow, operating_profit):
    """
    FCF Conversion

    Formula:
        FCF / Operating Profit * 100
    """

    if operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100


def get_cashflow_sign(value):
    """
    Returns '+' for positive or zero values,
    '-' for negative values.
    """

    if value >= 0:
        return "+"

    return "-"


def classify_capital_allocation(
    cfo,
    cfi,
    cff,
    cfo_quality=None,
):
    """
    Classify capital allocation pattern.
    """

    cfo_sign = get_cashflow_sign(cfo)
    cfi_sign = get_cashflow_sign(cfi)
    cff_sign = get_cashflow_sign(cff)

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_quality == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"