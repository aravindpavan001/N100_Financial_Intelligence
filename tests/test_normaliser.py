import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.etl.normaliser import normalize_year, normalize_ticker


# ----------------------
# normalize_year tests
# ----------------------

from src.etl.normaliser import normalize_year

def test_year_2020():
    assert normalize_year("2020") == 2020

def test_year_2021():
    assert normalize_year("2021") == 2021

def test_year_2022():
    assert normalize_year("2022") == 2022

def test_year_2023():
    assert normalize_year("2023") == 2023

def test_year_2024():
    assert normalize_year("2024") == 2024

def test_year_int_2020():
    assert normalize_year(2020) == 2020

def test_year_int_2021():
    assert normalize_year(2021) == 2021

def test_year_int_2022():
    assert normalize_year(2022) == 2022

def test_year_fy2020():
    assert normalize_year("FY2020") == 2020

def test_year_fy2021():
    assert normalize_year("FY2021") == 2021

def test_year_fy2022():
    assert normalize_year("FY2022") == 2022

def test_year_fy2023():
    assert normalize_year("FY2023") == 2023

def test_year_spaces():
    assert normalize_year(" 2023 ") == 2023

def test_year_float():
    assert normalize_year("2024.0") == 2024

def test_year_report():
    assert normalize_year("Annual Report 2024") == 2024

def test_year_text():
    assert normalize_year("Year 2022") == 2022

def test_year_none():
    assert normalize_year(None) is None

def test_year_empty():
    assert normalize_year("") is None

def test_year_invalid():
    assert normalize_year("abc") is None

def test_year_old():
    assert normalize_year("1999") is None


# ----------------------
# normalize_ticker tests
# ----------------------

from src.etl.normaliser import normalize_ticker

def test_ticker_tcs():
    assert normalize_ticker("TCS") == "TCS"

def test_ticker_lower():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_spaces():
    assert normalize_ticker(" tcs ") == "TCS"

def test_ticker_ns():
    assert normalize_ticker("TCS.NS") == "TCS"

def test_ticker_bo():
    assert normalize_ticker("TCS.BO") == "TCS"

def test_reliance_ns():
    assert normalize_ticker("RELIANCE.NS") == "RELIANCE"

def test_reliance_bo():
    assert normalize_ticker("RELIANCE.BO") == "RELIANCE"

def test_infy_ns():
    assert normalize_ticker("INFY.NS") == "INFY"

def test_infy_bo():
    assert normalize_ticker("INFY.BO") == "INFY"

def test_hdfc():
    assert normalize_ticker("HDFC") == "HDFC"

def test_hdfc_lower():
    assert normalize_ticker("hdfc") == "HDFC"

def test_sbin():
    assert normalize_ticker("SBIN") == "SBIN"

def test_blank():
    assert normalize_ticker("") == ""

def test_none():
    assert normalize_ticker(None) is None

def test_spaces_only():
    assert normalize_ticker("   ") == ""