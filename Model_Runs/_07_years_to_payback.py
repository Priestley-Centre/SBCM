"""
add docstring

"""

import pandas as pd
import sbcm
import variables as var
from variables import SPP as spp
import numpy as np

s_cols = ["max", "min", "mean", "sterman"]
summary = pd.DataFrame(index=var.SPP, columns=s_cols)


for sp in spp:
    if __name__ == "__main__":
        print(f"{sp}")
    pdata = pd.read_csv(
        f"04_curve_fit_subset_results\\{sp}_param_data.csv", index_col=0
    )
    bdata = pd.read_csv(f"05_full_params_run_results\\{sp}_SBCM_bio.csv", index_col=0)
    sdata = pd.read_csv(f"05_full_params_run_results\\{sp}_SBCM_soil.csv", index_col=0)
    pcols = list(pdata.columns.values)
    payback_values = []

    for col in pcols:
        scenario = sbcm.Scenario(sp)
        scenario.forest_variables = pdata[col][2:9]
        bcol = f"{col} biomass"
        scol = f"{col} soil"

        # set start values to equilibrium for a specific case
        scenario.forest_start = bdata[bcol][5000]
        scenario.soil_start = sdata[scol][5000]
        scenario.cf_variables = var.coal_use
        scenario.bio_variables = var.forest_use
        scenario.fell_age = 502

        scenario.initialise()
        for _ in range(502):
            scenario.runstep()
        rept = scenario.report()
        payback_values.append(scenario.payback[0])

    summary.loc[sp, "max"] = np.max(payback_values)
    summary.loc[sp, "min"] = np.min(payback_values)
    summary.loc[sp, "mean"] = np.round(np.mean(payback_values), 1)
    summary.loc[sp, "sterman"] = payback_values[0]

summary.to_csv(f"07_years_to_payback_results\\payback.csv")
