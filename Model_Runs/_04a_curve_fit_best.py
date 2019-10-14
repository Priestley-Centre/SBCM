"""
add docstring

"""
import pandas as pd
from variables import SPP as spp


summary = pd.read_csv(f"curve_fit_subset_results\\summary.csv", index_col=0)

rough = pd.read_csv(f"curve_fit_subset_results\\NE_MBB_param_data.csv", index_col=0)
output = pd.DataFrame(index=rough.index)
del rough


for sp in spp:
    data = pd.read_csv(f"curve_fit_subset_results\\{sp}_param_data.csv", index_col=0)
    #    print(data.columns.values)
    x = summary.index[summary[sp] == summary[sp].min()]
    x = str(x[0])
    x = x.replace("/", "_")
    x

    output[sp] = data[f"{sp} {x}"]
#    output[f"{sp} Sterman"] = data["Sterman"]


output.to_csv(f"curve_fit_best_results\\summary.csv")
if __name__ == "__main__":
    output.to_clipboard()
