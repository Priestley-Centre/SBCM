# -*- coding: utf-8 -*-
r"""
Replicates the forest growth model as used by Sterman et al 2018
(https://doi.org/10.1088/1748-9326/aaa512)

Compares the model run to the original data as used by Sterman et al:
Smith et al 2006 Methods for Calculating Forest Ecosystem and Harvested
Carbon with Standard Estimates for Forest Types of the United States
available from https://www.fs.fed.us/ne/durham/4104/papers/ne_gtr343.pdf

Switches in the settings section determine output and output location
"""

import matplotlib.pyplot as plt
import formatting as form
import variables as var
import pandas as pd
from variables import SPP as spp

form.mpl_font_setup()
soil = pd.read_csv("soil.csv")
biomass = pd.read_csv("forest.csv")
soil = soil.set_index(["Unnamed: 0"])
biomass = biomass.set_index(["Unnamed: 0"])

# Set up figure with common x and y axes and a pallet . We're aiming for
# a combined figure with 8 subplots about a4 size.

mm = (146, 156)  # x value then y value
inches = (mm[0] / 25.4, mm[1] / 25.4)
fig, axs = plt.subplots(4, 2, sharex="all", sharey="all", figsize=inches)
axs = axs.flatten()

fig.text(0.5, 0.1, "Time (years)", ha="center", fontsize=14)
fig.text(
    0.03, 0.6, r"Carbon (t.ha$^{-1}$)", va="center", rotation="vertical", fontsize=14
)
palette = plt.get_cmap("tab10")  # pretty colours


for sp in spp:
    i = spp.index(sp)
    ax = axs[i]

    # Set up graph, x and y lists
    ax.set_title(form.forest_labels(sp, short="star", eng=True), fontsize=10)
    y1 = biomass[sp]
    y2 = soil[sp]
    x = list(soil.index)
    # And plot to graph
    ax.plot(x, y1, linewidth=1.0, label="Forest carbon", color=palette(0))
    ax.plot(x, y2, linewidth=1.0, label="Soil carbon", color=palette(1))

    # Add original smith et al data
    x2 = var.original_biomass_data[sp]["x"]
    y1 = var.original_biomass_data[sp]["y"]
    y2 = var.original_soil_data[sp]["y"]
    ax.scatter(
        x2, y1, color="k", s=8, marker="x", zorder=10, label="USDA forest carbon data"
    )
    ax.scatter(
        x2, y2, color="k", s=6, marker=".", zorder=10, label="USDA soil carbon data"
    )

    # Make sure the X and y axes are the same for each subplot
    # (so we can see what's going on easily)
    ax.set_xlim(left=0, right=100)
    ax.set_ylim(bottom=0, top=215)

    # Add a grid
    ax.grid(color="k", alpha=0.2, linestyle=":")

# add a legend and correct pacing
ax.legend(
    ncol=2,
    loc="lower center",
    bbox_to_anchor=(-1, -1.3, 2, 0.5),
    borderaxespad=0,
    frameon=False,
    labelspacing=0.75,
)

plt.subplots_adjust(
    top=0.937, bottom=0.18, left=0.14, right=0.957, hspace=0.494, wspace=0.125
)

plt.show()
plt.savefig("Fig_1_forest_growth.png", format="png", dpi=600)
# plt.savefig("forest_growth.svg", format="svg")
