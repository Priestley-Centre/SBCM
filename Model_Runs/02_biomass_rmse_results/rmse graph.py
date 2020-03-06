import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from variables import SPP
import formatting as form


summary = pd.read_csv("rmse_scores.csv", index_col=0)


summary["sterman_forest"] = [
    1.518,
    3.046,
    1.358,
    1.531,
    0.554,
    0.666,
    0.826,
    0.759,
]  # from Sterman et al 2018 supplementary table S3

summary["sterman_soil"] = [
    6.611,
    5.415,
    6.026,
    2.615,
    2.072,
    1.522,
    1.700,
    1.672,
]  # from Sterman et al 2018 supplementary table S3


print(summary.to_string())
index = np.arange(8)

# Matplotlib figure setup
form.mpl_font_setup()
mm = (120, 100)  # x value then y value
inches = (mm[0] / 25.4, mm[1] / 25.4)
fig = plt.figure(figsize=inches)

palette = plt.get_cmap("tab10")
chart = fig.add_subplot(1, 1, 1)

scat = chart.scatter(
    index,
    summary["sterman_soil"],
    color=palette(1),
    marker="x",
    label="Sterman et al. soil",
    s=30,
)

scat = chart.scatter(
    index,
    summary["Soil RMSE"],
    color=palette(0),
    label="SBCM soil",
    marker="x",
    s=30,
    alpha=0.5,
)

scat = chart.scatter(
    index,
    summary["sterman_forest"],
    color=palette(1),
    marker="o",
    label="Sterman et al. forest",
    s=30,
)

scat = chart.scatter(
    index,
    summary["Biomass RMSE"],
    color=palette(0),
    label="SBCM forest",
    marker="o",
    s=30,
    alpha=0.5,
)


labs = [form.forest_labels(i, short="star", eng=True) for i in SPP]
labs.insert(0, "")
chart.set_ylabel("RMSE (tC.ha$^{-1}$)", fontsize=12)
chart.tick_params(axis="both", which="major", labelsize=10)
chart.set_xticklabels((labs), rotation=45, fontsize=10, horizontalalignment="right")

chart.grid(color="k", alpha=0.2, linestyle=":", zorder=1)
chart.legend(fontsize=10)
plt.ylim(ymin=0, ymax=7.5)
plt.xlim(xmin=-0.5, xmax=7.5)

plt.subplots_adjust(
    top=0.949, bottom=0.356, left=0.227, right=0.968, hspace=0.2, wspace=0.2
)

plt.show()
plt.savefig("Fig_3_RMSE_graph.png", dpi=600)
# plt.savefig("Fig_3_RMSE_graph.svg")
