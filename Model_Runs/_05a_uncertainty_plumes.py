import pandas as pd
import numpy as np
from variables import SPP as spp
import formatting as form

data_rmse = pd.read_csv(f"curve_fit_subset_results\\summary.csv", index_col=0)
# spp = ["NE_MBB"]
for sp in spp:
    data_usda = pd.read_csv(f"full_params_run_results\\{sp}_usda.csv", index_col=0)
    data_bio = pd.read_csv(f"full_params_run_results\\{sp}_sbcm_bio.csv", index_col=0)
    data_soil = pd.read_csv(f"full_params_run_results\\{sp}_sbcm_soil.csv", index_col=0)
    output = pd.DataFrame(index=np.arange(-1, 5001, 1))
    #    output_bio = pd.DataFrame(index=np.arange(0,501,1))

    interim_soil_upper = pd.DataFrame(index=np.arange(-1, 5001, 1))
    interim_soil_lower = pd.DataFrame(index=np.arange(-1, 5001, 1))
    interim_bio_upper = pd.DataFrame(index=np.arange(-1, 5001, 1))
    interim_bio_lower = pd.DataFrame(index=np.arange(-1, 5001, 1))

    rmse_list = []
    rmse_values = list(data_rmse[sp])
    for i in rmse_values:
        if not np.isnan(i):
            rmse_list.append(i)
    rmse_values = rmse_list
    bio_column_names = list(data_bio.columns.values)
    soil_column_names = list(data_soil.columns.values)

    for value in rmse_values:
        if not np.isnan(value):
            i = rmse_values.index(value)
            soil_col = soil_column_names[i]
            bio_col = bio_column_names[i]
            interim_soil_upper[f"{soil_col}"] = data_soil.iloc[:, i] + value
            interim_soil_lower[f"{soil_col}"] = data_soil.iloc[:, i] - value
            interim_bio_upper[f"{bio_col}"] = data_bio.iloc[:, i] + value
            interim_bio_lower[f"{bio_col}"] = data_bio.iloc[:, i] - value

    output["soil_low"] = interim_soil_lower.min(axis=1)
    output["soil_high"] = interim_soil_upper.max(axis=1)
    output["bio_low"] = interim_bio_lower.min(axis=1)
    output["bio_high"] = interim_bio_upper.max(axis=1)  #
    output["soil_diff"] = output["soil_high"] - output["soil_low"]
    output["bio_diff"] = output["bio_high"] - output["bio_low"]
    output["total diff"] = output["soil_diff"] + output["bio_diff"]
    if __name__ == "__main__":
        print(
            f"{form.forest_labels(sp, eng=True)} : {np.round(output['total diff'][500],1)}"
        )
        output.to_clipboard()
    output.to_csv(f"full_params_run_results\\{sp}_uncertainty.csv")
