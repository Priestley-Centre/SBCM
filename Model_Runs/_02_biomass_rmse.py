#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Single use code to determine biomass and soil carbon equilibrium points as described
in Sterman et al 2018 (https://doi.org/10.1088/1748-9326/aaa512
"""
# ==============================================================================
#                           Functions
# ==============================================================================
import pandas as pd
import variables as var
import numpy as np
import warnings
from sklearn.metrics import mean_squared_error as mse


def rmse(y1, y2):
    return np.sqrt(mse(y1, y2))


def growth(x, pb, ps, B, phi_ab, k, v, phi_ba, phi_bs, phi_sa):
    """Chapman Richards Growth Function as used by Sterman et al 2018
    based on a range of parameters (described more fully in the model code) and
    a biomass switch (either 1 or 0) which controls whether biomass carbon or
    soil carbon results are returned
    """
    # The original data may have gaps in, so we have to work out how long it runs for
    # and then run the correct number of steps so everything lines up
    new_x = []
    new_y_bio = []
    new_y_soil = []
    output_bio = []
    output_soil = []
    run_length = max(x) + 1
    for i in range(run_length):
        # Cycles through the time-frame calculating new x and y values for each year
        new_x.append(i)  # add a new x value
        new_y_bio.append(pb)  # add a biomass value
        new_y_soil.append(ps)  # add soil carbon value
        f = var.f_value  # Make sure we include carbon fertilisation
        growth = (
            ((phi_ab * pb) + (k * B)) * (1 - (pb / B) ** v)
        ) * f  # NPP based on previous growth
        resp_emission = pb * phi_ba  # respiration (i.e. re-emission of C to atmos)
        soils_addition = pb * phi_bs  # movement of C from biomass to soils
        biomass = pb + growth - resp_emission - soils_addition  # new biomass figure
        soils_emission = ps * phi_sa  # soil respiration
        soils = ps + ((pb * phi_bs) - (ps * phi_sa))  # new soils figure
        soils = ps + (soils_addition - soils_emission)  # new soils figure
        pb = biomass
        ps = soils
    for i in x:
        # Cycles through the original data and returns a y value for each x value
        # This means that if we have data for 10, 20, 30 years we only return y values
        # for these points
        offset = new_x.index(i)
        output_bio.append(new_y_bio[offset])
        output_soil.append(new_y_soil[offset])
        output = {"bio": output_bio, "soil": output_soil}
    return output


warnings.simplefilter("ignore")
species_list = var.SPP

# species_list =["NE_MBB"]
output = pd.DataFrame(index=species_list)
biomass_rmse_list = []
soil_rmse_list = []

for sp in species_list:
    x = var.original_biomass_data[sp]["x"]
    out = pd.DataFrame(index=x)
    out["USDA_biomass_carbon"] = var.original_biomass_data[sp]["y"]
    out["USDA_soil_carbon"] = var.original_soil_data[sp]["y"]

    p = var.forest_variables[sp]
    forest_params = [
        p["forest_start"],
        p["soil_start"],
        p["B"],
        p["phi_ab"],
        p["k"],
        p["v"],
        p["phi_ba"],
        p["phi_bs"],
        p["phi_sa"],
    ]

    growth_curve = growth(x, *forest_params)

    out["biomass_carbon"] = growth_curve["bio"]
    out["soil_carbon"] = growth_curve["soil"]
    if __name__ == "__main__":
        out.to_clipboard()
    rmse_bio = rmse(out["biomass_carbon"], out["USDA_biomass_carbon"])
    rmse_soil = rmse(out["soil_carbon"], out["USDA_soil_carbon"])
    biomass_rmse_list.append(rmse_bio)
    soil_rmse_list.append(rmse_soil)
    out.to_csv(f"02_biomass_rmse_results\\{sp} growth results.csv")
output["Soil RMSE"] = soil_rmse_list
output["Biomass RMSE"] = biomass_rmse_list
output.to_csv("02_biomass_rmse_results\\RMSE_scores.csv")
if __name__ == "__main__":
    print(output.to_string())
