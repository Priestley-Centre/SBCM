"""
add docstring

"""


import pandas as pd
from variables import SPP
import numpy as np


def oprint(text, end="\n"):
    if __name__ == "__main__":
        print(text, end=end)


summary = pd.read_csv(f"03_curve_fit_results\\summary.csv", index_col=0)
summary2 = summary
col = summary.columns.values
for i in col:
    summary2[i] = np.where(summary[i] <= summary[i]["Sterman"], summary[i], np.NaN)

# We have manually dropped these because they result in linear increase in either
# soil or forest carbon - which is clearly just wrong.
summary2.loc["trf/soft_l1 "]["SC_OP"] = np.nan
summary2.loc["trf/cauchy "]["SC_OH"] = np.nan
summary2.loc["trf/huber "]["SC_OP"] = np.nan

summary2.to_csv("04_curve_fit_subset_results\\summary.csv")

with pd.ExcelWriter(
    r"04_curve_fit_subset_results\prototype_output.xlsx"
) as writer:  # set up excel output

    for sp in SPP:
        oprint(f"\n{sp}\n{'-'*47}")
        pdata = pd.read_csv(f"03_curve_fit_results\\{sp}_param_data.csv", index_col=0)
        pdata2 = pd.DataFrame(index=pdata.index)
        gdata = pd.read_csv(f"03_curve_fit_results\\{sp}_raw_data.csv", index_col=0)
        gdata2 = pd.DataFrame(index=gdata.index)
        summary

        pcols = list(pdata.columns.values)
        gcols = list(gdata.columns.values)
        comparison_value = pdata.loc["RMSE", "Sterman"]

        for col in pcols:
            col_index = pcols.index(col)
            col2 = gcols[(col_index * 2) + 2]
            col3 = gcols[(col_index * 2 + 1) + 2]
            oprint(f"{col:40}", end="")

            if pdata.loc["RMSE", col] <= comparison_value:
                oprint("...pass")
                pdata2[col] = pdata[col]
                gdata2[col2] = gdata[col2]
                gdata2[col3] = gdata[col3]
            else:
                oprint("...fail")

        pdata2.to_csv(f"04_curve_fit_subset_results\\{sp}_param_data.csv")
        gdata2.to_csv(f"04_curve_fit_subset_results\\{sp}_raw_data.csv")
        pdata2.to_excel(writer, sheet_name=f"{sp}_params")
        gdata2.to_excel(writer, sheet_name=f"{sp}_raw")
