# -*- coding: utf-8 -*-
r"""
Replicates the forest growth model as used by Sterman et al 2018
(https://doi.org/10.1088/1748-9326/aaa512)

"""

import matplotlib.pyplot as plt
import formatting as form
import pandas as pd
from variables import SPP as spp

form.mpl_font_setup()

# Set up figure with common x and y axes and a pallet . We're aiming for
# a combined figure with 8 subplots about a4 size.

mm = (146, 156)  # x value then y value
inches = (mm[0] / 25.4, mm[1] / 25.4)
fig, axs = plt.subplots(4, 2, sharex="all", sharey="all", figsize=inches)
axs = axs.flatten()

fig.text(0.55, 0.1, "Time (years)", ha="center", fontsize=14)
fig.text(
    0.03, 0.6, r"Carbon (t.ha$^{-1}$)", va="center", rotation="vertical", fontsize=14
)
palette = plt.get_cmap("tab10")  # pretty colours


for sp in spp:
    data_usda = pd.read_csv(f"{sp}_usda.csv", index_col=0)
    data_bio = pd.read_csv(f"{sp}_sbcm_bio.csv", index_col=0)
    data_soil = pd.read_csv(f"{sp}_sbcm_soil.csv", index_col=0)
    data_uncert = pd.read_csv(f"{sp}_uncertainty.csv", index_col=0)

    x_sbcm = data_bio.index.values
    x_usda = data_usda.index.values

    y_soil_sterman = data_soil.iloc[:, 0]
    y_soil_usda = data_usda.iloc[:, 0]
    y_bio_sterman = data_bio.iloc[:, 0]
    y_bio_usda = data_usda.iloc[:, 1]

    y_soil_low = data_uncert.iloc[:, 0]
    y_soil_high = data_uncert.iloc[:, 1]
    y_bio_low = data_uncert.iloc[:, 2]
    y_bio_high = data_uncert.iloc[:, 3]

    i = spp.index(sp)
    ax = axs[i]
    # Set up graph, x and y lists
    ax.set_title(form.forest_labels(sp, short="star", eng=True), fontsize=10)
    # And plot to graph
    ax.plot(
        x_sbcm,
        y_soil_sterman,
        linewidth=0.75,
        color=palette(1),
        label="Sterman $et\ al$ soil carbon",
    )
    ax.plot(
        x_sbcm,
        y_bio_sterman,
        linewidth=0.75,
        color=palette(0),
        label="Sterman $et\ al$ forest carbon",
    )

    ax.fill_between(
        x_sbcm,
        y_soil_low,
        y_soil_high,
        color=palette(1),
        alpha=0.2,
        label="Possible soil carbon values",
    )
    ax.fill_between(
        x_sbcm,
        y_bio_low,
        y_bio_high,
        color=palette(0),
        alpha=0.2,
        label="Possible forest carbon values",
    )

    # Make sure the X and y axes are the same for each subplot
    # (so we can see what's going on easily)
    ax.set_xlim(left=0, right=10000)
    ax.set_ylim(bottom=0, top=500)

    # Add a grid
    ax.grid(color="k", alpha=0.2, linestyle=":")

# add a legend and correct pacing
plt.legend(
    ncol=2, bbox_to_anchor=(-1, -0.7), borderaxespad=0, frameon=False, labelspacing=0.75
)

plt.subplots_adjust(
    top=0.937, bottom=0.175, left=0.14, right=0.957, hspace=0.494, wspace=0.125
)

plt.show()
plt.savefig("Fig_05_uncertainty_plumes.png", format="png", dpi=600)
# plt.savefig("Fig_05_uncertainty_plumes.svg", format="svg")
