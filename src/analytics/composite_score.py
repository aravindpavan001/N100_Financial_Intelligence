def calculate_quality_score(
    roe,
    net_margin,
    revenue_cagr,
    pat_cagr,
    debt
):
    score = 0

    # ROE (25 Marks)
    if roe is not None:
        score += min(max(roe, 0), 25)

    # Net Profit Margin (20 Marks)
    if net_margin is not None:
        score += min(max(net_margin, 0), 20)

    # Revenue CAGR (20 Marks)
    if revenue_cagr is not None:
        score += min(max(revenue_cagr, 0), 20)

    # PAT CAGR (20 Marks)
    if pat_cagr is not None:
        score += min(max(pat_cagr, 0), 20)

    # Debt (15 Marks)
    if debt is not None:
        score += max(15 - debt * 5, 0)

    return round(score, 2)