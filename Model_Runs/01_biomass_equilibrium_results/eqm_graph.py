import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from variables import SPP
import formatting as form

summary = pd.read_csv("biomass_equilibrium_500_results.csv", index_col=0)
summary = summary.T
summary["sterman"] = [
    158,
    280,
    165,
    211,
    156,
    131,
    141,
    130,
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
    summary["Eqm biomass"],
    color=palette(0),
    label="SBCM equilibrium values",
    marker="o",
    s=30,
    alpha=0.5,
)
scat = chart.scatter(
    index,
    summary["sterman"],
    color=palette(0),
    marker="x",
    label="Sterman et al. equilibrium values",
    s=40,
)

labs = [form.forest_labels(i, short="star", eng=True) for i in SPP]

chart.set_ylabel("Forest carbon at\nequilibrium (tC.ha$^{-1}$)", fontsize=12)
chart.tick_params(axis="both", which="major", labelsize=10)
chart.set_xticklabels((labs), rotation=45, fontsize=10, horizontalalignment="right")

chart.grid(color="k", alpha=0.2, linestyle=":", zorder=1)
chart.legend(fontsize=10)
chart.set_xticks(index)
plt.ylim(ymin=0, ymax=350)
plt.xlim(xmin=-0.5, xmax=7.5)

plt.subplots_adjust(
    top=0.949, bottom=0.356, left=0.227, right=0.968, hspace=0.2, wspace=0.2
)

plt.show()
plt.savefig("Fig_2_eqm_graph.png", dpi=600)
# plt.savefig("eqm_graph.svg")
