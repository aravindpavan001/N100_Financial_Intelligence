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