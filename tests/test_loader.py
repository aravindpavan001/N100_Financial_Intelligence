import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import tempfile

import pandas as pd

def load_excel(file_path, header=0):
    return pd.read_excel(file_path, header=header)


def test_load_excel():
    df = pd.DataFrame({
        "Ticker": ["TCS"],
        "Year": [2024]
    })

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df.to_excel(tmp.name, index=False)

        loaded_df = load_excel(tmp.name, header=0)

        assert len(loaded_df) == 1
        assert loaded_df.iloc[0]["Ticker"] == "TCS"