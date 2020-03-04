# -*- coding: utf-8 -*-
r"""
Replicates the forest growth model as used by Sterman et al 2018
(https://doi.org/10.1088/1748-9326/aaa512)

Compares the model run to the original data as used by Sterman et al:
Smith et al 2006 Methods for Calculating Forest Ecosystem and Harvested
Carbon with Standard Estimates for Forest Types of the United States
available from https://www.fs.fed.us/ne/durham/4104/papers/ne_gtr343.pdf

TODO Add comments and proper descriptions
"""

import pandas as pd
import numpy as np
import sbcm
from variables import SPP

runtime = 120
time = list(np.arange(-1, runtime + 1, 1))

soil_out = pd.DataFrame(index=time)
biomass_out = pd.DataFrame(index=time)

for sp in SPP:
    forest = sbcm.Scenario(sp)  # initialise the forest object
    forest.initialise()
    forest.biomass = forest.forest_start
    forest.soil = forest.soil_start
    biomass = [0]
    soil = [0]

    for year in time[1:]:
        biomass.append(forest.biomass)
        soil.append(forest.soil)
        forest.runstep()

    soil_out[sp] = soil
    biomass_out[sp] = biomass

soil_out.to_csv(r"09_growth_model_illustration\soil.csv")
biomass_out.to_csv(r"09_growth_model_illustration\forest.csv")
