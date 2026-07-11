import yaml

from src.screener.engine import apply_filters


PRESET_PATH = "config/presets.yaml"


def load_presets(path):

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        presets = yaml.safe_load(file)

    return presets
def run_preset(
    df,
    preset_name,
    presets,
):

    if preset_name not in presets:
        raise KeyError(
            f"Preset '{preset_name}' not found."
        )

    filters = {
        "filters": presets[preset_name]
    }

    return apply_filters(
        df,
        filters,
    )
import pandas as pd

from src.screener.engine import (
    load_financial_ratios,
    DB_PATH,
)


if __name__ == "__main__":

    presets = load_presets(
        PRESET_PATH,
    )

    df = load_financial_ratios(
        DB_PATH,
    )

    print("=" * 70)
    print("PRESET RESULTS")
    print("=" * 70)

    for preset_name in presets:

        result = run_preset(
            df,
            preset_name,
            presets,
        )

        print()
        print(result.head())
        print("-" * 70)

        print(
            f"{preset_name:<25} : {len(result)} companies"
        )