"""
add docstring

"""


import pandas as pd
import variables as var
from variables import SPP as spp
import numpy as np


s_cols = ["max", "min", "mean", "sterman"]
summary = pd.DataFrame(index=var.SPP, columns=s_cols)


for sp in spp:
    sp_summary = pd.DataFrame()
    data = pd.read_csv(f"05_full_params_run_results\\{sp}_sbcm_bio.csv", index_col=0)
    cols = list(data.columns.values)
    values = []

    series = data[cols[0]]
    length = len(series)
    for i in range(1, length):
        if series[i] / series.max() > 0.99:
            summary.loc[sp, "sterman"] = int(i)
            break

    for col in cols:
        series = data[col]
        length = len(series)
        #        print(length)
        for i in range(1, length):
            if series[i] / series.max() > 0.99:
                values.append(i)
                break
    sp_summary["values"] = values
    summary.loc[sp, "max"] = max(values)
    summary.loc[sp, "min"] = min(values)
    summary.loc[sp, "mean"] = int(np.round(np.mean(values), 0))
    sp_summary.to_csv(f"06_years_to_maturity_results\\{sp}_maturity_forest.csv")

if __name__ == "__main__":
    print(summary)
summary.to_csv(f"06_years_to_maturity_results\\years to maturity (forest).csv")
