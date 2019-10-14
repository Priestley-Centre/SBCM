"""
An analysis of parameters developed by Sterman et al 2018
"""
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import variables as var
import formatting as form
import warnings


def rmse(y1, y2):
    """Returns root mean squared error
    This is the mean of absolute differences between datasets
    y1 and y2 (both lists)"""
    return np.mean([abs(a - b) for a, b in zip(y1, y2)])


def growth(x, pb, ps, B, phi_ab, k, v, phi_ba, phi_bs, phi_sa, biomass_switch):
    """ Chapman Richards Growth Function as used by Sterman et al 2018
    based on a range of parameters (described more fully in the model code) and
    a biomass switch (either 1 or 0) which controls whether biomass carbon or
    soil carbon results are returned
    """
    # The original data may have gaps in, so we have to work out how long it runs for
    # and then run the correct number of steps so everything lines up
    new_x = []
    new_y = []
    output = []
    run_length = max(x + 1)
    for i in range(run_length):
        # Cycles through the time-frame calculating new x and y values for each year
        new_x.append(i)  # add a new x value
        if biomass_switch == 1:
            new_y.append(pb)  # add a biomass value
        else:
            new_y.append(ps)  # add soil carbon value
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
        output.append(new_y[offset])
    return output


def combinedFunction(comboData, pb, ps, B, phi_ab, k, v, phi_ba, phi_bs, phi_sa):
    """ A function for merging the calculations for soil and biomass carbon to
    allow curve-matching of all parameters against 2 data-sets simultaneously"""
    # single data reference passed in, extract separate data
    extract1 = comboData[: len(x)]  # soil data
    extract2 = comboData[len(x) :]  # biomass data
    # all the parameters for calculating growth
    params = [pb, ps, B, phi_ab, k, v, phi_ba, phi_bs, phi_sa]
    result1 = growth(extract1, *params, biomass_switch=1)
    result2 = growth(extract2, *params, biomass_switch=0)
    return np.append(result1, result2)  # returns an np array of results


warnings.simplefilter("ignore")
summary = pd.DataFrame()
SPP = var.SPP  # every species / region type
# SPP = ["NE_MBB"]


