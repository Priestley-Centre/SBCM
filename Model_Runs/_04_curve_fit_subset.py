"""
add docstring

"""


import pandas as pd
from variables import SPP
import numpy as np

summary = pd.read_csv(f"curve_fit_results\\summary.csv", index_col=0)
summary2 = summary
col = summary.columns.values
# print(col)
for i in col:
    summary2[i] = np.where(summary[i] <= summary[i]["Sterman"], summary[i], np.NaN)
summary2.loc["trf/soft_l1 "]["SC_OP"] = np.nan
summary2.to_csv("curve_fit_subset_results\\summary.csv")

with pd.ExcelWriter(
    r"curve_fit_subset_results\prototype_output.xlsx"
) as writer:  # set up excel output

    for sp in SPP:
        if __name__ == "__main__":
            print(f"\n{sp}\n{'-'*47}")
        pdata = pd.read_csv(f"curve_fit_results\\{sp}_param_data.csv", index_col=0)
        pdata2 = pd.DataFrame(index=pdata.index)
        gdata = pd.read_csv(f"curve_fit_results\\{sp}_raw_data.csv", index_col=0)
        gdata2 = pd.DataFrame(index=gdata.index)
        summary

        pcols = list(pdata.columns.values)
        gcols = list(gdata.columns.values)
        comparison_value = pdata.loc["RMSE", "Sterman"]

        for col in pcols:

            col_index = pcols.index(col)
            col2 = gcols[(col_index * 2) + 2]
            col3 = gcols[(col_index * 2 + 1) + 2]
            if __name__ == "__main__":
                print(f"{col:40}", end="")

            # We have manually dropped the SC_OP trf/ soft / l1 because the results are weird. See
            # the paper for details

            if (pdata.loc["RMSE", col] <= comparison_value) and (
                col != "SC_OP trf_soft_l1 "
            ):  # results with RMSE <= Sterman
                if __name__ == "__main__":
                    print("...pass")
                pdata2[col] = pdata[col]
                gdata2[col2] = gdata[col2]
                gdata2[col3] = gdata[col3]
            else:
                if __name__ == "__main__":
                    print("...fail")

        pdata2.to_csv(f"curve_fit_subset_results\\{sp}_param_data.csv")
        gdata2.to_csv(f"curve_fit_subset_results\\{sp}_raw_data.csv")
        pdata2.to_excel(writer, sheet_name=f"{sp}_params")
        gdata2.to_excel(writer, sheet_name=f"{sp}_raw")
