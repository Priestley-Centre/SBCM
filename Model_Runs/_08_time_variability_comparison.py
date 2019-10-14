"""
add docstring

"""

import pandas as pd
from variables import SPP as spp


x_data = pd.read_csv(
    "years_to_maturity_results\\years to maturity (soil).csv", index_col=0
)
x_data = x_data.T

x_data1 = x_data - 125
x_data2 = x_data - 90

x_data["NE_MBB"] = x_data1["NE_MBB"]
x_data["NE_OH"] = x_data1["NE_OH"]
x_data["NE_OP"] = x_data1["NE_OP"]
x_data["SC_OH"] = x_data2["SC_OH"]
x_data["SC_OP"] = x_data2["SC_OP"]
x_data["SC_SLP"] = x_data2["SC_SLP"]
x_data["SE_SLP"] = x_data2["SE_SLP"]
x_data["SE_LSP"] = x_data2["SE_LSP"]

x_data = x_data.T
x_data.to_csv(f"time_variability_comparison_results\\time.csv")
y_data = pd.read_csv("full_params_run_results\\eqm_summary.csv", index_col=0)
if __name__ == "__main__":
    print(x_data)
    print(y_data)

y_values = x_data

# print(x_values.to_string(),"\n")
for sp in spp:

    y_values["min"][sp] = y_data["soil_min"][sp] + y_data["bio_min"][sp]
    y_values["max"][sp] = y_data["soil_max"][sp] + y_data["bio_max"][sp]
    y_values["mean"][sp] = y_data["soil_mean"][sp] + y_data["bio_mean"][sp]
    y_values["sterman"][sp] = y_data["sterman_soil"][sp] + y_data["sterman_bio"][sp]

if __name__ == "__main__":
    print(y_values.to_string(), "\n")

y_values.to_csv(f"time_variability_comparison_results\\site_carbon.csv")
