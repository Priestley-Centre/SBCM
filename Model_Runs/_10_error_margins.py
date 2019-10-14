import pandas as pd
import numpy as np
from variables import SPP as spp
import formatting as form

years = [25, 50, 100, 150, 200, 250, 500, 1000]

summary = pd.read_csv(f"curve_fit_subset_results\\summary.csv", index_col=0)
output = pd.DataFrame(index=years)
# spp = ["NE_MBB"]

# Find the best match (same as curve fit best.py)
for sp in spp:
    data = pd.read_csv(f"curve_fit_subset_results\\{sp}_param_data.csv", index_col=0)
    #    print(data.columns.values)
    x = summary.index[summary[sp] == summary[sp].min()]
    x = str(x[0])
    x = x.replace("/", "_")
    if __name__ == "__main__":
        print(f"{sp} best result: \t{x}")
    x = f"{sp} {x}"

    data_bio_best = pd.read_csv(
        f"full_params_run_results\\{sp}_sbcm_bio.csv", index_col=0
    )
    data_soil_best = pd.read_csv(
        f"full_params_run_results\\{sp}_sbcm_soil.csv", index_col=0
    )

    uncertainty_data = pd.read_csv(f"full_params_run_results\\{sp}_uncertainty.csv")

    #    print(data_bio.columns.values)

    output_bio_max = []
    output_soil_max = []
    output_bio_min = []
    output_soil_min = []
    output_bio_best = []
    output_soil_best = []

    for y in years:  # All the +1 elements are to correct the indexing
        output_bio_max.append(uncertainty_data.loc[y + 1, "bio_high"])
        output_soil_max.append(uncertainty_data.loc[y + 1, "soil_high"])
        output_bio_min.append(uncertainty_data.loc[y + 1, "bio_low"])
        output_soil_min.append(uncertainty_data.loc[y + 1, "soil_low"])
        output_bio_best.append(data_bio_best.loc[y, f"{x} biomass"])
        output_soil_best.append(data_soil_best.loc[y, f"{x} soil"])

    #    print(f'''
    #        {output_bio_max}
    #        {output_soil_max}
    #        {output_bio_min}
    #        {output_soil_min}
    #        {output_bio_best}
    #        {output_soil_best}''')

    output[f"{sp} bio min"] = output_bio_min
    output[f"{sp} bio best"] = output_bio_best
    output[f"{sp} bio max"] = output_bio_max
    output[f"{sp} soil min"] = output_soil_min
    output[f"{sp} soil best"] = output_soil_best
    output[f"{sp} soil max"] = output_soil_max

    output[f"{sp} bio max"] = np.round(
        output[f"{sp} bio max"] - output[f"{sp} bio best"], 1
    )
    output[f"{sp} bio min"] = np.round(
        output[f"{sp} bio min"] - output[f"{sp} bio best"], 1
    )
    output[f"{sp} soil max"] = np.round(
        output[f"{sp} soil max"] - output[f"{sp} soil best"], 1
    )
    output[f"{sp} soil min"] = np.round(
        output[f"{sp} soil min"] - output[f"{sp} soil best"], 1
    )
    output[f"{sp} bio best"] = np.round(output[f"{sp} bio best"], 1)
    output[f"{sp} soil best"] = np.round(output[f"{sp} soil best"], 1)

output.to_csv(r"error_margins_results\summary.csv")
output2 = pd.DataFrame(index=output.index.values)
for sp in spp:
    forest_list = []
    soil_list = []
    for (
        i
    ) in (
        output2.index.values
    ):  # NB dropping some random characters in here to allow word find/replace for proper formatting
        forest_list.append(
            f'{output.loc[i,f"{sp} bio best"]} #+{output.loc[i,f"{sp} bio max"]}@#{output.loc[i,f"{sp} bio min"]}'
        )
        soil_list.append(
            f'{output.loc[i,f"{sp} soil best"]} #+{output.loc[i,f"{sp} soil max"]}@#{output.loc[i,f"{sp} soil min"]}'
        )

    output2[f"{form.forest_labels(sp, eng=True, short=False)} forest"] = forest_list
    output2[f"{form.forest_labels(sp, eng=True, short=False)} soil"] = soil_list

output2.to_csv(r"error_margins_results\formattable table.csv")
if __name__ == "__main__":
    output2.to_clipboard()
