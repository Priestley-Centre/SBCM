"""
add docstring

"""
def oprint(text, end="\n"):
    if __name__ == "__main__":
        print(text, end=end)


import pandas as pd
import sbcm
import variables as var
from variables import SPP as spp
import numpy as np
import winsound

s_cols = [
    "soil_max",
    "soil_min",
    "bio_max",
    "bio_min",
    "soil_mean",
    "bio_mean",
    "soil_range",
    "bio_range",
    "sterman_soil",
    "sterman_bio",
]
summary = pd.DataFrame(index=var.SPP, columns=s_cols)

max_year = 10000

# spp = ["NE_MBB"]
for sp in spp:
    oprint(f"{sp}...")
    pdata = pd.read_csv(f"04_curve_fit_subset_results\\{sp}_param_data.csv", index_col=0)
    pcols = list(pdata.columns.values)

    output1 = pd.DataFrame(index=var.original_biomass_data[sp]["x"])
    output1["usda_soil"] = var.original_soil_data[sp]["y"]
    output1["usda_biomass"] = var.original_biomass_data[sp]["y"]
    output1.to_csv(f"05_full_params_run_results\\{sp}_usda.csv")

    output2 = pd.DataFrame(index=range(-1, max_year + 1))
    output3 = pd.DataFrame(index=range(-1, max_year + 1))

    for col in pcols:
        oprint(f"\t{col}")
        scenario = sbcm.Scenario(sp)
        scenario.forest_variables = pdata[col][2:9]
        #        print(pdata[col][2:9])

        rmse = np.round(pdata[col][-1], 1)

        # TODO Watch out, this is an artificial soil equilibrium value - because Sterman
        scenario.soil = scenario.soil_start
        #'        scenario.biomass = 0#scenario.forest_start
        scenario.cf_variables = var.coal_use
        scenario.bio_variables = var.forest_use

        scenario.fell_age = max_year + 10
        #        scenario.no_fell = True
        scenario.initialise()
        scenario.spinup()

        #        scenario.soil = scenario.soil_start
        scenario.biomass = 0  # scenario.forest_start
        for _ in range(max_year + 1):
            scenario.runstep()
        rept = scenario.report()
        #        print(scenario.area)
        #        print(rept.index.values)
        output2[f"{col} biomass"] = rept["biomass_carbon"]  # [2:]
        output3[f"{col} soil"] = rept["soil_carbon"]  # [2:]

    output2.to_csv(f"05_full_params_run_results\\{sp}_sbcm_bio.csv")
    output3.to_csv(f"05_full_params_run_results\\{sp}_sbcm_soil.csv")

    summary.loc[sp, "soil_max"] = output3.max(axis=1)[max_year]
    summary.loc[sp, "soil_min"] = output3.min(axis=1)[max_year]
    summary.loc[sp, "bio_max"] = output2.max(axis=1)[max_year]
    summary.loc[sp, "bio_min"] = output2.min(axis=1)[max_year]
    summary.loc[sp, "soil_range"] = (
        output3.max(axis=1)[max_year] - output3.min(axis=1)[max_year]
    )
    summary.loc[sp, "bio_range"] = (
        output2.max(axis=1)[max_year] - output2.min(axis=1)[max_year]
    )
    summary.loc[sp, "soil_mean"] = output3.mean(axis=1)[max_year]
    summary.loc[sp, "bio_mean"] = output2.mean(axis=1)[max_year]

    summary.loc[sp, "sterman_soil"] = output3.loc[max_year]["Sterman soil"]
    summary.loc[sp, "sterman_bio"] = output2.loc[max_year]["Sterman biomass"]

if __name__ == "__main__":
    output3.to_clipboard()
    winsound.Beep(262, 500) # In case you care, this is middle C (more or less)
summary.to_csv(f"05_full_params_run_results\\eqm_summary.csv")
