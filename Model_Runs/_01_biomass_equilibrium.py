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
import sbcm


out = pd.DataFrame(index=["Eqm biomass", "Eqm Soil"])

species_list = var.SPP
for sp in species_list:
    spinup_scenario = sbcm.Scenario(sp)
    spinup_scenario.fell_age = 500
    spinup_scenario.initialise()
    spinup_scenario.spinup(n=10)

    out[sp] = [spinup_scenario.biomass, spinup_scenario.soil]

out.to_csv("01_biomass_equilibrium_results\\biomass_equilibrium_500_results.csv")
if __name__ == "__main__":
    print(out.T)
    out.to_clipboard()
