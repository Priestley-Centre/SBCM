# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:43:52 2019

@author: earwr
"""

"""
MORE SLLLLOOOOOWWWWW code

"""

import pandas as pd
import sbcm
import variables as var
from variables import SPP as spp
import numpy as np

intervals = [0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]
output = pd.DataFrame(index=intervals)


for i in intervals:
    s_cols = ["max", "min", "mean", "sterman"]
    summary = pd.DataFrame(index=var.SPP, columns=s_cols)

    for sp in spp:
        if __name__ == "__main__":
            print(f"{sp} ({int(i*100)}% carbon)")
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

            # Playing with this order changes the effect (a bit) as during initialise:
            # Forest is felled
            # area is calculated
            # so we can end up with a large area with very little biomass, or a smaller
            # area with loads
            # There is no effect on soil carbon, so that can go anywhere.
            scenario.soil = scenario.soil_start
            scenario.soil = scenario.soil * i
            #            scenario.biomass = scenario.biomass * i
            scenario.initialise()

            for _ in range(502):
                scenario.runstep()
            rept = scenario.report()
            payback_values.append(scenario.payback[0])

        summary.loc[sp, "max"] = np.max(payback_values)
        summary.loc[sp, "min"] = np.min(payback_values)
        summary.loc[sp, "mean"] = np.round(np.mean(payback_values), 1)
        summary.loc[sp, "sterman"] = payback_values[0]

        #        output.loc[i, f"{sp}_e"] = scenario.energy
        #        output.loc[i, f"{sp}_a"] = scenario.area
        output.loc[i, sp] = summary.loc[sp, "sterman"]
    # summary.to_csv(f"years_to_payback_results\\payback_{i}.csv")
if __name__ == "__main__":
    output.to_clipboard()
