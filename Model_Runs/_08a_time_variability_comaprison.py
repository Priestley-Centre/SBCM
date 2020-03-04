import pandas as pd
from variables import SPP as spp


for sp in spp:  # Yeah, hard-coded variables. These come from the USDA data
    if sp == "NE_MBB":
        pad = 125
    elif sp == "NE_OH":
        pad = 125
    elif sp == "NE_OP":
        pad = 125
    else:
        pad = 90

    if __name__ == "__main__":
        print("\n\n", sp, pad)

    output = pd.DataFrame()
    y_data1 = pd.read_csv(f"05_full_params_run_results\\{sp}_sbcm_bio.csv", index_col=0)
    y_data2 = pd.read_csv(
        f"05_full_params_run_results\\{sp}_sbcm_soil.csv", index_col=0
    )
    x_data = pd.read_csv(
        f"06_years_to_maturity_results\\{sp}_maturity_soil.csv", index_col=0
    )

    x_val = []
    for i in x_data["values"]:
        if __name__ == "__main__":
            print(f"{i}-{pad} = {i-pad}")
        x_val.append(i - pad)
    output["x"] = x_val
    output["y"] = y_data1.iloc[5000, :].values + y_data2.iloc[5000, :].values
    if __name__ == "__main__":
        print(output)
    output.to_csv(f"08_time_variability_comparison_results\\{sp}_values.csv")