with pd.ExcelWriter(
    "curve_fit_results\\prototype_output.xlsx"
) as writer:  # set up excel output
    for SP in SPP:
        if __name__ == "__main__":
            print(f"\nStarting {form.forest_labels(SP, short=True, eng=True)}")
        # import usda data
        biomass_carbon = np.array(var.original_biomass_data[SP]["y"])
        soil_carbon = np.array(var.original_soil_data[SP]["y"])
        x = np.array(var.original_biomass_data[SP]["x"])

        # Combine datasets
        comboY = np.append(biomass_carbon, soil_carbon)
        comboX = np.append(x, x)

        # Check they match length
        if len(biomass_carbon) != len(x):
            raise Exception("Unequal x1 and y1 data length")
        if len(soil_carbon) != len(x):
            raise Exception("Unequal x2 and y2 data length")

        # set up output dataframe
        output = pd.DataFrame(index=x)
        output["USDA_biomass"] = biomass_carbon
        output["USDA_soil"] = soil_carbon

        # set up parameters output dataframe
        index = [
            "forest_start",
            "soil_start",
            "B",
            "phi_ab",
            "k",
            "v",
            "phi_ba",
            "phi_bs",
            "phi_sa",
            "RMSE",
        ]
        output_params = pd.DataFrame(index=index)

        # Collect Sterman's attempt at parameters
        p = var.forest_variables[SP]
        sterman_params = [
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

        # Model growth according to Sterman
        sterman_biomass = np.array(growth(x, *sterman_params, biomass_switch=1))
        sterman_soil = np.array(growth(x, *sterman_params, biomass_switch=0))

        # And dump to output
        output["sterman_biomass"] = sterman_biomass
        output["sterman_soil"] = sterman_soil

        # Calculate RMSE
        usda_rmse = comboY  # The original datasets combined
        sterman_rmse = np.append(sterman_biomass, sterman_soil)  # Sterman datasets
        r = rmse(usda_rmse, sterman_rmse)  # Calculate RMSE between the two
        sterman_params.append(r)  # Add the RMSE to Sterman's parameters
        output_params["Sterman"] = sterman_params  # and drop it in params output

        # curve fit the combined data to the combined function
        # forest_start, soil_start, B, phi_ab, k, v, phi_ba, phi_bs, phi_sa

        # set minimum and maximum constraints on variable values
        boundaries_min = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        boundaries_max = [500.0, 500.0, 1000.0, 0.5, 0.05, 1.5, 0.05, 0.02, 0.02]
        boundaries = (boundaries_min, boundaries_max)  # and combine

        cboundaries_min = [
            p["forest_start"],
            p["soil_start"],
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]
        cboundaries_max = [
            p["forest_start"] + 1,
            p["soil_start"] + 1,
            1000.0,
            0.5,
            0.05,
            1.5,
            0.05,
            0.02,
            0.02,
        ]
        cboundaries = (cboundaries_min, cboundaries_max)  # and combine

        """
        Methods describe the algorithm for matching and are:
        methods = ["lm",
                   "dogbox",
                   "trf"]
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
        for details

        Loss functions describe the weighting of outliers and are:
        losses = ["linear",
                  "soft_l1",
                  "huber",
                  "cauchy",
                  "arctan"]
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
        """

        # A restricted methods and losses set, which is based on earlier,
        # successful runs
        #        methods = ["trf"]
        #        losses = ["soft_l1",
        #                  "huber",
        #                  "cauchy"]

        constraints = [boundaries, cboundaries]
        constraint_labels = ["", "(constrained)"]

        methods = ["trf", "lm", "dogbox"]
        losses = ["linear", "soft_l1", "huber", "cauchy", "arctan"]

        #         Setting up for a short csv file showing RMSE functions for different
        #         combinations of method, loss, species
        summary_index = ["Sterman"]
        for m in methods:
            for l in losses:
                for b in constraints:
                    cons = constraint_labels[constraints.index(b)]
                    summary_index.append(f"{m}/{l} {cons}")

        # Run all the combinations and send results to appropriate places.
        # This is profoundly ugly code and I am truly embarassed
        # There really is no place in the world for for-loops nested this deep
        # I am ashamed of myself.
        species_summary = [r]
        for m in methods:
            for l in losses:
                for b in constraints:
                    # Some text to show what we're up to

                    cons = constraint_labels[constraints.index(b)]
                    notice = f"Attempting {SP} {m}/{l} {cons}"
                    pad = 50 - len(notice)
                    if __name__ == "__main__":
                        print(f"{notice}{pad*' '}", end="")

                    try:  # we need to _try_ this so if it fails we can keep going
                        fittedParameters, pcov = curve_fit(
                            combinedFunction, comboX, comboY, bounds=b, method=m, loss=l
                        )
                        run_name = f"{SP} {m}_{l} {cons}"  # Add a label

                        # take the fitted parameters and associate them correctly
                        forest_start, soil_start, B, phi_ab, k, v, phi_ba, phi_bs, phi_sa = (
                            fittedParameters
                        )

                        # re-run the growth model to get explicit results
                        biomass_result = growth(
                            x,
                            forest_start,
                            soil_start,
                            B,
                            phi_ab,
                            k,
                            v,
                            phi_ba,
                            phi_bs,
                            phi_sa,
                            biomass_switch=1,
                        )
                        soil_result = growth(
                            x,
                            forest_start,
                            soil_start,
                            B,
                            phi_ab,
                            k,
                            v,
                            phi_ba,
                            phi_bs,
                            phi_sa,
                            biomass_switch=0,
                        )

                        # Add output to the output dataframe
                        output[run_name + "_biomass"] = biomass_result
                        output[run_name + "_soil"] = soil_result

                        # Calculate the RMSE for this iteration
                        iteration_rmse = np.append(biomass_result, soil_result)
                        r = rmse(usda_rmse, iteration_rmse)
                        species_summary.append(r)  # and add it to the output
                        # output parameters to the dataframe
                        fittedParameters = list(fittedParameters)
                        fittedParameters.append(r)
                        output_params[run_name] = fittedParameters
                        if __name__ == "__main__":
                            print(
                                f"... success (RMSE = {np.round(r,3)})"
                            )  # Well damn, it worked!
                    except:
                        # This didn't work at all, add a padding value to maintian
                        # dataframe integrity and tell the user.
                        species_summary.append(999)  #
                        if __name__ == "__main__":
                            print(f"... failed")

        # add the RMSE error by species to the summary dataframe
        summary[SP] = species_summary
        summary.index = summary_index

        # Add the parameters, RMSE, and run output to an excel spreadsheet
        output_params.to_excel(writer, sheet_name=f"{SP}_run")
        output.to_excel(writer, sheet_name=f"{SP}_raw")

        # Output everything to CSV files as well.
        output_params.to_csv(f"curve_fit_results\\{SP}_param_data.csv")
        output.to_csv(f"curve_fit_results\\{SP}_raw_data.csv")

    summary.to_csv(f"curve_fit_results\\summary.csv")
